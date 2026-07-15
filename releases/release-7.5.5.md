---
title: TiDB 7.5.5 Release Notes
summary: TiDB 7.5.5 における互換性の変更、改善、およびバグ修正について説明します。
---

# TiDB 7.5.5 リリースノート {#tidb-7-5-5-release-notes}

発売日：2024年12月31日

TiDB バージョン: 7.5.5

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v7.5/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v7.5/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   インデックスを追加する際の取り込みフェーズの最大速度を制限する新しいシステム変数[`tidb_ddl_reorg_max_write_speed`](https://docs.pingcap.com/tidb/v7.5/system-variables#tidb_ddl_reorg_max_write_speed-new-in-v6512-and-v755)を追加します。 [＃57156](https://github.com/pingcap/tidb/issues/57156) @ [CbcWestwolf](https://github.com/CbcWestwolf)
-   TiKV構成項目[`raft-client-queue-size`](/tikv-configuration-file.md#raft-client-queue-size)のデフォルト値を`8192`から`16384` に変更します [＃17101](https://github.com/tikv/tikv/issues/17101) @ [Connor1996](https://github.com/Connor1996)

## 改善点 {#improvements}

-   TiDB

    -   統計情報がすべて TopN で構成され、対応するテーブル統計の変更された行数が 0 以外である場合に、TopN にヒットしない等価条件の推定結果を 0 から 1 に調整します[＃47400](https://github.com/pingcap/tidb/issues/47400) @ [terry1purcell](https://github.com/terry1purcell)

-   TiKV

    -   Raftと RocksDB が異なるディスクにデプロイされている場合、RocksDB が配置されているディスクでは低速ディスク検出が機能しない問題を修正[＃17884](https://github.com/tikv/tikv/issues/17884) @ [LykxSassinator](https://github.com/LykxSassinator)
    -   ピアのスローログを追加し、メッセージを保存します。 [＃16600](https://github.com/tikv/tikv/issues/16600) @ [Connor1996](https://github.com/Connor1996)
    -   ログの適用を待つために TiKV を再起動するときに発生する不安定なアクセス遅延を最適化し、TiKV の安定性を向上しました。 [＃15874](https://github.com/tikv/tikv/issues/15874) @ [LykxSassinator](https://github.com/LykxSassinator)

-   TiFlash

    -   TLS を有効にした後に証明書を更新することでTiFlash がpanic可能性がある問題を軽減します[＃8535](https://github.com/pingcap/tiflash/issues/8535) @ [windtalker](https://github.com/windtalker)
    -   クラスター化インデックスを持つテーブルで、バックグラウンドでの古いデータのガベージコレクションの速度が向上しました。 [＃9529](https://github.com/pingcap/tiflash/issues/9529) @ [JaySon-Huang](https://github.com/JaySon-Huang)
    -   分散ストレージおよびコンピューティングアーキテクチャ内のTiFlashコンピューティングノードの再試行戦略を最適化して、Amazon S3 からファイルをダウンロードする際の例外を処理します。 [＃9695](https://github.com/pingcap/tiflash/issues/9695) @ [JinheLin](https://github.com/JinheLin)

-   ツール

    -   Backup & Restore (BR)

        -   バックアップ中の不要なログ出力を削減[＃55902](https://github.com/pingcap/tidb/issues/55902) @ [Leavrth](https://github.com/Leavrth)

    -   TiDB Data Migration (DM)

        -   認識されないMariaDBbinlogイベントのログレベルを下げる[＃10204](https://github.com/pingcap/tiflow/issues/10204) @ [dveeden](https://github.com/dveeden)

## バグ修正 {#bug-fixes}

-   TiDB

    -   DDL 所有者ノードがに切り替えられた後、TiDB が以前の進行状況から再編成 DDL タスクを再開できない問題を修正しました。 [＃56506](https://github.com/pingcap/tidb/issues/56506) @ [tangenta](https://github.com/tangenta)
    -   非厳密モードで無効な`NULL`値が挿入される問題を修正 ( `sql_mode = ''` ) [＃56381](https://github.com/pingcap/tidb/issues/56381) @ [joechenrh](https://github.com/joechenrh)
    -   Grafanaの**Stats Healthy Distribution**パネルのデータが正しくない可能性がある問題を修正しました[＃57176](https://github.com/pingcap/tidb/issues/57176) @ [hawkingrei](https://github.com/hawkingrei)
    -   共通テーブル式 (CTE) に複数のデータ コンシューマーがあり、1 つのコンシューマーがデータを読み取らずに終了した場合に発生する可能性のある無効なメモリアクセスの問題を修正しました[＃55881](https://github.com/pingcap/tidb/issues/55881) @ [windtalker](https://github.com/windtalker)
    -   v6.5からv7.5以降にアップグレードされたクラスターで、既存のTTLタスクが予期せず頻繁に実行される問題を修正[＃56539](https://github.com/pingcap/tidb/issues/56539) @ [lcwangchao](https://github.com/lcwangchao)
    -   `tidb_ttl_job_enable`変数が無効になった後、TTL タスクがキャンセルされない問題を修正[＃57404](https://github.com/pingcap/tidb/issues/57404) @ [YangKeao](https://github.com/YangKeao)
    -   情報スキーマキャッシュミスにより、古い読み取りのクエリレイテンシーが増加する問題を修正しました。 [＃53428](https://github.com/pingcap/tidb/issues/53428) @ [crazycs520](https://github.com/crazycs520)
    -   stale read が読み取り操作のタイムスタンプを厳密に検証しない問題を修正しました。その結果、TSO と実際の物理時間の間にオフセットが存在する場合に、トランザクションの一貫性にわずかながら影響する可能性が生じます。 [＃56809](https://github.com/pingcap/tidb/issues/56809) @ [MyonKeminta](https://github.com/MyonKeminta)
    -   `IMPORT INTO`ステートメントを使用してデータをインポートした後、 `AUTO_INCREMENT`フィールドが正しく設定されない問題を修正しました。 [＃56476](https://github.com/pingcap/tidb/issues/56476) @ [D3Hunter](https://github.com/D3Hunter)
    -   2人のDDL所有者が同時に存在する可能性がある問題を修正[＃54689](https://github.com/pingcap/tidb/issues/54689) @ [joccau](https://github.com/joccau)
    -   ストレージエンジンとしてTiKVが選択されていない場合にTTLが失敗する可能性がある問題を修正 [＃56402](https://github.com/pingcap/tidb/issues/56402) @ [YangKeao](https://github.com/YangKeao)
    -   `ADD INDEX` を実行するときに TiDB がインデックスの長さ制限をチェックしない問題を修正しました [＃56930](https://github.com/pingcap/tidb/issues/56930) @ [fzzf678](https://github.com/fzzf678)
    -   TTLタスクをキャンセルした際に、対応するSQLが強制終了されない問題を修正[＃56511](https://github.com/pingcap/tidb/issues/56511) @ [lcwangchao](https://github.com/lcwangchao)
    -   エイリアスを持つマルチテーブル`DELETE`ステートメントに対して実行プラン バインディングを作成できない問題を修正しました。 [＃56726](https://github.com/pingcap/tidb/issues/56726) @ [hawkingrei](https://github.com/hawkingrei)
    -   `ANALYZE`使用してテーブルの統計情報を収集するときに、テーブルに仮想生成列の式インデックスが含まれていると、実行時にエラーが報告される問題を修正しました。 [＃57079](https://github.com/pingcap/tidb/issues/57079) @ [hawkingrei](https://github.com/hawkingrei)
    -   配置ルールを含むテーブル構造をインポートするときに Plan Replayer がエラーを報告する可能性がある問題を修正しました。 [＃54961](https://github.com/pingcap/tidb/issues/54961) @ [hawkingrei](https://github.com/hawkingrei)
    -   CTE でデータベース名を解析するときに間違ったデータベース名が返される問題を修正しました [＃54582](https://github.com/pingcap/tidb/issues/54582) @ [hawkingrei](https://github.com/hawkingrei)
    -   `INSERT ... ON DUPLICATE KEY`文が`mysql_insert_id` と互換性がない問題を修正 [＃55965](https://github.com/pingcap/tidb/issues/55965) @ [tiancaiamao](https://github.com/tiancaiamao)
    -   特定の状況下でプランキャッシュを使用する際に、メタデータロックの不適切な使用によって異常なデータが書き込まれる可能性がある問題を修正しました[＃53634](https://github.com/pingcap/tidb/issues/53634) @ [zimulala](https://github.com/zimulala)
    -   グローバルソートを使用してインデックスを追加するときにパフォーマンスが不安定になる問題を修正しました [＃54147](https://github.com/pingcap/tidb/issues/54147) @ [tangenta](https://github.com/tangenta)
    -   外部キーを含むテーブル構造をインポートするときに Plan Replayer がエラーを報告する可能性がある問題を修正しました。 [＃56456](https://github.com/pingcap/tidb/issues/56456) @ [hawkingrei](https://github.com/hawkingrei)
    -   `RANGE COLUMNS`パーティション関数と`utf8mb4_0900_ai_ci`照合順序を同時に使用すると、クエリ結果が正しくなくなる可能性がある問題を修正しました。 [＃57261](https://github.com/pingcap/tidb/issues/57261) @ [Defined2014](https://github.com/Defined2014)
    -   `NATURAL JOIN`または`USING`句の後にサブクエリを使用するとエラーが発生する可能性がある問題を修正しました [＃53766](https://github.com/pingcap/tidb/issues/53766) @ [dash12653](https://github.com/dash12653)
    -   書き込み競合が発生したときにTTLタスクをキャンセルできない問題を修正[＃56422](https://github.com/pingcap/tidb/issues/56422) @ [YangKeao](https://github.com/YangKeao)
    -   CTE に`ORDER BY` 、 `LIMIT` 、または`SELECT DISTINCT`句が含まれており、別の CTE の再帰部分によって参照されている場合、誤ってインライン化され、実行エラーが発生する可能性がある問題を修正しました。 [＃56603](https://github.com/pingcap/tidb/issues/56603) @ [elsa0520](https://github.com/elsa0520)
    -   `UPDATE`文が`ENUM`型の値を誤って更新する問題を修正しました [＃56832](https://github.com/pingcap/tidb/issues/56832) @ [xhebox](https://github.com/xhebox)
    -   `RECOVER TABLE BY JOB JOB_ID;`実行すると TiDB がpanicを起こす可能性がある問題を修正[＃55113](https://github.com/pingcap/tidb/issues/55113) @ [crazycs520](https://github.com/crazycs520)
    -   クエリに利用可能なインデックスマージ実行プランがある場合に`read_from_storage`ヒントが有効にならない可能性がある問題を修正しました [＃56217](https://github.com/pingcap/tidb/issues/56217) @ [AilinKid](https://github.com/AilinKid)
    -   異常終了時に`INDEX_HASH_JOIN`アップする可能性がある問題を修正[＃54055](https://github.com/pingcap/tidb/issues/54055) @ [wshwsh12](https://github.com/wshwsh12)
    -   分散実行フレームワーク (DXF) に関連するシステム テーブルをクエリすると、アップグレードが失敗する可能性がある問題を修正しました[＃49263](https://github.com/pingcap/tidb/issues/49263) @ [D3Hunter](https://github.com/D3Hunter)
    -   DDL内部トランザクションエラー`GC life time is shorter than transaction duration`によりインデックス追加が失敗する問題を修正[＃57043](https://github.com/pingcap/tidb/issues/57043) @ [tangenta](https://github.com/tangenta)
    -   `EXCHANGE PARTITION`実行して無効な行に遭遇すると、InfoSchema が完全にロードされ、エラー`failed to load schema diff`が[＃56685](https://github.com/pingcap/tidb/issues/56685) @ [D3Hunter](https://github.com/D3Hunter)で報告される問題を修正しました。
    -   `tidb_ddl_enable_fast_reorg`と`new_collations_enabled_on_first_bootstrap`有効になっているときに照合順序が正しく処理されず、データ インデックスが不一致になる問題を修正しました。 [＃58036](https://github.com/pingcap/tidb/issues/58036) @ [djshow832](https://github.com/djshow832)
    -   プランキャッシュがインデックスを追加するときに間違ったスキーマを使用するため、データインデックスが不整合になる問題を修正しました。 [＃56733](https://github.com/pingcap/tidb/issues/56733) @ [wjhuang2016](https://github.com/wjhuang2016)
    -   アップグレード中に`ALTER TABLE TIFLASH REPLICA`実行するとTiDBノードがクラッシュする問題を修正[＃57863](https://github.com/pingcap/tidb/issues/57863) @ [tangenta](https://github.com/tangenta)
    -   クエリ`INFORMATION_SCHEMA.columns`のパフォーマンスが@ [lance6716](https://github.com/lance6716)で低下する問題を修正 [＃58184](https://github.com/pingcap/tidb/issues/58184)
    -   TiFlashシステムテーブルを照会するためのデフォルトのタイムアウトが短すぎる問題を修正[＃57816](https://github.com/pingcap/tidb/issues/57816) @ [JaySon-Huang](https://github.com/JaySon-Huang)
    -   `default_collation_for_utf8mb4`変数の値が`SET NAMES`ステートメントで機能しない問題を修正しました [＃56439](https://github.com/pingcap/tidb/issues/56439) @ [Defined2014](https://github.com/Defined2014)
    -   `mysql.tidb_timer`テーブルでタイマーを手動で削除すると、TTL 内部コルーチンがpanicになる可能性がある問題を修正しました。 [＃57112](https://github.com/pingcap/tidb/issues/57112) @ [lcwangchao](https://github.com/lcwangchao)
    -   `ALTER TABLE`ステートメントを使用して通常のテーブルをパーティションテーブルに変換するときに、チェックが不十分なために誤ったデータが生成される可能性がある問題を修正しました。 [＃55721](https://github.com/pingcap/tidb/issues/55721) @ [mjonss](https://github.com/mjonss)
    -   `tidb_gogc_tuner_max_value`と`tidb_gogc_tuner_min_value`を設定するときに最大値がnullの場合、誤った警告メッセージが表示される問題を修正しました[＃57889](https://github.com/pingcap/tidb/issues/57889) @ [hawkingrei](https://github.com/hawkingrei)
    -   TiDBの内部コルーチンで発生する可能性のあるデータ競合問題を修正しました [＃56053](https://github.com/pingcap/tidb/issues/56053) @ [fishiu](https://github.com/fishiu) [＃57798](https://github.com/pingcap/tidb/issues/57798) @ [tiancaiamao](https://github.com/tiancaiamao)
    -   潜在的なセキュリティリスクを防ぐためのアップデート`golang-jwt`と`jwt` [＃57135](https://github.com/pingcap/tidb/issues/57135) @ [hawkingrei](https://github.com/hawkingrei)
    -   `ALTER TABLE`文を使用して、クラスター化インデックスを持つテーブルをパーティションテーブルに変換するときに、同時書き込みによってデータが重複する可能性がある問題を修正しました。 [＃57510](https://github.com/pingcap/tidb/issues/57510) @ [mjonss](https://github.com/mjonss)

-   TiKV

    -   リージョンをマージすると稀に TiKV がpanicを起こす可能性がある問題を修正[＃17840](https://github.com/tikv/tikv/issues/17840) @ [glorv](https://github.com/glorv)
    -   Raftと RocksDB が異なるディスクにデプロイされている場合、RocksDB が配置されているディスクでは低速ディスク検出が機能しない問題を修正[＃17884](https://github.com/tikv/tikv/issues/17884) @ [LykxSassinator](https://github.com/LykxSassinator)
    -   `log-file`パラメータが指定されていない場合、jprof の出力が正しくキャプチャおよび処理されない問題を修正[＃17607](https://github.com/tikv/tikv/issues/17607) @ [Hexilee](https://github.com/Hexilee)
    -   休止状態のリージョンが起動しているときにレイテンシーが増加する可能性がある問題を修正[＃17101](https://github.com/tikv/tikv/issues/17101) @ [Connor1996](https://github.com/Connor1996)
    -   `RADIANS()`または`DEGREES()`関数を含むクエリを実行するとTiKVがpanic可能性がある問題を修正しました[＃17852](https://github.com/tikv/tikv/issues/17852) @ [gengliqi](https://github.com/gengliqi)
    -   読み取りスレッドがRaft EngineのMemTable内の古いインデックスにアクセスしたときに発生するpanic問題を修正しました。 [＃17383](https://github.com/tikv/tikv/issues/17383) @ [LykxSassinator](https://github.com/LykxSassinator)
    -   多数のトランザクションが同じキーのロック解除待ち行列に入っていて、キーが頻繁に更新される場合、デッドロック検出への過度の圧力によって TiKV OOM 問題が発生する可能性がある問題を修正しました [＃17394](https://github.com/tikv/tikv/issues/17394) @ [MyonKeminta](https://github.com/MyonKeminta)
    -   すべての休止状態のリージョンが[＃17101](https://github.com/tikv/tikv/issues/17101) @ [hhwyt](https://github.com/hhwyt)で起動すると書き込みジッターが発生する可能性がある問題を修正しました
    -   TiKVがブラジルとエジプトのタイムゾーンを誤って変換する問題を修正[＃16220](https://github.com/tikv/tikv/issues/16220) @ [overvenus](https://github.com/overvenus)
    -   オンラインアンセーフリカバリがマージ中止を処理できない問題を修正 [＃15580](https://github.com/tikv/tikv/issues/15580) @ [v01dstar](https://github.com/v01dstar)
    -   エラー発生時にCPUプロファイリングフラグが正しくリセットされない問題を修正[＃17234](https://github.com/tikv/tikv/issues/17234) @ [Connor1996](https://github.com/Connor1996)
    -   `raft-entry-max-size` と高く設定されすぎると、大規模なバッチ書き込みによってパフォーマンスジッターが発生する問題を修正しました。 [＃17701](https://github.com/tikv/tikv/issues/17701) @ [SpadeA-Tang](https://github.com/SpadeA-Tang)
    -   インポートモジュールの競合検出インターフェースにおける不適切なエラー処理により、TiKV がpanicを起こす可能性がある問題を修正しました[＃17830](https://github.com/tikv/tikv/issues/17830) @ [joccau](https://github.com/joccau)

-   PD

    -   `evict-leader-scheduler`または`grant-leader-scheduler`作成時にエラーが発生しても、エラーメッセージが pd-ctl に返されない問題を修正しました。 [＃8759](https://github.com/tikv/pd/issues/8759) @ [okJiang](https://github.com/okJiang)
    -   etcdリーダー遷移中にPDがリーダーを素早く再選出できない問題を修正 [＃8823](https://github.com/tikv/pd/issues/8823) @ [rleungx](https://github.com/rleungx)
    -   ラベル統計のメモリリーク問題を修正 [＃8700](https://github.com/tikv/pd/issues/8700) @ [lhy1024](https://github.com/lhy1024)
    -   同じストアID で繰り返し作成された場合に`evict-leader-scheduler`正常に動作しない問題を修正 [＃8756](https://github.com/tikv/pd/issues/8756) @ [okJiang](https://github.com/okJiang)
    -   リソース グループ クライアントでスロットが完全に削除されず、割り当てられたトークンの数が指定された値より少なくなる問題を修正しました。 [＃7346](https://github.com/tikv/pd/issues/7346) @ [guo-shaoge](https://github.com/guo-shaoge)
    -   `evict-leader-scheduler`で間違ったパラメータを使用すると、PD がエラーを正しく報告せず、一部のスケジューラが利用できなくなる問題を修正しました[＃8619](https://github.com/tikv/pd/issues/8619) @ [rleungx](https://github.com/rleungx)
    -   ホットスポット キャッシュのメモリリーク問題を修正 [＃8698](https://github.com/tikv/pd/issues/8698) @ [lhy1024](https://github.com/lhy1024)
    -   乱数ジェネレータの頻繁な作成によって発生するパフォーマンスジッターの問題を修正しました [＃8674](https://github.com/tikv/pd/issues/8674) @ [rleungx](https://github.com/rleungx)

-   TiFlash

    -   TiFlash が同時 DDL 実行中に競合に遭遇した場合のTiFlashpanic問題を修正[＃8578](https://github.com/pingcap/tiflash/issues/8578) @ [JaySon-Huang](https://github.com/JaySon-Huang)
    -   `LPAD()`と`RPAD()`関数が、場合によっては誤った結果を返す問題を修正しました[＃9465](https://github.com/pingcap/tiflash/issues/9465) @ [guo-shaoge](https://github.com/guo-shaoge)
    -   2番目のパラメータが負のの場合に`SUBSTRING()`関数が誤った結果を返す問題を修正しました [＃9604](https://github.com/pingcap/tiflash/issues/9604) @ [guo-shaoge](https://github.com/guo-shaoge)
    -   テーブルに無効な文字を含むデフォルト値を持つビット型の列が含まれている場合、 TiFlash がテーブル スキーマを解析できない問題を修正しました。 [＃9461](https://github.com/pingcap/tiflash/issues/9461) @ [Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    -   分散ストレージおよびコンピューティングアーキテクチャで新しい列をクエリすると誤った結果が返される可能性がある問題を修正しました [＃9665](https://github.com/pingcap/tiflash/issues/9665) @ [zimulala](https://github.com/zimulala)

-   ツール

    -   Backup & Restore (BR)

        -   データの復元に失敗した後、チェックポイントから再開するとエラー`the target cluster is not fresh`が発生する問題を修正しました[＃50232](https://github.com/pingcap/tidb/issues/50232) @ [Leavrth](https://github.com/Leavrth)
        -   ログバックアップが残留ロックをすぐに解決できず、チェックポイントがに進まない問題を修正しました。 [＃57134](https://github.com/pingcap/tidb/issues/57134) @ [3pointer](https://github.com/3pointer)
        -   ログに暗号化された情報が出力される問題を修正 [＃57585](https://github.com/pingcap/tidb/issues/57585) @ [kennytm](https://github.com/kennytm)
        -   `TestStoreRemoved`テストケースが不安定になる問題を修正[＃52791](https://github.com/pingcap/tidb/issues/52791) @ [YuJuncen](https://github.com/YuJuncen)
        -   `k8s.io/api`ライブラリバージョンにアップグレードして潜在的なセキュリティ脆弱性を修正します [＃57790](https://github.com/pingcap/tidb/issues/57790) @ [BornChanger](https://github.com/BornChanger)
        -   クラスター内に多数のテーブルがあるが、実際のデータサイズが小さい場合に PITR タスクが`Information schema is out of date`エラーを返す可能性がある問題を修正しました[＃57743](https://github.com/pingcap/tidb/issues/57743) @ [Tristan1900](https://github.com/Tristan1900)

    -   TiCDC

        -   有効なインデックスのないテーブルで`TRUNCATE TABLE` DDL を複製するときに TiCDC がエラーを報告する可能性がある問題を修正しました。 [＃11765](https://github.com/pingcap/tiflow/issues/11765) @ [asddongmen](https://github.com/asddongmen)
        -   シンプルプロトコルメッセージでパーティションテーブルの`tableID`正しく設定されていない問題を修正しました。 [＃11846](https://github.com/pingcap/tiflow/issues/11846) @ [3AceShowHand](https://github.com/3AceShowHand)
        -   やり直しモジュールがエラーを正しく報告できない問題を修正しました [＃11744](https://github.com/pingcap/tiflow/issues/11744) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   `ignore-event`で`add table partition`イベントをフィルタリングするように設定した後、TiCDC が関連パーティションの他のタイプの DML 変更をダウンストリームに複製しない問題を修正しました。 [＃10524](https://github.com/pingcap/tiflow/issues/10524) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   TiDB DDL 所有者の変更中に DDL タスクのスキーマ バージョンが非増分になったときに、TiCDC が誤って DDL タスクを破棄する問題を修正[＃11714](https://github.com/pingcap/tiflow/issues/11714) @ [wlwilliamx](https://github.com/wlwilliamx)

    -   TiDB Data Migration (DM)

        -   物理インポートモードでデータをインポートした後に、テーブル内の自動生成された ID に大きなジャンプが発生する可能性がある問題を修正しました。 [＃11768](https://github.com/pingcap/tiflow/issues/11768) @ [D3Hunter](https://github.com/D3Hunter)
        -   TLSと`shard-mode`両方がに設定されている場合に`start-task`の事前チェックが失敗する問題を修正 [＃11842](https://github.com/pingcap/tiflow/issues/11842) @ [sunxiaoguang](https://github.com/sunxiaoguang)
        -   パスワードの長さが19文字を超えるとMySQL 8.0への接続に失敗する問題を修正[＃11603](https://github.com/pingcap/tiflow/issues/11603) @ [fishiu](https://github.com/fishiu)

    -   TiDB Lightning

        -   TiDB LightningがTiKV から送信されたサイズ超過のメッセージを受信できない問題を修正しました [＃56114](https://github.com/pingcap/tidb/issues/56114) @ [fishiu](https://github.com/fishiu)
        -   物理インポートモードを使用してデータをインポートした後に`AUTO_INCREMENT`値が高すぎる値に設定される問題を修正しました [＃56814](https://github.com/pingcap/tidb/issues/56814) @ [D3Hunter](https://github.com/D3Hunter)
        -   メタデータ更新中に`Lock wait timeout`エラーが発生した場合にTiDB Lightning が自動的に再試行しない問題を修正しました[＃53042](https://github.com/pingcap/tidb/issues/53042) @ [guoshouyan](https://github.com/guoshouyan)
        -   高同時実行シナリオでクラウドストレージからデータをインポートするときにパフォーマンスが低下する問題を修正[＃57413](https://github.com/pingcap/tidb/issues/57413) @ [xuanyu66](https://github.com/xuanyu66)
        -   多数の Parquet ファイルをインポートする際の準備フェーズでTiDB Lightning が長時間停止する可能性がある問題を修正しました [＃56104](https://github.com/pingcap/tidb/issues/56104) @ [zeminzhou](https://github.com/zeminzhou)
        -   TiDB Lightning を使用してデータをインポートするときにエラーレポートの出力が切り捨てられる問題を修正しました [＃58085](https://github.com/pingcap/tidb/issues/58085) @ [lance6716](https://github.com/lance6716)

    -   Dumpling

        -   Google Cloud Storage (GCS) から 503 エラーを受信したときにDumpling が適切に再試行できない問題を修正しました [＃56127](https://github.com/pingcap/tidb/issues/56127) @ [OliverS929](https://github.com/OliverS929)
