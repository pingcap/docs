---
title: TiDB 6.5.1 Release Notes
summary: TiDB 6.5.1 の互換性の変更、改善、バグ修正について説明します。
---

# TiDB 6.5.1 リリースノート {#tidb-6-5-1-release-notes}

発売日: 2023年3月10日

TiDB バージョン: 6.5.1

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [実稼働環境への導入](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   2023 年 2 月 20 日以降、v6.5.1 を含む TiDB および TiDB Dashboard の新しいバージョンでは[テレメトリ機能](/telemetry.md)デフォルトで無効になっており、使用状況情報は収集されず、PingCAP と共有されません。これらのバージョンにアップグレードする前に、クラスターがデフォルトのテレメトリ構成を使用している場合、アップグレード後にテレメトリ機能が無効になります。特定のバージョンについては[TiDB リリース タイムライン](/releases/release-timeline.md)を参照してください。

    -   [`tidb_enable_telemetry`](/system-variables.md#tidb_enable_telemetry-new-in-v402)システム変数のデフォルト値が`ON`から`OFF`に変更されます。
    -   TiDB [`enable-telemetry`](/tidb-configuration-file.md#enable-telemetry-new-in-v402)構成項目のデフォルト値が`true`から`false`に変更されます。
    -   PD [`enable-telemetry`](/pd-configuration-file.md#enable-telemetry)構成項目のデフォルト値が`true`から`false`に変更されます。

-   v1.11.3 以降、新しく導入されたTiUPではテレメトリ機能がデフォルトで無効になっており、使用状況情報は収集されません。v1.11.3 より前のバージョンのTiUPから v1.11.3 以降のバージョンにアップグレードした場合、テレメトリ機能はアップグレード前と同じ状態を維持します。

-   潜在的な正確性の問題のため、パーティション化されたテーブルでの列タイプの変更はサポートされなくなりました[＃40620](https://github.com/pingcap/tidb/issues/40620) @ [ミョンス](https://github.com/mjonss)

-   TiKV [`advance-ts-interval`](/tikv-configuration-file.md#advance-ts-interval)構成項目のデフォルト値が`1s`から`20s`に変更されました。この構成項目を変更して、レイテンシーを減らし、ステイル読み取りデータの適時性を向上させることができます。詳細については、 [ステイル読み取りのレイテンシーを削減](/stale-read.md#reduce-stale-read-latency)を参照してください。

## 改善点 {#improvements}

-   ティビ

    -   v6.5.1 以降、 TiDB Operator v1.4.3 以降でデプロイされた TiDB クラスターは IPv6 アドレスをサポートします。つまり、TiDB はより大きなアドレス空間をサポートし、セキュリティとネットワーク パフォーマンスを向上させることができます。

        -   IPv6 アドレス指定の完全サポート: TiDB は、クライアント接続、ノード間の内部通信、外部システムとの通信など、すべてのネットワーク接続で IPv6 アドレスの使用をサポートします。
        -   デュアル スタック サポート: IPv6 に完全に切り替える準備ができていない場合、TiDB はデュアル スタック ネットワークもサポートします。つまり、同じ TiDB クラスターで IPv4 アドレスと IPv6 アドレスの両方を使用し、構成によって IPv6 を優先するネットワーク展開モードを選択できます。

        IPv6 導入の詳細については、 [Kubernetes 上の TiDB ドキュメント](https://docs.pingcap.com/tidb-in-kubernetes/stable/configure-a-tidb-cluster#ipv6-support)参照してください。

    -   TiDB クラスタの初期化時に実行される SQL スクリプトの指定をサポート[＃35624](https://github.com/pingcap/tidb/issues/35624) @ [モルゴ](https://github.com/morgo)

        TiDB v6.5.1 では、新しい構成項目[`initialize-sql-file`](https://docs.pingcap.com/tidb/v6.5/tidb-configuration-file#initialize-sql-file-new-in-v651)が追加されました。TiDB クラスターを初めて起動するときに、コマンドライン パラメータ`--initialize-sql-file`を構成することで、実行する SQL スクリプトを指定できます。この機能は、システム変数の値の変更、ユーザーの作成、権限の付与などの操作を実行する必要がある場合に使用できます。詳細については、 [ドキュメンテーション](https://docs.pingcap.com/tidb/v6.5/tidb-configuration-file#initialize-sql-file-new-in-v651)を参照してください。

    -   メモリリークやパフォーマンスの低下を防ぐために、期限切れの領域キャッシュを定期的にクリアします[＃40461](https://github.com/pingcap/tidb/issues/40461) @ [スティクナーフ](https://github.com/sticnarf)

    -   PROXYプロトコルフォールバックモードを有効にするかどうかを制御するための新しい構成項目`--proxy-protocol-fallbackable`を追加します。このパラメータが`true`に設定されている場合、TiDBはPROXYクライアント接続とPROXYプロトコルヘッダー[＃41409](https://github.com/pingcap/tidb/issues/41409) @ [えり](https://github.com/blacktear23)のないクライアント接続を受け入れます。

    -   メモリトラッカー[#40900](https://github.com/pingcap/tidb/issues/40900) [#40500](https://github.com/pingcap/tidb/issues/40500) @ [うわー](https://github.com/wshwsh12)の精度を向上させる

    -   プランキャッシュが有効にならない場合、システムはその理由を警告として返します[#40210](https://github.com/pingcap/tidb/pull/40210) @ [qw4990](https://github.com/qw4990)

    -   範囲外推定の最適化戦略を改善する[＃39008](https://github.com/pingcap/tidb/issues/39008) @ [時間と運命](https://github.com/time-and-fate)

-   ティクヴ

    -   1コア未満のCPUでのTiKVの起動をサポート[＃13586](https://github.com/tikv/tikv/issues/13586) [＃13752](https://github.com/tikv/tikv/issues/13752) [＃14017](https://github.com/tikv/tikv/issues/14017) @ [アンドレイドDB](https://github.com/andreid-db)
    -   統合読み取りプール（ `readpool.unified.max-thread-count` ）のスレッド制限をCPUクォータの10倍に増やし、高同時実行クエリ[＃13690](https://github.com/tikv/tikv/issues/13690) @ [v01dスター](https://github.com/v01dstar)をより適切に処理します。
    -   デフォルト値`resolved-ts.advance-ts-interval`を`"1s"`から`"20s"`に変更して、リージョン間のトラフィック[＃14100](https://github.com/tikv/tikv/issues/14100) @ [金星の上](https://github.com/overvenus)を削減します。

-   TiFlash

    -   データ量が多い場合にTiFlashの起動を大幅に高速化[＃6395](https://github.com/pingcap/tiflash/issues/6395) @ [ヘヘチェン](https://github.com/hehechen)

-   ツール

    -   バックアップと復元 (BR)

        -   TiKV 側でのログ バックアップ ファイルのダウンロードの同時実行を最適化して、通常のシナリオでの PITR のパフォーマンスを向上させます[＃14206](https://github.com/tikv/tikv/issues/14206) @ [ユジュンセン](https://github.com/YuJuncen)

    -   ティCDC

        -   プルベースのシンクを有効にしてシステムスループットを最適化[＃8232](https://github.com/pingcap/tiflow/issues/8232) @ [ハイラスティン](https://github.com/hi-rustin)
        -   GCS 互換または Azure 互換のオブジェクトstorageへの REDO ログの保存をサポート[＃7987](https://github.com/pingcap/tiflow/issues/7987) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)
        -   シンクのスループットを向上させるために、非同期モードでMQシンクとMySQLシンクを実装する[＃5928](https://github.com/pingcap/tiflow/issues/5928) @ [アミヤンフェイ](https://github.com/amyangfei) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)

## バグの修正 {#bug-fixes}

-   ティビ

    -   [`pessimistic-auto-commit`](/tidb-configuration-file.md#pessimistic-auto-commit-new-in-v600)構成項目がポイント取得クエリ[＃39928](https://github.com/pingcap/tidb/issues/39928) @ [ジグアン](https://github.com/zyguan)で有効にならない問題を修正しました
    -   長いセッション接続[＃40351](https://github.com/pingcap/tidb/issues/40351) @ [ウィノロス](https://github.com/winoros)で`INSERT`または`REPLACE`ステートメントがpanicになる可能性がある問題を修正しました
    -   `auto analyze`により正常なシャットダウンに長い時間がかかる問題を修正[＃40038](https://github.com/pingcap/tidb/issues/40038) @ [翻訳者](https://github.com/xuyifangreeneyes)
    -   DDL取り込み[＃40970](https://github.com/pingcap/tidb/issues/40970) @ [タンジェンタ](https://github.com/tangenta)中にデータ競合が発生する可能性がある問題を修正
    -   インデックスを[＃40879](https://github.com/pingcap/tidb/issues/40879) @ [タンジェンタ](https://github.com/tangenta)で追加するとデータ競合が発生する可能性がある問題を修正しました
    -   テーブル[＃38436](https://github.com/pingcap/tidb/issues/38436) @ [タンジェンタ](https://github.com/tangenta)に多数のリージョンがある場合、無効なリージョンキャッシュが原因でインデックス追加操作が非効率になる問題を修正しました。
    -   初期化中に TiDB がデッドロックする可能性がある問題を修正[＃40408](https://github.com/pingcap/tidb/issues/40408) @ [定義2014](https://github.com/Defined2014)
    -   TiDB がキー範囲[＃40158](https://github.com/pingcap/tidb/issues/40158) @ [天菜まお](https://github.com/tiancaiamao)を構築するときに`NULL`値を不適切に処理するため、予期しないデータが読み取られる問題を修正しました。
    -   メモリの再利用により、システム変数の値が誤って変更される場合がある問題を修正[＃40979](https://github.com/pingcap/tidb/issues/40979) @ [lcwangchao](https://github.com/lcwangchao)
    -   テーブルの主キーに`ENUM`列[＃40456](https://github.com/pingcap/tidb/issues/40456) @ [lcwangchao](https://github.com/lcwangchao)が含まれている場合にTTLタスクが失敗する問題を修正
    -   ユニークインデックス[＃40592](https://github.com/pingcap/tidb/issues/40592) @ [タンジェンタ](https://github.com/tangenta)を追加するときに TiDB がパニックになる問題を修正
    -   同じテーブルを同時に切り捨てるときに、一部の切り捨て操作が MDL によってブロックされない問題を修正[＃40484](https://github.com/pingcap/tidb/issues/40484) @ [翻訳:](https://github.com/wjhuang2016)
    -   動的トリミングモード[＃40368](https://github.com/pingcap/tidb/issues/40368) @ [イサール](https://github.com/Yisaer)でパーティションテーブルにグローバルバインディングが作成された後に TiDB が再起動できない問題を修正しました。
    -   「カーソル読み取り」メソッドを使用してデータを読み取ると、GC [＃39447](https://github.com/pingcap/tidb/issues/39447) @ [ジグアン](https://github.com/zyguan)が原因でエラーが返される可能性がある問題を修正しました。
    -   `SHOW PROCESSLIST` [＃41156](https://github.com/pingcap/tidb/issues/41156) @ [ヤンケオ](https://github.com/YangKeao)の結果で`EXECUTE`情報が null になる問題を修正しました
    -   `globalMemoryControl`クエリを強制終了しているときに、 `KILL`操作が[＃41057](https://github.com/pingcap/tidb/issues/41057) @ [うわー](https://github.com/wshwsh12)で終了しない可能性がある問題を修正しました。
    -   `indexMerge`でエラーが発生した後に TiDB がpanicになる可能性がある問題を修正[＃41047](https://github.com/pingcap/tidb/issues/41047) [＃40877](https://github.com/pingcap/tidb/issues/40877) @ [グオシャオゲ](https://github.com/guo-shaoge) @ [風の話し手](https://github.com/windtalker)
    -   `ANALYZE`文が`KILL` [＃41825](https://github.com/pingcap/tidb/issues/41825) @ [徐淮宇](https://github.com/XuHuaiyu)で終了する可能性がある問題を修正しました
    -   `indexMerge` [＃41545](https://github.com/pingcap/tidb/issues/41545) [＃41605](https://github.com/pingcap/tidb/issues/41605) @ [グオシャオゲ](https://github.com/guo-shaoge)で goroutine リークが発生する可能性がある問題を修正
    -   符号なし`TINYINT` / `SMALLINT` / `INT`値を`0` [＃41736](https://github.com/pingcap/tidb/issues/41736) @ [リトルフォール](https://github.com/LittleFall)より小さい`DECIMAL` / `FLOAT` / `DOUBLE`の値と比較するときに誤った結果になる可能性がある問題を修正しました。
    -   `tidb_enable_reuse_chunk`有効にするとメモリリーク[＃40987](https://github.com/pingcap/tidb/issues/40987) @ [グオシャオゲ](https://github.com/guo-shaoge)が発生する可能性がある問題を修正
    -   タイムゾーンでのデータ競合によりデータインデックスの不整合が発生する可能性がある問題を修正[＃40710](https://github.com/pingcap/tidb/issues/40710) @ [翻訳:](https://github.com/wjhuang2016)
    -   `batch cop`実行中のスキャン詳細情報が不正確になる可能性がある問題を修正[＃41582](https://github.com/pingcap/tidb/issues/41582) @ [あなた06](https://github.com/you06)
    -   `cop`の上限同時実行数が[＃41134](https://github.com/pingcap/tidb/issues/41134) @ [あなた06](https://github.com/you06)に制限されない問題を修正
    -   `cursor read`の`statement context`が誤って[＃39998](https://github.com/pingcap/tidb/issues/39998) @ [ジグアン](https://github.com/zyguan)にキャッシュされる問題を修正
    -   メモリリークとパフォーマンスの低下を防ぐために、古くなったリージョンキャッシュを定期的にクリーンアップします[＃40355](https://github.com/pingcap/tidb/issues/40355) @ [スティクナーフ](https://github.com/sticnarf)
    -   `year <cmp> const`を含むクエリでプラン キャッシュを使用すると間違った結果[＃41626](https://github.com/pingcap/tidb/issues/41626) @ [qw4990](https://github.com/qw4990)が返される可能性がある問題を修正しました。
    -   大きな範囲と大量のデータ変更を伴うクエリを実行すると、推定誤差が大きくなる問題を修正[＃39593](https://github.com/pingcap/tidb/issues/39593) @ [時間と運命](https://github.com/time-and-fate)
    -   Plan Cache [＃40093](https://github.com/pingcap/tidb/issues/40093) [＃38205](https://github.com/pingcap/tidb/issues/38205) @ [qw4990](https://github.com/qw4990)の使用時に、一部の条件が Join 演算子を通じてプッシュダウンできない問題を修正しました。
    -   IndexMerge プランが SET 型列[＃41273](https://github.com/pingcap/tidb/issues/41273) [＃41293](https://github.com/pingcap/tidb/issues/41293) @ [時間と運命](https://github.com/time-and-fate)に誤った範囲を生成する可能性がある問題を修正しました
    -   `int_col <cmp> decimal`条件[＃40679](https://github.com/pingcap/tidb/issues/40679) [＃41032](https://github.com/pingcap/tidb/issues/41032) @ [qw4990](https://github.com/qw4990)を処理するときにプラン キャッシュが FullScan プランをキャッシュする可能性がある問題を修正しました
    -   `int_col in (decimal...)`条件[#40224](https://github.com/pingcap/tidb/issues/40224) @ [qw4990](https://github.com/qw4990)を処理するときにプラン キャッシュが FullScan プランをキャッシュする可能性がある問題を修正しました
    -   `ignore_plan_cache`ヒントが`INSERT`ステートメント[＃40079](https://github.com/pingcap/tidb/issues/40079) [＃39717](https://github.com/pingcap/tidb/issues/39717) @ [qw4990](https://github.com/qw4990)で機能しない可能性がある問題を修正しました
    -   自動分析により TiDB が[＃40038](https://github.com/pingcap/tidb/issues/40038) @ [翻訳者](https://github.com/xuyifangreeneyes)で終了できなくなる問題を修正
    -   パーティションテーブル[#40309](https://github.com/pingcap/tidb/issues/40309) @ [ウィノロス](https://github.com/winoros)の符号なし主キーに不正なアクセス間隔が構築される可能性がある問題を修正しました。
    -   プラン キャッシュがシャッフル演算子をキャッシュし、誤った結果を返す可能性がある問題を修正[＃38335](https://github.com/pingcap/tidb/issues/38335) @ [qw4990](https://github.com/qw4990)
    -   パーティションテーブルにグローバルバインディングを作成すると、TiDB が[＃40368](https://github.com/pingcap/tidb/issues/40368) @ [イサール](https://github.com/Yisaer)で起動に失敗する可能性がある問題を修正しました。
    -   スローログ[＃41458](https://github.com/pingcap/tidb/issues/41458) @ [時間と運命](https://github.com/time-and-fate)でクエリプラン演算子が欠落する可能性がある問題を修正しました
    -   仮想列を持つ TopN 演算子が誤って TiKV またはTiFlash [＃41355](https://github.com/pingcap/tidb/issues/41355) @ [ドゥージール9](https://github.com/Dousir9)にプッシュダウンすると、誤った結果が返される可能性がある問題を修正しました。
    -   インデックス[＃40698](https://github.com/pingcap/tidb/issues/40698) [＃40730](https://github.com/pingcap/tidb/issues/40730) [＃41459](https://github.com/pingcap/tidb/issues/41459) [＃40464](https://github.com/pingcap/tidb/issues/40464) [＃40217](https://github.com/pingcap/tidb/issues/40217) @ [タンジェンタ](https://github.com/tangenta)を追加するときにデータの不整合が発生する問題を修正
    -   インデックス[＃41515](https://github.com/pingcap/tidb/issues/41515) @ [タンジェンタ](https://github.com/tangenta)を追加するときに`Pessimistic lock not found`エラーが発生する問題を修正しました
    -   一意のインデックス[＃41630](https://github.com/pingcap/tidb/issues/41630) @ [タンジェンタ](https://github.com/tangenta)を追加するときに誤って報告される重複キー エラーの問題を修正しました
    -   TiDB [＃40741](https://github.com/pingcap/tidb/issues/40741) @ [ソロッツ](https://github.com/solotzg)で`paging`使用するとパフォーマンスが低下する問題を修正

-   ティクヴ

    -   解決されたTSによりネットワークトラフィックが増加する問題を修正[＃14092](https://github.com/tikv/tikv/issues/14092) @ [金星の上](https://github.com/overvenus)
    -   悲観的DML [＃14038](https://github.com/tikv/tikv/issues/14038) @ [ミョンケミンタ](https://github.com/MyonKeminta)が失敗した後の DML 実行中に TiDB と TiKV 間のネットワーク障害によって発生するデータ不整合の問題を修正しました。
    -   `const Enum`型を他の型[＃14156](https://github.com/tikv/tikv/issues/14156) @ [うわー](https://github.com/wshwsh12)にキャストするときに発生するエラーを修正
    -   警官タスクのページングが不正確になる問題を修正[＃14254](https://github.com/tikv/tikv/issues/14254) @ [あなた06](https://github.com/you06)
    -   `batch_cop`モード[＃14109](https://github.com/tikv/tikv/issues/14109) @ [あなた06](https://github.com/you06)で`scan_detail`フィールドが不正確になる問題を修正
    -   Raft Engineの潜在的なエラーを修正しました。このエラーにより、TiKV がRaftデータの破損を検出し、 [＃14338](https://github.com/tikv/tikv/issues/14338) @ [トニー](https://github.com/tonyxuqqi)の再起動に失敗する可能性があります。

-   PD

    -   特定の条件下で実行`replace-down-peer`遅くなる問題を修正[＃5788](https://github.com/tikv/pd/issues/5788) @ [フンドゥンDM](https://github.com/HunDunDM)
    -   PD が予期せず複数の学習者をリージョン[＃5786](https://github.com/tikv/pd/issues/5786) @ [ハンダンDM](https://github.com/HunDunDM)に追加する可能性がある問題を修正しました。
    -   リージョンスキャッタータスクが予期せず冗長レプリカを生成する問題を修正[＃5909](https://github.com/tikv/pd/issues/5909) @ [フンドゥンDM](https://github.com/HunDunDM)
    -   `ReportMinResolvedTS`の呼び出しが頻繁すぎる場合に発生する PD OOM 問題を修正[＃5965](https://github.com/tikv/pd/issues/5965) @ [フンドゥンDM](https://github.com/HunDunDM)
    -   リージョン散布によりリーダー[＃6017](https://github.com/tikv/pd/issues/6017) @ [ハンダンDM](https://github.com/HunDunDM)の分布が不均一になる可能性がある問題を修正しました。

-   TiFlash

    -   直交積[＃6730](https://github.com/pingcap/tiflash/issues/6730) @ [ゲンリキ](https://github.com/gengliqi)を計算するときにセミ結合が過剰なメモリを使用する問題を修正しました
    -   TiFlashログ検索が遅すぎる問題を修正[＃6829](https://github.com/pingcap/tiflash/issues/6829) @ [ヘヘチェン](https://github.com/hehechen)
    -   再起動を繰り返すとファイルが誤って削除され、 TiFlash が起動できない問題を修正[＃6486](https://github.com/pingcap/tiflash/issues/6486) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)
    -   新しい列[＃6726](https://github.com/pingcap/tiflash/issues/6726) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)を追加した後にクエリを実行すると、 TiFlash がエラーを報告する可能性がある問題を修正しました。
    -   TiFlashがIPv6構成[＃6734](https://github.com/pingcap/tiflash/issues/6734) @ [うわー](https://github.com/ywqzzy)をサポートしない問題を修正

-   ツール

    -   バックアップと復元 (BR)

        -   PD と tidb-server 間の接続障害により PITR バックアップの進行が[＃41082](https://github.com/pingcap/tidb/issues/41082) @ [ユジュンセン](https://github.com/YuJuncen)に進まない問題を修正しました。
        -   PDとTiKV [＃14159](https://github.com/tikv/tikv/issues/14159) @ [ユジュンセン](https://github.com/YuJuncen)間の接続障害によりTiKVがPITRタスクをリッスンできない問題を修正
        -   PITRがPDクラスタ[＃14165](https://github.com/tikv/tikv/issues/14165) @ [ユジュンセン](https://github.com/YuJuncen)の構成変更をサポートしない問題を修正
        -   PITR機能がCAバンドル[＃38775](https://github.com/pingcap/tidb/issues/38775) @ [3ポインター](https://github.com/3pointer)をサポートしない問題を修正
        -   PITR バックアップ タスクを削除すると、残りのバックアップ データによって新しいタスク[#40403](https://github.com/pingcap/tidb/issues/40403) @ [ジョッカウ](https://github.com/joccau)でデータの不整合が発生する問題を修正しました。
        -   BRが`backupmeta`ファイル[＃40878](https://github.com/pingcap/tidb/issues/40878) @ [モクイシュル28](https://github.com/MoCuishle28)を解析するときにpanicを引き起こす問題を修正
        -   リージョンサイズ[＃36053](https://github.com/pingcap/tidb/issues/36053) @ [ユジュンセン](https://github.com/YuJuncen)の取得に失敗したために復元が中断される問題を修正しました
        -   TiDB クラスター[＃40759](https://github.com/pingcap/tidb/issues/40759) @ [ジョッカウ](https://github.com/joccau)に PITR バックアップ タスクがない場合に`resolve lock`の頻度が高すぎる問題を修正
        -   ログバックアップが実行されているクラスターにデータを復元すると、ログバックアップファイルを復元できなくなる問題を修正[＃40797](https://github.com/pingcap/tidb/issues/40797) @ [リーヴルス](https://github.com/Leavrth)
        -   完全バックアップの失敗後にチェックポイントからバックアップを再開しようとしたときに発生するpanic問題を修正[＃40704](https://github.com/pingcap/tidb/issues/40704) @ [リーヴルス](https://github.com/Leavrth)
        -   PITRエラーが[＃40576](https://github.com/pingcap/tidb/issues/40576) @ [リーヴルス](https://github.com/Leavrth)で上書きされる問題を修正
        -   PITR バックアップ タスクで、先行所有者と gc 所有者が異なる場合にチェックポイントが進まない問題を修正[＃41806](https://github.com/pingcap/tidb/issues/41806) @ [ジョッカウ](https://github.com/joccau)

    -   ティCDC

        -   TiKV または TiCDC ノード[＃8174](https://github.com/pingcap/tiflow/issues/8174) @ [ヒック](https://github.com/hicqu)のスケールインまたはスケールアウトなどの特殊なシナリオで、changefeed がスタックする可能性がある問題を修正しました。
        -   REDOログ[＃6335](https://github.com/pingcap/tiflow/issues/6335) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)のstorageパスで事前チェ​​ックが実行されない問題を修正
        -   S3storage障害[＃8089](https://github.com/pingcap/tiflow/issues/8089) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)に対して REDO ログが許容できる期間が不十分である問題を修正
        -   `transaction_atomicity`と`protocol`構成ファイル[＃7935](https://github.com/pingcap/tiflow/issues/7935) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)経由で更新できない問題を修正
        -   TiCDC が過度に多くのテーブル[＃8004](https://github.com/pingcap/tiflow/issues/8004) @ [金星の上](https://github.com/overvenus)を複製するとチェックポイントが進まない問題を修正しました。
        -   レプリケーション遅延が過度に大きい場合に、REDO ログを適用すると OOM が発生する可能性がある問題を修正[＃8085](https://github.com/pingcap/tiflow/issues/8085) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)
        -   メタ[＃8074](https://github.com/pingcap/tiflow/issues/8074) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)への書き込みに REDO ログが有効になっている場合にパフォーマンスが低下する問題を修正しました。
        -   TiCDC が大規模なトランザクションを分割せずにデータを複製するとコンテキスト期限が超過するバグを修正[＃7982](https://github.com/pingcap/tiflow/issues/7982) @ [ハイラスティン](https://github.com/hi-rustin)
        -   PD が異常なときにチェンジフィードを一時停止すると、誤ったステータス[＃8330](https://github.com/pingcap/tiflow/issues/8330) @ [スドジ](https://github.com/sdojjy)になる問題を修正しました。
        -   TiDB または MySQL シンクにデータを複製するときに、主キー[＃8420](https://github.com/pingcap/tiflow/issues/8420) @ [アズドンメン](https://github.com/asddongmen)のない非 NULL ユニーク インデックスを持つ列に`CHARACTER SET`指定されている場合に発生するデータの不整合を修正します。
        -   テーブル スケジューリングとブラックホール シンクのpanic問題を修正[＃8024](https://github.com/pingcap/tiflow/issues/8024) [＃8142](https://github.com/pingcap/tiflow/issues/8142) @ [ヒック](https://github.com/hicqu)

    -   TiDB データ移行 (DM)

        -   `binlog-schema delete`コマンドが[＃7373](https://github.com/pingcap/tiflow/issues/7373) @ [りゅうめんぎゃ](https://github.com/liumengya94)の実行に失敗する問題を修正
        -   最後のbinlogがスキップされた DDL [＃8175](https://github.com/pingcap/tiflow/issues/8175) @ [D3ハンター](https://github.com/D3Hunter)の場合にチェックポイントが進まない問題を修正しました
        -   1 つのテーブルに「更新」と「非更新」の両方のタイプの式フィルターが指定されている場合、すべての`UPDATE`ステートメントがスキップされるバグを修正しました[＃7831](https://github.com/pingcap/tiflow/issues/7831) @ [ランス6716](https://github.com/lance6716)

    -   TiDB Lightning

        -   TiDB Lightning の事前チェックで、以前に失敗したインポートによって残されたダーティ データを見つけられない問題を修正[＃39477](https://github.com/pingcap/tidb/issues/39477) @ [ダシュン](https://github.com/dsdashun)
        -   TiDB Lightningが分割領域フェーズ[＃40934](https://github.com/pingcap/tidb/issues/40934) @ [ランス6716](https://github.com/lance6716)でパニックになる問題を修正
        -   競合解決ロジック（ `duplicate-resolution` ）によりチェックサム[＃40657](https://github.com/pingcap/tidb/issues/40657) @ [眠いモグラ](https://github.com/sleepymole)の不一致が発生する可能性がある問題を修正
        -   並列インポート中に最後のTiDB Lightningインスタンスを除くすべてのインスタンスでローカル重複レコードが検出された場合、 TiDB Lightning が競合解決を誤ってスキップする可能性がある問題を修正[＃40923](https://github.com/pingcap/tidb/issues/40923) @ [リチュンジュ](https://github.com/lichunzhu)
        -   ローカル バックエンド モードでデータをインポートするときに、インポートされたターゲット テーブルの複合プライマリ キーに`auto_random`列があり、ソース データ[＃41454](https://github.com/pingcap/tidb/issues/41454) @ [D3ハンター](https://github.com/D3Hunter)でその列の値が指定されていない場合、ターゲット列が自動的にデータを生成しない問題を修正しました。
