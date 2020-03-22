# Ultimaker Cura Plugin for Adventurer3 WiFi Print.
## Adventurer3Print

### How to install
0. 前提として、Ultimaker Cura で FlashForge Adventurer3 を使う設定が必要です。次のサイトを参照して設定してください。
   https://andybradford.dev/2020/01/12/using-the-monoprice-voxel-with-ultimaker-cura/
1. Cura の Plugin フォルダに適当なフォルダを作り、Plugin のファイル（Adventurer3Pint.py, \_\_init\_\_.py, pligin.json）をコピーしてください。<BR>
   ex.<BR>
   Windows10: %APPDATA%\cura\\$CURA_VERSION\plugins\Adventurer3Print<BR>
   Mac OS   : $User/Library/Application\ Support/Cura/$CURA_VERSION/plugins/Adventurer3Print<BR>
画像：Macの例
![Folder example for Mac user](../image/image/Folder.png)
2. Cura の Machin name の設定の後ろに IP Address を追記してください。（Machine name + IP Address となるようにしてください。）<BR>
   ex. Flashforge Adventurer3 192.168.1.5<BR>
![Manage Printers](../image/image/ManagePrinters01.png)<BR>
![Manage Printers](../image/image/ManagePrinters02.png)<BR>
![Manage Printers](../image/image/ManagePrinters03.png)<BR>
![Manage Printers](../image/image/ManagePrinters04.png)<BR>

### How to use
モデルを Slice した後にファイル保存のボタンが表示されますが、この Plugin をインストールするとファイル保存ボタンとして ”Send to Adv.3” という表示のボタンが選択できるようになります。その ”Send to Adv.3” ボタンを押してください。
![Send Buttton](../image/image/SendButton01.png)<BR>
![Send Buttton](../image/image/SendButton02.png)<BR>
![Send Buttton](../image/image/SendButton03.png)<BR>
ボタンを押すと G-Code のファイルが Adventurer3 に WiFi 経由で送信されます。
送信が完了すると、完了した旨のメッセージが表示されます。
![Send Buttton](../image/image/SendButton04.png)<BR>

### Notice
- この Plugin は、OS の USER フォルダを TEMP File 作成フォルダとして利用しています。G-Code の temporary file を作成して、WiFI 送信後に削除しています。<BR>
- Cura　のマシン名は .3MF ファイルに保存されているようです。.3MF ファイルを Load するとマシン名の設定が変わることがあります。
この Plugin では、IP アドレスの設定をマシン名に追加していますので、マシン名の設定が変更されると IP アドレスの設定が失われることがあります。
- Cura Version 4.5.0 の Mac版と Win10版で動作確認しています。他の Version の Cura でも動作すると思いますが、確認できていません。もし他の Version で使う場合は、plugin.json の API セクションの数値を編集してください。
数値は次の URL を参照してください。（API 7.1 が Cura 4.5.0）複数値のリストも可能です。（例: "api": ["7.0", "7.1"]）
https://github.com/Ultimaker/Cura/wiki/CuraAPI-and-SDK-Versions)

_plugin.json_
'''
{
    "name": "Adventurer3 Print",
    "author": "Cottonhouse",
    "version": "1.0",
    "api": "7.1",
    "description": "G-code print use WiFi at Flashforge Adventurer3.",
    "catalog": "cotton"
}
'''

- この Plugin の作成にあたり、以下のコードを参照しています。（take4blue 様に感謝）
https://github.com/take4blue/Adventurer3Web
- この Plugin の作成のきっかけは、以下のサイトです。（Andy Bradford 様に感謝）
https://andybradford.dev/2020/01/12/using-the-monoprice-voxel-with-ultimaker-cura/
- また、以下を参照しています。
https://github.com/andycb/AdventurerClientDotNet

### License
この Plugin は AGPLv3 or Higher License です。（元にした Plugin サンプルファイルが AGPLv3 or higherなので。）<BR>
This software is released under the AGPLv3 or higher License
