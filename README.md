# ChatEx

![image](https://user-images.githubusercontent.com/11075065/91656177-9bcad280-eaf1-11ea-831e-cbe4252c34c3.png)

## 概要

WoT 1.10.0.0 で廃止されたチャットコマンドです。

WoT 1.10.0.0 でチャットシステムが大きく変更され
([[更新] 戦闘コミュニケーションが進化！](https://worldoftanks.asia/ja/news/general-news/1-10-battle-communication/))、
従来あった F5 の "了解！" (Affirmative) や、F6 の "拒否！" (Negative) コマンドは廃止されました。

この mod は F5 で "了解! (Affirmative!)", F6 で "拒否! (Negative!)" のチャットメッセージを送信するものです。

組み込みのチャットコマンドではなく、テキストメッセージを送信するので、
受信側のクライアントでの翻訳はありません。
英語クライアントに対しても日本語メッセージがそのまま送られます
(そのため、英語メッセージも同時に送るようにしています)。

日本語以外のクライアントで使用した場合には、
単に "Affirmative!", "Negative!" のように英語メッセージのみを送信します。
