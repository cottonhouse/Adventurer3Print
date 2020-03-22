#Adventurer3Print

##Ultimaker Cura Plugin for Adventurer3 WiFi Print.

###How to install
1. Cura の Plugin フォルダに適当なフォルダを作り、Plugin のファイルを全てコピーして下さい。
    ex.  Windows10: %APPDATA%\cura\$CURA_VERSION\plugins\Adventurer3Print
         Mac OS   : $User/Library/Application\ Support/Cura/$CURA_VERSION/plugins/Adventurer3Print
2. Cura の Machin name の設定の後ろに IP Address を追記してください。（Machine name + IP Address となるようにしてください。）
    ex. Flashforge Adventurer3 192.168.1.5

###How to use
モデルを Slice した後にファイル保存のボタンが表示されますが、この Plugin をインストールするとファイル保存ボタンとして ”Send Adv.3” という表示のボタンが選択できるようになります。その ”Send Adv.3” を押してください。G-Code のファイルが Adventurer3 に WiFi 経由で送信されます。

###Notice
- この Plugin は、OS の USER フォルダを TEMP File 作成フォルダとして利用しています。G-Code の temporary file を作成して、WiFI 送信後に削除しています。
- Cura　のマシン名は .3MF ファイルに保存されているようです。.3MF ファイルを Load するとマシン名の設定が変わることがあります。
この Plugin では、IP アドレスの設定をマシン名に追加していますので、マシン名の設定が変更されると IP アドレスの設定が失われることがあります。
- Cura Version 4.5 の Mac版と Win10版で動作確認しています。他の Version の Cura でも動作すると思いますが、確認できていません。もし他の Version で使う場合は、plugin.json の API セクションの数値を編集してください。
数値は次の URL を参照してください。
https://github.com/Ultimaker/Cura/wiki/CuraAPI-and-SDK-Versions)
- この Plugin の作成にあたり、以下のコードを参照しています。（take4blue 様に感謝）
https://github.com/take4blue/Adventurer3Web
- この Plugin の作成のきっかけは、以下のサイトです。（andy bradford 様に感謝）
https://andybradford.dev/2020/01/12/using-the-monoprice-voxel-with-ultimaker-cura/

この Plugin は AGPLv3 License です。（元にした Plugin サンプルファイルがAGPLv3なので。）
