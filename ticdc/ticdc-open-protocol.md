---
title: TiCDC Open Protocol
summary: Learn the concept of TiCDC Open Protocol and how to use it.
---

# TiCDC オープン プロトコル {#ticdc-open-protocol}

TiCDC Open Protocol は、監視、キャッシング、フルテキスト インデックス作成、分析エンジン、および異なるデータベース間のプライマリ/セカンダリ レプリケーションのためのデータ ソースを提供する、行レベルのデータ変更通知プロトコルです。 TiCDC は TiCDC Open Protocol に準拠し、TiDB のデータ変更を MQ (Message Queue) などのサードパーティのデータ媒体に複製します。

TiCDC Open Protocol は、イベントを基本単位として使用して、データ変更イベントをダウンストリームに複製します。イベントは次の 3 つのカテゴリに分類されます。

-   行変更イベント: 行のデータ変更を表します。行が変更されると、このイベントが送信され、変更された行に関する情報が含まれます。
-   DDL イベント: DDL の変更を表します。このイベントは、DDL ステートメントがアップストリームで正常に実行された後に送信されます。 DDL イベントはすべての MQ パーティションにブロードキャストされます。
-   解決済みイベント: 受信したイベントが完了する前の特別な時点を表します。

## 制限 {#restrictions}

-   ほとんどの場合、バージョンの Row Changed Event は 1 回だけ送信されますが、ノード障害やネットワーク パーティションなどの特殊な状況では、同じバージョンの Row Changed Event が複数回送信されることがあります。
-   同じテーブルで、最初に送信された各バージョンの行変更イベントは、イベント ストリームのタイムスタンプ (TS) の順序で増加します。
-   解決済みイベントは、各 MQ パーティションに定期的にブロードキャストされます。 Resolved Event は、Resolved Event TS より前の TS を持つイベントがダウンストリームに送信されたことを意味します。
-   DDL イベントは各 MQ パーティションにブロードキャストされます。
-   行の複数の行変更イベントが同じ MQ パーティションに送信されます。

## メッセージ形式 {#message-format}

メッセージには、次の形式で配置された 1 つ以上のイベントが含まれます。

鍵：

| オフセット(バイト) | 0~7         | 8~15 | 16~(15+丈1) | ... | ...     |
| :--------- | :---------- | :--- | :--------- | :-- | :------ |
| パラメータ      | プロトコルのバージョン | 長さ1  | イベント キー 1  | 長さN | イベントキーN |

価値：

| オフセット(バイト) | 0~7 | 8~(7+長さ1) | ... | ...    |
| :--------- | :-- | :-------- | :-- | :----- |
| パラメータ      | 長さ1 | イベント値1    | 長さN | イベント値N |

-   `LengthN` `N`番目のキー/値の長さを表します。
-   長さとプロトコルバージョンはビッグエンディアンの`int64`型です。
-   現在のプロトコルのバージョンは`1`です。

## イベント形式 {#event-format}

このセクションでは、行変更イベント、DDL イベント、および解決イベントの形式を紹介します。

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
    | TS    | 番号  | 行変更の原因となったトランザクションのタイムスタンプ。 |
    | スキーマ名 | 弦   | 行が含まれるスキーマの名前。              |
    | テーブル名 | 弦   | 行が含まれるテーブルの名前。              |

