---
title: TiDB 3.0.5 Release Notes
---

# TiDB3.0.5リリースノート {#tidb-3-0-5-release-notes}

発売日：2019年10月25日

TiDBバージョン：3.0.5

TiDB Ansibleバージョン：3.0.5

## TiDB {#tidb}

-   SQLオプティマイザー
    -   ウィンドウ関数[＃12404](https://github.com/pingcap/tidb/pull/12404)の境界チェックをサポート
    -   パーティションテーブルの`IndexJoin`が誤った結果を返す問題を修正します[＃12712](https://github.com/pingcap/tidb/pull/12712)
    -   外部結合`Apply`演算子の上部にある`ifnull`関数が誤った結果を返す問題を修正します[＃12694](https://github.com/pingcap/tidb/pull/12694)
    -   サブクエリが[＃12597](https://github.com/pingcap/tidb/pull/12597)の`where`条件に含まれている場合の更新失敗の問題を修正し`UPDATE`
    -   `cast`関数がクエリ条件[＃12790](https://github.com/pingcap/tidb/pull/12790)に含まれている場合に、外部結合が誤って内部結合に変換される問題を修正します。
    -   [＃12799](https://github.com/pingcap/tidb/pull/12799)の結合条件で渡される誤った`AntiSemiJoin`を修正しました
    -   統計を初期化するときに浅いコピーによって引き起こされる統計エラーを修正します[＃12817](https://github.com/pingcap/tidb/pull/12817)
    -   日付文字列とフォーマット文字列が[＃12725](https://github.com/pingcap/tidb/pull/12725)と一致しない場合、TiDBの`str_to_date`関数がMySQLとは異なる結果を返す問題を修正します。
-   SQL実行エンジン
    -   `from_unixtime`関数がnull3を処理するときのパニックの問題を修正し[＃12551](https://github.com/pingcap/tidb/pull/12551)
    -   DDLジョブをキャンセルするときに報告される`invalid list index`のエラーを修正します[＃12671](https://github.com/pingcap/tidb/pull/12671)
    -   ウィンドウ関数が使用されているときに配列が範囲外であった問題を修正します[＃12660](https://github.com/pingcap/tidb/pull/12660)
    -   暗黙的に割り当てられた場合の`AutoIncrement`列の動作を改善し、MySQL自動インクリメントロックのデフォルトモードとの一貫性を維持します（ [「連続」ロックモード](https://dev.mysql.com/doc/refman/5.7/en/innodb-auto-increment-handling.html) ）。単一行の`Insert`ステートメントで複数の`AutoIncrement` IDを暗黙的に割り当てる場合、TiDBは割り当てられた値の連続性。この改善により、 `getGeneratedKeys()`メソッドはどのシナリオでも正しい結果を得ることができます。 [＃12602](https://github.com/pingcap/tidb/pull/12602)
    -   `HashAgg`が[＃12766](https://github.com/pingcap/tidb/pull/12766)の子ノードとして機能するときにクエリがハングする問題を修正し`Apply`
    -   型変換[＃12811](https://github.com/pingcap/tidb/pull/12811)に関して、 `AND`と`OR`の論理式が誤った結果を返す問題を修正します。
-   サーバ
    -   後で大規模なトランザクションをサポートできるようにトランザクションTTLを変更するインターフェイス機能を実装する[＃12397](https://github.com/pingcap/tidb/pull/12397)
    -   悲観的なトランザクションをサポートするために、必要に応じてトランザクションTTLの拡張をサポートします（最大10分） [＃12579](https://github.com/pingcap/tidb/pull/12579)
    -   TiDBがスキーマの変更と対応する変更されたテーブル情報を100から1024にキャッシュする回数を調整し、 `tidb_max_delta_schema_count`のシステム変数[＃12502](https://github.com/pingcap/tidb/pull/12502)を使用して変更をサポートします。
    -   `kvrpc.Cleanup`プロトコルの動作を更新して、時間外でないトランザクションのロックをクリーンアップしないようにします[＃12417](https://github.com/pingcap/tidb/pull/12417)
    -   `information_schema.tables`のテーブルへのパーティションテーブル情報のロギングをサポート[＃12631](https://github.com/pingcap/tidb/pull/12631)
    -   `region-cache-ttl` [＃12683](https://github.com/pingcap/tidb/pull/12683)を構成することにより、リージョンキャッシュのTTLの変更をサポートします
    -   実行プランの圧縮エンコードされた情報を低速ログに出力することをサポートします。この機能はデフォルトで有効になっており、 `slow-log-plan`構成または`tidb_record_plan_in_slow_log`変数を使用して制御できます。さらに、 `tidb_decode_plan`関数は、スローログ内の実行プラン列にエンコードされた情報を実行プラン情報にデコードできます。 [＃12808](https://github.com/pingcap/tidb/pull/12808)
    -   `information_schema.processlist`テーブル[＃12801](https://github.com/pingcap/tidb/pull/12801)でのメモリ使用量情報の表示をサポートします。
    -   TiKVクライアントがアイドル状態の接続を判断したときにエラーや予期しないアラームが発生する可能性がある問題を修正します[＃12846](https://github.com/pingcap/tidb/pull/12846)
    -   `tikvSnapshot`が[＃12872](https://github.com/pingcap/tidb/pull/12872)のKV結果を適切にキャッシュしないため、 `INSERT IGNORE`ステートメントのパフォーマンスが低下する問題を修正し`BatchGet()` 。
    -   一部のKVサービスへの接続が遅いためにTiDBの応答速度が比較的遅いという問題を修正します[＃12814](https://github.com/pingcap/tidb/pull/12814)
-   DDL
    -   `Create Table`操作でSet列[＃12267](https://github.com/pingcap/tidb/pull/12267)のIntタイプのデフォルト値が正しく設定されない問題を修正します。
    -   `Create Table`ステートメントで一意のインデックスを作成するときに複数の`unique`をサポートする[＃12463](https://github.com/pingcap/tidb/pull/12463)
    -   この列のデフォルト値を既存の行に入力すると、 `Alter Table`を使用してビットタイプの列を追加するときにエラーが発生する可能性がある問題を修正し[＃12489](https://github.com/pingcap/tidb/pull/12489) 。
    -   Rangeパーティションテーブルが日付または日時タイプの列をパーティションキーとして使用する場合のパーティションの追加の失敗を修正します[＃12815](https://github.com/pingcap/tidb/pull/12815)
    -   テーブルの作成時またはパーティションの追加時に、パーティションキーとして[日付]または[日時タイプ]列を持つ範囲パーティションテーブルのパーティションタイプとパーティションキータイプの整合性のチェックをサポートします[＃12792](https://github.com/pingcap/tidb/pull/12792)
    -   範囲パーティションテーブルを作成するときに、一意キー列セットがパーティション列セット以上である必要があるというチェックを追加します[＃12718](https://github.com/pingcap/tidb/pull/12718)
-   モニター
    -   コミットおよびロールバック操作の監視メトリックを`Transaction OPS`のダッシュボードに追加します[＃12505](https://github.com/pingcap/tidb/pull/12505)
    -   `Add Index`操作の進捗状況[＃12390](https://github.com/pingcap/tidb/pull/12390)の監視メトリックを追加します

## TiKV {#tikv}

-   保管所
    -   悲観的トランザクションの新機能を追加します。トランザクションクリーンアップインターフェイスは、TTLが古くなっているロックのクリーンアップのみをサポートします[＃5589](https://github.com/tikv/tikv/pull/5589)
    -   トランザクションの主キーのロールバックが折りたたまれている問題を修正し[＃5671](https://github.com/tikv/tikv/pull/5671) [＃5646](https://github.com/tikv/tikv/pull/5646)
    -   悲観的なロックの下で、ポイントクエリが以前のバージョンのデータを返す可能性があるという問題を修正します[＃5634](https://github.com/tikv/tikv/pull/5634)
-   ラフトストア
    -   Raftstoreでのメッセージフラッシュ操作を減らして、パフォーマンスを向上させ、CPU使用率を減らします[＃5617](https://github.com/tikv/tikv/pull/5617)
    -   リージョンサイズと推定キー数を取得するコストを最適化して、ハートビートのオーバーヘッドとCPU使用率を削減します[＃5620](https://github.com/tikv/tikv/pull/5620)
    -   Raftstoreがエラーログを出力し、無効なデータを取得するとパニックが発生する問題を修正します[＃5643](https://github.com/tikv/tikv/pull/5643)
-   エンジン
    -   `force_consistency_checks`を有効にしてデータの安全性を向上させる[＃5662](https://github.com/tikv/tikv/pull/5662)
    -   Titanでの同時フラッシュ操作がデータ損失を引き起こす可能性がある問題を修正します[＃5672](https://github.com/tikv/tikv/pull/5672)
    -   rust-rocksdbバージョンを更新して、L0内の圧縮によって引き起こされるTiKVのクラッシュと再起動の問題を回避します[＃5710](https://github.com/tikv/tikv/pull/5710)

## PD {#pd}

-   リージョン[＃1782](https://github.com/pingcap/pd/pull/1782)が占めるストレージの精度を向上させる
-   `--help`コマンドの出力を改善する[＃1763](https://github.com/pingcap/pd/pull/1763)
-   TLSを有効にした後にHTTPリクエストがリダイレクトに失敗する問題を修正します[＃1777](https://github.com/pingcap/pd/pull/1777)
-   pd-ctlが`store shows limit`コマンドを使用するときに発生したパニックの問題を修正します[＃1808](https://github.com/pingcap/pd/pull/1808)
-   誤ったレポートを回避するために、ラベル監視メトリックの読みやすさを改善し、リーダーが切り替わったときに元のリーダーの監視データをリセットします[＃1815](https://github.com/pingcap/pd/pull/1815)

## ツール {#tools}

-   TiDB Binlog
    -   `ALTER DATABASE`の関連するDDL操作によってDrainerが異常終了する問題を修正します[＃769](https://github.com/pingcap/tidb-binlog/pull/769)
    -   レプリケーション効率を向上させるために、コミットbinlogのトランザクションステータス情報のクエリをサポートする[＃757](https://github.com/pingcap/tidb-binlog/pull/757)
    -   [＃758](https://github.com/pingcap/tidb-binlog/pull/758)の`start_ts`がPumpの最大の35より大きい場合にPumpパニックが発生する可能性がある問題を修正し`commit_ts`
-   TiDB Lightning
    -   ローダーの完全なロジックインポート機能を統合し、バックエンドモードの構成をサポートします[＃221](https://github.com/pingcap/tidb-lightning/pull/221)

## TiDB Ansible {#tidb-ansible}

-   インデックス速度の追加の監視メトリックを追加する[＃986](https://github.com/pingcap/tidb-ansible/pull/986)
-   構成ファイルの内容を簡素化し、ユーザーが構成する必要のないパラメーターを削除し[＃998](https://github.com/pingcap/tidb-ansible/pull/998) [＃1043c](https://github.com/pingcap/tidb-ansible/commit/1043c3df7ddb72eb234c55858960e9fdd3830a14)
-   パフォーマンス読み取りおよびパフォーマンス書き込みの監視式エラーを修正[＃e90e7](https://github.com/pingcap/tidb-ansible/commit/e90e79f5117bb89197e01b1391fd02e25d57a440)
-   RaftstoreCPU使用率の監視表示方法とアラームルールを更新します[＃992](https://github.com/pingcap/tidb-ansible/pull/992)
-   概要監視ダッシュボードのTiKVCPU監視項目を更新して、過剰な監視コンテンツを除外します[＃1001](https://github.com/pingcap/tidb-ansible/pull/1001)
