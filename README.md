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


## 設定

デフォルトのメッセージを変更することができます。

設定ファイルは `<WoT_game_folder>/mods/configs/chirimen.chatex/config.json` です。

デフォルトの設定は、次の設定ファイルを設置した場合と等価です。
書式は JSON です。

```python
{
    "en": {
        "KEY_F5":   "Affirmative!",
        "KEY_F6":   "Negative!"
    },
    "ja": {
        "KEY_F5":   "了解! (Affirmative!)",
        "KEY_F6":   "拒否! (Negative!)"
    }
}
```

上の例で、"en" や "ja" のキーは WoT クライアントの言語設定に対応します。
該当する設定が存在しない場合は "en" が使用されます。

"KEY_F5", "KEY_F6" 以外のショートカットキー設定も可能ですが、
他の機能割当がされていない場合に限ります。
機能割当されているショートカットキーを指定した場合の動作は保証されません。