-   **価値：**

    `Insert`イベント。新たに追加された行データが出力されます。

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

    `Update`イベント。新たに追加された行データ（「u」）と更新前の行データ（「p」）が出力されます。後者 (「p」) は、古い値機能が有効になっている場合にのみ出力されます。

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

    `Delete`イベント。削除された行データが出力されます。古い値機能が有効になっている場合、 `Delete`イベントには、削除された行データのすべての列が含まれます。この機能が無効になっている場合、 `Delete`イベントには[ハンドルキー](#bit-flags-of-columns)列のみが含まれます。

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

    | パラメータ   | タイプ  | 説明                                                                         |
    | :------ | :--- | :------------------------------------------------------------------------- |
    | カラム名    | 弦    | 列名。                                                                        |
    | カラムの種類  | 番号   | 列のタイプ。詳細については、 [カラムタイプ コード](#column-type-code)を参照してください。                   |
    | どこでハンドル | ブール値 | この列が`Where`句のフィルター条件になるかどうかを決定します。この列がテーブルで一意の場合、 `Where Handle`は`true`です。 |
    | 国旗      | 番号   | 列のビット フラグ。詳細については、 [列のビット フラグ](#bit-flags-of-columns)を参照してください。            |
    | カラムの値   | どれでも | カラムの値。                                                                     |

### DDL イベント {#ddl-event}

-   **鍵：**

    ```
    {
        "ts":<TS>,
        "scm":<Schema Name>,
        "tbl":<Table Name>,
        "t":2
    }
    ```

    | パラメータ | タイプ | 説明                           |
    | :---- | :-- | :--------------------------- |
    | TS    | 番号  | DDL 変更を実行するトランザクションのタイムスタンプ。 |
    | スキーマ名 | 弦   | DDL 変更のスキーマ名。空の文字列の場合があります。  |
    | テーブル名 | 弦   | DDL 変更のテーブル名。空の文字列の場合があります。  |

-   **価値：**

    ```
    {
        "q":<DDL Query>,
        "t":<DDL Type>
    }
    ```

    | パラメータ   | タイプ | 説明                                                       |
    | :------ | :-- | :------------------------------------------------------- |
    | DDL クエリ | 弦   | DDL クエリ SQL                                              |
    | DDL タイプ | 弦   | DDL タイプ。詳細については、 [DDL タイプ コード](#ddl-type-code)を参照してください。 |

### 解決済みのイベント {#resolved-event}

-   **鍵：**

    ```
    {
        "ts":<TS>,
        "t":3
    }
    ```

    | パラメータ | タイプ | 説明                                       |
    | :---- | :-- | :--------------------------------------- |
    | TS    | 番号  | 解決済みのタイムスタンプ。このイベントより前の TS はすべて送信されています。 |

-   **値:**なし

## イベント ストリーム出力の例 {#examples-of-the-event-stream-output}

このセクションには、イベント ストリームの出力ログが表示されます。

アップストリームで次の SQL ステートメントを実行し、MQ パーティション番号が 2 であるとします。

{{< copyable "" >}}

```sql
CREATE TABLE test.t1(id int primary key, val varchar(16));
```

次のログ 1 とログ 3 から、DDL イベントがすべての MQ パーティションにブロードキャストされ、解決済みイベントが各 MQ パーティションに定期的にブロードキャストされていることがわかります。

```
1. [partition=0] [key="{\"ts\":415508856908021766,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":2}"] [value="{\"q\":\"CREATE TABLE test.t1(id int primary key, val varchar(16))\",\"t\":3}"]
2. [partition=0] [key="{\"ts\":415508856908021766,\"t\":3}"] [value=]
3. [partition=1] [key="{\"ts\":415508856908021766,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":2}"] [value="{\"q\":\"CREATE TABLE test.t1(id int primary key, val varchar(16))\",\"t\":3}"]
4. [partition=1] [key="{\"ts\":415508856908021766,\"t\":3}"] [value=]
```

アップストリームで次の SQL ステートメントを実行します。

{{< copyable "" >}}

```sql
BEGIN;
INSERT INTO test.t1(id, val) VALUES (1, 'aa');
INSERT INTO test.t1(id, val) VALUES (2, 'aa');
UPDATE test.t1 SET val = 'bb' WHERE id = 2;
INSERT INTO test.t1(id, val) VALUES (3, 'cc');
COMMIT;
```

-   次のログ 5 とログ 6 から、同じテーブルの行変更イベントが主キーに基づいて異なるパーティションに送信される可能性があることがわかりますが、同じ行への変更は同じパーティションに送信されるため、ダウンストリームは簡単に変更できます。イベントを同時に処理します。
-   ログ 6 以降、トランザクション内の同じ行に対する複数の変更は、1 つの行変更イベントでのみ送信されます。
-   ログ 8 はログ 7 の繰り返しイベントです。行変更イベントは繰り返される可能性がありますが、各バージョンの最初のイベントは順番に送信されます。

```
5. [partition=0] [key="{\"ts\":415508878783938562,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"u\":{\"id\":{\"t\":3,\"h\":true,\"v\":1},\"val\":{\"t\":15,\"v\":\"YWE=\"}}}"]
6. [partition=1] [key="{\"ts\":415508878783938562,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"u\":{\"id\":{\"t\":3,\"h\":true,\"v\":2},\"val\":{\"t\":15,\"v\":\"YmI=\"}}}"]
7. [partition=0] [key="{\"ts\":415508878783938562,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"u\":{\"id\":{\"t\":3,\"h\":true,\"v\":3},\"val\":{\"t\":15,\"v\":\"Y2M=\"}}}"]
8. [partition=0] [key="{\"ts\":415508878783938562,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"u\":{\"id\":{\"t\":3,\"h\":true,\"v\":3},\"val\":{\"t\":15,\"v\":\"Y2M=\"}}}"]
```

アップストリームで次の SQL ステートメントを実行します。

{{< copyable "" >}}

```sql
BEGIN;
DELETE FROM test.t1 WHERE id = 1;
UPDATE test.t1 SET val = 'dd' WHERE id = 3;
UPDATE test.t1 SET id = 4, val = 'ee' WHERE id = 2;
COMMIT;
```

-   ログ 9 は、 `Delete`タイプの行変更イベントです。このタイプのイベントには、主キー列または一意のインデックス列のみが含まれます。
-   ログ 13 とログ 14 は解決済みイベントです。 Resolved Event は、このパーティションで Resolved TS より小さいイベント (Row Changed Event および DDL Event を含む) が送信されたことを意味します。

```
9. [partition=0] [key="{\"ts\":415508881418485761,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"d\":{\"id\":{\"t\":3,\"h\":true,\"v\":1}}}"]
10. [partition=1] [key="{\"ts\":415508881418485761,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"d\":{\"id\":{\"t\":3,\"h\":true,\"v\":2}}}"]
11. [partition=0] [key="{\"ts\":415508881418485761,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"u\":{\"id\":{\"t\":3,\"h\":true,\"v\":3},\"val\":{\"t\":15,\"v\":\"ZGQ=\"}}}"]
12. [partition=0] [key="{\"ts\":415508881418485761,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"u\":{\"id\":{\"t\":3,\"h\":true,\"v\":4},\"val\":{\"t\":15,\"v\":\"ZWU=\"}}}"]
13. [partition=0] [key="{\"ts\":415508881038376963,\"t\":3}"] [value=]
14. [partition=1] [key="{\"ts\":415508881038376963,\"t\":3}"] [value=]
```

## コンシューマー向けのプロトコル解析 {#protocol-parsing-for-consumers}

現在、TiCDC は TiCDC Open Protocol の標準解析ライブラリを提供していませんが、解析例のGolangバージョンとJavaバージョンが提供されています。このドキュメントで提供されているデータ形式と次の例を参照して、コンシューマー向けのプロトコル解析を実装できます。

-   [Golang の例](https://github.com/pingcap/tiflow/tree/master/cmd/kafka-consumer)
-   [Javaの例](https://github.com/pingcap/tiflow/tree/master/examples/java)

## カラムタイプ コード {#column-type-code}

`Column Type Code`行変更イベントの列データ型を表します。

| タイプ                   | コード    | 出力例                                                                                                                       | 説明                                                                |
| :-------------------- | :----- | :------------------------------------------------------------------------------------------------------------------------ | :---------------------------------------------------------------- |
| TINYINT/ブール値          | 1      | {&quot;t&quot;:1,&quot;v&quot;:1}                                                                                         |                                                                   |
| SMALLINT              | 2      | {&quot;t&quot;:2,&quot;v&quot;:1}                                                                                         |                                                                   |
| INT                   | 3      | {&quot;t&quot;:3,&quot;v&quot;:123}                                                                                       |                                                                   |
| 浮く                    | 4      | {&quot;t&quot;:4,&quot;v&quot;:153.123}                                                                                   |                                                                   |
| ダブル                   | 5      | {&quot;t&quot;:5,&quot;v&quot;:153.123}                                                                                   |                                                                   |
| ヌル                    | 6      | {&quot;t&quot;:6,&quot;v&quot;:null}                                                                                      |                                                                   |
| タイムスタンプ               | 7      | {&quot;t&quot;:7,&quot;v&quot;:&quot;1973-12-30 15:30:00&quot;}                                                           |                                                                   |
| BIGINT                | 8      | {&quot;t&quot;:8,&quot;v&quot;:123}                                                                                       |                                                                   |
| ミディアムミント              | 9      | {&quot;t&quot;:9,&quot;v&quot;:123}                                                                                       |                                                                   |
| 日にち                   | 10/14  | {&quot;t&quot;:10,&quot;v&quot;:&quot;2000-01-01&quot;}                                                                   |                                                                   |
| 時間                    | 11     | {&quot;t&quot;:11,&quot;v&quot;:&quot;23:59:59&quot;}                                                                     |                                                                   |
| 日付時刻                  | 12     | {&quot;t&quot;:12,&quot;v&quot;:&quot;2015-12-20 23:58:58&quot;}                                                          |                                                                   |
| 年                     | 13     | {&quot;t&quot;:13,&quot;v&quot;:1970}                                                                                     |                                                                   |
| VARCHAR/VARBINARY     | 15/253 | {&quot;t&quot;:15,&quot;v&quot;:&quot;test&quot;} / {&quot;t&quot;:15,&quot;v&quot;:&quot;\\x89PNG\\r\\n\\x1a\\n&quot;}   | 値は UTF-8 でエンコードされます。アップストリーム タイプが VARBINARY の場合、非表示の文字はエスケープされます。 |
| 少し                    | 16     | {&quot;t&quot;:16,&quot;v&quot;:81}                                                                                       |                                                                   |
| JSON                  | 245    | {&quot;t&quot;:245,&quot;v&quot;:&quot;{\&quot;key1\&quot;: \&quot;value1\&quot;}&quot;}                                  |                                                                   |
| 小数                    | 246    | {&quot;t&quot;:246,&quot;v&quot;:&quot;129012.1230000&quot;}                                                              |                                                                   |
| 列挙型                   | 247    | {&quot;t&quot;:247,&quot;v&quot;:1}                                                                                       |                                                                   |
| 設定                    | 248    | {&quot;t&quot;:248,&quot;v&quot;:3}                                                                                       |                                                                   |
| TINYTEXT/TINYBLOB     | 249    | {&quot;t&quot;:249,&quot;v&quot;:&quot;5rWL6K+VdGV4dA==&quot;}                                                            | 値は Base64 でエンコードされます。                                             |
| MEDIUMTEXT/MEDIUMBLOB | 250    | {&quot;t&quot;:250,&quot;v&quot;:&quot;5rWL6K+VdGV4dA==&quot;}                                                            | 値は Base64 でエンコードされます。                                             |
| LONGTEXT/LONGBLOB     | 251    | {&quot;t&quot;:251,&quot;v&quot;:&quot;5rWL6K+VdGV4dA==&quot;}                                                            | 値は Base64 でエンコードされます。                                             |
| TEXT/BLOB             | 252    | {&quot;t&quot;:252,&quot;v&quot;:&quot;5rWL6K+VdGV4dA==&quot;}                                                            | 値は Base64 でエンコードされます。                                             |
| 文字/バイナリ               | 254    | {&quot;t&quot;:254,&quot;v&quot;:&quot;test&quot;} / {&quot;t&quot;:254,&quot;v&quot;:&quot;\\x89PNG\\r\\n\\x1a\\n&quot;} | 値は UTF-8 でエンコードされます。アップストリーム タイプが BINARY の場合、非表示の文字はエスケープされます。    |
| ジオメトリ                 | 255    |                                                                                                                           | サポートされていません                                                       |

## DDL タイプ コード {#ddl-type-code}

`DDL Type Code` DDL イベントの DDL ステートメント タイプを表します。

| タイプ                  | コード |
| :------------------- | :-- |
| スキーマの作成              | 1   |
| スキーマを削除              | 2   |
| テーブルの作成              | 3   |
| ドロップ テーブル            | 4   |
| カラムを追加               | 5   |
| カラムをドロップ             | 6   |
| インデックスを追加            | 7   |
| ドロップ インデックス          | 8   |
| 外部キーを追加              | 9   |
| 外部キーを削除              | 10  |
| テーブルの切り捨て            | 11  |
| カラムの変更               | 12  |
| 自動 ID のリベース          | 13  |
| テーブル名の変更             | 14  |
| デフォルト値を設定            | 15  |
| シャード RowID           | 16  |
| テーブル コメントの変更         | 17  |
| インデックスの名前を変更         | 18  |
| テーブル パーティションの追加      | 19  |
| テーブル パーティションの削除      | 20  |
| ビューを作成               | 21  |
| 表の文字セットを変更して照合する     | 22  |
| テーブル パーティションの切り捨て    | 23  |
| ビューをドロップ             | 24  |
| テーブルの回復              | 25  |
| スキーマの文字セットを変更して照合する  | 26  |
| テーブルのロック             | 27  |
| テーブルのロックを解除          | 28  |
| 修理表                  | 29  |
| TiFlashレプリカの設定       | 30  |
| TiFlashレプリカ ステータスの更新 | 31  |
| 主キーを追加               | 32  |
| 主キーを削除               | 33  |
| シーケンスを作成             | 34  |
| シーケンスの変更             | 35  |
| ドロップシーケンス            | 36  |

## 列のビット フラグ {#bit-flags-of-columns}

ビット フラグは、列の特定の属性を表します。

| 少し | 価値   | 名前                  | 説明                       |
| :- | :--- | :------------------ | :----------------------- |
| 1  | 0x01 | BinaryFlag          | 列がバイナリ エンコードされた列であるかどうか。 |
| 2  | 0x02 | ハンドルキーフラグ           | 列がハンドル インデックス列であるかどうか。   |
| 3  | 0x04 | GeneratedColumnFlag | 列が生成列かどうか。               |
| 4  | 0x08 | PrimaryKeyFlag      | 列が主キー列であるかどうか。           |
| 5  | 0x10 | ユニークキーフラグ           | 列が一意のインデックス列であるかどうか。     |
| 6  | 0x20 | 複数キーフラグ             | 列が複合インデックス列であるかどうか。      |
| 7  | 0x40 | NullableFlag        | 列が null 許容列であるかどうか。      |
| 8  | 0x80 | 未署名フラグ              | 列が署名されていない列かどうか。         |

例：

列フラグの値が`85`の場合、その列は null 許容列、一意のインデックス列、生成された列、およびバイナリ エンコードされた列です。

```
85 == 0b_101_0101
   == NullableFlag | UniqueKeyFlag | GeneratedColumnFlag | BinaryFlag
```

列の値が`46`の場合、その列は複合インデックス列、主キー列、生成列、およびハンドル キー列です。

```
46 == 0b_010_1110
   == MultipleKeyFlag | PrimaryKeyFlag | GeneratedColumnFlag | HandleKeyFlag
```

> **ノート：**
>
> -   `BinaryFlag`列の型が BLOB/ TEXT (TINYBLOB/TINYTEXT および BINARY/CHAR を含む) の場合のみ意味があります。上流の列が BLOB 型の場合、 `BinaryFlag`値は`1`に設定されます。上流列がTEXTタイプの場合、 `BinaryFlag`値は`0`に設定されます。
> -   アップストリームからテーブルを複製するために、TiCDC はハンドル インデックスとして[有効なインデックス](/ticdc/ticdc-overview.md#best-practices)を選択します。ハンドル インデックス列の`HandleKeyFlag`値は`1`に設定されます。
