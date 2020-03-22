# Ultimaker Cura Plugin for Adventurer3 WiFi Print.

## How to install
0. 前提として、Ultimaker Cura で FlashForge Adventurer3 を使う設定が必要です。次のサイトを参照して設定してください。
   https://andybradford.dev/2020/01/12/using-the-monoprice-voxel-with-ultimaker-cura/
1. Cura の Plugin フォルダに適当なフォルダを作り、Plugin のファイル（Adventurer3Pint.py, \_\_init\_\_.py, pligin.json）をコピーしてください。  
   ex.  
   Windows10: %APPDATA%\cura\\$CURA_VERSION\plugins\Adventurer3Print  
   Mac OS   : $User/Library/Application\ Support/Cura/$CURA_VERSION/plugins/Adventurer3Print  
画像：Macの例（\_\_pycache\_\_ フォルダは Cura が起動時に作成します。）  
![Folder example for Mac user](../image/image/Folder.png)  
2. Cura の Machin name の設定の後ろに IP Address を追記してください。（Machine name + IP Address となるようにしてください。）  
   ex. Flashforge Adventurer3 192.168.1.5  
![Manage Printers](../image/image/ManagePrinters01.png)  
![Manage Printers](../image/image/ManagePrinters02.png)  
![Manage Printers](../image/image/ManagePrinters03.png)  
![Manage Printers](../image/image/ManagePrinters04.png)  

## How to use
モデルを Slice した後にファイル保存のボタンが表示されますが、この Plugin をインストールするとファイル保存ボタンとして ”Send to Adv.3” という表示のボタンが選択できるようになります。その ”Send to Adv.3” ボタンを押してください。  
![Send Buttton](../image/image/SendButton01.png)  
![Send Buttton](../image/image/SendButton02.png)  
![Send Buttton](../image/image/SendButton03.png)  
ボタンを押すと G-Code のファイルが Adventurer3 に WiFi 経由で送信されます。  
送信が完了すると、完了した旨のメッセージが表示されます。  
![Send Buttton](../image/image/SendButton04.png)  

## Notice
- この Plugin は、OS の USER フォルダを TEMP File 作成フォルダとして利用しています。G-Code の temporary file を作成して、WiFi 送信後に削除しています。
- Cura では .3MF ファイルを Load するとマシン名の設定が変わることがあります。  
この Plugin では、IP アドレスの設定をマシン名の後に記載していることが前提ですので、マシン名の設定が変更されると IP アドレスの設定が失われ、Plugin が WiFi 接続できなくなることがあります。その場合は、マシン名を再設定してください。
- Cura Version 4.5.0 の Mac版と Windows10版で動作確認しています。他の Version の Cura  でも（おそらく 4.2 以降であれば）動作すると思いますが、確認できていません。もし他の Version で使う場合は、plugin.json の API セクションの数値を編集してください。
数値は次の URL を参照してください。（API 7.1 が Cura 4.5.0）複数値のリストも可能です。（例: "api": ["7.0", "7.1"]）  
API　セクションで指定しない Version の Cura では、ボタンが表示されません。  
https://github.com/Ultimaker/Cura/wiki/CuraAPI-and-SDK-Versions  

    _plugin.json_
```    {  
        "name": "Adventurer3 Print",  
        "author": "Cottonhouse",  
        "version": "1.0",  
        "api": "7.1",          <- **HERE**  
        "description": "G-code print use WiFi at Flashforge Adventurer3.",  
        "catalog": "cotton"  
    }
```  

## Acknowledgments
- この Plugin の作成にあたり、以下のコードを参照しています。（take4blue 様に感謝）  
https://github.com/take4blue/Adventurer3Web  
take4blue氏の Python ソースコードをほぼそのまま使わせて頂いています。G-Code 送信部分を主に作成しています。
- この Plugin の作成のきっかけは、以下のサイトです。（Andy Bradford 様に感謝）  
https://andybradford.dev/2020/01/12/using-the-monoprice-voxel-with-ultimaker-cura/  
Andy Bradford氏による Ultimate Cura で Adventurer3 用の G-Code を作成する設定と、氏が WiFi での印刷を行おうとしている様子を見て、この Plugin 作成を思い立ちました。
また、Andy氏による以下のソースコードを参考にしています。  
https://github.com/andycb/AdventurerClientDotNet  
- Python でコーディングするのは初めてでしたが、使いやすい言語と感じました。関数呼び出しに必ず付けなければいけないスコープ self. を除外して・・・。
- Cura の Plugin 開発も初めてでしたが、Document が少ないのでソースを見なければならず、また試行錯誤の連続でした。Python なので Cura 付属の他の Plugin のソースが確認できたのは幸いでした。  

## License
この Plugin は AGPLv3 or Higher License です。（元にした Plugin サンプルファイルが AGPLv3 or higherなので。）  
This software is released under the AGPLv3 or higher License.  
