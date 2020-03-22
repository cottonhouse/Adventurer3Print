Adventurer3Print

Ultimaker Cura Plugin for Adventurer3 WiFi Print.
(Test in Cura 4.5 (Mac & Win10).  If you use other Ver. of Cura, edit plugin.json API section.) 

How to install
 Make some folder at cura Plugin folder.
    ex.  Windows10: %APPDATA%\cura\$CURA_VERSION\plugins\Adventurer3Print
         Mac OS   : $User/Library/Application\ Support/Cura/$CURA_VERSION/plugins/Adventurer3Print
 Copy this plugin files (__init__.py, Adventurer3Print.py, plugin.json).
 In Cura, Edit Machine name as Machine name + IP Address.
    ex. Flashforge Adventurer3 192.168.1.5

How to use
 Slice a model.
 Switch save button to "Send Adv.3" button and push it.

Notice
 This plugin uses USER Folder to Temp File foder.
 Cura's Machine name is saved in .3MF files. So machine name may changes after loading .3MF file. 
  (IP Address setting may lost.)
