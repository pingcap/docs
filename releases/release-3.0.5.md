---
title: TiDB 3.0.5 Release Notes
---

# TiDB 3.0.5 リリースノート {#tidb-3-0-5-release-notes}

発売日：2019年10月25日

TiDB バージョン: 3.0.5

TiDB アンシブル バージョン: 3.0.5

## TiDB {#tidb}

-   SQL オプティマイザー
    -   Window 関数の境界チェックをサポート[#12404](https://github.com/pingcap/tidb/pull/12404)
    -   パーティション テーブルの`IndexJoin`が間違った結果を返す問題を修正[#12712](https://github.com/pingcap/tidb/pull/12712)
    -   外部結合`Apply`演算子の上部にある`ifnull`関数が間違った結果を返す問題を修正します[#12694](https://github.com/pingcap/tidb/pull/12694)
    -   `UPDATE` [#12597](https://github.com/pingcap/tidb/pull/12597)の`where`条件にサブクエリが含まれていると更新に失敗する問題を修正
    -   `cast`関数がクエリ条件に含まれている場合、外部結合が内部結合に誤って変換される問題を修正[#12790](https://github.com/pingcap/tidb/pull/12790)
    -   `AntiSemiJoin` [#12799](https://github.com/pingcap/tidb/pull/12799)の結合条件で誤った式を渡す問題を修正
    -   統計の初期化時に浅いコピーによって引き起こされる統計エラーを修正します[#12817](https://github.com/pingcap/tidb/pull/12817)
    -   日付文字列とフォーマット文字列が一致しない場合、TiDB の`str_to_date`関数が MySQL とは異なる結果を返す問題を修正します[#12725](https://github.com/pingcap/tidb/pull/12725)
-   SQL 実行エンジン
    -   `from_unixtime`関数が null [#12551](https://github.com/pingcap/tidb/pull/12551)を処理するときのpanicの問題を修正
    -   DDL ジョブのキャンセル時に報告された`invalid list index`エラーを修正[#12671](https://github.com/pingcap/tidb/pull/12671)
    -   ウィンドウ関数使用時に配列が範囲外になる問題を修正[#12660](https://github.com/pingcap/tidb/pull/12660)
    -   `AutoIncrement`列が暗黙的に割り当てられた場合の動作を改善し、MySQL 自動インクリメント ロックのデフォルト モードとの一貫性を保ちます ( [「連続」ロックモード](https://dev.mysql.com/doc/refman/5.7/en/innodb-auto-increment-handling.html) ): 1 行の`Insert`ステートメントで複数の`AutoIncrement` ID を暗黙的に割り当てる場合、TiDB は割り当てられた値の連続性。この改善により、JDBC `getGeneratedKeys()`メソッドがどのシナリオでも正しい結果を得ることが保証されます。 [#12602](https://github.com/pingcap/tidb/pull/12602)
    -   `HashAgg` `Apply` [#12766](https://github.com/pingcap/tidb/pull/12766)の子ノードになるとクエリがハングアップする問題を修正
    -   型変換時に`AND`と`OR`論理式が間違った結果を返す問題を修正[#12811](https://github.com/pingcap/tidb/pull/12811)
-   サーバ
    -   後で大規模なトランザクションをサポートできるようにトランザクション TTL を変更するインターフェイス関数を実装する[#12397](https://github.com/pingcap/tidb/pull/12397)
    -   悲観的トランザクションをサポートするために、必要に応じてトランザクション TTL を延長するサポート (最大 10 分) [#12579](https://github.com/pingcap/tidb/pull/12579)
    -   TiDB がスキーマの変更とそれに対応する変更されたテーブル情報をキャッシュする回数を 100 から 1024 に調整し、 `tidb_max_delta_schema_count`システム変数[#12502](https://github.com/pingcap/tidb/pull/12502)を使用して変更をサポートします
    -   `kvrpc.Cleanup`プロトコルの動作を更新して、残業していないトランザクションのロックを消去しないようにします[#12417](https://github.com/pingcap/tidb/pull/12417)
    -   `information_schema.tables`テーブル[#12631](https://github.com/pingcap/tidb/pull/12631)へのパーティション テーブル情報のロギングをサポート
    -   `region-cache-ttl` [#12683](https://github.com/pingcap/tidb/pull/12683)を構成することにより、リージョンキャッシュの TTL の変更をサポートします。
    -   実行計画の圧縮エンコードされた情報のスロー ログへの出力をサポートします。この機能はデフォルトで有効になっており、 `slow-log-plan`構成または`tidb_record_plan_in_slow_log`変数を使用して制御できます。さらに、 `tidb_decode_plan`関数は、スロー ログ内の実行計画列のエンコードされた情報を実行計画情報にデコードできます。 [#12808](https://github.com/pingcap/tidb/pull/12808)
    -   `information_schema.processlist`テーブルでのメモリ使用量情報の表示をサポート[#12801](https://github.com/pingcap/tidb/pull/12801)
    -   TiKV クライアントがアイドル状態の接続を判断すると、エラーや予期しないアラームが発生する可能性がある問題を修正します[#12846](https://github.com/pingcap/tidb/pull/12846)
    -   `tikvSnapshot`が`BatchGet()` [#12872](https://github.com/pingcap/tidb/pull/12872)の KV 結果を適切にキャッシュしないため、 `INSERT IGNORE`ステートメントのパフォーマンスが低下する問題を修正します。
    -   一部の KV サービスへの接続が遅いため、TiDB の応答速度が比較的遅かった問題を修正しました[#12814](https://github.com/pingcap/tidb/pull/12814)
-   DDL
    -   `Create Table`操作で Set 列[#12267](https://github.com/pingcap/tidb/pull/12267)の Int 型のデフォルト値が正しく設定されない問題を修正
    -   `Create Table`ステートメントで一意のインデックスを作成するときに複数の`unique`をサポートします[#12463](https://github.com/pingcap/tidb/pull/12463)
    -   `Alter Table` [#12489](https://github.com/pingcap/tidb/pull/12489)使用してビット タイプの列を追加するときに、既存の行にこの列の既定値を入力するとエラーが発生する可能性があるという問題を修正します。
    -   範囲パーティションテーブルが日付型または日時型の列を分割キーとして使用している場合に、分割を追加できない問題を修正します[#12815](https://github.com/pingcap/tidb/pull/12815)
    -   Date または Datetime 型の列をパーティション キーとして使用する Range パーティションパーティションテーブルについて、テーブルの作成時またはパーティションの追加時に、パーティションの種類とパーティション キーの種類の整合性チェックをサポートします[#12792](https://github.com/pingcap/tidb/pull/12792)
    -   レンジパーティションテーブル[#12718](https://github.com/pingcap/tidb/pull/12718)を作成するときに、一意のキー列セットがパーティション分割された列セット以上である必要があるというチェックを追加します。
-   モニター
    -   コミットおよびロールバック操作のモニタリング メトリックをダッシュボードに追加する`Transaction OPS` [#12505](https://github.com/pingcap/tidb/pull/12505)
    -   `Add Index`操作の進行状況の監視メトリクスを追加[#12390](https://github.com/pingcap/tidb/pull/12390)

## TiKV {#tikv}

-   保管所
    -   悲観的トランザクションの新機能を追加: トランザクション クリーンアップ インターフェイスは、TTL が古いロックのクリーンアップのみをサポートします[#5589](https://github.com/tikv/tikv/pull/5589)
    -   トランザクションのロールバック主キーが崩れる問題を修正[#5646](https://github.com/tikv/tikv/pull/5646) , [#5671](https://github.com/tikv/tikv/pull/5671)
    -   悲観的ロックの下で、ポイント クエリが以前のバージョンのデータを返す可能性があるという問題を修正します[#5634](https://github.com/tikv/tikv/pull/5634)
-   Raftstore
    -   Raftstoreでのメッセージ フラッシュ操作を減らしてパフォーマンスを改善し、CPU 使用率を削減する[#5617](https://github.com/tikv/tikv/pull/5617)
    -   リージョンサイズとキーの推定数を取得するコストを最適化し、ハートビートのオーバーヘッドと CPU 使用率を削減します[#5620](https://github.com/tikv/tikv/pull/5620)
    -   無効なデータを取得すると、 Raftstore がエラー ログを出力panicが発生する問題を修正します[#5643](https://github.com/tikv/tikv/pull/5643)
-   エンジン
    -   RocksDB `force_consistency_checks`有効にしてデータの安全性を向上させる[#5662](https://github.com/tikv/tikv/pull/5662)
    -   Titan での同時フラッシュ操作がデータ損失を引き起こす可能性があるという問題を修正します[#5672](https://github.com/tikv/tikv/pull/5672)
    -   [#5710](https://github.com/tikv/tikv/pull/5710)内圧縮による TiKV のクラッシュと再起動の問題を回避するために、rust-rocksdb のバージョンを更新します。

## PD {#pd}

-   リージョン[#1782](https://github.com/pingcap/pd/pull/1782)が占有するstorageの精度を向上させる
-   `--help`コマンド[#1763](https://github.com/pingcap/pd/pull/1763)の出力を改善する
-   TLS が有効になった後、HTTP 要求がリダイレクトに失敗する問題を修正します[#1777](https://github.com/pingcap/pd/pull/1777)
-   pd-ctl が`store shows limit`コマンド[#1808](https://github.com/pingcap/pd/pull/1808)を使用するときに発生したpanicの問題を修正します。
-   ラベル監視メトリクスの読みやすさを改善し、リーダーが切り替わったときに元のリーダーの監視データをリセットして、誤ったレポートを回避します[#1815](https://github.com/pingcap/pd/pull/1815)

## ツール {#tools}

-   TiDBBinlog
    -   `ALTER DATABASE`関連する DDL 操作によってDrainerが異常終了する問題を修正[#769](https://github.com/pingcap/tidb-binlog/pull/769)
    -   コミットbinlogのトランザクション ステータス情報のクエリをサポートして、レプリケーションの効率を向上させます[#757](https://github.com/pingcap/tidb-binlog/pull/757)
    -   Drainer の`start_ts` Pump の最大の`commit_ts` [#758](https://github.com/pingcap/tidb-binlog/pull/758)より大きい場合、 Pumppanicが発生する可能性がある問題を修正します。
-   TiDB Lightning
    -   ローダーの完全なロジック インポート機能を統合し、バックエンド モードの構成をサポートします[#221](https://github.com/pingcap/tidb-lightning/pull/221)

## TiDB アンシブル {#tidb-ansible}

-   インデックス速度[#986](https://github.com/pingcap/tidb-ansible/pull/986)を追加するモニタリング メトリックを追加します。
-   構成ファイルの内容を簡素化し、ユーザーが構成する必要のないパラメーターを削除します[#1043c](https://github.com/pingcap/tidb-ansible/commit/1043c3df7ddb72eb234c55858960e9fdd3830a14) 、 [#998](https://github.com/pingcap/tidb-ansible/pull/998)
-   パフォーマンスリード、パフォーマンスライト[#e90e7](https://github.com/pingcap/tidb-ansible/commit/e90e79f5117bb89197e01b1391fd02e25d57a440)の監視式エラーを修正
-   Raftstore CPU使用率[#992](https://github.com/pingcap/tidb-ansible/pull/992)の監視表示方法とアラームルールを更新
-   オーバービュー モニタリング ダッシュボードの TiKV CPU モニタリング アイテムを更新して、余分なモニタリング コンテンツを除外します[#1001](https://github.com/pingcap/tidb-ansible/pull/1001)
