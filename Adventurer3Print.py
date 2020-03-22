# Copyright (c) 2017 Ultimaker B.V.
# This example is released under the terms of the AGPLv3 or higher.
# modified by Cottonhouse 2020/03/21

import os.path #To get a file name to write to.
from UM.PluginRegistry import PluginRegistry #Getting the location of Hello.qml.
from UM.Application import Application #To find the scene to get the current g-code to write.
from UM.FileHandler.WriteFileJob import WriteFileJob #To serialise nodes to text.
from UM.Logger import Logger
from UM.Message import Message
from UM.OutputDevice.OutputDevice import OutputDevice #An interface to implement.
from UM.OutputDevice.OutputDeviceError import WriteRequestFailedError #For when something goes wrong.
from UM.OutputDevice.OutputDevicePlugin import OutputDevicePlugin #The class we need to extend.
from cura.Settings.ExtruderManager import ExtruderManager

from UM.i18n import i18nCatalog
catalog = i18nCatalog("cura")

import socket
import requests
import re
from enum import Enum
from time import sleep
import binascii

class MachineStatus(Enum):
    Ready = 0
    Busy = 1
    Building = 2
    Transfer = 3

class Adventurer3Print(OutputDevicePlugin): #We need to be an OutputDevicePlugin for the plug-in system.
    ##  Called upon launch.
    #
    #   You can use this to make a connection to the device or service, and
    #   register the output device to be displayed to the user.
    def start(self):
        self.plugin_path = Application.getInstance().getPluginRegistry().getPluginPath(self.getPluginId())
        self.getOutputDeviceManager().addOutputDevice(Adv3OutputDevice(self.plugin_path)) #Since this class is also an output device, we can just register ourselves.
        #You could also add more than one output devices here.
        #For instance, you could listen to incoming connections and add an output device when a new device is discovered on the LAN.

    ##  Called upon closing.
    #
    #   You can use this to break the connection with the device or service, and
    #   you should unregister the output device to be displayed to the user.
    def stop(self):
        self.getOutputDeviceManager().removeOutputDevice("Adventurer3_Print") #Remove all devices that were added. In this case it's only one.

