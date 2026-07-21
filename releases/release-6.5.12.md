---
title: TiDB 6.5.12 Release Notes
summary: TiDB 6.5.12 の改善点とバグ修正について説明します。
---

# TiDB 6.5.12 リリースノート {#tidb-6-5-12-release-notes}

発売日：2025年2月27日

TiDBバージョン: 6.5.12

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   openEuler 22.03 LTS SP3/SP4 オペレーティングシステムをサポートします。詳細については、 [OSおよびプラットフォームの要件](https://docs.pingcap.com/tidb/v6.5/hardware-and-software-requirements#os-and-platform-requirements)参照してください。
-   [TiDB HTTP API](https://github.com/pingcap/tidb/blob/release-6.5/docs/tidb_http_api.md)から取得される DDL 履歴タスクのデフォルトの制限を 2048 に設定して、過剰な履歴タスクによる OOM の問題を防止します。 [＃55711](https://github.com/pingcap/tidb/issues/55711) @ [joccau](https://github.com/joccau)
-   インデックスを追加する際の取り込みフェーズの最大速度を制限する新しいシステム変数[`tidb_ddl_reorg_max_write_speed`](https://docs.pingcap.com/tidb/v6.5/system-variables#tidb_ddl_reorg_max_write_speed-new-in-v6512)を追加します。 [＃57156](https://github.com/pingcap/tidb/issues/57156) @ [CbcWestwolf](https://github.com/CbcWestwolf)

## 改善点 {#improvements}

-   TiDB

    -   読み取りタイムスタンプの有効性チェックを強化 [＃57786](https://github.com/pingcap/tidb/issues/57786) @ [MyonKeminta](https://github.com/MyonKeminta)

-   TiKV

    -   無効な`max_ts`更新の検出メカニズムを追加[＃17916](https://github.com/tikv/tikv/issues/17916) @ [ekexium](https://github.com/ekexium)

-   TiFlash

    -   クラスター化インデックスを持つテーブルで、バックグラウンドでの古いデータのガベージコレクションの速度が向上しました。 [＃9529](https://github.com/pingcap/tiflash/issues/9529) @ [JaySon-Huang](https://github.com/JaySon-Huang)

-   ツール

    -   Backup & Restore (BR)

        -   完全復元のためにターゲットクラスタが空のクラスタであるかどうかを確認するチェックを追加します[＃35744](https://github.com/pingcap/tidb/issues/35744) @ [3pointer](https://github.com/3pointer)
        -   非完全復元の場合、ターゲット クラスターに同じ名前のテーブルが含まれているかどうかを確認するチェックを追加します。 [＃55087](https://github.com/pingcap/tidb/issues/55087) @ [RidRisR](https://github.com/RidRisR)
        -   `br log restore`サブコマンドを除き、他の`br log`サブコマンドはすべて、メモリ消費量を削減するために TiDB `domain`データ構造のロードをスキップすることをサポートしています[＃52088](https://github.com/pingcap/tidb/issues/52088) @ [Leavrth](https://github.com/Leavrth)
        -   バックアップパフォーマンスを向上させるために、フルバックアップ中のテーブルレベルのチェックサム計算をデフォルトで無効にする（ `--checksum=false` ） [＃56373](https://github.com/pingcap/tidb/issues/56373) @ [Tristan1900](https://github.com/Tristan1900)

    -   TiDB Lightning

        -   CSV ファイルを解析するときに行幅チェックを追加して、OOM の問題を防ぐ[＃58590](https://github.com/pingcap/tidb/issues/58590) @ [D3Hunter](https://github.com/D3Hunter)

## バグ修正 {#bug-fixes}

-   TiDB

    -   `NATURAL JOIN`または`USING`句の後にサブクエリを使用するとエラーが発生する可能性がある問題を修正しました [＃53766](https://github.com/pingcap/tidb/issues/53766) @ [dash12653](https://github.com/dash12653)
    -   `CAST`関数が文字セットの明示的な設定をサポートしていない問題を修正しました [＃55677](https://github.com/pingcap/tidb/issues/55677) @ [Defined2014](https://github.com/Defined2014)
    -   `LOAD DATA ... REPLACE INTO`操作でデータの不整合が発生する問題を修正[＃56408](https://github.com/pingcap/tidb/issues/56408) @ [fzzf678](https://github.com/fzzf678)
    -   `ADD INDEX` を実行するときに TiDB がインデックスの長さ制限をチェックしない問題を修正しました [＃56930](https://github.com/pingcap/tidb/issues/56930) @ [fzzf678](https://github.com/fzzf678)
    -   共通テーブル式 (CTE) に複数のデータ コンシューマーがあり、1 つのコンシューマーがデータを読み取らずに終了した場合に発生する可能性のある無効なメモリアクセスの問題を修正しました[＃55881](https://github.com/pingcap/tidb/issues/55881) @ [windtalker](https://github.com/windtalker)
    -   `IndexMerge` を構築するときに一部の述語が失われる可能性がある問題を修正しました [＃58476](https://github.com/pingcap/tidb/issues/58476) @ [hawkingrei](https://github.com/hawkingrei)
    -   `BIT`型から`CHAR`型にデータを変換すると TiKV パニックが発生する可能性がある問題を修正しました [＃56494](https://github.com/pingcap/tidb/issues/56494) @ [lcwangchao](https://github.com/lcwangchao)
    -   `CREATE VIEW`ステートメントで変数またはパラメータを使用してもエラーが報告されない問題を修正[＃53176](https://github.com/pingcap/tidb/issues/53176) @ [mjonss](https://github.com/mjonss)
    -   解放されていないセッションリソースがメモリリークを引き起こす可能性がある問題を修正[＃56271](https://github.com/pingcap/tidb/issues/56271) @ [lance6716](https://github.com/lance6716)
    -   分散実行フレームワークの PD メンバーを変更した後に`ADD INDEX`実行が失敗する可能性がある問題を修正しました [＃48680](https://github.com/pingcap/tidb/issues/48680) @ [lance6716](https://github.com/lance6716)
    -   `cluster_slow_query table`をクエリするときに`ORDER BY`を使用すると、順序付けられていない結果が生成される可能性がある問題を修正しました。 [＃51723](https://github.com/pingcap/tidb/issues/51723) @ [Defined2014](https://github.com/Defined2014)
    -   stale read が読み取り操作のタイムスタンプを厳密に検証しない問題を修正しました。その結果、TSO と実際の物理時間の間にオフセットが存在する場合に、トランザクションの一貫性にわずかながら影響する可能性が生じます。 [＃56809](https://github.com/pingcap/tidb/issues/56809) @ [MyonKeminta](https://github.com/MyonKeminta)
    -   クエリ`INFORMATION_SCHEMA.columns`のパフォーマンスが@ [lance6716](https://github.com/lance6716)で低下する問題を修正 [＃58184](https://github.com/pingcap/tidb/issues/58184)
    -   `INSERT ... ON DUPLICATE KEY`文が`mysql_insert_id` と互換性がない問題を修正 [＃55965](https://github.com/pingcap/tidb/issues/55965) @ [tiancaiamao](https://github.com/tiancaiamao)
    -   クエリ条件`column IS NULL` で一意インデックスにアクセスするときに、オプティマイザが行数を誤って 1 と推定する問題を修正しました。 [＃56116](https://github.com/pingcap/tidb/issues/56116) @ [hawkingrei](https://github.com/hawkingrei)
    -   `IndexLookUp`演算子のメモリの一部が追跡されない問題を修正 [＃56440](https://github.com/pingcap/tidb/issues/56440) @ [wshwsh12](https://github.com/wshwsh12)
    -   TiDBの内部コルーチンで発生する可能性のあるデータ競合問題を修正しました [＃56053](https://github.com/pingcap/tidb/issues/56053) @ [fishiu](https://github.com/fishiu) [＃57798](https://github.com/pingcap/tidb/issues/57798) @ [tiancaiamao](https://github.com/tiancaiamao)
    -   クエリに利用可能なインデックスマージ実行プランがある場合に`read_from_storage`ヒントが有効にならない可能性がある問題を修正しました [＃56217](https://github.com/pingcap/tidb/issues/56217) @ [AilinKid](https://github.com/AilinKid)
    -   エイリアスを持つマルチテーブル`DELETE`ステートメントに対して実行プラン バインディングを作成できない問題を修正しました。 [＃56726](https://github.com/pingcap/tidb/issues/56726) @ [hawkingrei](https://github.com/hawkingrei)
    -   異常終了時に`INDEX_HASH_JOIN`アップする可能性がある問題を修正[＃54055](https://github.com/pingcap/tidb/issues/54055) @ [wshwsh12](https://github.com/wshwsh12)
    -   2人のDDL所有者が同時に存在する可能性がある問題を修正[＃54689](https://github.com/pingcap/tidb/issues/54689) @ [joccau](https://github.com/joccau)
    -   `information_schema.cluster_slow_query`テーブルをクエリするときに、時間フィルターが追加されていない場合、最新のスローログファイルのみがクエリされる問題を修正しました[＃56100](https://github.com/pingcap/tidb/issues/56100) @ [crazycs520](https://github.com/crazycs520)
    -   一意インデックスを追加するときに`duplicate entry`発生する可能性がある問題を修正 [＃56161](https://github.com/pingcap/tidb/issues/56161) @ [tangenta](https://github.com/tangenta)
    -   特定の型変換エラーでエラーメッセージが正しく表示されない問題を修正 [＃41730](https://github.com/pingcap/tidb/issues/41730) @ [hawkingrei](https://github.com/hawkingrei)
    -   `VIEW`で定義されたCTEが誤ってインライン化される問題を修正[＃56582](https://github.com/pingcap/tidb/issues/56582) @ [elsa0520](https://github.com/elsa0520)
    -   `UPDATE`文が`ENUM`型の値を誤って更新する問題を修正しました [＃56832](https://github.com/pingcap/tidb/issues/56832) @ [xhebox](https://github.com/xhebox)
    -   `DATE`列を追加した後に`UPDATE`文を実行すると、場合によってはのエラー`Incorrect date value: '0000-00-00'`が発生する問題を修正しました。 [＃59047](https://github.com/pingcap/tidb/issues/59047) @ [mjonss](https://github.com/mjonss)
    -   Prepareプロトコルで、クライアントがUTF8以外の文字セットを使用するとエラーが発生する問題を修正しました。 [＃58870](https://github.com/pingcap/tidb/issues/58870) @ [xhebox](https://github.com/xhebox)
    -   一時テーブルをクエリすると、場合によっては予期しない TiKV リクエストがトリガーされる可能性がある問題を修正しました[＃58875](https://github.com/pingcap/tidb/issues/58875) @ [tiancaiamao](https://github.com/tiancaiamao)
    -   ビューのステートメントに`ONLY_FULL_GROUP_BY`設定が反映されない問題を修正しました [＃53175](https://github.com/pingcap/tidb/issues/53175) @ [mjonss](https://github.com/mjonss)
    -   不一致な値型と型変換エラーを含む`IN`条件を使用してパーティション テーブルをクエリすると、誤ったクエリ結果が発生する問題を修正しました [＃54746](https://github.com/pingcap/tidb/issues/54746) @ [mjonss](https://github.com/mjonss)
    -   特定のフィールドに空の値が含まれている場合にスローログのクエリが失敗する可能性がある問題を修正[＃58147](https://github.com/pingcap/tidb/issues/58147) @ [yibin87](https://github.com/yibin87)
    -   `RADIANS()`関数が誤った順序で値を計算する問題を修正[＃57671](https://github.com/pingcap/tidb/issues/57671) @ [gengliqi](https://github.com/gengliqi)
    -   `BIT`列のデフォルト値が正しくない問題を修正[＃57301](https://github.com/pingcap/tidb/issues/57301) @ [YangKeao](https://github.com/YangKeao)
    -   CTE に`ORDER BY` 、 `LIMIT` 、または`SELECT DISTINCT`個の節が含まれており、別の CTE の再帰部分によって参照されている場合にインライン エラーが発生する可能性がある問題を修正しました。 [＃56603](https://github.com/pingcap/tidb/issues/56603) @ [elsa0520](https://github.com/elsa0520)
    -   統計情報を同期的にロードする際に発生するタイムアウトが正しく処理されない可能性がある問題を修正[＃57710](https://github.com/pingcap/tidb/issues/57710) @ [hawkingrei](https://github.com/hawkingrei)
    -   CTE でデータベース名を解析するときに誤ったデータベース名が返される可能性がある問題を修正しました [＃54582](https://github.com/pingcap/tidb/issues/54582) @ [hawkingrei](https://github.com/hawkingrei)
    -   無効なデータバインディングにより、TiDB が起動時にpanicする可能性がある問題を修正しました [＃58016](https://github.com/pingcap/tidb/issues/58016) @ [qw4990](https://github.com/qw4990)
    -   特定の極端なケースでコスト推定によって無効な INF/NaN 値が生成される可能性があり、その結果、結合したテーブルの再配置の結果が不正確になる可能性がある問題を修正しました[＃56704](https://github.com/pingcap/tidb/issues/56704) @ [winoros](https://github.com/winoros)
    -   統計ファイルに NULL 値が含まれている場合、統計を手動でロードすると失敗する可能性がある問題を修正しました。 [＃53966](https://github.com/pingcap/tidb/issues/53966) @ [King-Dylan](https://github.com/King-Dylan)
    -   同じ名前のビューを2つ作成してもエラーが報告されない問題を修正[＃58769](https://github.com/pingcap/tidb/issues/58769) @ [tiancaiamao](https://github.com/tiancaiamao)
    -   仮想生成列の依存関係に属性`ON UPDATE`を持つ列が含まれている場合、更新された行のデータとそのインデックスデータが不整合になる可能性がある問題を修正しました[＃56829](https://github.com/pingcap/tidb/issues/56829) @ [joechenrh](https://github.com/joechenrh)
    -   `INFORMATION_SCHEMA.TABLES`システムテーブルが誤った結果を返す問題を修正しました [＃57345](https://github.com/pingcap/tidb/issues/57345) @ [tangenta](https://github.com/tangenta)

-   TiKV

    -   Follower Readが古いデータを読み取る可能性がある問題を修正しました [＃17018](https://github.com/tikv/tikv/issues/17018) @ [glorv](https://github.com/glorv)
    -   ピアを破壊するときに TiKV がpanicする可能性がある問題を修正しました [＃18005](https://github.com/tikv/tikv/issues/18005) @ [glorv](https://github.com/glorv)
    -   タイムロールバックによって異常なRocksDBフロー制御が発生し、パフォーマンスジッターが発生する可能性がある問題を修正しました。 [＃17995](https://github.com/tikv/tikv/issues/17995) @ [LykxSassinator](https://github.com/LykxSassinator)
    -   ディスクストールによりリーダーの移行が妨げられ、パフォーマンスジッターが発生する問題を修正しました [＃17363](https://github.com/tikv/tikv/issues/17363) @ [hhwyt](https://github.com/hhwyt)
    -   1フェーズコミット（1PC）のみが有効で、非同期コミットが有効になっていない場合に、最後に書き込まれたデータが読み取れない可能性がある問題を修正[＃18117](https://github.com/tikv/tikv/issues/18117) @ [zyguan](https://github.com/zyguan)
    -   GCワーカーの負荷が高いときにデッドロックが発生する可能性がある問題を修正[＃18214](https://github.com/tikv/tikv/issues/18214) @ [zyguan](https://github.com/zyguan)
    -   Grafana の TiKV パネルの**ストレージ非同期書き込み期間の**監視メトリックが不正確であるという問題を修正しました[＃17579](https://github.com/tikv/tikv/issues/17579) @ [overvenus](https://github.com/overvenus)
    -   `RADIANS()`または`DEGREES()`関数を含むクエリを実行するとTiKVがpanicする可能性がある問題を修正しました[＃17852](https://github.com/tikv/tikv/issues/17852) @ [gengliqi](https://github.com/gengliqi)
    -   リージョンをマージすると稀に TiKV がpanicを起こす可能性がある問題を修正[＃17840](https://github.com/tikv/tikv/issues/17840) @ [glorv](https://github.com/glorv)
    -   リージョンを分割した後、リーダーをすぐに選出できない問題を修正しました [＃17602](https://github.com/tikv/tikv/issues/17602) @[LykxSassinator](https://github.com/LykxSassinator)
    -   GBK/GB18030エンコードデータの処理時にエンコードが失敗する可能性がある問題を修正 [＃17618](https://github.com/tikv/tikv/issues/17618) @ [CbcWestwolf](https://github.com/CbcWestwolf)

-   PD

    -   TSO を割り当てるときにメモリリークが発生する可能性がある問題を修正しました [＃9004](https://github.com/tikv/pd/issues/9004) @ [rleungx](https://github.com/rleungx)
    -   `tidb_enable_tso_follower_proxy`システム変数が有効にならない可能性がある問題を修正しました [＃8947](https://github.com/tikv/pd/issues/8947) @ [JmPotato](https://github.com/JmPotato)
    -   PD がpanicを起こす可能性のある潜在的な問題を修正[＃8915](https://github.com/tikv/pd/issues/8915) @ [bufferflies](https://github.com/bufferflies)
    -   長時間実行クラスタでメモリリークが発生する可能性がある問題を修正 [＃9047](https://github.com/tikv/pd/issues/9047) @ [bufferflies](https://github.com/bufferflies)
    -   PDノードがLeaderでない場合でもTSOを生成する可能性がある問題を修正しました [＃9051](https://github.com/tikv/pd/issues/9051) @ [rleungx](https://github.com/rleungx)
    -   PDリーダーの切り替え時にリージョン同期が間に合わない問題を修正しました [＃9017](https://github.com/tikv/pd/issues/9017) @[rleungx](https://github.com/rleungx)
    -   `evict-leader-scheduler`または`grant-leader-scheduler`作成時にエラーが発生しても、エラーメッセージが pd-ctl に返されない問題を修正しました。 [＃8759](https://github.com/tikv/pd/issues/8759) @ [okJiang](https://github.com/okJiang)
    -   ホットスポット キャッシュのメモリリーク問題を修正 [＃8698](https://github.com/tikv/pd/issues/8698) @ [lhy1024](https://github.com/lhy1024)
    -   多数のリージョンが存在する場合にPDのリージョンAPIをリクエストできない問題を修正[＃55872](https://github.com/pingcap/tidb/issues/55872) @ [rleungx](https://github.com/rleungx)
    -   同じストアID で繰り返し作成された場合に`evict-leader-scheduler`正常に動作しない問題を修正 [＃8756](https://github.com/tikv/pd/issues/8756) @ [okJiang](https://github.com/okJiang)
    -   潜在的なセキュリティ脆弱性を修正するために、Gin Web Framework のバージョンを v1.9.1 から v1.10.0 にアップグレードしました[＃8643](https://github.com/tikv/pd/issues/8643) @ [JmPotato](https://github.com/JmPotato)
    -   `evict-leader-scheduler`で間違ったパラメータを使用すると、PD がエラーを正しく報告せず、一部のスケジューラが利用できなくなる問題を修正しました[＃8619](https://github.com/tikv/pd/issues/8619) @ [rleungx](https://github.com/rleungx)
    -   ラベル統計のメモリリーク問題を修正 [＃8700](https://github.com/tikv/pd/issues/8700) @ [lhy1024](https://github.com/lhy1024)
    -   TiDB DashboardがPD `trace`データを正しく読み取れない問題を修正[＃7253](https://github.com/tikv/pd/issues/7253) @ [nolouch](https://github.com/nolouch)
    -   リージョン統計のメモリリーク問題を修正 [＃8710](https://github.com/tikv/pd/issues/8710) @ [rleungx](https://github.com/rleungx)
    -   etcdリーダー遷移中にPDがリーダーを素早く再選出できない問題を修正 [＃8823](https://github.com/tikv/pd/issues/8823) @ [rleungx](https://github.com/rleungx)

-   TiFlash

    -   `SUBSTRING()`関数が特定の整数型に対して`pos`と`len`引数をサポートせず、クエリエラーが発生する問題を修正しました [＃9473](https://github.com/pingcap/tiflash/issues/9473) @ [gengliqi](https://github.com/gengliqi)
    -   TiFlashでサポートされていない一部の JSON関数がTiFlash にプッシュダウンされる問題を修正しました [＃9444](https://github.com/pingcap/tiflash/issues/9444) @ [windtalker](https://github.com/windtalker)
    -   2番目のパラメータが負のの場合に`SUBSTRING()`関数が誤った結果を返す問題を修正しました [＃9604](https://github.com/pingcap/tiflash/issues/9604) @ [guo-shaoge](https://github.com/guo-shaoge)
    -   `LPAD()`と`RPAD()`関数が、場合によっては誤った結果を返す問題を修正しました[＃9465](https://github.com/pingcap/tiflash/issues/9465) @ [guo-shaoge](https://github.com/guo-shaoge)
    -   大きなテーブルで`DROP TABLE`を実行するとTiFlash OOM が発生する可能性がある問題を修正しました [＃9437](https://github.com/pingcap/tiflash/issues/9437) @ [JaySon-Huang](https://github.com/JaySon-Huang)
    -   CPUコア数を取得する際にゼロ除算エラーが発生し、 TiFlashが起動に失敗する問題を修正しました。 [＃9212](https://github.com/pingcap/tiflash/issues/9212) @ [xzhangxian1008](https://github.com/xzhangxian1008)
    -   大量のデータをインポートした後にTiFlash のメモリ使用量が高くなる可能性がある問題を修正[＃9812](https://github.com/pingcap/tiflash/issues/9812) @ [CalvinNeo](https://github.com/CalvinNeo)

-   ツール

    -   Backup & Restore (BR)

        -   TiKV にリクエストを送信するときに`rpcClient is idle`エラーが発生し、 BR が復元に失敗する問題を修正しました。 [＃58845](https://github.com/pingcap/tidb/issues/58845) @ [Tristan1900](https://github.com/Tristan1900)
        -   `br log status --json` を使用してログバックアップタスクをクエリすると、結果に`status`フィールドが表示されない問題を修正しました。 [＃57959](https://github.com/pingcap/tidb/issues/57959) @ [Leavrth](https://github.com/Leavrth)
        -   ログバックアップ中のPDLeaderI/Oレイテンシーによりチェックポイントレイテンシーが増加する可能性がある問題を修正しました。 [＃58574](https://github.com/pingcap/tidb/issues/58574) @ [YuJuncen](https://github.com/YuJuncen)
        -   `tiup br restore`コマンドがデータベースまたはテーブルの復元中にターゲット クラスタ テーブルが既に存在するかどうかのチェックを省略し、既存のテーブルを上書きする可能性がある問題を修正しました。 [＃58168](https://github.com/pingcap/tidb/issues/58168) @ [RidRisR](https://github.com/RidRisR)
        -   アドバンサー所有者が切り替わったときに、ログバックアップが予期せず一時停止状態になる可能性がある問題を修正しました。 [＃58031](https://github.com/pingcap/tidb/issues/58031) @ [3pointer](https://github.com/3pointer)
        -   ログバックアップが残留ロックをすぐに解決できず、チェックポイントが進まない問題を修正しました。 [＃57134](https://github.com/pingcap/tidb/issues/57134) @ [3pointer](https://github.com/3pointer)
        -   BR統合テストケースが不安定になる問題を修正し、スナップショットまたはログバックアップファイルの破損をシミュレートする新しいテストケースを追加します[＃53835](https://github.com/pingcap/tidb/issues/53835) @ [Leavrth](https://github.com/Leavrth)
        -   ログに暗号化された情報が出力される問題を修正 [＃57585](https://github.com/pingcap/tidb/issues/57585) @ [kennytm](https://github.com/kennytm)
        -   クラスター内に多数のテーブルがあるが、実際のデータサイズが小さい場合に PITR タスクが`Information schema is out of date`エラーを返す可能性がある問題を修正しました[＃57743](https://github.com/pingcap/tidb/issues/57743) @ [Tristan1900](https://github.com/Tristan1900)

    -   TiCDC

        -   TiCDC が`RENAME TABLE`操作中にフィルタリングに誤ったテーブル名を使用する問題を修正しました [＃11946](https://github.com/pingcap/tiflow/issues/11946) @ [wk989898](https://github.com/wk989898)
        -   Avroプロトコル経由で`default NULL`文を複製するときにTiCDCがエラーを報告する問題を修正 [＃11994](https://github.com/pingcap/tiflow/issues/11994) @ [wk989898](https://github.com/wk989898)
        -   PDスケールイン後にTiCDCがPDに正しく接続できない問題を修正 [＃12004](https://github.com/pingcap/tiflow/issues/12004) @ [lidezhu](https://github.com/lidezhu)
        -   チェンジフィードが停止または削除された後に初期スキャンがキャンセルされない問題を修正[＃11638](https://github.com/pingcap/tiflow/issues/11638) @ [3AceShowHand](https://github.com/3AceShowHand)
        -   アップストリームで新しく追加された列のデフォルト値を`NOT NULL`から`NULL`に変更すると、ダウンストリームのその列のデフォルト値が正しくなくなる問題を修正しました[＃12037](https://github.com/pingcap/tiflow/issues/12037) @ [wk989898](https://github.com/wk989898)
        -   `changefeed pause`コマンドで`--overwrite-checkpoint-ts`パラメータを使用すると、変更フィードが停止する可能性がある問題を修正しました。 [＃12055](https://github.com/pingcap/tiflow/issues/12055) @ [hongyunyan](https://github.com/hongyunyan)
        -   `CREATE TABLE IF NOT EXISTS`または`CREATE DATABASE IF NOT EXISTS`ステートメントを複製するときに TiCDC がpanicする可能性がある問題を修正しました [＃11839](https://github.com/pingcap/tiflow/issues/11839) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   有効なインデックスのないテーブルで`TRUNCATE TABLE` DDL を複製するときに TiCDC がエラーを報告する可能性がある問題を修正しました。 [＃11765](https://github.com/pingcap/tiflow/issues/11765) @ [asddongmen](https://github.com/asddongmen)
        -   TiDB DDL 所有者の変更中に DDL タスクのスキーマ バージョンが非増分になったときに、TiCDC が誤って DDL タスクを破棄する問題を修正[＃11714](https://github.com/pingcap/tiflow/issues/11714) @ [wlwilliamx](https://github.com/wlwilliamx)
        -   新しい TiKV ノードがクラスターに追加された後に、変更フィードがスタックする可能性がある問題を修正しました。 [＃11766](https://github.com/pingcap/tiflow/issues/11766) @ [lidezhu](https://github.com/lidezhu)
        -   Sarama クライアントによって再送信された順序外メッセージによって Kafka メッセージの順序が正しくなくなる問題を修正[＃11935](https://github.com/pingcap/tiflow/issues/11935) @ [3AceShowHand](https://github.com/3AceShowHand)
        -   PullerモジュールのResolved TSレイテンシーモニタリングで誤った値が表示される問題を修正しました [＃11561](https://github.com/pingcap/tiflow/issues/11561) @ [wlwilliamx](https://github.com/wlwilliamx)
        -   やり直しモジュールがエラーを正しく報告できない問題を修正しました [＃11744](https://github.com/pingcap/tiflow/issues/11744) @ [CharlesCheung96](https://github.com/CharlesCheung96)

    -   TiDB Data Migration (DM)

        -   複数の DM マスターノードが同時にリーダーになり、データの不整合が発生する可能性がある問題を修正しました[＃11602](https://github.com/pingcap/tiflow/issues/11602) @ [GMHDBJD](https://github.com/GMHDBJD)
        -   パスワードの長さが19文字を超えるとMySQL 8.0への接続に失敗する問題を修正[＃11603](https://github.com/pingcap/tiflow/issues/11603) @ [fishiu](https://github.com/fishiu)
        -   TLSと`shard-mode`の両方が設定されている場合に`start-task`の事前チェックが失敗する問題を修正 [＃11842](https://github.com/pingcap/tiflow/issues/11842) @ [sunxiaoguang](https://github.com/sunxiaoguang)

    -   TiDB Lightning

        -   ログが適切に感度調整されない問題を修正[＃59086](https://github.com/pingcap/tidb/issues/59086) @ [GMHDBJD](https://github.com/GMHDBJD)
        -   エンコードフェーズでのキャッシュ不足によりパフォーマンスが低下する問題を修正[＃56705](https://github.com/pingcap/tidb/issues/56705) @ [OliverS929](https://github.com/OliverS929)
        -   高同時実行シナリオでクラウドストレージからデータをインポートするときにパフォーマンスが低下する問題を修正[＃57413](https://github.com/pingcap/tidb/issues/57413) @ [xuanyu66](https://github.com/xuanyu66)
        -   メタデータ更新中に`Lock wait timeout`エラーが発生した場合にTiDB Lightning が自動的に再試行しない問題を修正しました[＃53042](https://github.com/pingcap/tidb/issues/53042) @ [guoshouyan](https://github.com/guoshouyan)
        -   TiDB LightningがTiKV から送信されたサイズ超過のメッセージを受信できない問題を修正しました [＃56114](https://github.com/pingcap/tidb/issues/56114) @ [fishiu](https://github.com/fishiu)
        -   TiDB Lightning を使用してデータをインポートするときにエラーレポートの出力が切り捨てられる問題を修正しました [＃58085](https://github.com/pingcap/tidb/issues/58085) @ [lance6716](https://github.com/lance6716)

    -   Dumpling

        -   Google Cloud Storage (GCS) から 503 エラーを受信したときにDumpling が適切に再試行できない問題を修正しました [＃56127](https://github.com/pingcap/tidb/issues/56127) @ [OliverS929](https://github.com/OliverS929)
