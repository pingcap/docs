---
title: TiDB 3.0.5 Release Notes
---

# TiDB 3.0.5 リリースノート {#tidb-3-0-5-release-notes}

発売日：2019年10月25日

TiDB バージョン: 3.0.5

TiDB Ansible バージョン: 3.0.5

## TiDB {#tidb}

-   SQLオプティマイザー
    -   Window Functions [#12404](https://github.com/pingcap/tidb/pull/12404)での境界チェックのサポート
    -   パーティション テーブルの`IndexJoin`が間違った結果を返す問題を修正します[#12712](https://github.com/pingcap/tidb/pull/12712)
    -   外部結合`Apply`演算子の先頭にある`ifnull`関数が誤った結果を返す問題を修正します[#12694](https://github.com/pingcap/tidb/pull/12694)
    -   `UPDATE` [#12597](https://github.com/pingcap/tidb/pull/12597)の`where`条件にサブクエリが含まれる場合に更新に失敗する問題を修正
    -   クエリ条件[#12790](https://github.com/pingcap/tidb/pull/12790)に関数`cast`が含まれている場合、外部結合が誤って内部結合に変換されてしまう問題を修正
    -   `AntiSemiJoin` [#12799](https://github.com/pingcap/tidb/pull/12799)の結合条件に渡される誤った式を修正しました。
    -   統計[#12817](https://github.com/pingcap/tidb/pull/12817)の初期化時にシャロー コピーによって引き起こされる統計エラーを修正しました。
    -   日付文字列と形式文字列が一致しない場合、TiDB の関数`str_to_date` MySQL とは異なる結果を返す問題を修正します[#12725](https://github.com/pingcap/tidb/pull/12725)
-   SQL実行エンジン
    -   `from_unixtime`関数が null [#12551](https://github.com/pingcap/tidb/pull/12551)を処理するときのpanicの問題を修正
    -   DDL ジョブ[#12671](https://github.com/pingcap/tidb/pull/12671)をキャンセルするときに報告される`invalid list index`エラーを修正します。
    -   ウィンドウ関数使用時に配列が範囲外になる問題を修正[#12660](https://github.com/pingcap/tidb/pull/12660)
    -   MySQL 自動インクリメント ロック ( [「連続」ロックモード](https://dev.mysql.com/doc/refman/5.7/en/innodb-auto-increment-handling.html) ) のデフォルト モードとの一貫性を維持するために、暗黙的に割り当てられたときの`AutoIncrement`カラムの動作を改善します。単一行`Insert`ステートメントでの複数の`AutoIncrement` ID の暗黙的割り当てについて、TiDB は割り当てられた値の連続性。この改善により、JDBC `getGeneratedKeys()`メソッドがどのようなシナリオでも正しい結果を取得できるようになります。 [#12602](https://github.com/pingcap/tidb/pull/12602)
    -   `HashAgg` `Apply` [#12766](https://github.com/pingcap/tidb/pull/12766)の子ノードとして機能する場合にクエリがハングする問題を修正
    -   型変換[#12811](https://github.com/pingcap/tidb/pull/12811)に関して、 `AND`と`OR`の論理式が誤った結果を返す問題を修正
-   サーバ
    -   後で大規模なトランザクションをサポートできるように、トランザクション TTL を変更するインターフェイス関数を実装します[#12397](https://github.com/pingcap/tidb/pull/12397)
    -   悲観的トランザクションをサポートするために、必要に応じてトランザクション TTL を延長 (最大 10 分) するサポート[#12579](https://github.com/pingcap/tidb/pull/12579)
    -   TiDB がスキーマ変更および対応する変更されたテーブル情報をキャッシュする回数を 100 から 1024 まで調整し、 `tidb_max_delta_schema_count`システム変数[#12502](https://github.com/pingcap/tidb/pull/12502)を使用した変更をサポートします。
    -   `kvrpc.Cleanup`プロトコルの動作を更新して、超過していないトランザクションのロックをクリーンアップしなくなりました[#12417](https://github.com/pingcap/tidb/pull/12417)
    -   パーティション テーブル情報の`information_schema.tables`テーブル[#12631](https://github.com/pingcap/tidb/pull/12631)へのログ記録をサポートします。
    -   `region-cache-ttl` [#12683](https://github.com/pingcap/tidb/pull/12683)の構成によるリージョンキャッシュの TTL 変更のサポート
    -   実行プランの圧縮エンコードされた情報を低速ログに出力できるようになりました。この機能はデフォルトで有効になっており、 `slow-log-plan`構成または`tidb_record_plan_in_slow_log`変数を使用して制御できます。さらに、 `tidb_decode_plan`機能は、スロー ログ内の実行計画列エンコード情報を実行計画情報にデコードできます。 [#12808](https://github.com/pingcap/tidb/pull/12808)
    -   `information_schema.processlist`表[#12801](https://github.com/pingcap/tidb/pull/12801)でのメモリ使用量情報の表示をサポート
    -   TiKVクライアントがアイドル接続と判断した場合にエラーや予期せぬアラームが発生する場合がある問題を修正[#12846](https://github.com/pingcap/tidb/pull/12846)
    -   `tikvSnapshot`が`BatchGet()` [#12872](https://github.com/pingcap/tidb/pull/12872)の KV 結果を適切にキャッシュしないため、 `INSERT IGNORE`ステートメントのパフォーマンスが低下する問題を修正します。
    -   一部の KV サービスへの接続が遅いため、TiDB の応答速度が比較的遅くなる問題を修正[#12814](https://github.com/pingcap/tidb/pull/12814)
-   DDL
    -   `Create Table`操作でSet列[#12267](https://github.com/pingcap/tidb/pull/12267)のInt型のデフォルト値が正しく設定されない問題を修正
    -   `Create Table`ステートメントで一意のインデックスを作成するときに複数の`unique`をサポートします[#12463](https://github.com/pingcap/tidb/pull/12463)
    -   `Alter Table` [#12489](https://github.com/pingcap/tidb/pull/12489)使用してビット型列を追加するときに、既存の行にこの列のデフォルト値を設定するとエラーが発生する可能性がある問題を修正します。
    -   レンジパーティションテーブルがパーティション キーとして日付型または日時型の列を使用している場合にパーティションを追加できない問題を修正します[#12815](https://github.com/pingcap/tidb/pull/12815)
    -   Date 型または Datetime 型の列をパーティション キーとして持つレンジ パーティションパーティションテーブルに対して、テーブルの作成時またはパーティションの追加時に、パーティション タイプとパーティション キー タイプの整合性チェックをサポートします[#12792](https://github.com/pingcap/tidb/pull/12792)
    -   範囲パーティションテーブル[#12718](https://github.com/pingcap/tidb/pull/12718)を作成するときに、一意のキー列セットがパーティション列セット以上である必要があることを確認するチェックを追加します。
-   モニター
    -   コミットおよびロールバック操作の監視メトリックをダッシュ​​ボードに追加します`Transaction OPS`ダッシュボード[#12505](https://github.com/pingcap/tidb/pull/12505)
    -   `Add Index`操作の進行状況[#12390](https://github.com/pingcap/tidb/pull/12390)の監視メトリクスを追加します。

## TiKV {#tikv}

-   ストレージ
    -   悲観的トランザクションの新機能を追加します。トランザクション クリーンアップ インターフェイスは、TTL が古いロックのクリーンアップのみをサポートします[#5589](https://github.com/tikv/tikv/pull/5589)
    -   トランザクションの主キーのロールバックが折りたたまれている問題を修正[#5646](https://github.com/tikv/tikv/pull/5646) 、 [#5671](https://github.com/tikv/tikv/pull/5671)
    -   悲観的ロックの下で、ポイント クエリが以前のバージョンのデータを返す可能性がある問題を修正します[#5634](https://github.com/tikv/tikv/pull/5634)
-   Raftstore
    -   Raftstoreでのメッセージ フラッシュ操作を減らしてパフォーマンスを向上させ、CPU 使用率を削減します[#5617](https://github.com/tikv/tikv/pull/5617)
    -   リージョンサイズとキーの推定数を取得するコストを最適化し、ハートビートオーバーヘッドと CPU 使用率を削減します[#5620](https://github.com/tikv/tikv/pull/5620)
    -   Raftstore がエラー ログを出力、無効なデータを取得したときにpanicが発生する問題を修正します[#5643](https://github.com/tikv/tikv/pull/5643)
-   エンジン
    -   RocksDB `force_consistency_checks`有効にしてデータの安全性を向上させる[#5662](https://github.com/tikv/tikv/pull/5662)
    -   Titan での同時フラッシュ操作によりデータ損失が発生する可能性がある問題を修正します[#5672](https://github.com/tikv/tikv/pull/5672)
    -   L0 内圧縮による TiKV のクラッシュと再起動の問題を回避するには、rust-rocksdb バージョンを更新します[#5710](https://github.com/tikv/tikv/pull/5710)

## PD {#pd}

-   リージョン[#1782](https://github.com/pingcap/pd/pull/1782)が占有するstorageの精度を向上します。
-   `--help`コマンド[#1763](https://github.com/pingcap/pd/pull/1763)の出力を改善します。
-   TLS が有効になった後に HTTP リクエストがリダイレクトに失敗する問題を修正します[#1777](https://github.com/pingcap/pd/pull/1777)
-   pd-ctl が`store shows limit`コマンド[#1808](https://github.com/pingcap/pd/pull/1808)を使用するときに発生するpanicの問題を修正しました。
-   ラベル監視メトリクスの可読性を向上させ、リーダーが切り替わったときに元のリーダーの監視データをリセットして、誤ったレポートを回避します[#1815](https://github.com/pingcap/pd/pull/1815)

## ツール {#tools}

-   TiDBBinlog
    -   `ALTER DATABASE`関連する DDL 操作によりDrainerが異常終了する問題を修正します[#769](https://github.com/pingcap/tidb-binlog/pull/769)
    -   レプリケーション効率を向上させるために、コミットbinlogのトランザクション ステータス情報のクエリをサポートします[#757](https://github.com/pingcap/tidb-binlog/pull/757)
    -   ドレイナーの`start_ts`ポンプの最大値`commit_ts` [#758](https://github.com/pingcap/tidb-binlog/pull/758)より大きい場合にPumppanicが発生することがある問題を修正
-   TiDB Lightning
    -   ローダーの完全なロジック インポート機能を統合し、バックエンド モード[#221](https://github.com/pingcap/tidb-lightning/pull/221)の構成をサポートします。

## TiDB Ansible {#tidb-ansible}

-   インデックス速度[#986](https://github.com/pingcap/tidb-ansible/pull/986)を追加する監視メトリクスを追加します。
-   構成ファイルの内容を簡素化し、ユーザーが構成する必要のないパラメーターを削除します[#1043c](https://github.com/pingcap/tidb-ansible/commit/1043c3df7ddb72eb234c55858960e9fdd3830a14) 、 [#998](https://github.com/pingcap/tidb-ansible/pull/998)
-   パフォーマンスリード、パフォーマンスライト[#e90e7](https://github.com/pingcap/tidb-ansible/commit/e90e79f5117bb89197e01b1391fd02e25d57a440)の監視式エラーを修正
-   Raftstore CPU使用率[#992](https://github.com/pingcap/tidb-ansible/pull/992)の監視表示方法とアラームルールを更新
-   概要監視ダッシュボードの TiKV CPU 監視項目を更新して、過剰な監視コンテンツを除外します[#1001](https://github.com/pingcap/tidb-ansible/pull/1001)
