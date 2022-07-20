---
title: TiCDC Open Protocol
summary: Learn the concept of TiCDC Open Protocol and how to use it.
---

# TiCDCオープンプロトコル {#ticdc-open-protocol}

TiCDC Open Protocolは、行レベルのデータ変更通知プロトコルであり、監視、キャッシング、フルテキストインデックス作成、分析エンジン、および異なるデータベース間のプライマリ-セカンダリレプリケーション用のデータソースを提供します。 TiCDCはTiCDCOpenProtocolに準拠し、TiDBのデータ変更をMQ（メッセージキュー）などのサードパーティのデータメディアに複製します。

TiCDC Open Protocolは、イベントを基本ユニットとして使用して、データ変更イベントをダウンストリームに複製します。イベントは3つのカテゴリに分けられます。

-   行変更イベント：行のデータ変更を表します。行が変更されると、このイベントが送信され、変更された行に関する情報が含まれます。
-   DDLイベント：DDLの変更を表します。このイベントは、アップストリームでDDLステートメントが正常に実行された後に送信されます。 DDLイベントはすべてのMQパーティションにブロードキャストされます。
-   解決されたイベント：受信したイベントが完了する前の特別な時点を表します。

## 制限 {#restrictions}

-   ほとんどの場合、バージョンの行変更イベントは1回だけ送信されますが、ノード障害やネットワークパーティションなどの特殊な状況では、同じバージョンの行変更イベントが複数回送信される場合があります。
-   同じテーブルで、最初に送信された各バージョンの行変更イベントは、イベントストリームのタイムスタンプ（TS）の順序でインクリメントされます。
-   解決されたイベントは、各MQパーティションに定期的にブロードキャストされます。解決済みイベントとは、解決済みイベントTSより前のTSを持つイベントがダウンストリームに送信されたことを意味します。
-   DDLイベントは各MQパーティションにブロードキャストされます。
-   行の複数の行変更イベントが同じMQパーティションに送信されます。

## メッセージ形式 {#message-format}

メッセージには、次の形式で配置された1つ以上のイベントが含まれます。

鍵：

| オフセット（バイト） | 0〜7        | 8〜15 | 16〜（15 +長さ1） | ..。 | ..。      |
| :--------- | :--------- | :--- | :----------- | :-- | :------- |
| パラメータ      | プロトコルバージョン | 長さ1  | イベントキー1      | 長さN | イベントKeyN |

価値：

| オフセット（バイト） | 0〜7 | 8〜（7 +長さ1） | ..。 | ..。    |
| :--------- | :-- | :--------- | :-- | :----- |
| パラメータ      | 長さ1 | イベント値1     | 長さN | イベント値N |

-   `LengthN`は、 `N`番目のキー/値の長さを表します。
-   長さとプロトコルバージョンはビッグエンディアン`int64`タイプです。
-   現在のプロトコルのバージョンは`1`です。

## イベント形式 {#event-format}

このセクションでは、行変更イベント、DDLイベント、および解決済みイベントの形式を紹介します。

### 行変更イベント {#row-changed-event}

-   **鍵：**

    ```
    {
        "ts":<TS>,
        "scm":<Schema Name>,
        "tbl":<Table Name>,
        "t":1
    }
    ```

    | パラメータ | タイプ | 説明                          |
    | :---- | :-- | :-------------------------- |
    | TS    | 番号  | 行の変更を引き起こすトランザクションのタイムスタンプ。 |
    | スキーマ名 | 弦   | 行が含まれるスキーマの名前。              |
    | テーブル名 | 弦   | 行が含まれるテーブルの名前。              |

