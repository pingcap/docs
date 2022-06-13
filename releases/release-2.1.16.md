---
title: TiDB 2.1.16 Release Notes
---

# TiDB2.1.16リリースノート {#tidb-2-1-16-release-notes}

発売日：2019年8月15日

TiDBバージョン：2.1.16

TiDB Ansibleバージョン：2.1.16

## TiDB {#tidb}

-   SQLオプティマイザー
    -   時間列[＃11526](https://github.com/pingcap/tidb/pull/11526)の等しい条件に対して、行数が不正確に推定される問題を修正します。
    -   `TIDB_INLJ`ヒントが有効にならない、または指定されたテーブルで有効にならないという問題を修正します[＃11361](https://github.com/pingcap/tidb/pull/11361)
    -   クエリの`NOT EXISTS`の実装をOUTERJOINからANTIJOINに変更して、より最適化された実行プラン[＃11291](https://github.com/pingcap/tidb/pull/11291)を見つけます。
    -   `SHOW`ステートメント内のサブクエリをサポートし、 [＃11461](https://github.com/pingcap/tidb/pull/11461)などの構文を許可し`SHOW COLUMNS FROM tbl WHERE FIELDS IN (SELECT 'a')`
    -   定数畳み込みの最適化によって`SELECT … CASE WHEN … ELSE NULL ...`クエリが誤った結果を取得する問題を修正します[＃11441](https://github.com/pingcap/tidb/pull/11441)
-   SQL実行エンジン
    -   `INTERVAL`が負の場合に`DATE_ADD`関数が間違った結果を得る問題を修正します[＃11616](https://github.com/pingcap/tidb/pull/11616)
    -   `FLOAT` 、または`DECIMAL`型`DOUBLE`の引数を受け入れると、型変換が誤って実行されるため、 `DATE_ADD`関数が誤った結果を取得する可能性がある問題を修正し[＃11628](https://github.com/pingcap/tidb/pull/11628) 。
    -   CAST（JSON AS SIGNED）がオーバーフローしたときにエラーメッセージが不正確になる問題を修正します[＃11562](https://github.com/pingcap/tidb/pull/11562)
    -   1つの子ノードを閉じることができず、Executor [＃11598](https://github.com/pingcap/tidb/pull/11598)を閉じるプロセス中にエラーを返すと、他の子ノードが閉じられない問題を修正します。
    -   タイムアウト[＃11487](https://github.com/pingcap/tidb/pull/11487)の前にリージョンスキャッターのスケジューリングが終了していない場合に、エラーではなく、正常に分割されたリージョンの数と終了したパーセンテージを返す`SPLIT TABLE`のステートメントをサポートします。
    -   MySQL [＃11505](https://github.com/pingcap/tidb/pull/11505)と互換性があるように、 `REGEXP BINARY`の関数の大文字と小文字を区別する
    -   5/7の結果の`YEAR`の値が`DATE_ADD`より小さいか`DATE_SUB`より大きい場合にオーバーフローするため、 `NULL`が正しく返されない問題を修正し[＃11477](https://github.com/pingcap/tidb/pull/11477) 。
    -   低速クエリテーブルに、実行が成功したかどうかを示す`Succ`フィールドを追加します[＃11412](https://github.com/pingcap/tidb/pull/11421)
    -   SQLステートメントに現在の時刻（ `CURRENT_TIMESTAMP`や`NOW`など）の計算が含まれる場合に、現在のタイムスタンプを複数回フェッチすることによって引き起こされるMySQLの非互換性の問題を修正します[＃11392](https://github.com/pingcap/tidb/pull/11392)
    -   AUTO_INCREMENT列がFLOATまたはDOUBLEタイプ[＃11389](https://github.com/pingcap/tidb/pull/11389)を処理しない問題を修正します
    -   `CONVERT_TZ`関数が無効な引数[＃11357](https://github.com/pingcap/tidb/pull/11357)を受け入れると、 `NULL`が正しく返されない問題を修正します。
    -   `PARTITION BY LIST`ステートメントでエラーが報告される問題を修正します。 （現在、構文のみがサポートされています。TiDBがステートメントを実行すると、通常のテーブルが作成され、プロンプトメッセージが表示されます） [＃11236](https://github.com/pingcap/tidb/pull/11236)
    -   `Mod(%)` 、および`Multiple(*)`の操作で、小数点以下の桁数が多い場合（ `0` `Minus(-)`結果が返される問題を修正し`select 0.000 % 0.11234500000000000000` [＃11353](https://github.com/pingcap/tidb/pull/11353)
-   サーバ
    -   `OnInit`がコールバックされたときにプラグインが`NULL`のドメインを取得する問題を修正します[＃11426](https://github.com/pingcap/tidb/pull/11426)
    -   スキーマが削除された後も、スキーマ内のテーブル情報がHTTPインターフェイスを介して取得できるという問題を修正します[＃11586](https://github.com/pingcap/tidb/pull/11586)
-   DDL
    -   この操作によって引き起こされる自動インクリメント列の誤った結果を回避するために、自動インクリメント列へのインデックスの削除を禁止します[＃11402](https://github.com/pingcap/tidb/pull/11402)
    -   異なる文字セットと照合でテーブルを作成および変更するときに、列の文字セットが正しくないという問題を修正します[＃11423](https://github.com/pingcap/tidb/pull/11423)
    -   `alter table ... set default...`と、この列を変更する別のDDLステートメントが並行して実行されるときに列スキーマが正しくなくなる可能性がある問題を修正します[＃11374](https://github.com/pingcap/tidb/pull/11374)
    -   生成された列Aが生成された列Bに依存し、Aを使用してインデックス[＃11538](https://github.com/pingcap/tidb/pull/11538)を作成すると、データが埋め戻されない問題を修正します。
    -   `ADMIN CHECK TABLE`の操作をスピードアップ[＃11538](https://github.com/pingcap/tidb/pull/11676)

## TiKV {#tikv}

-   クライアントが閉じられているTiKV領域にアクセスしたときにエラーメッセージを返すことをサポートします[＃4820](https://github.com/tikv/tikv/pull/4820)
-   リバース`raw_scan`および`raw_batch_scan`インターフェイス[＃5148](https://github.com/tikv/tikv/pull/5148)をサポート

## ツール {#tools}

-   TiDB Binlog
    -   トランザクション[＃697](https://github.com/pingcap/tidb-binlog/pull/697)で一部のステートメントの実行をスキップするには、Drainerに`ignore-txn-commit-ts`の構成アイテムを追加します。
    -   起動時に構成項目チェックを追加します。これにより、Pump and Drainerの実行が停止し、無効な構成項目を満たすとエラーメッセージが返されます[＃708](https://github.com/pingcap/tidb-binlog/pull/708)
    -   Drainerに`node-id`の構成を追加して、Drainerのノード[＃706](https://github.com/pingcap/tidb-binlog/pull/706)を指定します。
-   TiDB Lightning
    -   2つのチェックサムが同時に実行されているときに`tikv_gc_life_time`が元の値に戻らないという問題を修正します[＃224](https://github.com/pingcap/tidb-lightning/pull/224)

## TiDB Ansible {#tidb-ansible}

-   Spark3に`log4j`の構成ファイルを追加し[＃842](https://github.com/pingcap/tidb-ansible/pull/842)
-   tisparkjarパッケージを[＃863](https://github.com/pingcap/tidb-ansible/pull/863)に更新します。
-   [＃845](https://github.com/pingcap/tidb-ansible/pull/845)がKafkaまたはZooKeeper1を使用すると、Prometheus構成ファイルが間違った形式で生成される問題を修正します。
-   `rolling_update.yml`操作の実行時にPDがリーダーの切り替えに失敗するバグを修正します[＃888](https://github.com/pingcap/tidb-ansible/pull/888)
-   安定性を向上させるために、PDノードのローリング更新のロジックを最適化します-最初にフォロワーをアップグレードし、次にリーダーをアップグレードします[＃895](https://github.com/pingcap/tidb-ansible/pull/895)
