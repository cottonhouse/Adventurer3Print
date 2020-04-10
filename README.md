# Ultimaker Cura Plugin for Adventurer3 WiFi Print.

## What is this?
- 3D Print の OSS スライサーソフト Ultimaker Cura で、3D プリンタ FlashForge Adventurer3 に G-Code ファイルを WiFi 経由で送信する機能を持った、Ultimaker Cura の Plug-in です。
- Ultimaker Cura 4.5.0 で動作確認しています。（おそらく Cura 4.4 でも動作しますが、設定ファイルの編集が必要です。）


## How to install
0. 前提として、Ultimaker Cura で FlashForge Adventurer3 を使う設定が必要です。次のサイトを参照して設定してください。
   https://andybradford.dev/2020/01/12/using-the-monoprice-voxel-with-ultimaker-cura/
1. Cura の Plugin フォルダに適当なフォルダを作り、Plugin のファイル（Adventurer3Print.py, \_\_init\_\_.py, plugin.json）をコピーしてください。  
   ex.  
   Windows10: %APPDATA%\cura\\$CURA_VERSION\plugins\Adventurer3Print  
   Mac OS   : $User/Library/Application\ Support/Cura/$CURA_VERSION/plugins/Adventurer3Print  
画像：Macの例（\_\_pycache\_\_ フォルダは Cura が起動時に自動作成しますので、コピー不要です。）  
![Folder example for Mac user](../image/image/Folder.png)  
2. Cura の Machin name の設定の後ろに IP Address を追記してください。（Machine name + IP Address となるようにしてください。）  
   ex. Flashforge Adventurer3 192.168.1.5（画像では 192.168.11.8）  
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
- Cura Version 4.5.0 の Mac版と Windows10版で動作確認しています。他の Version の Cura  でも（おそらく 4.4 以降であれば）動作すると思いますが、確認できていません。もし他の Version で使う場合は、plugin.json の API セクションの数値を編集してください。API セクションで指定しない Version の Cura では、”Send to Adv.3” のボタンが表示されません。  
数値は次の URL を参照してください。（API 7.1 が Cura 4.5.0）複数値のリストも可能です。（例: "api": ["7.0", "7.1"]）  
https://github.com/Ultimaker/Cura/wiki/CuraAPI-and-SDK-Versions  

```
    plugin.json
    {  
        "name": "Adventurer3 Print",  
        "author": "Cottonhouse",  
        "version": "1.1",  
        "api": "7.1",        <- ***HERE***  
        "description": "G-code print through WiFi with Flashforge Adventurer3.",  
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
- FlashPrint よりも Ultimaker Cura の方が明らかに印刷精度が上です。Cura で Adventurer3 を使える設定を公開してくれた Andy Bradford氏に改めて感謝の意を表します。
- Cura のマシン設定で追加する Adventurer3 用の設定で、x と y の設定は 150 ではなく 155 で良いと思います。ただし、z は 150 です。
- Python でコーディングするのは初めてでしたが、使いやすい言語と感じました。関数呼び出しに必ず付けなければいけないスコープ self. に何度もやられましたが・・・。
- Cura の Plugin 開発も初めてでしたが、Document が少ないので試行錯誤の連続でした。Cura 付属の他の Plugin のソースコードが確認できたのは幸いでした。  

## Revision history
- 1.1 (M104ADDT0 Branch) Cure 4.5.0 で作成された G-code では M104 コマンドでエクストルーダの指定がなく、Adventurer3 の温度設定ができない事象に対応しました。
  具体的には、エクストルーダ指定なしで M104 コマンドを用いて温度設定がされていたら、エクストルーダ指定を付与します。（0度指定以外で付与） 

## License
この Plugin は AGPLv3 or Higher License です。（元にした Plugin サンプルファイルが AGPLv3 or higherなので。）  
This software is released under the AGPLv3 or higher License.  
