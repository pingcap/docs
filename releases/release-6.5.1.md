---
title: TiDB 6.5.1 Release Notes
summary: TiDB 6.5.1 における互換性の変更、改善、およびバグ修正について説明します。
---

# TiDB 6.5.1 リリースノート {#tidb-6-5-1-release-notes}

発売日：2023年3月10日

TiDB バージョン: 6.5.1

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   2023年2月20日以降、TiDBおよびTiDBダッシュボードの新しいバージョン（v6.5.1を含む）では、 [テレメトリ機能](/telemetry.md)デフォルトで無効化され、使用状況情報は収集されず、PingCAPと共有されません。これらのバージョンにアップグレードする前に、クラスターがデフォルトのテレメトリ設定を使用している場合、アップグレード後にテレメトリ機能が無効化されます。具体的なバージョンについては、 [TiDB リリース タイムライン](/releases/release-timeline.md)参照してください。

    -   [`tidb_enable_telemetry`](/system-variables.md#tidb_enable_telemetry-new-in-v402)システム変数のデフォルト値が`ON`から`OFF`に変更されます。
    -   TiDB [`enable-telemetry`](/tidb-configuration-file.md#enable-telemetry-new-in-v402)構成項目のデフォルト値が`true`から`false`に変更されます。
    -   PD [`enable-telemetry`](/pd-configuration-file.md#enable-telemetry)構成項目のデフォルト値が`true`から`false`に変更されます。

-   v1.11.3 以降、新規に導入されたTiUPではテレメトリ機能がデフォルトで無効化され、使用状況情報は収集されません。v1.11.3 より前のバージョンのTiUPから v1.11.3 以降のバージョンにアップグレードした場合、テレメトリ機能はアップグレード前と同じ状態を維持します。

-   潜在的な正確性の問題のため、パーティション化されたテーブルでの列タイプの変更はサポートされなくなりました[＃40620](https://github.com/pingcap/tidb/issues/40620) @ [ミョンス](https://github.com/mjonss)

-   TiKV [`advance-ts-interval`](/tikv-configuration-file.md#advance-ts-interval)設定項目のデフォルト値が`1s`から`20s`に変更されました。この設定項目を変更することで、レイテンシーを短縮し、 ステイル読み取りデータの適時性を向上させることができます。詳細は[ステイル読み取りのレイテンシーを削減](/stale-read.md#reduce-stale-read-latency)ご覧ください。

-   ネットワーク トラフィックを削減するために、TiKV [`cdc.min-ts-interval`](/tikv-configuration-file.md#min-ts-interval)構成項目の既定値が`"200ms"`から`"1s"`に変更されました。

## 改善点 {#improvements}

-   TiDB

    -   v6.5.1以降、 TiDB Operator v1.4.3以降でデプロイされたTiDBクラスタはIPv6アドレスをサポートします。これにより、TiDBはより広いアドレス空間をサポートし、セキュリティとネットワークパフォーマンスを向上させることができます。

        -   IPv6 アドレスの完全サポート: TiDB は、クライアント接続、ノード間の内部通信、外部システムとの通信など、すべてのネットワーク接続で IPv6 アドレスの使用をサポートします。
        -   デュアルスタックのサポート：まだIPv6への完全移行の準備が整っていない場合でも、TiDBはデュアルスタックネットワークをサポートしています。つまり、同じTiDBクラスタ内でIPv4とIPv6の両方のアドレスを使用し、設定によってIPv6を優先するネットワーク展開モードを選択できます。

        IPv6 の導入の詳細については、 [Kubernetes 上の TiDB ドキュメント](https://docs.pingcap.com/tidb-in-kubernetes/stable/configure-a-tidb-cluster#ipv6-support)参照してください。

    -   TiDB クラスタの初期化時に実行される SQL スクリプトの指定をサポート[＃35624](https://github.com/pingcap/tidb/issues/35624) @ [モルゴ](https://github.com/morgo)

        TiDB v6.5.1 では、新しい設定項目[`initialize-sql-file`](https://docs.pingcap.com/tidb/v6.5/tidb-configuration-file#initialize-sql-file-new-in-v651)が追加されました。TiDB クラスタを初めて起動する際に、コマンドラインパラメータ`--initialize-sql-file`を設定することで、実行する SQL スクリプトを指定できます。この機能は、システム変数の値の変更、ユーザーの作成、権限の付与などの操作を行う際に使用できます。詳細については、 [ドキュメント](https://docs.pingcap.com/tidb/v6.5/tidb-configuration-file#initialize-sql-file-new-in-v651)参照してください。

    -   メモリリークとパフォーマンスの低下を防ぐため、期限切れのリージョンキャッシュを定期的にクリアします[＃40461](https://github.com/pingcap/tidb/issues/40461) @ [スティクナーフ](https://github.com/sticnarf)

    -   PROXYプロトコルフォールバックモードを有効にするかどうかを制御する新しい設定項目`--proxy-protocol-fallbackable`を追加します。このパラメータを`true`に設定すると、TiDBはPROXYクライアント接続とPROXYプロトコルヘッダー[＃41409](https://github.com/pingcap/tidb/issues/41409) @ [ブラックティア23](https://github.com/blacktear23)のないクライアント接続を受け入れます。

    -   メモリトラッカー[＃40900](https://github.com/pingcap/tidb/issues/40900) [＃40500](https://github.com/pingcap/tidb/issues/40500) @ [wshwsh12](https://github.com/wshwsh12)の精度を向上させる

    -   プランキャッシュが有効にならない場合、システムはその理由を警告として返します[＃40210](https://github.com/pingcap/tidb/pull/40210) @ [qw4990](https://github.com/qw4990)

    -   範囲外推定の最適化戦略を改善する[＃39008](https://github.com/pingcap/tidb/issues/39008) @ [時間と運命](https://github.com/time-and-fate)

-   TiKV

    -   1コア未満のCPUでTiKVの起動をサポート[＃13586](https://github.com/tikv/tikv/issues/13586) [＃13752](https://github.com/tikv/tikv/issues/13752) [＃14017](https://github.com/tikv/tikv/issues/14017) @ [andreid-db](https://github.com/andreid-db)
    -   統合読み取りプールのスレッド制限（ `readpool.unified.max-thread-count` ）をCPUクォータの10倍に増やし、高同時実行クエリ[＃13690](https://github.com/tikv/tikv/issues/13690) @ [v01dスター](https://github.com/v01dstar)をより適切に処理します。
    -   デフォルト値の`resolved-ts.advance-ts-interval`を`"1s"`から`"20s"`に変更して、リージョン間のトラフィック[＃14100](https://github.com/tikv/tikv/issues/14100) @ [金星の上](https://github.com/overvenus)を削減します。

-   TiFlash

    -   データ量が多いときにTiFlashの起動を大幅に高速化[＃6395](https://github.com/pingcap/tiflash/issues/6395) @ [ヘヘチェン](https://github.com/hehechen)

-   ツール

    -   バックアップと復元 (BR)

        -   TiKV側でのログバックアップファイルのダウンロードの同時実行を最適化して、通常のシナリオ[＃14206](https://github.com/tikv/tikv/issues/14206) @ [ユジュンセン](https://github.com/YuJuncen)でのPITRのパフォーマンスを向上させます。

    -   TiCDC

        -   プルベースのシンクを有効にしてシステムスループットを最適化します[＃8232](https://github.com/pingcap/tiflow/issues/8232) @ [ハイラスティン](https://github.com/Rustin170506)
        -   GCS 互換または Azure 互換のオブジェクトstorage[＃7987](https://github.com/pingcap/tiflow/issues/7987) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)への REDO ログの保存をサポート
        -   シンクのスループットを向上させるために、非同期モードでMQシンクとMySQLシンクを実装します[＃5928](https://github.com/pingcap/tiflow/issues/5928) @ [アミャンフェイ](https://github.com/amyangfei) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)

## バグ修正 {#bug-fixes}

-   TiDB

    -   [`pessimistic-auto-commit`](/tidb-configuration-file.md#pessimistic-auto-commit-new-in-v600)構成項目がポイント取得クエリ[＃39928](https://github.com/pingcap/tidb/issues/39928) @ [ジグアン](https://github.com/zyguan)で有効にならない問題を修正しました
    -   長いセッション接続[＃40351](https://github.com/pingcap/tidb/issues/40351) @ [ウィノロス](https://github.com/winoros)で`INSERT`または`REPLACE`ステートメントがpanic可能性がある問題を修正しました
    -   `auto analyze`正常なシャットダウンに長い時間がかかる問題を修正[＃40038](https://github.com/pingcap/tidb/issues/40038) @ [xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    -   DDL取り込み[＃40970](https://github.com/pingcap/tidb/issues/40970) @ [接線](https://github.com/tangenta)中にデータ競合が発生する可能性がある問題を修正
    -   インデックスを[＃40879](https://github.com/pingcap/tidb/issues/40879) @ [接線](https://github.com/tangenta)で追加するとデータ競合が発生する可能性がある問題を修正しました
    -   テーブル[＃38436](https://github.com/pingcap/tidb/issues/38436) @ [接線](https://github.com/tangenta)に多数のリージョンがある場合に無効なリージョンキャッシュが原因でインデックスの追加操作が非効率になる問題を修正しました。
    -   初期化中にTiDBがデッドロックする可能性がある問題を修正[＃40408](https://github.com/pingcap/tidb/issues/40408) @ [定義2014](https://github.com/Defined2014)
    -   TiDB がキー範囲[＃40158](https://github.com/pingcap/tidb/issues/40158) @ [天菜まお](https://github.com/tiancaiamao)を構築するときに`NULL`値を不適切に処理するため、予期しないデータが読み取られる問題を修正しました。
    -   メモリの再利用により、システム変数の値が誤って変更される可能性がある問題を修正[＃40979](https://github.com/pingcap/tidb/issues/40979) @ [lcwangchao](https://github.com/lcwangchao)
    -   テーブルの主キーに`ENUM`列[＃40456](https://github.com/pingcap/tidb/issues/40456) @ [lcwangchao](https://github.com/lcwangchao)が含まれている場合にTTLタスクが失敗する問題を修正しました
    -   ユニークインデックス[＃40592](https://github.com/pingcap/tidb/issues/40592) @ [接線](https://github.com/tangenta)を追加するときに TiDB がパニックを起こす問題を修正しました
    -   同じテーブルを同時に切り捨てるときに、一部の切り捨て操作が MDL によってブロックされない問題を修正[＃40484](https://github.com/pingcap/tidb/issues/40484) @ [wjhuang2016](https://github.com/wjhuang2016)
    -   動的トリミングモード[＃40368](https://github.com/pingcap/tidb/issues/40368) @ [イーサール](https://github.com/Yisaer)でパーティションテーブルにグローバルバインディングが作成された後にTiDBが再起動できない問題を修正しました
    -   「カーソル読み取り」メソッドを使用してデータを読み取ると、GC [＃39447](https://github.com/pingcap/tidb/issues/39447) @ [ジグアン](https://github.com/zyguan)のためにエラーが返される可能性がある問題を修正しました。
    -   `SHOW PROCESSLIST` [＃41156](https://github.com/pingcap/tidb/issues/41156) @ [ヤンケオ](https://github.com/YangKeao)の結果で`EXECUTE`情報が null になる問題を修正しました
    -   `globalMemoryControl`クエリを強制終了しているときに、 `KILL`操作が[＃41057](https://github.com/pingcap/tidb/issues/41057) @ [wshwsh12](https://github.com/wshwsh12)で終了しない可能性がある問題を修正しました
    -   `indexMerge`エラーに遭遇した後に TiDB がpanic可能性がある問題を修正[＃41047](https://github.com/pingcap/tidb/issues/41047) [＃40877](https://github.com/pingcap/tidb/issues/40877) @ [グオシャオゲ](https://github.com/guo-shaoge) @ [ウィンドトーカー](https://github.com/windtalker)
    -   `ANALYZE`文が`KILL` [＃41825](https://github.com/pingcap/tidb/issues/41825) @ [徐淮嶼](https://github.com/XuHuaiyu)で終了する可能性がある問題を修正しました
    -   `indexMerge` [＃41545](https://github.com/pingcap/tidb/issues/41545) [＃41605](https://github.com/pingcap/tidb/issues/41605) @ [グオシャオゲ](https://github.com/guo-shaoge)で goroutine リークが発生する可能性がある問題を修正しました
    -   符号なしの`TINYINT` / `SMALLINT` / `INT`値を`0` [＃41736](https://github.com/pingcap/tidb/issues/41736) @ [リトルフォール](https://github.com/LittleFall)より小さい`DECIMAL` / `FLOAT` / `DOUBLE`値と比較するときに誤った結果になる可能性がある問題を修正しました。
    -   `tidb_enable_reuse_chunk`有効にするとメモリリーク[＃40987](https://github.com/pingcap/tidb/issues/40987) @ [グオシャオゲ](https://github.com/guo-shaoge)が発生する可能性がある問題を修正
    -   タイムゾーンでのデータ競合によりデータインデックスの不整合が発生する可能性がある問題を修正[＃40710](https://github.com/pingcap/tidb/issues/40710) @ [wjhuang2016](https://github.com/wjhuang2016)
    -   `batch cop`実行中のスキャン詳細情報が不正確になる可能性がある問題を修正[＃41582](https://github.com/pingcap/tidb/issues/41582) @ [あなた06](https://github.com/you06)
    -   `cop`の上限同時実行数が[＃41134](https://github.com/pingcap/tidb/issues/41134) @ [あなた06](https://github.com/you06)に制限されない問題を修正
    -   `cursor read`分の`statement context`が誤って[＃39998](https://github.com/pingcap/tidb/issues/39998) @ [ジグアン](https://github.com/zyguan)キャッシュされる問題を修正
    -   メモリリークとパフォーマンスの低下を防ぐため、古くなったリージョンキャッシュを定期的にクリーンアップします[＃40355](https://github.com/pingcap/tidb/issues/40355) @ [スティクナーフ](https://github.com/sticnarf)
    -   `year <cmp> const`含むクエリでプラン キャッシュを使用すると間違った結果[＃41626](https://github.com/pingcap/tidb/issues/41626) @ [qw4990](https://github.com/qw4990)が返される可能性がある問題を修正しました
    -   大きな範囲と大量のデータ変更を伴うクエリを実行するときに大きな推定エラーが発生する問題を修正[＃39593](https://github.com/pingcap/tidb/issues/39593) @ [時間と運命](https://github.com/time-and-fate)
    -   Plan Cache [＃40093](https://github.com/pingcap/tidb/issues/40093) [＃38205](https://github.com/pingcap/tidb/issues/38205) @ [qw4990](https://github.com/qw4990)の使用時に、一部の条件が Join 演算子を通じてプッシュダウンできない問題を修正しました。
    -   IndexMerge プランが SET 型の列[＃41273](https://github.com/pingcap/tidb/issues/41273) [＃41293](https://github.com/pingcap/tidb/issues/41293) @ [時間と運命](https://github.com/time-and-fate)に誤った範囲を生成する可能性がある問題を修正しました
    -   プランキャッシュが`int_col <cmp> decimal`条件[＃40679](https://github.com/pingcap/tidb/issues/40679) [＃41032](https://github.com/pingcap/tidb/issues/41032) @ [qw4990](https://github.com/qw4990)を処理するときにフルスキャン プランをキャッシュする可能性がある問題を修正しました
    -   プランキャッシュが`int_col in (decimal...)`条件[＃40224](https://github.com/pingcap/tidb/issues/40224) @ [qw4990](https://github.com/qw4990)を処理するときにフルスキャン プランをキャッシュする可能性がある問題を修正しました
    -   `ignore_plan_cache`ヒントが`INSERT`ステートメント[＃40079](https://github.com/pingcap/tidb/issues/40079) [＃39717](https://github.com/pingcap/tidb/issues/39717) @ [qw4990](https://github.com/qw4990)では機能しない可能性がある問題を修正しました
    -   自動分析により TiDB が[＃40038](https://github.com/pingcap/tidb/issues/40038) @ [xuyifangreeneyes](https://github.com/xuyifangreeneyes)で終了できなくなる問題を修正しました
    -   パーティションテーブル[＃40309](https://github.com/pingcap/tidb/issues/40309) @ [ウィノロス](https://github.com/winoros)の符号なし主キーに不正なアクセス間隔が構築される可能性がある問題を修正しました。
    -   プランキャッシュがシャッフル演算子をキャッシュし、誤った結果を返す可能性がある問題を修正[＃38335](https://github.com/pingcap/tidb/issues/38335) @ [qw4990](https://github.com/qw4990)
    -   パーティションテーブルにグローバルバインディングを作成すると、TiDB が[＃40368](https://github.com/pingcap/tidb/issues/40368) @ [イーサール](https://github.com/Yisaer)で起動に失敗する可能性がある問題を修正しました。
    -   スローログ[＃41458](https://github.com/pingcap/tidb/issues/41458) @ [時間と運命](https://github.com/time-and-fate)でクエリプラン演算子が欠落する可能性がある問題を修正しました
    -   仮想列を持つ TopN 演算子が誤って TiKV またはTiFlash [＃41355](https://github.com/pingcap/tidb/issues/41355) @ [ドゥーシル9](https://github.com/Dousir9)にプッシュダウンすると、誤った結果が返される可能性がある問題を修正しました。
    -   インデックス[＃40698](https://github.com/pingcap/tidb/issues/40698) [＃40730](https://github.com/pingcap/tidb/issues/40730) [＃41459](https://github.com/pingcap/tidb/issues/41459) [＃40464](https://github.com/pingcap/tidb/issues/40464) [＃40217](https://github.com/pingcap/tidb/issues/40217) @ [接線](https://github.com/tangenta)を追加するときにデータの不整合が発生する問題を修正しました
    -   インデックス[＃41515](https://github.com/pingcap/tidb/issues/41515) @ [接線](https://github.com/tangenta)を追加するときに`Pessimistic lock not found`エラーが発生する問題を修正しました
    -   ユニークインデックス[＃41630](https://github.com/pingcap/tidb/issues/41630) @ [接線](https://github.com/tangenta)を追加するときに誤って報告される重複キーエラーの問題を修正しました
    -   TiDB [＃40741](https://github.com/pingcap/tidb/issues/40741) @ [ソロツグ](https://github.com/solotzg)で`paging`使用するとパフォーマンスが低下する問題を修正

-   TiKV

    -   解決されたTSによりネットワークトラフィックが増加する問題を修正[＃14092](https://github.com/tikv/tikv/issues/14092) @ [金星の上](https://github.com/overvenus)
    -   悲観的DML [＃14038](https://github.com/tikv/tikv/issues/14038) @ [ミョンケミンタ](https://github.com/MyonKeminta)失敗後のDML実行中にTiDBとTiKV間のネットワーク障害によって発生するデータの不整合の問題を修正しました。
    -   `const Enum`型を他の型[＃14156](https://github.com/tikv/tikv/issues/14156) @ [wshwsh12](https://github.com/wshwsh12)にキャストするときに発生するエラーを修正しました
    -   警官タスクのページングが不正確になる問題を修正[＃14254](https://github.com/tikv/tikv/issues/14254) @ [あなた06](https://github.com/you06)
    -   `batch_cop`モード[＃14109](https://github.com/tikv/tikv/issues/14109) @ [あなた06](https://github.com/you06)で`scan_detail`フィールドが不正確になる問題を修正
    -   Raft Engineの潜在的なエラーを修正しました。このエラーにより、TiKV がRaftデータの破損を検出し、 [＃14338](https://github.com/tikv/tikv/issues/14338) @ [トニー・シュッキ](https://github.com/tonyxuqqi)の再起動に失敗する可能性があります。

-   PD

    -   特定の条件下で実行`replace-down-peer`が遅くなる問題を修正[＃5788](https://github.com/tikv/pd/issues/5788) @ [フンドゥンDM](https://github.com/HunDunDM)
    -   PD が予期せず複数の学習者をリージョン[＃5786](https://github.com/tikv/pd/issues/5786) @ [ハンドゥンDM](https://github.com/HunDunDM)に追加する可能性がある問題を修正しました。
    -   リージョンスキャッタタスクが予期せず冗長レプリカを生成する問題を修正[＃5909](https://github.com/tikv/pd/issues/5909) @ [フンドゥンDM](https://github.com/HunDunDM)
    -   `ReportMinResolvedTS`の呼び出しが[＃5965](https://github.com/tikv/pd/issues/5965) @ [フンドゥンDM](https://github.com/HunDunDM)で頻繁に発生する PD OOM 問題を修正しました
    -   リージョン散布により、リーダー[＃6017](https://github.com/tikv/pd/issues/6017) @ [ハンドゥンDM](https://github.com/HunDunDM)の分布が不均一になる可能性がある問題を修正しました。

-   TiFlash

    -   直交積[＃6730](https://github.com/pingcap/tiflash/issues/6730) @ [ゲンリキ](https://github.com/gengliqi)を計算するときにセミ結合が過剰なメモリを使用する問題を修正しました
    -   TiFlashログ検索が遅すぎる問題を修正[＃6829](https://github.com/pingcap/tiflash/issues/6829) @ [ヘヘチェン](https://github.com/hehechen)
    -   繰り返し再起動するとファイルが誤って削除され、 TiFlash が起動できなくなる問題を修正[＃6486](https://github.com/pingcap/tiflash/issues/6486) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)
    -   新しい列[＃6726](https://github.com/pingcap/tiflash/issues/6726) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)を追加した後にクエリを実行すると、 TiFlash がエラーを報告する可能性がある問題を修正しました。
    -   TiFlashがIPv6構成[＃6734](https://github.com/pingcap/tiflash/issues/6734) @ [ywqzzy](https://github.com/ywqzzy)をサポートしない問題を修正

-   ツール

    -   バックアップと復元 (BR)

        -   PDとtidb-server間の接続障害により、PITRバックアップの進行が[＃41082](https://github.com/pingcap/tidb/issues/41082) @ [ユジュンセン](https://github.com/YuJuncen)に進まない問題を修正しました。
        -   PDとTiKV [＃14159](https://github.com/tikv/tikv/issues/14159) @ [ユジュンセン](https://github.com/YuJuncen)間の接続障害によりTiKVがPITRタスクをリッスンできない問題を修正しました
        -   PITRがPDクラスタ[＃14165](https://github.com/tikv/tikv/issues/14165) @ [ユジュンセン](https://github.com/YuJuncen)の構成変更をサポートしない問題を修正
        -   PITR機能がCAバンドル[＃38775](https://github.com/pingcap/tidb/issues/38775) @ [3ポイントシュート](https://github.com/3pointer)をサポートしない問題を修正
        -   PITRバックアップタスクを削除すると、残りのバックアップデータによって新しいタスク[#40403](https://github.com/pingcap/tidb/issues/40403) @ [ジョッカウ](https://github.com/joccau)でデータの不整合が発生する問題を修正しました。
        -   BRが`backupmeta`ファイル[＃40878](https://github.com/pingcap/tidb/issues/40878) @ [モクイシュル28](https://github.com/MoCuishle28)を解析するときにpanicを引き起こす問題を修正しました
        -   リージョンサイズ[＃36053](https://github.com/pingcap/tidb/issues/36053) @ [ユジュンセン](https://github.com/YuJuncen)取得に失敗したために復元が中断される問題を修正しました
        -   TiDBクラスタ[＃40759](https://github.com/pingcap/tidb/issues/40759) @ [ジョッカウ](https://github.com/joccau)にPITRバックアップタスクがない場合に頻度`resolve lock`が高すぎる問題を修正
        -   ログバックアップが実行中のクラスタにデータを復元すると、ログバックアップファイルが復元できなくなる問題を修正[＃40797](https://github.com/pingcap/tidb/issues/40797) @ [リーヴルス](https://github.com/Leavrth)
        -   完全バックアップの失敗後にチェックポイントからバックアップを再開しようとしたときに発生するpanicの問題を修正[＃40704](https://github.com/pingcap/tidb/issues/40704) @ [リーヴルス](https://github.com/Leavrth)
        -   PITRエラーが[＃40576](https://github.com/pingcap/tidb/issues/40576) @ [リーヴルス](https://github.com/Leavrth)で上書きされる問題を修正
        -   PITR バックアップ タスクで、先行所有者と GC 所有者が異なる場合にチェックポイントが進まない問題を修正しました[＃41806](https://github.com/pingcap/tidb/issues/41806) @ [ジョッカウ](https://github.com/joccau)

    -   TiCDC

        -   TiKV または TiCDC ノード[＃8174](https://github.com/pingcap/tiflow/issues/8174) @ [ヒック](https://github.com/hicqu)スケールインまたはスケールアウトなどの特別なシナリオで、changefeed がスタックする可能性がある問題を修正しました。
        -   REDOログ[＃6335](https://github.com/pingcap/tiflow/issues/6335) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)のstorageパスで事前チェックが実行されない問題を修正
        -   S3storage障害[＃8089](https://github.com/pingcap/tiflow/issues/8089) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)に対して、REDO ログが許容できる期間が不十分である問題を修正しました
        -   `transaction-atomicity`と`protocol`構成ファイル[＃7935](https://github.com/pingcap/tiflow/issues/7935) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)経由で更新できない問題を修正
        -   TiCDC が過度に多数のテーブル[＃8004](https://github.com/pingcap/tiflow/issues/8004) @ [金星の上](https://github.com/overvenus)を複製するとチェックポイントが進めなくなる問題を修正しました
        -   レプリケーション遅延が過度に高い場合に、REDOログを適用するとOOMが発生する可能性がある問題を修正[＃8085](https://github.com/pingcap/tiflow/issues/8085) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)
        -   REDOログがメタ[＃8074](https://github.com/pingcap/tiflow/issues/8074) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)への書き込みを有効にするとパフォーマンスが低下する問題を修正しました
        -   TiCDCが大きなトランザクション[＃7982](https://github.com/pingcap/tiflow/issues/7982)を[ハイラスティン](https://github.com/Rustin170506)に分割せずにデータを複製するとコンテキスト期限が超過するバグを修正
        -   PDが異常なときにチェンジフィードを一時停止すると、誤ったステータス[＃8330](https://github.com/pingcap/tiflow/issues/8330) @ [スドジ](https://github.com/sdojjy)になる問題を修正しました。
        -   TiDB または MySQL シンクにデータを複製するときに、主キー[＃8420](https://github.com/pingcap/tiflow/issues/8420) @ [アズドンメン](https://github.com/asddongmen)のない非 NULL ユニーク インデックスを持つ列に`CHARACTER SET`指定した場合に発生するデータの不整合を修正しました。
        -   テーブルスケジューリングとブラックホールシンクのpanic問題を修正[＃8024](https://github.com/pingcap/tiflow/issues/8024) [＃8142](https://github.com/pingcap/tiflow/issues/8142) @ [ヒック](https://github.com/hicqu)

    -   TiDB データ移行 (DM)

        -   `binlog-schema delete`コマンドが[＃7373](https://github.com/pingcap/tiflow/issues/7373) @ [liumengya94](https://github.com/liumengya94)実行に失敗する問題を修正
        -   最後のbinlogがスキップされたDDL [＃8175](https://github.com/pingcap/tiflow/issues/8175) @ [D3ハンター](https://github.com/D3Hunter)の場合にチェックポイントが進まない問題を修正しました
        -   1つのテーブルに「更新」と「非更新」の両方の式フィルタが指定されている場合、すべての`UPDATE`文がスキップされるバグを修正しました[＃7831](https://github.com/pingcap/tiflow/issues/7831) @ [ランス6716](https://github.com/lance6716)

    -   TiDB Lightning

        -   TiDB Lightningの事前チェックで、以前に失敗したインポートによって残されたダーティデータを見つけられない問題を修正[＃39477](https://github.com/pingcap/tidb/issues/39477) @ [dsdashun](https://github.com/dsdashun)
        -   TiDB Lightningが分割領域フェーズ[＃40934](https://github.com/pingcap/tidb/issues/40934) @ [ランス6716](https://github.com/lance6716)でパニックになる問題を修正
        -   競合解決ロジック（ `duplicate-resolution` ）によってチェックサム[＃40657](https://github.com/pingcap/tidb/issues/40657) @ [眠そうなモグラ](https://github.com/sleepymole)の不一致が発生する可能性がある問題を修正しました。
        -   並列インポート中に、最後のTiDB Lightningインスタンスを除くすべてのインスタンスがローカル重複レコードに遭遇した場合に、 TiDB Lightning が競合解決を誤ってスキップする可能性がある問題を修正しました[＃40923](https://github.com/pingcap/tidb/issues/40923) @ [リチュンジュ](https://github.com/lichunzhu)
        -   ローカルバックエンドモードでデータをインポートする際に、インポートされたターゲットテーブルの複合主キーに`auto_random`列があり、ソースデータ[＃41454](https://github.com/pingcap/tidb/issues/41454) @ [D3ハンター](https://github.com/D3Hunter)でその列の値が指定されていない場合、ターゲット列が自動的にデータを生成しない問題を修正しました。