-   **価値：**

    `Insert`イベント。新しく追加された行データが出力されます。

    ```
    {
        "u":{
            <Column Name>:{
                "t":<Column Type>,
                "h":<Where Handle>,
                "f":<Flag>,
                "v":<Column Value>
            },
            <Column Name>:{
                "t":<Column Type>,
                "h":<Where Handle>,
                "f":<Flag>,
                "v":<Column Value>
            }
        }
    }
    ```

    `Update`イベント。新しく追加された行データ（ &quot;u&quot;）と更新前の行データ（ &quot;p&quot;）が出力されます。後者（ &quot;p&quot;）は、古い値機能が有効になっている場合にのみ出力されます。

    ```
    {
        "u":{
            <Column Name>:{
                "t":<Column Type>,
                "h":<Where Handle>,
                "f":<Flag>,
                "v":<Column Value>
            },
            <Column Name>:{
                "t":<Column Type>,
                "h":<Where Handle>,
                "f":<Flag>,
                "v":<Column Value>
            }
        },
        "p":{
            <Column Name>:{
                "t":<Column Type>,
                "h":<Where Handle>,
                "f":<Flag>,
                "v":<Column Value>
            },
            <Column Name>:{
                "t":<Column Type>,
                "h":<Where Handle>,
                "f":<Flag>,
                "v":<Column Value>
            }
        }
    }
    ```

    `Delete`イベント。削除した行データを出力します。古い値機能が有効になっている場合、 `Delete`イベントには、削除された行データのすべての列が含まれます。この機能を無効にすると、 `Delete`イベントには[HandleKey](#bit-flags-of-columns)列のみが含まれます。

    ```
    {
        "d":{
            <Column Name>:{
                "t":<Column Type>,
                "h":<Where Handle>,
                "f":<Flag>,
                "v":<Column Value>
            },
            <Column Name>:{
                "t":<Column Type>,
                "h":<Where Handle>,
                "f":<Flag>,
                "v":<Column Value>
            }
        }
    }
    ```

    | パラメータ    | タイプ  | 説明                                                                              |
    | :------- | :--- | :------------------------------------------------------------------------------ |
    | カラム名     | 弦    | 列名。                                                                             |
    | カラムタイプ   | 番号   | 列タイプ。詳細については、 [カラムタイプコード](#column-type-code)を参照してください。                          |
    | ハンドルする場所 | ブール値 | この列が`Where`節のフィルター条件になり得るかどうかを判別します。この列がテーブル上で一意である場合、 `Where Handle`は`true`です。 |
    | 国旗       | 番号   | 列のビットフラグ。詳細については、 [列のビットフラグ](#bit-flags-of-columns)を参照してください。                   |
    | カラムの値    | どれでも | カラムの値。                                                                          |

### DDLイベント {#ddl-event}

-   **鍵：**

    ```
    {
        "ts":<TS>,
        "scm":<Schema Name>,
        "tbl":<Table Name>,
        "t":2
    }
    ```

    | パラメータ | タイプ | 説明                            |
    | :---- | :-- | :---------------------------- |
    | TS    | 番号  | DDL変更を実行するトランザクションのタイムスタンプ。   |
    | スキーマ名 | 弦   | DDL変更のスキーマ名。空の文字列である可能性があります。 |
    | テーブル名 | 弦   | DDL変更のテーブル名。空の文字列である可能性があります。 |

-   **価値：**

    ```
    {
        "q":<DDL Query>,
        "t":<DDL Type>
    }
    ```

    | パラメータ  | タイプ | 説明                                                    |
    | :----- | :-- | :---------------------------------------------------- |
    | DDLクエリ | 弦   | DDLクエリSQL                                             |
    | DDLタイプ | 弦   | DDLタイプ。詳細については、 [DDLタイプコード](#ddl-type-code)を参照してください。 |

### 解決されたイベント {#resolved-event}

-   **鍵：**

    ```
    {
        "ts":<TS>,
        "t":3
    }
    ```

    | パラメータ | タイプ | 説明                                 |
    | :---- | :-- | :--------------------------------- |
    | TS    | 番号  | 解決されたタイムスタンプ。このイベントより前のTSが送信されました。 |

-   **値：**なし

## イベントストリーム出力の例 {#examples-of-the-event-stream-output}

このセクションでは、イベントストリームの出力ログを表示および表示します。

アップストリームで次のSQLステートメントを実行し、MQパーティション番号が2であるとします。

{{< copyable "" >}}

```sql
CREATE TABLE test.t1(id int primary key, val varchar(16));
```

次のログ1とログ3から、DDLイベントがすべてのMQパーティションにブロードキャストされ、解決されたイベントが各MQパーティションに定期的にブロードキャストされていることがわかります。

```
1. [partition=0] [key="{\"ts\":415508856908021766,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":2}"] [value="{\"q\":\"CREATE TABLE test.t1(id int primary key, val varchar(16))\",\"t\":3}"]
2. [partition=0] [key="{\"ts\":415508856908021766,\"t\":3}"] [value=]
3. [partition=1] [key="{\"ts\":415508856908021766,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":2}"] [value="{\"q\":\"CREATE TABLE test.t1(id int primary key, val varchar(16))\",\"t\":3}"]
4. [partition=1] [key="{\"ts\":415508856908021766,\"t\":3}"] [value=]
```

アップストリームで次のSQLステートメントを実行します。

{{< copyable "" >}}

```sql
BEGIN;
INSERT INTO test.t1(id, val) VALUES (1, 'aa');
INSERT INTO test.t1(id, val) VALUES (2, 'aa');
UPDATE test.t1 SET val = 'bb' WHERE id = 2;
INSERT INTO test.t1(id, val) VALUES (3, 'cc');
COMMIT;
```

-   次のログ5とログ6から、同じテーブルの行変更イベントが主キーに基づいて異なるパーティションに送信される可能性があることがわかりますが、同じ行への変更は同じパーティションに送信されるため、ダウンストリームは簡単に実行できますイベントを同時に処理します。
-   ログ6から、トランザクション内の同じ行に対する複数の変更は、1つの行変更イベントでのみ送信されます。
-   ログ8は、ログ7の繰り返しイベントです。行変更イベントは繰り返される場合がありますが、各バージョンの最初のイベントは順番に送信されます。

```
5. [partition=0] [key="{\"ts\":415508878783938562,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"u\":{\"id\":{\"t\":3,\"h\":true,\"v\":1},\"val\":{\"t\":15,\"v\":\"YWE=\"}}}"]
6. [partition=1] [key="{\"ts\":415508878783938562,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"u\":{\"id\":{\"t\":3,\"h\":true,\"v\":2},\"val\":{\"t\":15,\"v\":\"YmI=\"}}}"]
7. [partition=0] [key="{\"ts\":415508878783938562,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"u\":{\"id\":{\"t\":3,\"h\":true,\"v\":3},\"val\":{\"t\":15,\"v\":\"Y2M=\"}}}"]
8. [partition=0] [key="{\"ts\":415508878783938562,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"u\":{\"id\":{\"t\":3,\"h\":true,\"v\":3},\"val\":{\"t\":15,\"v\":\"Y2M=\"}}}"]
```

アップストリームで次のSQLステートメントを実行します。

{{< copyable "" >}}

```sql
BEGIN;
DELETE FROM test.t1 WHERE id = 1;
UPDATE test.t1 SET val = 'dd' WHERE id = 3;
UPDATE test.t1 SET id = 4, val = 'ee' WHERE id = 2;
COMMIT;
```

-   ログ9は、 `Delete`タイプの行変更イベントです。このタイプのイベントには、主キー列または一意のインデックス列のみが含まれます。
-   ログ13とログ14は解決されたイベントです。解決済みイベントとは、このパーティションで、解決済みTSよりも小さいイベント（行変更イベントおよびDDLイベントを含む）が送信されたことを意味します。

```
9. [partition=0] [key="{\"ts\":415508881418485761,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"d\":{\"id\":{\"t\":3,\"h\":true,\"v\":1}}}"]
10. [partition=1] [key="{\"ts\":415508881418485761,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"d\":{\"id\":{\"t\":3,\"h\":true,\"v\":2}}}"]
11. [partition=0] [key="{\"ts\":415508881418485761,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"u\":{\"id\":{\"t\":3,\"h\":true,\"v\":3},\"val\":{\"t\":15,\"v\":\"ZGQ=\"}}}"]
12. [partition=0] [key="{\"ts\":415508881418485761,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"u\":{\"id\":{\"t\":3,\"h\":true,\"v\":4},\"val\":{\"t\":15,\"v\":\"ZWU=\"}}}"]
13. [partition=0] [key="{\"ts\":415508881038376963,\"t\":3}"] [value=]
14. [partition=1] [key="{\"ts\":415508881038376963,\"t\":3}"] [value=]
```

## 消費者のためのプロトコル解析 {#protocol-parsing-for-consumers}

現在、TiCDCはTiCDC Open Protocolの標準解析ライブラリを提供していませんが、GolangバージョンとJavaバージョンの解析例が提供されています。このドキュメントと次の例で提供されているデータ形式を参照して、コンシューマーのプロトコル解析を実装できます。

-   [Golangの例](https://github.com/pingcap/tiflow/tree/master/cmd/kafka-consumer)
-   [Javaの例](https://github.com/pingcap/tiflow/tree/master/examples/java)

## カラムタイプコード {#column-type-code}

`Column Type Code`は、行変更イベントの列データ型を表します。

| タイプ                     | コード    | 出力例                                                                                                                                    | 説明                                                           |
| :---------------------- | :----- | :------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------- |
| TINYINT / BOOLEAN       | 1      | {&quot;t&quot;：1、 &quot;v&quot;：1}                                                                                                     |                                                              |
| SMALLINT                | 2      | {&quot;t&quot;：2、 &quot;v&quot;：1}                                                                                                     |                                                              |
| INT                     | 3      | {&quot;t&quot;：3、 &quot;v&quot;：123}                                                                                                   |                                                              |
| 浮く                      | 4      | {&quot;t&quot;：4、 &quot;v&quot;：153.123}                                                                                               |                                                              |
| ダブル                     | 5      | {&quot;t&quot;：5、 &quot;v&quot;：153.123}                                                                                               |                                                              |
| ヌル                      | 6      | {&quot;t&quot;：6、 &quot;v&quot;：null}                                                                                                  |                                                              |
| タイムスタンプ                 | 7      | {&quot;t&quot;：7、 &quot;v&quot;： &quot;1973-12-30 15:30:00&quot;}                                                                      |                                                              |
| BIGINT                  | 8      | {&quot;t&quot;：8、 &quot;v&quot;：123}                                                                                                   |                                                              |
| MEDIUMINT               | 9      | {&quot;t&quot;：9、 &quot;v&quot;：123}                                                                                                   |                                                              |
| 日にち                     | 10/14  | {&quot;t&quot;：10、 &quot;v&quot;： &quot;2000-01-01&quot;}                                                                              |                                                              |
| 時間                      | 11     | {&quot;t&quot;：11、 &quot;v&quot;： &quot;23:59:59&quot;}                                                                                |                                                              |
| 日付時刻                    | 12     | {&quot;t&quot;：12、 &quot;v&quot;： &quot;2015-12-20 23:58:58&quot;}                                                                     |                                                              |
| 年                       | 13     | {&quot;t&quot;：13、 &quot;v&quot;：1970}                                                                                                 |                                                              |
| VARCHAR / VARBINARY     | 15/253 | {&quot;t&quot;：15、 &quot;v&quot;： &quot;test&quot;} / {&quot;t&quot;：15、 &quot;v&quot;： &quot;\\ x89PNG \\ r \\ n \\ x1a \\ n&quot;}   | 値はUTF-8でエンコードされます。アップストリームタイプがVARBINARYの場合、非表示の文字はエスケープされます。 |
| 少し                      | 16     | {&quot;t&quot;：16、 &quot;v&quot;：81}                                                                                                   |                                                              |
| JSON                    | 245    | {&quot;t&quot;：245、 &quot;v&quot;： &quot;{\&quot; key1 \ &quot;：\&quot; value1 \ &quot;}&quot;}                                        |                                                              |
| 10進数                    | 246    | {&quot;t&quot;：246、 &quot;v&quot;： &quot;129012.1230000&quot;}                                                                         |                                                              |
| ENUM                    | 247    | {&quot;t&quot;：247、 &quot;v&quot;：1}                                                                                                   |                                                              |
| 設定                      | 248    | {&quot;t&quot;：248、 &quot;v&quot;：3}                                                                                                   |                                                              |
| TINYTEXT / TINYBLOB     | 249    | {&quot;t&quot;：249、 &quot;v&quot;： &quot;5rWL6K + VdGV4dA ==&quot;}                                                                    | 値はBase64でエンコードされます。                                          |
| MEDIUMTEXT / MEDIUMBLOB | 250    | {&quot;t&quot;：250、 &quot;v&quot;： &quot;5rWL6K + VdGV4dA ==&quot;}                                                                    | 値はBase64でエンコードされます。                                          |
| LONGTEXT / LONGBLOB     | 251    | {&quot;t&quot;：251、 &quot;v&quot;： &quot;5rWL6K + VdGV4dA ==&quot;}                                                                    | 値はBase64でエンコードされます。                                          |
| TEXT / BLOB             | 252    | {&quot;t&quot;：252、 &quot;v&quot;： &quot;5rWL6K + VdGV4dA ==&quot;}                                                                    | 値はBase64でエンコードされます。                                          |
| CHAR / BINARY           | 254    | {&quot;t&quot;：254、 &quot;v&quot;： &quot;test&quot;} / {&quot;t&quot;：254、 &quot;v&quot;： &quot;\\ x89PNG \\ r \\ n \\ x1a \\ n&quot;} | 値はUTF-8でエンコードされます。アップストリームタイプがBINARYの場合、非表示の文字はエスケープされます。    |
| 幾何学                     | 255    |                                                                                                                                        | サポートされていません                                                  |

## DDLタイプコード {#ddl-type-code}

`DDL Type Code`は、DDLイベントのDDLステートメントタイプを表します。

| タイプ                 | コード |
| :------------------ | :-- |
| スキーマの作成             | 1   |
| ドロップスキーマ            | 2   |
| テーブルの作成             | 3   |
| ドロップテーブル            | 4   |
| カラムを追加              | 5   |
| ドロップカラム             | 6   |
| インデックスを追加           | 7   |
| ドロップインデックス          | 8   |
| 外部キーを追加する           | 9   |
| 外部キーをドロップする         | 10  |
| テーブルの切り捨て           | 11  |
| カラムを変更              | 12  |
| 自動IDをリベース           | 13  |
| テーブルの名前を変更          | 14  |
| デフォルト値の設定           | 15  |
| シャードRowID           | 16  |
| テーブルコメントの変更         | 17  |
| インデックスの名前を変更        | 18  |
| テーブルパーティションを追加する    | 19  |
| テーブルパーティションを削除する    | 20  |
| ビューの作成              | 21  |
| テーブルの文字セットを変更して照合する | 22  |
| テーブルパーティションを切り捨てる   | 23  |
| ドロップビュー             | 24  |
| テーブルを回復する           | 25  |
| スキーマ文字セットを変更して照合する  | 26  |
| ロックテーブル             | 27  |
| テーブルのロックを解除         | 28  |
| 修理テーブル              | 29  |
| TiFlashレプリカを設定します   | 30  |
| TiFlashレプリカステータスの更新 | 31  |
| 主キーを追加する            | 32  |
| 主キーを削除します           | 33  |
| シーケンスの作成            | 34  |
| シーケンスの変更            | 35  |
| ドロップシーケンス           | 36  |

## 列のビットフラグ {#bit-flags-of-columns}

ビットフラグは、列の特定の属性を表します。

| 少し | 価値   | 名前                  | 説明                      |
| :- | :--- | :------------------ | :---------------------- |
| 1  | 0x01 | BinaryFlag          | 列がバイナリエンコードされた列であるかどうか。 |
| 2  | 0x02 | HandleKeyFlag       | 列がハンドルインデックス列であるかどうか。   |
| 3  | 0x04 | GeneratedColumnFlag | 列が生成された列であるかどうか。        |
| 4  | 0x08 | PrimaryKeyFlag      | 列が主キー列であるかどうか。          |
| 5  | 0x10 | UniqueKeyFlag       | 列が一意のインデックス列であるかどうか。    |
| 6  | 0x20 | MultipleKeyFlag     | 列が複合インデックス列であるかどうか。     |
| 7  | 0x40 | NullableFlag        | 列がNULL可能列であるかどうか。       |
| 8  | 0x80 | UnsignedFlag        | 列が符号なし列であるかどうか。         |

例：

列フラグの値が`85`の場合、その列はnull許容列、一意のインデックス列、生成された列、およびバイナリエンコードされた列です。

```
85 == 0b_101_0101
   == NullableFlag | UniqueKeyFlag | GeneratedColumnFlag | BinaryFlag
```

列の値が`46`の場合、その列は複合インデックス列、主キー列、生成された列、およびハンドルキー列です。

```
46 == 0b_010_1110
   == MultipleKeyFlag | PrimaryKeyFlag | GeneratedColumnFlag | HandleKeyFlag
```

> **ノート：**
>
> -   `BinaryFlag`は、列タイプがBLOB / TEXT（TINYBLOB/TINYTEXTおよびBINARY/CHARを含む）の場合にのみ意味があります。アップストリーム列がBLOBタイプの場合、 `BinaryFlag`の値は`1`に設定されます。アップストリーム列がTEXTタイプの場合、 `BinaryFlag`の値は`0`に設定されます。
> -   アップストリームからテーブルを複製するために、TiCDCはハンドルインデックスとして[有効なインデックス](/ticdc/ticdc-overview.md#restrictions)を選択します。 Handleインデックス列の`HandleKeyFlag`値は`1`に設定されます。