class Adv3OutputDevice(OutputDevice): #We need an actual device to do the writing.
    def __init__(self, plugin_path):
        super().__init__("Adventurer3_Print") #Give an ID which is used to refer to the output device.

        self._plugin_path = plugin_path
        #Optionally set some metadata.
        self.setName("Adventurer3_Print") #Human-readable name (you may want to internationalise this). Gets put in messages and such.
        self.setShortDescription("Send Adv.3") #This is put on the save button.
        self.setDescription("Send Adv.3")
        self.setIconName("save")

    ##  Called when the user clicks on the button to save to this device.
    #
    #   The primary function of this should be to select the correct file writer
    #   and file format to write to.
    #
    #   \param nodes A list of scene nodes to write to the file. This may be one
    #   or multiple nodes. For instance, if the user selects a couple of nodes
    #   to write it may have only those nodes. If the user wants the entire
    #   scene to be written, it will be the root node. For the most part this is
    #   not your concern, just pass this to the correct file writer.
    #   \param file_name A name for the print job, if available. If no such name
    #   is available but you still need a name in the device, your plug-in is
    #   expected to come up with a name. You could try `uuid.uuid4()`.
    #   \param limit_mimetypes Limit the possible MIME types to use to serialise
    #   the data. If None, no limits are imposed.
    #   \param file_handler What file handler to get the mesh from.
    #   \kwargs Some extra parameters may be passed here if other plug-ins know
    #   for certain that they are talking to your plug-in, not to some other
    #   output device.
    def requestWrite(self, nodes, file_name = None, limit_mimetypes = None, file_handler = None, **kwargs):
        filter_by_machine = True # This plugin is intended to be used by machine (regardless of what it was told to do)
        # Formats supported by this application (File types that we can actually write)
        if file_handler:
            file_formats = file_handler.getSupportedFileTypesWrite()
        else:
            file_formats = Application.getInstance().getMeshFileHandler().getSupportedFileTypesWrite()

        if filter_by_machine:
            container = Application.getInstance().getGlobalContainerStack().findContainer({"file_formats": "*"})

            # Create a list from supported file formats string
            machine_file_formats = [file_type.strip() for file_type in container.getMetaDataEntry("file_formats").split(";")]

            # Take the intersection between file_formats and machine_file_formats.
            format_by_mimetype = {format["mime_type"]: format for format in file_formats}
            file_formats = [format_by_mimetype[mimetype] for mimetype in machine_file_formats] #Keep them ordered according to the preference in machine_file_formats.

        if len(file_formats) == 0:
            Logger.log("e", "Plugin Adv3: There are no file formats available to write with!")
            raise OutputDeviceError.WriteRequestFailedError(catalog.i18nc("@info:status", "Plugin Adv3: There are no file formats available to write with!"))
        preferred_format = file_formats[0]

        # Just take the first file format available.
        if file_handler is not None:
            file_handler = Application.getInstance().getMeshFileHandler()
        writer = file_handler.getWriterByMimeType(preferred_format["mime_type"])
        extension = preferred_format["extension"]

        if file_name is None:
            file_name = self._automaticFileName(nodes)
        self.fileNoExt = file_name

        if extension:  # Not empty string.
            #if extension == "gcode":
            #    extension = "g"
            extension = "." + extension
        file_name = os.path.splitext(file_name)[0] + extension

        #For this example, we will write to a file in a fixed location.
        self.output_file_name = os.path.expanduser("~/" + file_name)
        file_stream = open(self.output_file_name, "w", encoding = "utf-8")
        job = WriteFileJob(writer, file_stream, nodes, preferred_format["mode"]) #We'll create a WriteFileJob, which gets run asynchronously in the background.

        #job.progress.connect(self._onProgress) #You can listen to the event for when it's done and when it's progressing.
        job.finished.connect(self._onFinished) #This way we can properly close the file stream.

        Logger.log("d", "Plugin Adv3: saveing file started...")
        job.start()

    def _onProgress(self, job, progress):
        #self.writeProgress.emit(self, progress)
        Logger.log("d", "Saving file... {progress}%".format(progress = progress))

    def _onFinished(self, job):
        Logger.log("d", "Done saving file!")        
        job.getStream().close() #Don't forget to close the stream after it's finished.

        # Get IP Addr
        stcode = Application.getInstance().getMachineManager().activeMachine.name
        Logger.log("d", "Plugin Adv3: Machine name = " + stcode)
        stcode = stcode.split(" ")[-1]
        if not self.isIPAddress(stcode):
            message = Message(catalog.i18nc("@error:status", "Please set IP Address of your Adventurer3 after Printer Name. (ex. Flahforge Adventurer3 192.168.1.5 )"), title = catalog.i18nc("@error:title", "Wrong IP Adress settings."))
            message.show()
            return
        Logger.log("d", "Plugin Adv3: IP Address = " + stcode)

        # For socket
        Logger.log("d", "Plugin Adv3: Sending data to WiFi Printer...")
        self.IPAddr = stcode #"192.168.11.8"
        self.adv3 = Controller()
        self.adv3.setHostname(self.IPAddr)
        self.status = False
        if self.adv3.start():
            Logger.log("d", "Plugin Adv3: Now calls a WiFi Print job...")
            self.status = self.adv3.start_job(self.output_file_name)
            self.adv3.end()
        else:
            message = Message(catalog.i18nc("@error:status", "Can not connect Adventurer3."), title = catalog.i18nc("@error:title", "Network Error."))
            message.show()
            return
        
        try:
            os.remove(self.output_file_name)
        except OSError:
            Logger.log("e", "Plugin Adv3: Can't delete .gcode file.")
        
        if self.status:
            mes = "Already transferred a file '{0}' to the Adventurer3."
        else:
            mes = "Transfer FAILED. ({0}) "
        message = Message(catalog.i18nc("@info:status", mes).format(os.path.splitext(os.path.basename(self.output_file_name))[0] + ".g"), title = catalog.i18nc("@info:title", "File transferred."))
        message.show()

    def isIPAddress(self, add):
        tmp = add.split(".")
        if len(tmp) != 4:
            return False
        else:
            for i in tmp:
                if not i.isdecimal():
                    return False
        return True

