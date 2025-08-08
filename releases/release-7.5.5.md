---
title: TiDB 7.5.5 Release Notes
summary: TiDB 7.5.5 における互換性の変更、改善、およびバグ修正について説明します。
---

# TiDB 7.5.5 リリースノート {#tidb-7-5-5-release-notes}

発売日：2024年12月31日

TiDB バージョン: 7.5.5

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v7.5/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v7.5/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   インデックス[＃57156](https://github.com/pingcap/tidb/issues/57156) @ [CbcWestwolf](https://github.com/CbcWestwolf)を追加する際の取り込みフェーズの最大速度を制限する新しいシステム変数[`tidb_ddl_reorg_max_write_speed`](https://docs.pingcap.com/tidb/v7.5/system-variables#tidb_ddl_reorg_max_write_speed-new-in-v6512-and-v755)を追加します。
-   TiKV構成項目[`raft-client-queue-size`](/tikv-configuration-file.md#raft-client-queue-size)のデフォルト値を`8192`から`16384` [＃17101](https://github.com/tikv/tikv/issues/17101) @ [コナー1996](https://github.com/Connor1996)に変更します

## 改善点 {#improvements}

-   TiDB

    -   統計情報がすべて TopN で構成され、対応するテーブル統計の変更された行数が 0 以外である場合に、TopN にヒットしない等価条件の推定結果を 0 から 1 に調整します[＃47400](https://github.com/pingcap/tidb/issues/47400) @ [テリー・パーセル](https://github.com/terry1purcell)

-   TiKV

    -   Raftと RocksDB が異なるディスクにデプロイされている場合、RocksDB が配置されているディスクでは低速ディスク検出が機能しない問題を修正[＃17884](https://github.com/tikv/tikv/issues/17884) @ [LykxSassinator](https://github.com/LykxSassinator)
    -   ピアのスローログを追加し、メッセージ[＃16600](https://github.com/tikv/tikv/issues/16600) @ [コナー1996](https://github.com/Connor1996)を保存します
    -   ログの適用を待つために TiKV を再起動するときに発生する不安定なアクセス遅延を最適化し、TiKV [＃15874](https://github.com/tikv/tikv/issues/15874) @ [LykxSassinator](https://github.com/LykxSassinator)の安定性を向上しました。

-   TiFlash

    -   TLS を有効にした後に証明書を更新することでTiFlash がpanic可能性がある問題を軽減します[＃8535](https://github.com/pingcap/tiflash/issues/8535) @ [ウィンドトーカー](https://github.com/windtalker)
    -   クラスター化インデックス[＃9529](https://github.com/pingcap/tiflash/issues/9529) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)を持つテーブルのバックグラウンドでの古いデータのガベージコレクション速度を改善
    -   分散storageおよびコンピューティングアーキテクチャ内のTiFlashコンピューティングノードの再試行戦略を最適化して、Amazon S3 [＃9695](https://github.com/pingcap/tiflash/issues/9695) @ [ジンヘリン](https://github.com/JinheLin)からファイルをダウンロードする際の例外を処理します。

-   ツール

    -   バックアップと復元 (BR)

        -   バックアップ中の不要なログ出力を削減[＃55902](https://github.com/pingcap/tidb/issues/55902) @ [リーヴルス](https://github.com/Leavrth)

    -   TiDB データ移行 (DM)

        -   認識されないMariaDBbinlogイベントのログレベルを下げる[＃10204](https://github.com/pingcap/tiflow/issues/10204) @ [ドヴェーデン](https://github.com/dveeden)

## バグ修正 {#bug-fixes}

-   TiDB

    -   DDL所有者ノードが[＃56506](https://github.com/pingcap/tidb/issues/56506) @ [接線](https://github.com/tangenta)に切り替えられた後、TiDBが以前の進行状況から再編成DDLタスクを再開できない問題を修正しました
    -   非厳密モードで無効な値`NULL`が挿入される問題を修正 ( `sql_mode = ''` ) [＃56381](https://github.com/pingcap/tidb/issues/56381) @ [ヨッヘンrh](https://github.com/joechenrh)
    -   Grafanaの**Stats Healthy Distribution**パネルのデータが正しくない可能性がある問題を修正しました[＃57176](https://github.com/pingcap/tidb/issues/57176) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   共通テーブル式 (CTE) に複数のデータ コンシューマーがあり、1 つのコンシューマーがデータを読み取らずに終了した場合に発生する可能性のある不正なメモリアクセスの問題を修正しました[＃55881](https://github.com/pingcap/tidb/issues/55881) @ [ウィンドトーカー](https://github.com/windtalker)
    -   v6.5からv7.5以降にアップグレードされたクラスターで、既存のTTLタスクが予期せず頻繁に実行される問題を修正[＃56539](https://github.com/pingcap/tidb/issues/56539) @ [lcwangchao](https://github.com/lcwangchao)
    -   `tidb_ttl_job_enable`変数が無効になった後、TTL タスクがキャンセルされない問題を修正[＃57404](https://github.com/pingcap/tidb/issues/57404) @ [ヤンケオ](https://github.com/YangKeao)
    -   情報スキーマキャッシュミス[＃53428](https://github.com/pingcap/tidb/issues/53428) @ [crazycs520](https://github.com/crazycs520)により、古い読み取りのクエリレイテンシーが増加する問題を修正しました。
    -   stale read が読み取り操作のタイムスタンプを厳密に検証しない問題を修正しました。その結果、TSO と実際の物理時間[＃56809](https://github.com/pingcap/tidb/issues/56809) @ [ミョンケミンタ](https://github.com/MyonKeminta)間にオフセットが存在する場合にトランザクションの一貫性に影響を及ぼす可能性がわずかにあります。
    -   `IMPORT INTO`ステートメント[＃56476](https://github.com/pingcap/tidb/issues/56476) @ [D3ハンター](https://github.com/D3Hunter)を使用してデータをインポートした後、 `AUTO_INCREMENT`フィールドが正しく設定されない問題を修正しました。
    -   2人のDDL所有者が同時に存在する可能性がある問題を修正[＃54689](https://github.com/pingcap/tidb/issues/54689) @ [ジョッカウ](https://github.com/joccau)
    -   storageエンジン[＃56402](https://github.com/pingcap/tidb/issues/56402) @ [ヤンケオ](https://github.com/YangKeao)としてTiKVが選択されていない場合にTTLが失敗する可能性がある問題を修正しました
    -   `ADD INDEX` [＃56930](https://github.com/pingcap/tidb/issues/56930) @ [fzzf678](https://github.com/fzzf678)実行時に TiDB がインデックスの長さ制限をチェックしない問題を修正しました
    -   TTLタスクをキャンセルした際に、対応するSQLが強制終了されない問題を修正[＃56511](https://github.com/pingcap/tidb/issues/56511) @ [lcwangchao](https://github.com/lcwangchao)
    -   エイリアス[＃56726](https://github.com/pingcap/tidb/issues/56726) @ [ホーキングレイ](https://github.com/hawkingrei)を持つマルチテーブル`DELETE`ステートメントに対して実行プラン バインディングを作成できない問題を修正しました。
    -   `ANALYZE`使用してテーブルの統計情報を収集する場合、テーブルに仮想生成列の式インデックスが含まれていると、実行時にエラー[＃57079](https://github.com/pingcap/tidb/issues/57079) @ [ホーキングレイ](https://github.com/hawkingrei)が報告される問題を修正しました。
    -   配置ルール[＃54961](https://github.com/pingcap/tidb/issues/54961) @ [ホーキングレイ](https://github.com/hawkingrei)を含むテーブル構造をインポートするときに Plan Replayer がエラーを報告する可能性がある問題を修正しました。
    -   CTE でデータベース名を解析するときに間違ったデータベース名[＃54582](https://github.com/pingcap/tidb/issues/54582) @ [ホーキングレイ](https://github.com/hawkingrei)が返される問題を修正しました
    -   `INSERT ... ON DUPLICATE KEY`文が`mysql_insert_id` [＃55965](https://github.com/pingcap/tidb/issues/55965) @ [天菜まお](https://github.com/tiancaiamao)と互換性がない問題を修正
    -   特定の状況下でプランキャッシュを使用する際に、メタデータロックの不適切な使用によって異常なデータが書き込まれる可能性がある問題を修正[＃53634](https://github.com/pingcap/tidb/issues/53634) @ [ジムララ](https://github.com/zimulala)
    -   グローバルソート[＃54147](https://github.com/pingcap/tidb/issues/54147) @ [接線](https://github.com/tangenta)を使用してインデックスを追加するとパフォーマンスが不安定になる問題を修正しました
    -   外部キー[＃56456](https://github.com/pingcap/tidb/issues/56456) @ [ホーキングレイ](https://github.com/hawkingrei)を含むテーブル構造をインポートするときに Plan Replayer がエラーを報告する可能性がある問題を修正しました。
    -   `RANGE COLUMNS`パーティション関数と`utf8mb4_0900_ai_ci`照合順序を同時に使用すると、クエリ結果[＃57261](https://github.com/pingcap/tidb/issues/57261) @ [定義2014](https://github.com/Defined2014)が正しくなくなる可能性がある問題を修正しました。
    -   `NATURAL JOIN`または`USING`節の後にサブクエリを使用するとエラー[＃53766](https://github.com/pingcap/tidb/issues/53766) @ [ダッシュ12653](https://github.com/dash12653)が発生する可能性がある問題を修正しました
    -   書き込み競合が発生したときにTTLタスクをキャンセルできない問題を修正[＃56422](https://github.com/pingcap/tidb/issues/56422) @ [ヤンケオ](https://github.com/YangKeao)
    -   CTE に`ORDER BY` 、 `LIMIT` 、または`SELECT DISTINCT`節が含まれており、別の CTE の再帰部分によって参照されている場合、誤ってインライン化され、実行エラー[＃56603](https://github.com/pingcap/tidb/issues/56603) @ [エルサ0520](https://github.com/elsa0520)が発生する可能性がある問題を修正しました。
    -   `UPDATE`文が`ENUM`型[＃56832](https://github.com/pingcap/tidb/issues/56832) @ [xhebox](https://github.com/xhebox)の値を誤って更新する問題を修正しました
    -   `RECOVER TABLE BY JOB JOB_ID;`実行すると TiDB がpanicを起こす可能性がある問題を修正[＃55113](https://github.com/pingcap/tidb/issues/55113) @ [crazycs520](https://github.com/crazycs520)
    -   クエリに利用可能なインデックスマージ実行プラン[＃56217](https://github.com/pingcap/tidb/issues/56217) @ [アイリンキッド](https://github.com/AilinKid)がある場合にヒント`read_from_storage`が有効にならない可能性がある問題を修正しました。
    -   異常終了時に`INDEX_HASH_JOIN`アップする可能性がある問題を修正[＃54055](https://github.com/pingcap/tidb/issues/54055) @ [wshwsh12](https://github.com/wshwsh12)
    -   分散実行フレームワーク (DXF) に関連するシステム テーブルをクエリすると、アップグレードが失敗する可能性がある問題を修正しました[＃49263](https://github.com/pingcap/tidb/issues/49263) @ [D3ハンター](https://github.com/D3Hunter)
    -   DDL内部トランザクションエラー`GC life time is shorter than transaction duration`によりインデックス追加が失敗する問題を修正[＃57043](https://github.com/pingcap/tidb/issues/57043) @ [接線](https://github.com/tangenta)
    -   `EXCHANGE PARTITION`実行して無効な行に遭遇すると、InfoSchema が完全にロードされ、エラー`failed to load schema diff`が[＃56685](https://github.com/pingcap/tidb/issues/56685) @ [D3ハンター](https://github.com/D3Hunter)で報告される問題を修正しました。
    -   `tidb_ddl_enable_fast_reorg`と`new_collations_enabled_on_first_bootstrap`有効になっているときに照合順序が正しく処理されず、データ インデックス[＃58036](https://github.com/pingcap/tidb/issues/58036) @ [djshow832](https://github.com/djshow832)が不一致になる問題を修正しました。
    -   プランキャッシュがインデックス[＃56733](https://github.com/pingcap/tidb/issues/56733) @ [wjhuang2016](https://github.com/wjhuang2016)を追加するときに間違ったスキーマを使用するため、データインデックスが不整合になる問題を修正しました。
    -   アップグレード中に`ALTER TABLE TIFLASH REPLICA`実行するとTiDBノードがクラッシュする問題を修正[＃57863](https://github.com/pingcap/tidb/issues/57863) @ [接線](https://github.com/tangenta)
    -   クエリ`INFORMATION_SCHEMA.columns`のパフォーマンスが[ランス6716](https://github.com/lance6716)で[＃58184](https://github.com/pingcap/tidb/issues/58184)低下する問題を修正
    -   TiFlashシステムテーブルを照会する際のデフォルトのタイムアウトが短すぎる問題を修正[＃57816](https://github.com/pingcap/tidb/issues/57816) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)
    -   `default_collation_for_utf8mb4`変数の値が`SET NAMES`ステートメント[＃56439](https://github.com/pingcap/tidb/issues/56439) @ [定義2014](https://github.com/Defined2014)で機能しない問題を修正しました
    -   `mysql.tidb_timer`テーブル[＃57112](https://github.com/pingcap/tidb/issues/57112) @ [lcwangchao](https://github.com/lcwangchao)でタイマーを手動で削除すると、TTL 内部コルーチンがpanicになる可能性がある問題を修正しました。
    -   `ALTER TABLE`文を使用して通常のテーブルをパーティションテーブルに変換するときに、不十分なチェックにより誤ったデータ[＃55721](https://github.com/pingcap/tidb/issues/55721) @ [ミョンス](https://github.com/mjonss)が生成される可能性がある問題を修正しました。
    -   `tidb_gogc_tuner_max_value`と`tidb_gogc_tuner_min_value`設定するときに最大値がnullの場合に誤った警告メッセージが表示される問題を修正しました[＃57889](https://github.com/pingcap/tidb/issues/57889) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   TiDBの内部コルーチン[＃57798](https://github.com/pingcap/tidb/issues/57798) [＃56053](https://github.com/pingcap/tidb/issues/56053) @ [魚類](https://github.com/fishiu) @ [天菜まお](https://github.com/tiancaiamao)で発生する可能性のあるデータ競合問題を修正しました
    -   潜在的なセキュリティリスクを防ぐためのアップデート`golang-jwt`と`jwt` [＃57135](https://github.com/pingcap/tidb/issues/57135) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   `ALTER TABLE`文[＃57510](https://github.com/pingcap/tidb/issues/57510) @ [ミョンス](https://github.com/mjonss)を使用して、クラスタ化インデックスを持つテーブルをパーティションテーブルに変換するときに、同時書き込みによってデータが重複する可能性がある問題を修正しました。

-   TiKV

    -   領域をマージすると稀に TiKV がpanic可能性がある問題を修正[＃17840](https://github.com/tikv/tikv/issues/17840) @ [栄光](https://github.com/glorv)
    -   Raftと RocksDB が異なるディスクにデプロイされている場合、RocksDB が配置されているディスクでは低速ディスク検出が機能しない問題を修正[＃17884](https://github.com/tikv/tikv/issues/17884) @ [LykxSassinator](https://github.com/LykxSassinator)
    -   `log-file`パラメータが指定されていない場合、jprof の出力が正しくキャプチャおよび処理されない問題を修正[＃17607](https://github.com/tikv/tikv/issues/17607) @ [ヘキシリー](https://github.com/Hexilee)
    -   休止状態のリージョンが起動しているときにレイテンシーが増加する可能性がある問題を修正[＃17101](https://github.com/tikv/tikv/issues/17101) @ [コナー1996](https://github.com/Connor1996)
    -   `RADIANS()`または`DEGREES()`関数を含むクエリを実行するとTiKVがpanic可能性がある問題を修正しました[＃17852](https://github.com/tikv/tikv/issues/17852) @ [ゲンリキ](https://github.com/gengliqi)
    -   読み取りスレッドがRaft Engine[＃17383](https://github.com/tikv/tikv/issues/17383) @ [LykxSassinator](https://github.com/LykxSassinator)のMemTable内の古いインデックスにアクセスしたときに発生するpanic問題を修正しました。
    -   同じキーのロック解除のために多数のトランザクションがキューイングされ、キーが頻繁に更新される場合、デッドロック検出への過度の圧力によって TiKV OOM 問題[＃17394](https://github.com/tikv/tikv/issues/17394) @ [ミョンケミンタ](https://github.com/MyonKeminta)が発生する可能性がある問題を修正しました。
    -   すべての休止状態の領域が[＃17101](https://github.com/tikv/tikv/issues/17101) @ [hhwyt](https://github.com/hhwyt)で起動すると書き込みジッターが発生する可能性がある問題を修正しました
    -   TiKVがブラジルとエジプトのタイムゾーンを誤って変換する問題を修正[＃16220](https://github.com/tikv/tikv/issues/16220) @ [金星の上](https://github.com/overvenus)
    -   オンラインアンセーフリカバリがマージ中止[＃15580](https://github.com/tikv/tikv/issues/15580) @ [v01dstar](https://github.com/v01dstar)を処理できない問題を修正
    -   エラー発生時にCPUプロファイリングフラグが正しくリセットされない問題を修正[＃17234](https://github.com/tikv/tikv/issues/17234) @ [コナー1996](https://github.com/Connor1996)
    -   `raft-entry-max-size` [＃17701](https://github.com/tikv/tikv/issues/17701) @ [スペードA-タン](https://github.com/SpadeA-Tang)と高く設定されすぎると、大規模なバッチ書き込みによってパフォーマンスジッターが発生する問題を修正しました。
    -   インポートモジュールの競合検出インターフェースにおける不適切なエラー処理により、TiKV がpanic可能性がある問題を修正しました[＃17830](https://github.com/tikv/tikv/issues/17830) @ [ジョッカウ](https://github.com/joccau)

-   PD

    -   `evict-leader-scheduler`または`grant-leader-scheduler`作成時にエラーが発生しても、エラーメッセージが pd-ctl [＃8759](https://github.com/tikv/pd/issues/8759) @ [okJiang](https://github.com/okJiang)に返されない問題を修正しました。
    -   etcdリーダー遷移[＃8823](https://github.com/tikv/pd/issues/8823) @ [rleungx](https://github.com/rleungx)中にPDがリーダーを素早く再選出できない問題を修正
    -   ラベル統計[＃8700](https://github.com/tikv/pd/issues/8700) @ [lhy1024](https://github.com/lhy1024)のメモリリーク問題を修正
    -   同じストアID [＃8756](https://github.com/tikv/pd/issues/8756) @ [okJiang](https://github.com/okJiang)で繰り返し作成された場合に`evict-leader-scheduler`正常に動作しない問題を修正
    -   リソース グループ クライアントでスロットが完全に削除されず、割り当てられたトークンの数が指定された値[＃7346](https://github.com/tikv/pd/issues/7346) @ [グオシャオゲ](https://github.com/guo-shaoge)より少なくなる問題を修正しました。
    -   `evict-leader-scheduler`で間違ったパラメータを使用すると、PD がエラーを正しく報告せず、一部のスケジューラが利用できなくなる問題を修正しました[＃8619](https://github.com/tikv/pd/issues/8619) @ [rleungx](https://github.com/rleungx)
    -   ホットスポット キャッシュ[＃8698](https://github.com/tikv/pd/issues/8698) @ [lhy1024](https://github.com/lhy1024)のメモリリーク問題を修正
    -   乱数ジェネレータ[＃8674](https://github.com/tikv/pd/issues/8674) @ [rleungx](https://github.com/rleungx)の頻繁な作成によって発生するパフォーマンスジッターの問題を修正しました

-   TiFlash

    -   TiFlash が同時 DDL 実行中に競合に遭遇した場合のTiFlashpanic問題を修正[＃8578](https://github.com/pingcap/tiflash/issues/8578) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)
    -   `LPAD()`と`RPAD()`関数が、場合によっては誤った結果を返す問題を修正[＃9465](https://github.com/pingcap/tiflash/issues/9465) @ [グオシャオゲ](https://github.com/guo-shaoge)
    -   2番目のパラメータが負の[＃9604](https://github.com/pingcap/tiflash/issues/9604) @ [グオシャオゲ](https://github.com/guo-shaoge)場合に`SUBSTRING()`関数が誤った結果を返す問題を修正しました
    -   テーブルに無効な文字[＃9461](https://github.com/pingcap/tiflash/issues/9461) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)を含むデフォルト値を持つビット型の列が含まれている場合、 TiFlash がテーブル スキーマを解析できない問題を修正しました。
    -   分散storageとコンピューティングアーキテクチャ[＃9665](https://github.com/pingcap/tiflash/issues/9665) @ [ジムララ](https://github.com/zimulala)で新しい列をクエリすると誤った結果が返される可能性がある問題を修正しました

-   ツール

    -   バックアップと復元 (BR)

        -   データの復元に失敗した後、チェックポイントから再開するとエラー`the target cluster is not fresh`が発生する問題を修正しました[＃50232](https://github.com/pingcap/tidb/issues/50232) @ [リーヴルス](https://github.com/Leavrth)
        -   ログバックアップが残留ロックをすぐに解決できず、チェックポイントが[＃57134](https://github.com/pingcap/tidb/issues/57134) @ [3ポイントシュート](https://github.com/3pointer)に進まない問題を修正しました。
        -   ログに暗号化された情報[＃57585](https://github.com/pingcap/tidb/issues/57585) @ [ケニーtm](https://github.com/kennytm)が出力される問題を修正
        -   `TestStoreRemoved`テストケースが不安定になる問題を修正[＃52791](https://github.com/pingcap/tidb/issues/52791) @ [ユジュンセン](https://github.com/YuJuncen)
        -   `k8s.io/api`ライブラリバージョン[＃57790](https://github.com/pingcap/tidb/issues/57790) @ [生まれ変わった人](https://github.com/BornChanger)にアップグレードして潜在的なセキュリティ脆弱性を修正します
        -   クラスター内に多数のテーブルがあるが、実際のデータサイズが小さい場合に PITR タスクが`Information schema is out of date`エラーを返す可能性がある問題を修正しました[＃57743](https://github.com/pingcap/tidb/issues/57743) @ [トリスタン1900](https://github.com/Tristan1900)

    -   TiCDC

        -   有効なインデックス[＃11765](https://github.com/pingcap/tiflow/issues/11765) @ [アズドンメン](https://github.com/asddongmen)のないテーブルで`TRUNCATE TABLE` DDL を複製するときに TiCDC がエラーを報告する可能性がある問題を修正しました。
        -   シンプルプロトコルメッセージ[＃11846](https://github.com/pingcap/tiflow/issues/11846) @ [3エースショーハンド](https://github.com/3AceShowHand)でパーティションテーブルの`tableID`が正しく設定されない問題を修正しました
        -   やり直しモジュールがエラー[＃11744](https://github.com/pingcap/tiflow/issues/11744) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)を正しく報告できない問題を修正しました
        -   `ignore-event`で`add table partition`イベントをフィルタリングするように構成した後、TiCDC が関連パーティションの他のタイプの DML 変更をダウンストリーム[＃10524](https://github.com/pingcap/tiflow/issues/10524) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)に複製しない問題を修正しました。
        -   TiDB DDL 所有者の変更中に DDL タスクのスキーマ バージョンが非増分になったときに、TiCDC が誤って DDL タスクを破棄する問題を修正しました[＃11714](https://github.com/pingcap/tiflow/issues/11714) @ [wlwilliamx](https://github.com/wlwilliamx)

    -   TiDB データ移行 (DM)

        -   物理インポートモード[＃11768](https://github.com/pingcap/tiflow/issues/11768) @ [D3ハンター](https://github.com/D3Hunter)でデータをインポートした後に、テーブル内の自動生成された ID に大きなジャンプが発生する可能性がある問題を修正しました。
        -   TLSと`shard-mode`両方が[＃11842](https://github.com/pingcap/tiflow/issues/11842) @ [孫暁光](https://github.com/sunxiaoguang)に設定されている場合に`start-task`の事前チェックが失敗する問題を修正
        -   パスワードの長さが19文字を超えるとMySQL 8.0への接続に失敗する問題を修正[＃11603](https://github.com/pingcap/tiflow/issues/11603) @ [魚類](https://github.com/fishiu)

    -   TiDB Lightning

        -   TiDB LightningがTiKV [＃56114](https://github.com/pingcap/tidb/issues/56114) @ [魚類](https://github.com/fishiu)から送信されたサイズ超過のメッセージを受信できない問題を修正しました
        -   物理インポートモード[＃56814](https://github.com/pingcap/tidb/issues/56814) @ [D3ハンター](https://github.com/D3Hunter)を使用してデータをインポートした後に`AUTO_INCREMENT`値が高すぎる値に設定される問題を修正しました
        -   メタデータ更新中に`Lock wait timeout`エラーが発生した場合にTiDB Lightning が自動的に再試行されない問題を修正しました[＃53042](https://github.com/pingcap/tidb/issues/53042) @ [グオショウヤン](https://github.com/guoshouyan)
        -   高同時実行シナリオでクラウドstorageからデータをインポートするときにパフォーマンスが低下する問題を修正[＃57413](https://github.com/pingcap/tidb/issues/57413) @ [xuanyu66](https://github.com/xuanyu66)
        -   多数の Parquet ファイル[＃56104](https://github.com/pingcap/tidb/issues/56104) @ [沢民州](https://github.com/zeminzhou)をインポートする際の準備フェーズでTiDB Lightning が長時間停止する可能性がある問題を修正しました
        -   TiDB Lightning [＃58085](https://github.com/pingcap/tidb/issues/58085) @ [ランス6716](https://github.com/lance6716)を使用してデータをインポートするときにエラーレポートの出力が切り捨てられる問題を修正しました

    -   Dumpling

        -   Dumpling がGoogle Cloud Storage (GCS) [＃56127](https://github.com/pingcap/tidb/issues/56127) @ [オリバーS929](https://github.com/OliverS929)から 503 エラーを受け取ったときに再試行に失敗する問題を修正しました
