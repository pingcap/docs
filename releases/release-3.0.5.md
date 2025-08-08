---
title: TiDB 3.0.5 Release Notes
summary: TiDB 3.0.5は、2019年10月25日にリリースされ、様々な改善とバグ修正が行われました。このリリースには、SQLオプティマイザー、SQL実行エンジン、サーバー、DDL、モニター、TiKV、PD、TiDB Binlog、 TiDB Lightning、TiDB Ansibleの機能強化が含まれています。改善点には、ウィンドウ関数の境界チェックのサポート、インデックス結合と外部結合の問題の修正、各種操作の監視メトリクスの追加などがあります。さらに、TiKVではstorageとパフォーマンスの最適化が行われ、PDではstorage精度とHTTPリクエスト処理が改善されました。TiDB Ansibleでは、監視メトリクスのアップデートと設定ファイルの簡素化も行われました。
---

# TiDB 3.0.5 リリースノート {#tidb-3-0-5-release-notes}

発売日：2019年10月25日

TiDB バージョン: 3.0.5

TiDB Ansible バージョン: 3.0.5

## TiDB {#tidb}

-   SQLオプティマイザー
    -   ウィンドウ関数[＃12404](https://github.com/pingcap/tidb/pull/12404)の境界チェックをサポート
    -   パーティションテーブル`IndexJoin`が誤った結果を返す問題を修正[＃12712](https://github.com/pingcap/tidb/pull/12712)
    -   外部結合演算子`Apply`の先頭の`ifnull`関数が誤った結果を返す問題を修正[＃12694](https://github.com/pingcap/tidb/pull/12694)
    -   `UPDATE` [＃12597](https://github.com/pingcap/tidb/pull/12597)の`where`条件にサブクエリが含まれていた場合の更新失敗の問題を修正しました
    -   クエリ条件に`cast`関数が含まれている場合に外部結合が誤って内部結合に変換される問題を修正しました[＃12790](https://github.com/pingcap/tidb/pull/12790)
    -   `AntiSemiJoin` [＃12799](https://github.com/pingcap/tidb/pull/12799)の結合条件で渡される誤った式を修正
    -   統計[＃12817](https://github.com/pingcap/tidb/pull/12817)初期化時に浅いコピーによって発生する統計エラーを修正しました
    -   日付文字列とフォーマット文字列が一致しない場合に、TiDBの`str_to_date`関数がMySQLとは異なる結果を返す問題を修正しました[＃12725](https://github.com/pingcap/tidb/pull/12725)
-   SQL実行エンジン
    -   `from_unixtime`関数が null [＃12551](https://github.com/pingcap/tidb/pull/12551)を処理するときに発生panic問題を修正
    -   DDLジョブ[＃12671](https://github.com/pingcap/tidb/pull/12671)をキャンセルする際に報告される`invalid list index`エラーを修正
    -   ウィンドウ関数の使用時に配列が範囲外になる問題を修正[＃12660](https://github.com/pingcap/tidb/pull/12660)
    -   `AutoIncrement`列が暗黙的に割り当てられた場合の動作を改善し、MySQLの自動インクリメントロックのデフォルトモード（ [「連続」ロックモード](https://dev.mysql.com/doc/refman/5.7/en/innodb-auto-increment-handling.html) ）との一貫性を保ちます。1行の`Insert`文で複数の`AutoIncrement` IDを暗黙的に割り当てる場合、TiDBは割り当てられた値の連続性を保証します。この改善により、JDBC `getGeneratedKeys()`メソッドはどのようなシナリオでも正しい結果を得ることができます[＃12602](https://github.com/pingcap/tidb/pull/12602)
    -   `HashAgg` `Apply` [＃12766](https://github.com/pingcap/tidb/pull/12766)の子ノードとして機能するときにクエリがハングする問題を修正しました
    -   型変換[＃12811](https://github.com/pingcap/tidb/pull/12811)に関して、 `AND`と`OR`論理式が誤った結果を返す問題を修正しました。
-   サーバ
    -   後で大規模なトランザクションをサポートするためにトランザクションTTLを変更するインターフェース関数を実装します[＃12397](https://github.com/pingcap/tidb/pull/12397)
    -   悲観的トランザクションをサポートするために、必要に応じてトランザクション TTL を延長する（最大 10 分）ことをサポートします[＃12579](https://github.com/pingcap/tidb/pull/12579)
    -   TiDBがスキーマの変更とそれに対応する変更されたテーブル情報をキャッシュする回数を100から1024に調整し、 `tidb_max_delta_schema_count`システム変数[＃12502](https://github.com/pingcap/tidb/pull/12502)を使用して変更をサポートします。
    -   `kvrpc.Cleanup`プロトコルの動作を更新して、時間外ではないトランザクションのロックをクリーンアップしないようにしました[＃12417](https://github.com/pingcap/tidb/pull/12417)
    -   パーティションテーブル情報を`information_schema.tables`テーブル[＃12631](https://github.com/pingcap/tidb/pull/12631)に記録するサポート
    -   `region-cache-ttl` [＃12683](https://github.com/pingcap/tidb/pull/12683)を設定することでリージョンキャッシュの TTL の変更をサポートします
    -   スローログ内の実行プランの圧縮エンコード情報の出力をサポートします。この機能はデフォルトで有効になっており、 `slow-log-plan`設定または`tidb_record_plan_in_slow_log`変数を使用して制御できます。さらに、 `tidb_decode_plan`関数は、スローログ内の実行プラン列エンコード情報を実行プラン情報にデコードします[＃12808](https://github.com/pingcap/tidb/pull/12808)
    -   `information_schema.processlist`表[＃12801](https://github.com/pingcap/tidb/pull/12801)にメモリ使用量情報を表示することをサポート
    -   TiKVクライアントがアイドル接続[＃12846](https://github.com/pingcap/tidb/pull/12846)と判断したときにエラーと予期しないアラームが発生する可能性がある問題を修正しました
    -   `tikvSnapshot` `BatchGet()` [＃12872](https://github.com/pingcap/tidb/pull/12872)の KV 結果を適切にキャッシュしないため、 `INSERT IGNORE`ステートメントのパフォーマンスが低下する問題を修正しました。
    -   一部のKVサービスへの接続が遅いため、TiDBの応答速度が比較的遅くなる問題を修正しました[＃12814](https://github.com/pingcap/tidb/pull/12814)
-   DDL
    -   `Create Table`操作で Set 列[＃12267](https://github.com/pingcap/tidb/pull/12267) Int 型のデフォルト値が正しく設定されない問題を修正しました。
    -   `Create Table`文[＃12463](https://github.com/pingcap/tidb/pull/12463)で一意のインデックスを作成するときに複数の`unique`をサポートする
    -   `Alter Table` [＃12489](https://github.com/pingcap/tidb/pull/12489)を使用してビット型の列を追加するときに、既存の行にこの列のデフォルト値を設定するとエラーが発生する可能性がある問題を修正しました。
    -   範囲パーティションテーブルで日付または日時型の列をパーティションキーとして使用している場合にパーティションを追加できない問題を修正[＃12815](https://github.com/pingcap/tidb/pull/12815)
    -   日付または日時型の列をパーティション キーとして持つ範囲パーティションテーブルの場合、テーブルの作成時またはパーティションの追加時に、パーティション タイプとパーティション キー タイプの一貫性をチェックする機能をサポート[＃12792](https://github.com/pingcap/tidb/pull/12792)
    -   範囲パーティションテーブルを作成するときに、一意キーの列セットがパーティション化された列セット以上である必要があるというチェックを追加します[＃12718](https://github.com/pingcap/tidb/pull/12718)
-   モニター
    -   コミットおよびロールバック操作の監視メトリックを`Transaction OPS`ダッシュボード[＃12505](https://github.com/pingcap/tidb/pull/12505)に追加します。
    -   `Add Index`操作の進行状況[＃12390](https://github.com/pingcap/tidb/pull/12390)の監視メトリックを追加します

## TiKV {#tikv}

-   ストレージ
    -   悲観的トランザクションの新機能を追加: トランザクションクリーンアップインターフェースは、TTLが期限切れのロックのクリーンアップのみをサポートします[＃5589](https://github.com/tikv/tikv/pull/5589)
    -   トランザクションのロールバックでプライマリキーが折りたたまれる問題を修正[＃5646](https://github.com/tikv/tikv/pull/5646) , [＃5671](https://github.com/tikv/tikv/pull/5671)
    -   悲観的ロック下でポイントクエリが以前のバージョンのデータを返す可能性がある問題を修正[＃5634](https://github.com/tikv/tikv/pull/5634)
-   Raftstore
    -   Raftstoreのメッセージフラッシュ操作を減らしてパフォーマンスを向上させ、CPU 使用率を削減します[＃5617](https://github.com/tikv/tikv/pull/5617)
    -   リージョンサイズとキーの推定数を取得するコストを最適化し、ハートビートのオーバーヘッドとCPU使用率を削減します[＃5620](https://github.com/tikv/tikv/pull/5620)
    -   無効なデータを取得するとRaftstoreがエラーログを出力panicが発生する問題を修正しました[＃5643](https://github.com/tikv/tikv/pull/5643)
-   エンジン
    -   RocksDB `force_consistency_checks`を有効にしてデータの安全性を向上[＃5662](https://github.com/tikv/tikv/pull/5662)
    -   Titan での同時フラッシュ操作によりデータ損失が発生する可能性がある問題を修正[＃5672](https://github.com/tikv/tikv/pull/5672)
    -   L0内圧縮によるTiKVのクラッシュと再起動の問題を回避するためにrust-rocksdbのバージョンを更新しました[＃5710](https://github.com/tikv/tikv/pull/5710)

## PD {#pd}

-   リージョン[＃1782](https://github.com/pingcap/pd/pull/1782)が占有するstorageの精度を向上
-   `--help`コマンド[＃1763](https://github.com/pingcap/pd/pull/1763)の出力を改善する
-   TLS を有効にした後に HTTP リクエストがリダイレクトに失敗する問題を修正[＃1777](https://github.com/pingcap/pd/pull/1777)
-   pd-ctlが`store shows limit`コマンド[＃1808](https://github.com/pingcap/pd/pull/1808)使用する際に発生するpanic問題を修正
-   ラベル監視メトリクスの可読性を向上させ、リーダーが切り替わるときに元のリーダーの監視データをリセットして、誤ったレポートを回避する[＃1815](https://github.com/pingcap/pd/pull/1815)

## ツール {#tools}

-   Tidb Binlog
    -   `ALTER DATABASE`関連する DDL 操作によりDrainerが異常終了する問題を修正[＃769](https://github.com/pingcap/tidb-binlog/pull/769)
    -   レプリケーション効率を向上させるためにコミットbinlog のトランザクション ステータス情報のクエリをサポートする[＃757](https://github.com/pingcap/tidb-binlog/pull/757)
    -   ドレイナーの`start_ts`ポンプの最大値`commit_ts` [＃758](https://github.com/pingcap/tidb-binlog/pull/758)より大きい場合にPumppanicが発生する可能性がある問題を修正しました。
-   TiDB Lightning
    -   Loaderの完全なロジックインポート機能を統合し、バックエンドモード[＃221](https://github.com/pingcap/tidb-lightning/pull/221)構成をサポートします。

## TiDB アンシブル {#tidb-ansible}

-   インデックス速度[＃986](https://github.com/pingcap/tidb-ansible/pull/986)追加の監視メトリックを追加します
-   設定ファイルの内容を簡素化し、ユーザーが設定する必要のないパラメータを削除します[#1043c](https://github.com/pingcap/tidb-ansible/commit/1043c3df7ddb72eb234c55858960e9fdd3830a14) 、 [＃998](https://github.com/pingcap/tidb-ansible/pull/998)
-   パフォーマンス読み取りとパフォーマンス書き込み[#e90e7](https://github.com/pingcap/tidb-ansible/commit/e90e79f5117bb89197e01b1391fd02e25d57a440)の監視式エラーを修正
-   Raftstore CPU使用率[＃992](https://github.com/pingcap/tidb-ansible/pull/992)の監視表示方法とアラームルールを更新
-   概要監視ダッシュボードの TiKV CPU 監視項目を更新して、余分な監視コンテンツをフィルタリングします[＃1001](https://github.com/pingcap/tidb-ansible/pull/1001)