class Controller:
    """Adventurer3との通信用制御クラス"""

    DEFAULT_PORT = 8899  # Adventurer3への接続ポート番号(一応固定)

    def __init__(self):
        """コンストラクタ"""
        ##self.hostname = hostname
        self.status = None
        self.current_temp_bed = 0
        self.current_temp_nozel = 0
        self.target_temp_bed = 0
        self.target_temp_nozel = 0
        self.sd_max = 100
        self.sd_progress = 0
        self.limit_x = False
        self.limit_y = False
        self.limit_z = False
        self.pos_e = 0
        self.pos_x = 0
        self.pos_y = 0
        self.pos_z = 0

    def start_job(self, path):
        """JOB開始"""
        self.blockSize_ = 4096
        self.headerSize_ = 16

        if path is not None:
            fsize = os.stat(path).st_size
        else:
            return False
        filename = os.path.splitext(os.path.basename(path))[0]

        try:
            Logger.log("d", "Plugin Adv3: Now Open file.")
            fp = open(path, "rb")
        except OSError:
            Logger.log("e", "Plugin Adv3: Error in def start_job at open file.")
            return False
        else:
            if self.is_ok(self.send("M28 " + str(fsize) + " 0:/user/" + filename + ".g")):
                Logger.log("d", "Plugin Adv3 Sent: M28 " + str(fsize) + " 0:/user/" + filename + ".g")
                fmod = fsize % self.blockSize_
                if fmod > 0:
                    iplus = 1
                else:
                    iplus = 0
                #ファイルを送る
                for i in range(fsize // self.blockSize_ + iplus):
                    Logger.log("d", "Plugin Adv3: Now sending data Page = " + str(i))
                    readBuffer = bytearray(self.blockSize_)
                    readBuffer = fp.read(self.blockSize_)
                    readByte = len(readBuffer)
                    if readByte == 0:
                        Logger.log("d", "Plugin Adv3: No Data. Break.")
                        break
                    #Logger.log("d", "Plugin Adv3: Creates packet header.")
                    writeBuffer = bytearray(self.headerSize_)
                    # sync header
                    writeBuffer[0] = 0x5a
                    writeBuffer[1] = 0x5a
                    writeBuffer[2] = 0xa5
                    writeBuffer[3] = 0xa5
                    # Page number
                    writeBuffer[4] = (i >> 24) & 0xFF
                    writeBuffer[5] = (i >> 16) & 0xFF
                    writeBuffer[6] = (i >> 8) & 0xFF
                    writeBuffer[7] = i & 0xFF
                    # Data Size
                    writeBuffer[8] = (readByte >> 24) & 0xFF
                    writeBuffer[9] = (readByte >> 16) & 0xFF
                    writeBuffer[10] = (readByte >> 8) & 0xFF
                    writeBuffer[11] = readByte & 0xFF
                    # CRC
                    #Logger.log("d", "Plugin Adv3: Calc CRC32.")
                    try:
                        chksum = binascii.crc32(readBuffer)
                    except Exception as e:
                        Logger.log("e", "Plugin Adv3: CRC32 Err: " + str(e))
                    #Logger.log("d", "Plugin Adv3: Calculated CRC32.")
                    writeBuffer[12] = (chksum >> 24) & 0xFF
                    writeBuffer[13] = (chksum >> 16) & 0xFF
                    writeBuffer[14] = (chksum >> 8) & 0xFF
                    writeBuffer[15] = chksum & 0xFF
                    # Data
                    Logger.log("d", "Plugin Adv3: Append data to pacekt.")
                    writeBuffer.extend(readBuffer)
                    # Zero padding
                    if self.blockSize_ > readByte:
                        Logger.log("d", "Plugin Adv3: Do zero padding.")
                        writeBuffer.extend(bytearray(self.blockSize_ - readByte))
                    # Send Data
                    Logger.log("d", "Plugin Adv3: Send raw data: page = " + str(i))
                    if not self.is_ok(self.sendRaw(writeBuffer)):
                        # データの送信ができなかったので中止
                        Logger.log("e", "Plugin Adv3: Err is back from Printer while sendingraw data.")
                        return False
                    else:
                        Logger.log("d", "Plugin Adv3: sendRaw Succeeded.")
                    #sleep(0.1)
                    #sleep(0.001) # 1ms

                sleep(0.01)
                Logger.log("d", "Plugin Adv3 Send: M29")
                if self.is_ok(self.send("M29")):
                    Logger.log("d", "Plugin Adv3 Send: M23 0:/user/" + filename + ".g")
                    if not self.is_ok(self.send("M23 " + "0:/user/" + filename + ".g")):
                        Logger.log("d", "Plugin Adv3: M23 is NG.")
                        return False
                    else:
                        Logger.log("d", "Plugin Adv3: M23 succeeded.")
                else:
                    Logger.log("d", "Plugin Adv3: M29 NG")
        finally:
            fp.close()
            return True

    def _onProgress(self, job, progress):
        Logger.log("d", "Sending file... {progress}%".format(progress = progress))

    def _onFinished(self, job):
        job.getStream().close() #Don't forget to close the stream after it's finished.
        Logger.log("d", "Sent file compete!")

    def setHostname(self, hostname):
        self.hostname = hostname

    def start(self):
        """
        Adventurer3との接続開始
        間違ったIPを指定すると、この関数のリターンにすごく時間がかかる場合がある。
        (タイムアウトまで待つため）
        """
        try:
            self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcp.settimeout(45.0) # timeout 45sec
            self.tcp.connect((self.hostname, self.DEFAULT_PORT))
        except OSError:
            Logger.log("e", "Plugin Adv3: Error in def start.")
            return False
        self.tcp.send("~M601 S1\r\n".encode())
        self.recv()
        return True

    def end(self):
        """Adventurer3との接続解除"""
        if self.is_connected:
            self.tcp.send("~M602 S1\r\n".encode())
            self.recv()
            self.tcp.close()
            self.tcp = None

    def recv(self):
        """データの受信"""
        data = self.tcp.recv(4096)
        if not data:
            return None
        else:
            return data.decode('utf-8')

    def send(self, data):
        """データの送信"""
        sendData = "~" + data
        return self.sendRaw(sendData.encode())

    def sendRaw(self, data):
        """データの送信"""
        if self.is_connected:
            #Logger.log("d", "Plugin Adv3: sendRaw()")
            try:
                self.tcp.send(data)
            except OSError:
                Logger.log("e", "Plugin Adv3: Error in def sendRaw().")
                return ""
            else:
                #Logger.log("d", "Plugin Adv3: sendRaw(): sent." )
                return self.recv()
        else:
            Logger.log("d", "Plugin Adv3: sendRaw(): Not connected.")
            return ""

    def is_connected(self):
        """Adventurer3と接続中かどうか"""
        if not self.tcp:
            return False
        else:
            return True

    def is_ok(self, data):
        """返ってきたデータがOKかどうかの判断"""
        if not data:
            return False
        else:
            trimLine = data.strip()
            if trimLine.endswith("ok") >= 0:
                return True
            elif trimLine.endswith("ok.") >= 0:
                return True
            else:
                return False

    def update_machine_status(self):
        """機器の状態取得"""
        work = self.send("M119")
        if self.is_ok(work):
            split = work.split("\n")
            for line in split:
                trimLine = line.strip()
                if trimLine.startswith("Endstop"):
                    endstop = trimLine.split(' ')
                    if len(endstop) == 4:
                        self.limit_x = self.limit_y = self.limit_z = True
                        if endstop[1].endswith("0"):
                            self.limit_x = False
                        if endstop[2].endswith("0"):
                            self.limit_y = False
                        if endstop[3].endswith("0"):
                            self.limit_z = False
                elif trimLine.startswith("MachineStatus"):
                    if trimLine.endswith("READY"):
                        self.status = MachineStatus.Ready
                    elif trimLine.endswith("BUILDING_FROM_SD"):
                        self.status = MachineStatus.Building
                    else:
                        self.status = MachineStatus.Busy

    def update_temp_status(self):
        """温度の情報を更新"""
        work = self.send("M105")
        if self.is_ok(work):
            split = work.split("\n")
            if len(split) >= 3:
                splitLine = re.split(':|/|B', split[1].strip())
                if len(splitLine) == 6:
                    self.current_temp_nozel = int(splitLine[1])
                    self.target_temp_nozel = int(splitLine[2])
                    self.current_temp_bed = int(splitLine[4])
                    self.target_temp_bed = int(splitLine[5])
    
    def update_job_status(self):
        """JOB状態を更新"""
        work = self.send("M27")
        if self.is_ok(work):
            split = work.split("\n")
            if len(split) >= 3:
                splitLine = re.split(' |/', split[1].strip())
                if len(splitLine) == 5:
                    self.sd_progress = int(splitLine[3])
                    self.sd_max = int(splitLine[4])

    def update_position(self):
        work = self.send("M114")
        if self.is_ok(work):
            split = work.split("\n")
            if len(split) >= 3:
                splitLine = re.split(' |:', split[1].strip())
                if len(splitLine) == 10:
                    self.pos_x = float(splitLine[1])
                    self.pos_y = float(splitLine[3])
                    self.pos_z = float(splitLine[5])
                    self.pos_e = float(splitLine[7])

    def update_status(self):
        """Adventurer3の情報の取り出し(更新)"""
        self.update_machine_status()
        self.update_temp_status()
        self.update_job_status()
        self.update_position()

    def led(self, OnOff):
        """LEDの表示・消去"""
        if OnOff == True:
            self.send("M146 r255 g255 b255 F0")
        else:
            self.send("M146 r0 g0 b0 F0")

    def stop_job(self):
        """JOB停止"""
        self.send("M26")

    def stop(self):
        """機器の緊急停止"""
        self.send("M112")
        self.update_position()

    def get_status(self):
        return "ノズル {0}/{1}, ベッド {2}/{3}, 機器 {4}, 印刷 {5}/{6}, X:{7} Y:{8} Z:{9} E:{10}".\
        format(self.current_temp_nozel, self.target_temp_nozel,
        self.current_temp_bed, self.target_temp_bed,
        self.status,
        self.sd_progress, self.sd_max,
        self.pos_x, self.pos_y, self.pos_z, self.pos_e)

def download_image(address, timeout = 10):
    """Adventurer3からカメラの静止画画像を取得する"""
    url = 'http://' + address + ':8080/?action=snapshot'
    response = requests.get(url, allow_redirects=False, timeout=timeout)
    if response.status_code != 200:
        e = Exception("HTTP status: " + response.status_code)
        raise e

    content_type = response.headers["content-type"]
    if 'image' not in content_type:
        e = Exception("Content-Type: " + content_type)
        raise e

    return response.content