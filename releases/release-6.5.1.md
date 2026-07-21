---
title: TiDB 6.5.1 Release Notes
summary: TiDB 6.5.1 における互換性の変更、改善、およびバグ修正について説明します。
---

# TiDB 6.5.1 リリースノート {#tidb-6-5-1-release-notes}

発売日：2023年3月10日

TiDB バージョン: 6.5.1

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   2023年2月20日以降、TiDBおよびTiDB Dashboardの新しいバージョン（v6.5.1を含む）では、 [テレメトリ機能](/telemetry.md)デフォルトで無効化され、使用状況情報は収集されず、PingCAPと共有されません。これらのバージョンにアップグレードする前に、クラスターがデフォルトのテレメトリ設定を使用している場合、アップグレード後にテレメトリ機能が無効化されます。具体的なバージョンについては、 [TiDB リリース タイムライン](/releases/release-timeline.md)参照してください。

    -   [`tidb_enable_telemetry`](/system-variables.md#tidb_enable_telemetry-new-in-v402)システム変数のデフォルト値が`ON`から`OFF`に変更されます。
    -   TiDB [`enable-telemetry`](/tidb-configuration-file.md#enable-telemetry-new-in-v402)構成項目のデフォルト値が`true`から`false`に変更されます。
    -   PD [`enable-telemetry`](/pd-configuration-file.md#enable-telemetry)構成項目のデフォルト値が`true`から`false`に変更されます。

-   v1.11.3 以降、新規に導入されたTiUPではテレメトリ機能がデフォルトで無効化され、使用状況情報は収集されません。v1.11.3 より前のバージョンのTiUPから v1.11.3 以降のバージョンにアップグレードした場合、テレメトリ機能はアップグレード前と同じ状態を維持します。

-   潜在的な正確性の問題のため、パーティション化されたテーブルでの列タイプの変更はサポートされなくなりました[＃40620](https://github.com/pingcap/tidb/issues/40620) @ [mjonss](https://github.com/mjonss)

-   TiKV [`advance-ts-interval`](/tikv-configuration-file.md#advance-ts-interval)設定項目のデフォルト値が`1s`から`20s`に変更されました。この設定項目を変更することで、レイテンシーを短縮し、 ステイル読み取りデータの適時性を向上させることができます。詳細は[ステイル読み取りのレイテンシーを削減](/stale-read.md#reduce-stale-read-latency)ご覧ください。

-   ネットワーク トラフィックを削減するために、TiKV [`cdc.min-ts-interval`](/tikv-configuration-file.md#min-ts-interval)構成項目の既定値が`"200ms"`から`"1s"`に変更されました。

## 改善点 {#improvements}

-   TiDB

    -   v6.5.1以降、 TiDB Operator v1.4.3以降でデプロイされたTiDBクラスタはIPv6アドレスをサポートします。これにより、TiDBはより広いアドレス空間をサポートし、セキュリティとネットワークパフォーマンスを向上させることができます。

        -   IPv6 アドレスの完全サポート: TiDB は、クライアント接続、ノード間の内部通信、外部システムとの通信など、すべてのネットワーク接続で IPv6 アドレスの使用をサポートします。
        -   デュアルスタックのサポート：まだIPv6への完全移行の準備が整っていない場合でも、TiDBはデュアルスタックネットワークをサポートしています。つまり、同じTiDBクラスタ内でIPv4とIPv6の両方のアドレスを使用し、設定によってIPv6を優先するネットワーク展開モードを選択できます。

        IPv6 の導入の詳細については、 [Kubernetes 上の TiDB ドキュメント](https://docs.pingcap.com/tidb-in-kubernetes/stable/configure-a-tidb-cluster#ipv6-support)参照してください。

    -   TiDB クラスタの初期化時に実行される SQL スクリプトの指定をサポート[＃35624](https://github.com/pingcap/tidb/issues/35624) @ [morgo](https://github.com/morgo)

        TiDB v6.5.1 では、新しい設定項目[`initialize-sql-file`](https://docs.pingcap.com/tidb/v6.5/tidb-configuration-file#initialize-sql-file-new-in-v651)が追加されました。TiDB クラスタを初めて起動する際に、コマンドラインパラメータ`--initialize-sql-file`を設定することで、実行する SQL スクリプトを指定できます。この機能は、システム変数の値の変更、ユーザーの作成、権限の付与などの操作を行う際に使用できます。詳細については、 [ドキュメント](https://docs.pingcap.com/tidb/v6.5/tidb-configuration-file#initialize-sql-file-new-in-v651)参照してください。

    -   メモリリークとパフォーマンスの低下を防ぐため、期限切れのリージョンキャッシュを定期的にクリアします[＃40461](https://github.com/pingcap/tidb/issues/40461) @ [sticnarf](https://github.com/sticnarf)

    -   PROXYプロトコルフォールバックモードを有効にするかどうかを制御する新しい設定項目`--proxy-protocol-fallbackable`を追加します。このパラメータを`true`に設定すると、TiDBはPROXYクライアント接続とPROXYプロトコルヘッダーのないクライアント接続を受け入れます。 [＃41409](https://github.com/pingcap/tidb/issues/41409) @ [blacktear23](https://github.com/blacktear23)

    -   メモリトラッカー の精度を向上させる [＃40500](https://github.com/pingcap/tidb/issues/40500) @ [wshwsh12](https://github.com/wshwsh12) [＃40900](https://github.com/pingcap/tidb/issues/40900)

    -   プランキャッシュが有効にならない場合、システムはその理由を警告として返します[＃40210](https://github.com/pingcap/tidb/pull/40210) @ [qw4990](https://github.com/qw4990)

    -   範囲外推定の最適化戦略を改善する[＃39008](https://github.com/pingcap/tidb/issues/39008) @ [time-and-fate](https://github.com/time-and-fate)

-   TiKV

    -   1コア未満のCPUでTiKVの起動をサポート[＃13586](https://github.com/tikv/tikv/issues/13586) [＃13752](https://github.com/tikv/tikv/issues/13752) [＃14017](https://github.com/tikv/tikv/issues/14017) @ [andreid-db](https://github.com/andreid-db)
    -   統合読み取りプールのスレッド制限（ `readpool.unified.max-thread-count` ）をCPUクォータの10倍に増やし、高同時実行クエリをより適切に処理します。 [＃13690](https://github.com/tikv/tikv/issues/13690) @ [v01dstar](https://github.com/v01dstar)
    -   デフォルト値の`resolved-ts.advance-ts-interval`を`"1s"`から`"20s"`に変更して、リージョン間のトラフィックを削減します。 [＃14100](https://github.com/tikv/tikv/issues/14100) @ [overvenus](https://github.com/overvenus)

-   TiFlash

    -   データ量が多いときにTiFlashの起動を大幅に高速化[＃6395](https://github.com/pingcap/tiflash/issues/6395) @ [hehechen](https://github.com/hehechen)

-   ツール

    -   Backup & Restore (BR)

        -   TiKV側でのログバックアップファイルのダウンロードの同時実行を最適化して、通常のシナリオでのPITRのパフォーマンスを向上させます。 [＃14206](https://github.com/tikv/tikv/issues/14206) @ [YuJuncen](https://github.com/YuJuncen)

    -   TiCDC

        -   プルベースのシンクを有効にしてシステムスループットを最適化します[＃8232](https://github.com/pingcap/tiflow/issues/8232) @ [Rustin170506](https://github.com/Rustin170506)
        -   GCS 互換または Azure 互換のオブジェクトストレージへの REDO ログの保存をサポート [＃7987](https://github.com/pingcap/tiflow/issues/7987) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   シンクのスループットを向上させるために、非同期モードでMQシンクとMySQLシンクを実装します[＃5928](https://github.com/pingcap/tiflow/issues/5928) @ [amyangfei](https://github.com/amyangfei) @ [CharlesCheung96](https://github.com/CharlesCheung96)

## バグ修正 {#bug-fixes}

-   TiDB

    -   [`pessimistic-auto-commit`](/tidb-configuration-file.md#pessimistic-auto-commit-new-in-v600)構成項目がPointGetクエリで有効にならない問題を修正しました [＃39928](https://github.com/pingcap/tidb/issues/39928) @ [zyguan](https://github.com/zyguan)
    -   長いセッション接続で`INSERT`または`REPLACE`ステートメントがpanicする可能性がある問題を修正しました [＃40351](https://github.com/pingcap/tidb/issues/40351) @ [winoros](https://github.com/winoros)
    -   `auto analyze`正常なシャットダウンに長い時間がかかる問題を修正[＃40038](https://github.com/pingcap/tidb/issues/40038) @ [xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    -   DDL取り込み中にデータ競合が発生する可能性がある問題を修正 [＃40970](https://github.com/pingcap/tidb/issues/40970) @ [tangenta](https://github.com/tangenta)
    -   インデックスを追加するとデータ競合が発生する可能性がある問題を修正しました [＃40879](https://github.com/pingcap/tidb/issues/40879) @ [tangenta](https://github.com/tangenta)
    -   テーブルに多数のリージョンがある場合に無効なリージョンキャッシュが原因でインデックスの追加操作が非効率になる問題を修正しました。 [＃38436](https://github.com/pingcap/tidb/issues/38436) @ [tangenta](https://github.com/tangenta)
    -   初期化中にTiDBがデッドロックする可能性がある問題を修正[＃40408](https://github.com/pingcap/tidb/issues/40408) @ [Defined2014](https://github.com/Defined2014)
    -   TiDB がキー範囲を構築するときに`NULL`値を不適切に処理するため、予期しないデータが読み取られる問題を修正しました。 [＃40158](https://github.com/pingcap/tidb/issues/40158) @ [tiancaiamao](https://github.com/tiancaiamao)
    -   メモリの再利用により、システム変数の値が誤って変更される可能性がある問題を修正[＃40979](https://github.com/pingcap/tidb/issues/40979) @ [lcwangchao](https://github.com/lcwangchao)
    -   テーブルの主キーに`ENUM`列が含まれている場合にTTLタスクが失敗する問題を修正しました [＃40456](https://github.com/pingcap/tidb/issues/40456) @ [lcwangchao](https://github.com/lcwangchao)
    -   一意インデックスを追加するときに TiDB がパニックを起こす問題を修正しました [＃40592](https://github.com/pingcap/tidb/issues/40592) @ [tangenta](https://github.com/tangenta)
    -   同じテーブルを同時に切り捨てるときに、一部の切り捨て操作が MDL によってブロックされない問題を修正[＃40484](https://github.com/pingcap/tidb/issues/40484) @ [wjhuang2016](https://github.com/wjhuang2016)
    -   動的トリミングモードでパーティションテーブルにグローバルバインディングが作成された後にTiDBが再起動できない問題を修正しました [＃40368](https://github.com/pingcap/tidb/issues/40368) @ [Yisaer](https://github.com/Yisaer)
    -   「カーソル読み取り」メソッドを使用してデータを読み取ると、GC のためにエラーが返される可能性がある問題を修正しました。 [＃39447](https://github.com/pingcap/tidb/issues/39447) @ [zyguan](https://github.com/zyguan)
    -   `SHOW PROCESSLIST` の結果で`EXECUTE`情報が null になる問題を修正しました [＃41156](https://github.com/pingcap/tidb/issues/41156) @ [YangKeao](https://github.com/YangKeao)
    -   `globalMemoryControl`クエリを強制終了しているときに、 `KILL`操作が終了しない可能性がある問題を修正しました [＃41057](https://github.com/pingcap/tidb/issues/41057) @ [wshwsh12](https://github.com/wshwsh12)
    -   `indexMerge`エラーに遭遇した後に TiDB がpanicする可能性がある問題を修正[＃41047](https://github.com/pingcap/tidb/issues/41047) [＃40877](https://github.com/pingcap/tidb/issues/40877) @ [guo-shaoge](https://github.com/guo-shaoge) @ [windtalker](https://github.com/windtalker)
    -   `ANALYZE`文が`KILL` で終了する可能性がある問題を修正しました [＃41825](https://github.com/pingcap/tidb/issues/41825) @ [XuHuaiyu](https://github.com/XuHuaiyu)
    -   `indexMerge` で goroutine リークが発生する可能性がある問題を修正しました [＃41605](https://github.com/pingcap/tidb/issues/41605) @ [guo-shaoge](https://github.com/guo-shaoge) [＃41545](https://github.com/pingcap/tidb/issues/41545)
    -   符号なしの`TINYINT` / `SMALLINT` / `INT`値を`0` より小さい`DECIMAL` / `FLOAT` / `DOUBLE`値と比較するときに誤った結果になる可能性がある問題を修正しました。 [＃41736](https://github.com/pingcap/tidb/issues/41736) @ [LittleFall](https://github.com/LittleFall)
    -   `tidb_enable_reuse_chunk`有効にするとメモリリークが発生する可能性がある問題を修正 [＃40987](https://github.com/pingcap/tidb/issues/40987) @ [guo-shaoge](https://github.com/guo-shaoge)
    -   タイムゾーンでのデータ競合によりデータインデックスの不整合が発生する可能性がある問題を修正[＃40710](https://github.com/pingcap/tidb/issues/40710) @ [wjhuang2016](https://github.com/wjhuang2016)
    -   `batch cop`実行中のスキャン詳細情報が不正確になる可能性がある問題を修正[＃41582](https://github.com/pingcap/tidb/issues/41582) @ [you06](https://github.com/you06)
    -   `cop`の上限同時実行数が制限されない問題を修正 [＃41134](https://github.com/pingcap/tidb/issues/41134) @ [you06](https://github.com/you06)
    -   `cursor read`分の`statement context`が誤ってキャッシュされる問題を修正 [＃39998](https://github.com/pingcap/tidb/issues/39998) @ [zyguan](https://github.com/zyguan)
    -   メモリリークとパフォーマンスの低下を防ぐため、古くなったリージョンキャッシュを定期的にクリーンアップします[＃40355](https://github.com/pingcap/tidb/issues/40355) @ [sticnarf](https://github.com/sticnarf)
    -   `year <cmp> const`含むクエリでプラン キャッシュを使用すると間違った結果が返される可能性がある問題を修正しました [＃41626](https://github.com/pingcap/tidb/issues/41626) @ [qw4990](https://github.com/qw4990)
    -   大きな範囲と大量のデータ変更を伴うクエリを実行するときに大きな推定エラーが発生する問題を修正[＃39593](https://github.com/pingcap/tidb/issues/39593) @ [time-and-fate](https://github.com/time-and-fate)
    -   Plan Cache の使用時に、一部の条件が Join 演算子を通じてプッシュダウンできない問題を修正しました。 [＃38205](https://github.com/pingcap/tidb/issues/38205) @ [qw4990](https://github.com/qw4990) [＃40093](https://github.com/pingcap/tidb/issues/40093)
    -   IndexMerge プランが SET 型の列 に誤った範囲を生成する可能性がある問題を修正しました [＃41293](https://github.com/pingcap/tidb/issues/41293) @ [time-and-fate](https://github.com/time-and-fate) [＃41273](https://github.com/pingcap/tidb/issues/41273)
    -   プランキャッシュが`int_col <cmp> decimal`条件 を処理するときにフルスキャン プランをキャッシュする可能性がある問題を修正しました [＃41032](https://github.com/pingcap/tidb/issues/41032) @ [qw4990](https://github.com/qw4990) [＃40679](https://github.com/pingcap/tidb/issues/40679)
    -   プランキャッシュが`int_col in (decimal...)`条件を処理するときにフルスキャン プランをキャッシュする可能性がある問題を修正しました [＃40224](https://github.com/pingcap/tidb/issues/40224) @ [qw4990](https://github.com/qw4990)
    -   `ignore_plan_cache`ヒントが`INSERT`ステートメント では機能しない可能性がある問題を修正しました [＃39717](https://github.com/pingcap/tidb/issues/39717) @ [qw4990](https://github.com/qw4990) [＃40079](https://github.com/pingcap/tidb/issues/40079)
    -   自動分析により TiDB が終了できなくなる問題を修正しました [＃40038](https://github.com/pingcap/tidb/issues/40038) @ [xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    -   パーティションテーブルの符号なし主キーに不正なアクセス間隔が構築される可能性がある問題を修正しました。 [＃40309](https://github.com/pingcap/tidb/issues/40309) @ [winoros](https://github.com/winoros)
    -   プランキャッシュがシャッフル演算子をキャッシュし、誤った結果を返す可能性がある問題を修正[＃38335](https://github.com/pingcap/tidb/issues/38335) @ [qw4990](https://github.com/qw4990)
    -   パーティションテーブルにグローバルバインディングを作成すると、TiDB が起動に失敗する可能性がある問題を修正しました。 [＃40368](https://github.com/pingcap/tidb/issues/40368) @ [Yisaer](https://github.com/Yisaer)
    -   スローログでクエリプラン演算子が欠落する可能性がある問題を修正しました [＃41458](https://github.com/pingcap/tidb/issues/41458) @ [time-and-fate](https://github.com/time-and-fate)
    -   仮想列を持つ TopN 演算子が誤って TiKV またはTiFlash にプッシュダウンすると、誤った結果が返される可能性がある問題を修正しました。 [＃41355](https://github.com/pingcap/tidb/issues/41355) @ [Dousir9](https://github.com/Dousir9)
    -   インデックス[＃40698](https://github.com/pingcap/tidb/issues/40698) [＃40730](https://github.com/pingcap/tidb/issues/40730) [＃41459](https://github.com/pingcap/tidb/issues/41459) を追加するときにデータの不整合が発生する問題を修正しました [＃40217](https://github.com/pingcap/tidb/issues/40217) @ [tangenta](https://github.com/tangenta) [＃40464](https://github.com/pingcap/tidb/issues/40464)
    -   インデックスを追加するときに`Pessimistic lock not found`エラーが発生する問題を修正しました [＃41515](https://github.com/pingcap/tidb/issues/41515) @ [tangenta](https://github.com/tangenta)
    -   一意インデックスを追加するときに誤って報告される重複キーエラーの問題を修正しました [＃41630](https://github.com/pingcap/tidb/issues/41630) @ [tangenta](https://github.com/tangenta)
    -   TiDB で`paging`を使用するとパフォーマンスが低下する問題を修正 [＃40741](https://github.com/pingcap/tidb/issues/40741) @ [solotzg](https://github.com/solotzg)

-   TiKV

    -   解決されたTSによりネットワークトラフィックが増加する問題を修正[＃14092](https://github.com/tikv/tikv/issues/14092) @ [overvenus](https://github.com/overvenus)
    -   悲観的DML 失敗後のDML実行中にTiDBとTiKV間のネットワーク障害によって発生するデータの不整合の問題を修正しました。 [＃14038](https://github.com/tikv/tikv/issues/14038) @ [MyonKeminta](https://github.com/MyonKeminta)
    -   `const Enum`型を他の型にキャストするときに発生するエラーを修正しました [＃14156](https://github.com/tikv/tikv/issues/14156) @ [wshwsh12](https://github.com/wshwsh12)
    -   警官タスクのページングが不正確になる問題を修正[＃14254](https://github.com/tikv/tikv/issues/14254) @ [you06](https://github.com/you06)
    -   `batch_cop`モードで`scan_detail`フィールドが不正確になる問題を修正 [＃14109](https://github.com/tikv/tikv/issues/14109) @ [you06](https://github.com/you06)
    -   Raft Engineの潜在的なエラーを修正しました。このエラーにより、TiKV がRaftデータの破損を検出し、 の再起動に失敗する可能性があります。 [＃14338](https://github.com/tikv/tikv/issues/14338) @ [tonyxuqqi](https://github.com/tonyxuqqi)

-   PD

    -   特定の条件下で実行`replace-down-peer`が遅くなる問題を修正[＃5788](https://github.com/tikv/pd/issues/5788) @ [HunDunDM](https://github.com/HunDunDM)
    -   PD が予期せず複数のラーナーをリージョンに追加する可能性がある問題を修正しました。 [＃5786](https://github.com/tikv/pd/issues/5786) @ [HunDunDM](https://github.com/HunDunDM)
    -   リージョンスキャッタタスクが予期せず冗長レプリカを生成する問題を修正[＃5909](https://github.com/tikv/pd/issues/5909) @ [HunDunDM](https://github.com/HunDunDM)
    -   `ReportMinResolvedTS`の呼び出しが頻繁に発生する PD OOM 問題を修正しました [＃5965](https://github.com/tikv/pd/issues/5965) @ [HunDunDM](https://github.com/HunDunDM)
    -   リージョン散布により、リーダーの分布が不均一になる可能性がある問題を修正しました。 [＃6017](https://github.com/tikv/pd/issues/6017) @ [HunDunDM](https://github.com/HunDunDM)

-   TiFlash

    -   直交積を計算するときにセミ結合が過剰なメモリを使用する問題を修正しました [＃6730](https://github.com/pingcap/tiflash/issues/6730) @ [gengliqi](https://github.com/gengliqi)
    -   TiFlashログ検索が遅すぎる問題を修正[＃6829](https://github.com/pingcap/tiflash/issues/6829) @ [hehechen](https://github.com/hehechen)
    -   繰り返し再起動するとファイルが誤って削除され、 TiFlash が起動できなくなる問題を修正[＃6486](https://github.com/pingcap/tiflash/issues/6486) @ [JaySon-Huang](https://github.com/JaySon-Huang)
    -   新しい列を追加した後にクエリを実行すると、 TiFlash がエラーを報告する可能性がある問題を修正しました。 [＃6726](https://github.com/pingcap/tiflash/issues/6726) @ [JaySon-Huang](https://github.com/JaySon-Huang)
    -   TiFlashがIPv6構成をサポートしない問題を修正 [＃6734](https://github.com/pingcap/tiflash/issues/6734) @ [ywqzzy](https://github.com/ywqzzy)

-   ツール

    -   Backup & Restore (BR)

        -   PDとtidb-server間の接続障害により、PITRバックアップの進行が進まない問題を修正しました。 [＃41082](https://github.com/pingcap/tidb/issues/41082) @ [YuJuncen](https://github.com/YuJuncen)
        -   PDとTiKV 間の接続障害によりTiKVがPITRタスクをリッスンできない問題を修正しました [＃14159](https://github.com/tikv/tikv/issues/14159) @ [YuJuncen](https://github.com/YuJuncen)
        -   PITRがPDクラスタの構成変更をサポートしない問題を修正 [＃14165](https://github.com/tikv/tikv/issues/14165) @ [YuJuncen](https://github.com/YuJuncen)
        -   PITR機能がCAバンドルをサポートしない問題を修正 [＃38775](https://github.com/pingcap/tidb/issues/38775) @ [3pointer](https://github.com/3pointer)
        -   PITRバックアップタスクを削除すると、残りのバックアップデータによって新しいタスク[#40403](https://github.com/pingcap/tidb/issues/40403) @ [joccau](https://github.com/joccau)でデータの不整合が発生する問題を修正しました。
        -   BRが`backupmeta`ファイルを解析するときにpanicを引き起こす問題を修正しました [＃40878](https://github.com/pingcap/tidb/issues/40878) @ [MoCuishle28](https://github.com/MoCuishle28)
        -   リージョンサイズ取得に失敗したために復元が中断される問題を修正しました [＃36053](https://github.com/pingcap/tidb/issues/36053) @ [YuJuncen](https://github.com/YuJuncen)
        -   TiDBクラスタにPITRバックアップタスクがない場合に頻度`resolve lock`が高すぎる問題を修正 [＃40759](https://github.com/pingcap/tidb/issues/40759) @ [joccau](https://github.com/joccau)
        -   ログバックアップが実行中のクラスタにデータを復元すると、ログバックアップファイルが復元できなくなる問題を修正[＃40797](https://github.com/pingcap/tidb/issues/40797) @ [Leavrth](https://github.com/Leavrth)
        -   完全バックアップの失敗後にチェックポイントからバックアップを再開しようとしたときに発生するpanicの問題を修正[＃40704](https://github.com/pingcap/tidb/issues/40704) @ [Leavrth](https://github.com/Leavrth)
        -   PITRエラーが上書きされる問題を修正 [＃40576](https://github.com/pingcap/tidb/issues/40576) @ [Leavrth](https://github.com/Leavrth)
        -   PITR バックアップ タスクで、先行所有者と GC 所有者が異なる場合にチェックポイントが進まない問題を修正しました[＃41806](https://github.com/pingcap/tidb/issues/41806) @ [joccau](https://github.com/joccau)

    -   TiCDC

        -   TiKV または TiCDC ノードスケールインまたはスケールアウトなどの特別なシナリオで、changefeed がスタックする可能性がある問題を修正しました。 [＃8174](https://github.com/pingcap/tiflow/issues/8174) @ [hicqu](https://github.com/hicqu)
        -   REDOログのストレージパスで事前チェックが実行されない問題を修正 [＃6335](https://github.com/pingcap/tiflow/issues/6335) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   S3storage障害に対して、REDO ログが許容できる期間が不十分である問題を修正しました [＃8089](https://github.com/pingcap/tiflow/issues/8089) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   `transaction-atomicity`と`protocol`構成ファイル経由で更新できない問題を修正 [＃7935](https://github.com/pingcap/tiflow/issues/7935) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   TiCDC が過度に多数のテーブルを複製するとチェックポイントが進めなくなる問題を修正しました [＃8004](https://github.com/pingcap/tiflow/issues/8004) @ [overvenus](https://github.com/overvenus)
        -   レプリケーション遅延が過度に高い場合に、REDOログを適用するとOOMが発生する可能性がある問題を修正[＃8085](https://github.com/pingcap/tiflow/issues/8085) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   REDOログがメタへの書き込みを有効にするとパフォーマンスが低下する問題を修正しました [＃8074](https://github.com/pingcap/tiflow/issues/8074) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   TiCDCが大きなトランザクションを@ [Rustin170506](https://github.com/Rustin170506)に分割せずにデータを複製するとコンテキスト期限が超過するバグを修正 [＃7982](https://github.com/pingcap/tiflow/issues/7982)
        -   PDが異常なときにチェンジフィードを一時停止すると、誤ったステータスになる問題を修正しました。 [＃8330](https://github.com/pingcap/tiflow/issues/8330) @ [sdojjy](https://github.com/sdojjy)
        -   TiDB または MySQL シンクにデータを複製するときに、主キーのない非 NULL ユニーク インデックスを持つ列に`CHARACTER SET`を指定した場合に発生するデータの不整合を修正しました。 [＃8420](https://github.com/pingcap/tiflow/issues/8420) @ [asddongmen](https://github.com/asddongmen)
        -   テーブルスケジューリングとブラックホールシンクのpanic問題を修正[＃8024](https://github.com/pingcap/tiflow/issues/8024) [＃8142](https://github.com/pingcap/tiflow/issues/8142) @ [hicqu](https://github.com/hicqu)

    -   TiDB Data Migration (DM)

        -   `binlog-schema delete`コマンドが実行に失敗する問題を修正 [＃7373](https://github.com/pingcap/tiflow/issues/7373) @ [liumengya94](https://github.com/liumengya94)
        -   最後のbinlogがスキップされたDDL の場合にチェックポイントが進まない問題を修正しました [＃8175](https://github.com/pingcap/tiflow/issues/8175) @ [D3Hunter](https://github.com/D3Hunter)
        -   1つのテーブルに「更新」と「非更新」の両方の式フィルタが指定されている場合、すべての`UPDATE`文がスキップされるバグを修正しました[＃7831](https://github.com/pingcap/tiflow/issues/7831) @ [lance6716](https://github.com/lance6716)

    -   TiDB Lightning

        -   TiDB Lightningの事前チェックで、以前に失敗したインポートによって残されたダーティデータを見つけられない問題を修正[＃39477](https://github.com/pingcap/tidb/issues/39477) @ [dsdashun](https://github.com/dsdashun)
        -   TiDB Lightningが分割領域フェーズでパニックになる問題を修正 [＃40934](https://github.com/pingcap/tidb/issues/40934) @ [lance6716](https://github.com/lance6716)
        -   競合解決ロジック（ `duplicate-resolution` ）によってチェックサムの不一致が発生する可能性がある問題を修正しました。 [＃40657](https://github.com/pingcap/tidb/issues/40657) @ [sleepymole](https://github.com/sleepymole)
        -   並列インポート中に、最後のTiDB Lightningインスタンスを除くすべてのインスタンスがローカル重複レコードに遭遇した場合に、 TiDB Lightning が競合解決を誤ってスキップする可能性がある問題を修正しました[＃40923](https://github.com/pingcap/tidb/issues/40923) @ [lichunzhu](https://github.com/lichunzhu)
        -   ローカルバックエンドモードでデータをインポートする際に、インポートされたターゲットテーブルの複合主キーに`auto_random`列があり、ソースデータでその列の値が指定されていない場合、ターゲット列が自動的にデータを生成しない問題を修正しました。 [＃41454](https://github.com/pingcap/tidb/issues/41454) @ [D3Hunter](https://github.com/D3Hunter)
