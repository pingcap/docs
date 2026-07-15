---
title: TiDB 2.1.16 Release Notes
summary: TiDB 2.1.16は2019年8月15日にリリースされました。SQLオプティマイザー、SQL実行エンジン、サーバー、DDL、TiKV、TiDB Binlog、 TiDB Lightning 、TiDB Ansibleに関する様々な修正と改善が含まれています。主な変更点としては、SHOWステートメント内のサブクエリのサポート、DATE_ADD関数の問題の修正、TiDB BinlogのDrainerへの設定項目の追加などが挙げられます。
---

# TiDB 2.1.16 リリースノート {#tidb-2-1-16-release-notes}

発売日：2019年8月15日

TiDB バージョン: 2.1.16

TiDB Ansible バージョン: 2.1.16

## TiDB {#tidb}

-   SQLオプティマイザー
    -   時間列等号条件で行数が不正確に推定される問題を修正しました [＃11526](https://github.com/pingcap/tidb/pull/11526)
    -   `TIDB_INLJ`ヒントが有効にならない、または指定されたテーブルに有効にならない問題を修正 [＃11361](https://github.com/pingcap/tidb/pull/11361)
    -   クエリの`NOT EXISTS`の実装をOUTER JOINからANTI JOINに変更して、より最適化された実行プラン見つけます [＃11291](https://github.com/pingcap/tidb/pull/11291)
    -   `SHOW`文内でサブクエリをサポートし、 `SHOW COLUMNS FROM tbl WHERE FIELDS IN (SELECT 'a')` のような構文が可能 [＃11461](https://github.com/pingcap/tidb/pull/11461)
    -   定数畳み込み最適化によって`SELECT … CASE WHEN … ELSE NULL ...`クエリが誤った結果を取得する問題を修正 [＃11441](https://github.com/pingcap/tidb/pull/11441)
-   SQL実行エンジン
    -   `INTERVAL`が負の場合に`DATE_ADD`関数が間違った結果を返す問題を修正しました [＃11616](https://github.com/pingcap/tidb/pull/11616)
    -   `DATE_ADD`関数が`FLOAT` 、 `DOUBLE` 、または`DECIMAL`型の引数を受け入れるときに型変換を誤って実行するため、誤った結果が返される可能性がある問題を修正しました[＃11628](https://github.com/pingcap/tidb/pull/11628)
    -   CAST(JSON AS SIGNED)がオーバーフローしたときにエラーメッセージが不正確になる問題を修正しました [＃11562](https://github.com/pingcap/tidb/pull/11562)
    -   1 つの子ノードが閉じられず、Executor を閉じる処理中にエラーが返された場合に、他の子ノードが閉じられない問題を修正しました。 [＃11598](https://github.com/pingcap/tidb/pull/11598)
    -   タイムアウトまでにリージョン分散のスケジュールが完了していない場合に、エラーではなく、正常に分割されたリージョンの数と完了したパーセンテージを返す`SPLIT TABLE`ステートメントをサポートします。 [＃11487](https://github.com/pingcap/tidb/pull/11487)
    -   MySQL との互換性を保つために、 `REGEXP BINARY`関数で大文字と小文字を区別する [＃11505](https://github.com/pingcap/tidb/pull/11505)
    -   `DATE_ADD` / `DATE_SUB`の結果の`YEAR`の値が 0 より小さいかより大きい場合にオーバーフローするため、 `NULL`が正しく返されない問題を修正しました。 [＃11477](https://github.com/pingcap/tidb/pull/11477)
    -   スロークエリテーブルに、実行が成功したかどうかを示すフィールドを`Succ`追加します[＃11412](https://github.com/pingcap/tidb/pull/11421)
    -   SQL文に現在の時刻（ `CURRENT_TIMESTAMP`や`NOW`など）の計算が含まれる場合に、現在のタイムスタンプを複数回取得することによって発生するMySQLの非互換性の問題を修正しました[＃11392](https://github.com/pingcap/tidb/pull/11392)
    -   AUTO_INCREMENT列がFLOATまたはDOUBLE型処理できない問題を修正 [＃11389](https://github.com/pingcap/tidb/pull/11389)
    -   `CONVERT_TZ`関数が無効な引数を受け入れたときに`NULL`が正しく返されない問題を修正しました [＃11357](https://github.com/pingcap/tidb/pull/11357)
    -   `PARTITION BY LIST`文でエラーが報告される問題を修正しました。(現在は構文のみがサポートされています。TiDBが文を実行すると、通常のテーブルが作成され、プロンプトメッセージが表示されます) [＃11236](https://github.com/pingcap/tidb/pull/11236)
    -   `Mod(%)` `Multiple(*)`演算で、 `Minus(-)`以下の桁数が多い場合（ `select 0.000 % 0.11234500000000000000`など）に MySQL の結果と矛盾する`0`結果が返される問題を修正しました[＃11353](https://github.com/pingcap/tidb/pull/11353)
-   サーバ
    -   `OnInit` コールバックされたときにプラグインが`NULL`ドメインを取得する問題を修正 [＃11426](https://github.com/pingcap/tidb/pull/11426)
    -   スキーマを削除した後でも、スキーマ内のテーブル情報が HTTP インターフェース経由で取得できる問題を修正しました[＃11586](https://github.com/pingcap/tidb/pull/11586)
-   DDL
    -   AUTO_INCREMENT列のインデックスの削除を禁止して、この操作によってAUTO_INCREMENT列の誤った結果が発生するのを防ぎます[＃11402](https://github.com/pingcap/tidb/pull/11402)
    -   異なる文字セットと照合順序でテーブルを作成および変更するときに、列の文字セットが正しくない問題を修正しました[＃11423](https://github.com/pingcap/tidb/pull/11423)
    -   `alter table ... set default...`とこの列を変更する別の DDL 文が並列で実行されると列スキーマが間違ってしまう可能性がある問題を修正しました[＃11374](https://github.com/pingcap/tidb/pull/11374)
    -   生成カラムAが生成カラムBに依存し、Aがインデックス作成に使用される場合、データのバックフィルが失敗する問題を修正しました。 [＃11538](https://github.com/pingcap/tidb/pull/11538)
    -   `ADMIN CHECK TABLE`操作高速化 [＃11538](https://github.com/pingcap/tidb/pull/11676)

## TiKV {#tikv}

-   クライアントが閉じられている TiKVリージョンにアクセスしたときにエラーメッセージを返す機能をサポート[＃4820](https://github.com/tikv/tikv/pull/4820)
-   リバース`raw_scan`および`raw_batch_scan`インターフェースサポート [＃5148](https://github.com/tikv/tikv/pull/5148)

## ツール {#tools}

-   TiDB Binlog
    -   トランザクション内の一部のステートメントの実行をスキップするために、 Drainerに`ignore-txn-commit-ts`構成項目を追加します。 [＃697](https://github.com/pingcap/tidb-binlog/pull/697)
    -   起動時に構成項目のチェックを追加し、PumpとDrainerの実行を停止し、無効な構成項目に該当する場合にエラーメッセージを返します。 [＃708](https://github.com/pingcap/tidb-binlog/pull/708)
    -   DrainerのノードID を指定するためにDrainerに`node-id`設定を追加します。 [＃706](https://github.com/pingcap/tidb-binlog/pull/706)
-   TiDB Lightning
    -   2つのチェックサムが同時に実行されているときに`tikv_gc_life_time`元の値に戻せない問題を修正しました[＃224](https://github.com/pingcap/tidb-lightning/pull/224)

## TiDB Ansible {#tidb-ansible}

-   Spark に`log4j`設定ファイルを追加する [＃842](https://github.com/pingcap/tidb-ansible/pull/842)
-   tispark jarパッケージをv2.1.2 に更新します [＃863](https://github.com/pingcap/tidb-ansible/pull/863)
-   TiDB Binlog がKafka または ZooKeeper 使用する場合に Prometheus 構成ファイルが間違った形式で生成される問題を修正しました [＃845](https://github.com/pingcap/tidb-ansible/pull/845)
-   `rolling_update.yml`オペレーション実行時にPDがLeaderの切り替えに失敗するバグを修正 [＃888](https://github.com/pingcap/tidb-ansible/pull/888)
-   PDノードのローリング更新ロジックを最適化 - フォロワーを最初にアップグレードし、次にLeaderをアップグレード - 安定性を向上[＃895](https://github.com/pingcap/tidb-ansible/pull/895)
