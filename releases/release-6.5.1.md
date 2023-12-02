---
title: TiDB 6.5.1 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 6.5.1.
---

# TiDB 6.5.1 リリースノート {#tidb-6-5-1-release-notes}

発売日：2023年3月10日

TiDB バージョン: 6.5.1

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [本番展開](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup) | [インストールパッケージ](https://www.pingcap.com/download/?version=v6.5.1#version-list)

## 互換性の変更 {#compatibility-changes}

-   2023 年 2 月 20 日以降、v6.5.1 を含む TiDB および TiDB ダッシュボードの新しいバージョンでは[テレメトリ機能](/telemetry.md)がデフォルトで無効になり、使用状況情報は収集されず、PingCAP と共有されません。これらのバージョンにアップグレードする前に、クラスターでデフォルトのテレメトリ構成が使用されている場合、アップグレード後にテレメトリ機能は無効になります。特定のバージョンについては[TiDB リリース タイムライン](/releases/release-timeline.md)参照してください。

    -   [`tidb_enable_telemetry`](/system-variables.md#tidb_enable_telemetry-new-in-v402)システム変数のデフォルト値が`ON`から`OFF`に変更されました。
    -   TiDB [`enable-telemetry`](/tidb-configuration-file.md#enable-telemetry-new-in-v402)構成項目のデフォルト値が`true`から`false`に変更されました。
    -   PD [`enable-telemetry`](/pd-configuration-file.md#enable-telemetry)設定項目のデフォルト値が`true`から`false`に変更されます。

-   v1.11.3 以降、新しく展開されたTiUPではテレメトリ機能がデフォルトで無効になっており、使用状況情報は収集されません。 TiUP のv1.11.3 より前のバージョンから v1.11.3 以降のバージョンにアップグレードすると、テレメトリ機能はアップグレード前と同じステータスを維持します。

-   正確性の問題が発生する可能性があるため、パーティション テーブルの列タイプの変更はサポートされなくなりました。 [#40620](https://github.com/pingcap/tidb/issues/40620) @ [むじょん](https://github.com/mjonss)

-   TiKV [`advance-ts-interval`](/tikv-configuration-file.md#advance-ts-interval)構成項目のデフォルト値が`1s`から`20s`に変更されます。この構成項目を変更して、レイテンシーを短縮し、 ステイル読み取りデータの適時性を向上させることができます。詳細は[ステイル読み取りレイテンシーを削減する](/stale-read.md#reduce-stale-read-latency)を参照してください。

## 改善点 {#improvements}

-   TiDB

    -   v6.5.1 以降、 TiDB Operator v1.4.3 以降によってデプロイされた TiDB クラスターは IPv6 アドレスをサポートします。これは、TiDB がより大きなアドレス空間をサポートし、より優れたセキュリティとネットワーク パフォーマンスを実現できることを意味します。

        -   IPv6 アドレス指定の完全サポート: TiDB は、クライアント接続、ノード間の内部通信、外部システムとの通信を含むすべてのネットワーク接続で IPv6 アドレスの使用をサポートします。
        -   デュアルスタックのサポート: まだ IPv6 に完全に切り替える準備ができていない場合は、TiDB はデュアルスタック ネットワークもサポートします。これは、同じ TiDB クラスター内で IPv4 アドレスと IPv6 アドレスの両方を使用でき、構成によって IPv6 を優先するネットワーク展開モードを選択できることを意味します。

        IPv6 展開の詳細については、 [Kubernetes 上の TiDB ドキュメント](https://docs.pingcap.com/tidb-in-kubernetes/stable/configure-a-tidb-cluster#ipv6-support)を参照してください。

    -   TiDB クラスターの初期化時に実行される SQL スクリプトの指定をサポート[#35624](https://github.com/pingcap/tidb/issues/35624) @ [モルゴ](https://github.com/morgo)

        TiDB v6.5.1 では、新しい構成項目[`initialize-sql-file`](https://docs.pingcap.com/tidb/v6.5/tidb-configuration-file#initialize-sql-file-new-in-v651)が追加されています。 TiDB クラスターを初めて起動するときは、コマンド ライン パラメーター`--initialize-sql-file`を構成することで、実行する SQL スクリプトを指定できます。この機能は、システム変数の値の変更、ユーザーの作成、権限の権限などの操作を実行する必要がある場合に使用できます。詳細については、 [ドキュメンテーション](https://docs.pingcap.com/tidb/v6.5/tidb-configuration-file#initialize-sql-file-new-in-v651)を参照してください。

    -   期限切れの領域キャッシュを定期的にクリアして、メモリリークとパフォーマンスの低下を回避します[#40461](https://github.com/pingcap/tidb/issues/40461) @ [スティックナーフ](https://github.com/sticnarf)

    -   新しい構成項目`--proxy-protocol-fallbackable`を追加して、PROXY プロトコル フォールバック モードを有効にするかどうかを制御します。このパラメータが`true`に設定されている場合、TiDB は PROXY クライアント接続および PROXY プロトコル ヘッダーなしのクライアント接続を受け入れます[#41409](https://github.com/pingcap/tidb/issues/41409) @ [ブラックティア23](https://github.com/blacktear23)

    -   Memory Tracker [#40900](https://github.com/pingcap/tidb/issues/40900) [#40500](https://github.com/pingcap/tidb/issues/40500) @ [wshwsh12](https://github.com/wshwsh12)の精度を向上させます。

    -   プラン キャッシュが有効にならない場合、システムはその理由を警告[#40210](https://github.com/pingcap/tidb/pull/40210) @ [qw4990](https://github.com/qw4990)として返します。

    -   範囲外の推定[#39008](https://github.com/pingcap/tidb/issues/39008) @ [時間と運命](https://github.com/time-and-fate)に対するオプティマイザ戦略を改善します。

-   TiKV

    -   1 コア未満の CPU での TiKV の起動をサポート[#13586](https://github.com/tikv/tikv/issues/13586) [#13752](https://github.com/tikv/tikv/issues/13752) [#14017](https://github.com/tikv/tikv/issues/14017) @ [アンドロイドデータベース](https://github.com/andreid-db)
    -   統合読み取りプール ( `readpool.unified.max-thread-count` ) のスレッド制限を CPU クォータの 10 倍に増やし、同時実行性の高いクエリの処理を改善します[#13690](https://github.com/tikv/tikv/issues/13690) @ [v01dstar](https://github.com/v01dstar)
    -   リージョン間のトラフィック[#14100](https://github.com/tikv/tikv/issues/14100) @ [オーバーヴィーナス](https://github.com/overvenus)を減らすために、デフォルト値`resolved-ts.advance-ts-interval`を`"1s"`から`"20s"`に変更します。

-   TiFlash

    -   データ量が多い場合にTiFlash の起動を大幅に高速化[#6395](https://github.com/pingcap/tiflash/issues/6395) @ [へへへん](https://github.com/hehechen)

-   ツール

    -   バックアップと復元 (BR)

        -   TiKV 側でのログ バックアップ ファイルのダウンロードの同時実行性を最適化し、通常のシナリオ[#14206](https://github.com/tikv/tikv/issues/14206) @ [ユジュンセン](https://github.com/YuJuncen)での PITR のパフォーマンスを向上させます。

    -   TiCDC

        -   プルベースのシンクを有効にしてシステム スループットを最適化[#8232](https://github.com/pingcap/tiflow/issues/8232) @ [こんにちはラスティン](https://github.com/hi-rustin)
        -   GCS 互換または Azure 互換のオブジェクトstorage[#7987](https://github.com/pingcap/tiflow/issues/7987) @ [CharlesCheung96](https://github.com/CharlesCheung96)への REDO ログの保存のサポート
        -   MQ シンクと MySQL シンクを非同期モードで実装して、シンクのスループットを向上させます[#5928](https://github.com/pingcap/tiflow/issues/5928) @ [咸陽飛](https://github.com/amyangfei) @ [CharlesCheung96](https://github.com/CharlesCheung96)

## バグの修正 {#bug-fixes}

-   TiDB

    -   ポイント取得クエリ[#39928](https://github.com/pingcap/tidb/issues/39928) @ [ジグアン](https://github.com/zyguan)で設定項目[`pessimistic-auto-commit`](/tidb-configuration-file.md#pessimistic-auto-commit-new-in-v600)が有効にならない問題を修正
    -   長いセッション接続[#40351](https://github.com/pingcap/tidb/issues/40351) @ [ウィノロス](https://github.com/winoros)で`INSERT`または`REPLACE`ステートメントがpanic可能性がある問題を修正
    -   `auto analyze`により正常なシャットダウンに時間がかかる問題を修正[#40038](https://github.com/pingcap/tidb/issues/40038) @ [シュイファングリーンアイズ](https://github.com/xuyifangreeneyes)
    -   DDL 取り込み[#40970](https://github.com/pingcap/tidb/issues/40970) @ [タンジェンタ](https://github.com/tangenta)中にデータ競合が発生する可能性がある問題を修正
    -   インデックス[#40879](https://github.com/pingcap/tidb/issues/40879) @ [タンジェンタ](https://github.com/tangenta)を追加するとデータ競合が発生する可能性がある問題を修正
    -   テーブル[#38436](https://github.com/pingcap/tidb/issues/38436) @ [タンジェンタ](https://github.com/tangenta)に多数のリージョンがある場合、無効なリージョンキャッシュによりインデックスの追加操作が非効率になる問題を修正
    -   TiDB が初期化[#40408](https://github.com/pingcap/tidb/issues/40408) @ [定義2014](https://github.com/Defined2014)中にデッドロックする可能性がある問題を修正
    -   キー範囲[#40158](https://github.com/pingcap/tidb/issues/40158) @ [ティエンチャイアマオ](https://github.com/tiancaiamao)を構築するときに TiDB が`NULL`値を適切に処理しないため、予期しないデータが読み取られる問題を修正
    -   メモリの再利用によりシステム変数の値が誤って変更される場合がある問題を修正[#40979](https://github.com/pingcap/tidb/issues/40979) @ [ルクワンチャオ](https://github.com/lcwangchao)
    -   テーブルの主キーに`ENUM`カラム[#40456](https://github.com/pingcap/tidb/issues/40456) @ [ルクワンチャオ](https://github.com/lcwangchao)が含まれる場合、TTL タスクが失敗する問題を修正します。
    -   一意のインデックス[#40592](https://github.com/pingcap/tidb/issues/40592) @ [タンジェンタ](https://github.com/tangenta)を追加するときに TiDB がパニックになる問題を修正
    -   同じテーブルを同時に切り捨てる場合、一部の切り捨て操作が MDL によってブロックされない問題を修正します[#40484](https://github.com/pingcap/tidb/issues/40484) @ [wjhuang2016](https://github.com/wjhuang2016)
    -   動的トリミング モード[#40368](https://github.com/pingcap/tidb/issues/40368) @ [イーサール](https://github.com/Yisaer)でパーティション テーブルのグローバル バインディングが作成された後、TiDB が再起動できない問題を修正します。
    -   「カーソル読み取り」メソッドを使用してデータを読み取ると、GC [#39447](https://github.com/pingcap/tidb/issues/39447) @ [ジグアン](https://github.com/zyguan)が原因でエラーが返される場合がある問題を修正
    -   `SHOW PROCESSLIST` [#41156](https://github.com/pingcap/tidb/issues/41156) @ [ヤンケオ](https://github.com/YangKeao)の結果で`EXECUTE`情報が null になる問題を修正
    -   `globalMemoryControl`がクエリを強制終了しているときに、 `KILL`操作が[#41057](https://github.com/pingcap/tidb/issues/41057) @ [wshwsh12](https://github.com/wshwsh12)で終了しない可能性がある問題を修正します。
    -   `indexMerge`でエラーが発生した後に TiDB がpanicになる可能性がある問題を修正[#41047](https://github.com/pingcap/tidb/issues/41047) [#40877](https://github.com/pingcap/tidb/issues/40877) @ [グオシャオゲ](https://github.com/guo-shaoge) @ [ウィンドトーカー](https://github.com/windtalker)
    -   `ANALYZE`ステートメントが`KILL` [#41825](https://github.com/pingcap/tidb/issues/41825) @ [徐淮嶼](https://github.com/XuHuaiyu)で終了する可能性がある問題を修正
    -   `indexMerge` [#41545](https://github.com/pingcap/tidb/issues/41545) [#41605](https://github.com/pingcap/tidb/issues/41605) @ [グオシャオゲ](https://github.com/guo-shaoge)で goroutine リークが発生する可能性がある問題を修正
    -   符号なし`TINYINT` / `SMALLINT` / `INT`の値を`0` [#41736](https://github.com/pingcap/tidb/issues/41736) @ [リトルフォール](https://github.com/LittleFall)より小さい`DECIMAL` / `FLOAT` / `DOUBLE`の値と比較するときに誤った結果が生じる可能性がある問題を修正
    -   `tidb_enable_reuse_chunk`を有効にするとメモリリーク[#40987](https://github.com/pingcap/tidb/issues/40987) @ [グオシャオゲ](https://github.com/guo-shaoge)が発生する可能性がある問題を修正
    -   タイムゾーン内のデータ競合によりデータインデックスの不整合が発生する可能性がある問題を修正[#40710](https://github.com/pingcap/tidb/issues/40710) @ [wjhuang2016](https://github.com/wjhuang2016)
    -   `batch cop`の実行時のスキャン詳細情報が不正確になる場合がある問題を修正[#41582](https://github.com/pingcap/tidb/issues/41582) @ [あなた06](https://github.com/you06)
    -   `cop`の同時実行数の上限が[#41134](https://github.com/pingcap/tidb/issues/41134) @ [あなた06](https://github.com/you06)に制限されない問題を修正
    -   `cursor read`の`statement context`誤って[#39998](https://github.com/pingcap/tidb/issues/39998) @ [ジグアン](https://github.com/zyguan)にキャッシュされる問題を修正
    -   メモリリークとパフォーマンスの低下を避けるために、古いリージョンキャッシュを定期的にクリーンアップします[#40355](https://github.com/pingcap/tidb/issues/40355) @ [スティックナーフ](https://github.com/sticnarf)
    -   `year <cmp> const`を含むクエリでプラン キャッシュを使用すると、間違った結果[#41626](https://github.com/pingcap/tidb/issues/41626) @ [qw4990](https://github.com/qw4990)が得られる可能性がある問題を修正します。
    -   広い範囲と大量のデータ変更を伴うクエリ時に大きな推定エラーが発生する問題を修正[#39593](https://github.com/pingcap/tidb/issues/39593) @ [時間と運命](https://github.com/time-and-fate)
    -   Plan Cache [#40093](https://github.com/pingcap/tidb/issues/40093) [#38205](https://github.com/pingcap/tidb/issues/38205) @ [qw4990](https://github.com/qw4990)を使用する場合、結合演算子を使用して一部の条件をプッシュダウンできない問題を修正します。
    -   IndexMerge プランが SET タイプの列[#41273](https://github.com/pingcap/tidb/issues/41273) [#41293](https://github.com/pingcap/tidb/issues/41293) @ [時間と運命](https://github.com/time-and-fate)に不正な範囲を生成する可能性がある問題を修正します。
    -   `int_col <cmp> decimal`条件[#40679](https://github.com/pingcap/tidb/issues/40679) [#41032](https://github.com/pingcap/tidb/issues/41032) @ [qw4990](https://github.com/qw4990)を処理するときにプラン キャッシュがフルスキャン プランをキャッシュする可能性がある問題を修正
    -   `int_col in (decimal...)`条件[#40224](https://github.com/pingcap/tidb/issues/40224) @ [qw4990](https://github.com/qw4990)を処理するときにプラン キャッシュがフルスキャン プランをキャッシュする可能性がある問題を修正
    -   `ignore_plan_cache`ヒントが`INSERT`ステートメント[#40079](https://github.com/pingcap/tidb/issues/40079) [#39717](https://github.com/pingcap/tidb/issues/39717) @ [qw4990](https://github.com/qw4990)に対して機能しない可能性がある問題を修正
    -   自動分析により TiDB の終了が妨げられる可能性がある問題を修正[#40038](https://github.com/pingcap/tidb/issues/40038) @ [シュイファングリーンアイズ](https://github.com/xuyifangreeneyes)
    -   パーティションテーブル[#40309](https://github.com/pingcap/tidb/issues/40309) @ [ウィノロス](https://github.com/winoros)の署名なし主キーに対して不正なアクセス間隔が構築される可能性がある問題を修正
    -   プラン キャッシュがシャッフル演算子をキャッシュし、誤った結果[#38335](https://github.com/pingcap/tidb/issues/38335) @ [qw4990](https://github.com/qw4990)を返す可能性がある問題を修正します。
    -   パーティション化されたテーブルにグローバル バインディングを作成すると、TiDB の起動に失敗する可能性がある問題を修正します[#40368](https://github.com/pingcap/tidb/issues/40368) @ [イーサール](https://github.com/Yisaer)
    -   低速ログ[#41458](https://github.com/pingcap/tidb/issues/41458) @ [時間と運命](https://github.com/time-and-fate)でクエリ プラン演算子が欠落する可能性がある問題を修正
    -   仮想列を持つ TopN オペレーターが誤って TiKV またはTiFlash [#41355](https://github.com/pingcap/tidb/issues/41355) @ [ドゥーシール9](https://github.com/Dousir9)にプッシュダウンすると、誤った結果が返される可能性がある問題を修正
    -   インデックス[#40698](https://github.com/pingcap/tidb/issues/40698) [#40730](https://github.com/pingcap/tidb/issues/40730) [#41459](https://github.com/pingcap/tidb/issues/41459) [#40464](https://github.com/pingcap/tidb/issues/40464) [#40217](https://github.com/pingcap/tidb/issues/40217) @ [タンジェンタ](https://github.com/tangenta)を追加する際のデータの不整合の問題を修正
    -   インデックス[#41515](https://github.com/pingcap/tidb/issues/41515) @ [タンジェンタ](https://github.com/tangenta)を追加するときに`Pessimistic lock not found`エラーが発生する問題を修正
    -   一意のインデックス[#41630](https://github.com/pingcap/tidb/issues/41630) @ [タンジェンタ](https://github.com/tangenta)を追加するときに重複キー エラーが誤って報告される問題を修正
    -   TiDB [#40741](https://github.com/pingcap/tidb/issues/40741) @ [ソロッツグ](https://github.com/solotzg)で`paging`を使用するとパフォーマンスが低下する問題を修正

-   TiKV

    -   解決された TS によりネットワーク トラフィックが増加する問題を修正[#14092](https://github.com/tikv/tikv/issues/14092) @ [オーバーヴィーナス](https://github.com/overvenus)
    -   悲観的DML [#14038](https://github.com/tikv/tikv/issues/14038) @ [ミョンケミンタ](https://github.com/MyonKeminta)が失敗した後の DML の実行中に、TiDB と TiKV の間のネットワーク障害によって引き起こされるデータの不整合の問題を修正しました。
    -   `const Enum`型を他の型[#14156](https://github.com/tikv/tikv/issues/14156) @ [wshwsh12](https://github.com/wshwsh12)にキャストするときに発生するエラーを修正
    -   cop タスクのページングが不正確である問題を修正[#14254](https://github.com/tikv/tikv/issues/14254) @ [あなた06](https://github.com/you06)
    -   `batch_cop`モード[#14109](https://github.com/tikv/tikv/issues/14109) @ [あなた06](https://github.com/you06)で`scan_detail`フィールドが不正確になる問題を修正
    -   TiKV がRaftデータの破損を検出し、 [#14338](https://github.com/tikv/tikv/issues/14338) @ [トニーシュクキ](https://github.com/tonyxuqqi)の再起動に失敗する可能性があるRaft Engineの潜在的なエラーを修正しました。

-   PD

    -   特定の条件下で実行`replace-down-peer`が遅くなる問題を修正[#5788](https://github.com/tikv/pd/issues/5788) @ [フンドゥンDM](https://github.com/HunDunDM)
    -   PD が予期せず複数の学習者をリージョン[#5786](https://github.com/tikv/pd/issues/5786) @ [フンドゥンDM](https://github.com/HunDunDM)に追加する可能性がある問題を修正
    -   リージョン分散タスクが予期せず冗長レプリカを生成する問題を修正します[#5909](https://github.com/tikv/pd/issues/5909) @ [フンドゥンDM](https://github.com/HunDunDM)
    -   `ReportMinResolvedTS` [#5965](https://github.com/tikv/pd/issues/5965) @ [フンドゥンDM](https://github.com/HunDunDM)の呼び出しが頻繁すぎる場合に発生する PD OOM 問題を修正します。
    -   リージョン分散によりリーダー[#6017](https://github.com/tikv/pd/issues/6017) @ [フンドゥンDM](https://github.com/HunDunDM)が不均一に分布する可能性がある問題を修正

-   TiFlash

    -   デカルト積[#6730](https://github.com/pingcap/tiflash/issues/6730) @ [ゲンリキ](https://github.com/gengliqi)を計算するときにセミ結合が過剰なメモリを使用する問題を修正
    -   TiFlashログ検索が遅すぎる問題を修正[#6829](https://github.com/pingcap/tiflash/issues/6829) @ [へへへん](https://github.com/hehechen)
    -   再起動を繰り返すと誤ってファイルが削除されてしまい、 TiFlashが起動できない問題を修正[#6486](https://github.com/pingcap/tiflash/issues/6486) @ [ジェイ・ソン・ファン](https://github.com/JaySon-Huang)
    -   新しい列[#6726](https://github.com/pingcap/tiflash/issues/6726) @ [ジェイ・ソン・ファン](https://github.com/JaySon-Huang)を追加した後にクエリを実行すると、 TiFlash がエラーを報告する可能性がある問題を修正
    -   TiFlash がIPv6 構成[#6734](https://github.com/pingcap/tiflash/issues/6734) @ [ywqzzy](https://github.com/ywqzzy)をサポートしていない問題を修正

-   ツール

    -   バックアップと復元 (BR)

        -   PD と tidb-server の間の接続障害により、PITR バックアップの進行状況が[#41082](https://github.com/pingcap/tidb/issues/41082) @ [ユジュンセン](https://github.com/YuJuncen)進まない問題を修正
        -   PD と TiKV [#14159](https://github.com/tikv/tikv/issues/14159) @ [ユジュンセン](https://github.com/YuJuncen)間の接続障害により、TiKV が PITR タスクをリッスンできない問題を修正
        -   PITR が PD クラスター[#14165](https://github.com/tikv/tikv/issues/14165) @ [ユジュンセン](https://github.com/YuJuncen)の構成変更をサポートしていない問題を修正
        -   PITR 機能が CA バンドル[#38775](https://github.com/pingcap/tidb/issues/38775) @ [3ポインター](https://github.com/3pointer)をサポートしない問題を修正
        -   PITR バックアップ タスクが削除されると、残ったバックアップ データにより新しいタスク[#40403](https://github.com/pingcap/tidb/issues/40403) @ [ジョッカウ](https://github.com/joccau)でデータの不整合が発生する問題を修正します。
        -   BR が`backupmeta`ファイル[#40878](https://github.com/pingcap/tidb/issues/40878) @ [モクイシュル28](https://github.com/MoCuishle28)を解析するときにpanicを引き起こす問題を修正します。
        -   リージョンサイズ[#36053](https://github.com/pingcap/tidb/issues/36053) @ [ユジュンセン](https://github.com/YuJuncen)の取得に失敗して復元が中断される問題を修正
        -   TiDB クラスター[#40759](https://github.com/pingcap/tidb/issues/40759) @ [ジョッカウ](https://github.com/joccau)に PITR バックアップ タスクがない場合、 `resolve lock`の頻度が高すぎる問題を修正
        -   ログ バックアップが実行されているクラスターにデータを復元すると、ログ バックアップ ファイルを復元できなくなる問題を修正します[#40797](https://github.com/pingcap/tidb/issues/40797) @ [レヴルス](https://github.com/Leavrth)
        -   完全バックアップの失敗後にチェックポイントからバックアップを再開しようとすると発生するpanicの問題を修正[#40704](https://github.com/pingcap/tidb/issues/40704) @ [レヴルス](https://github.com/Leavrth)
        -   PITR エラーが上書きされる問題を修正[#40576](https://github.com/pingcap/tidb/issues/40576) @ [レヴルス](https://github.com/Leavrth)
        -   事前所有者と gc 所有者が異なる場合、PITR バックアップ タスクでチェックポイントが進められない問題を修正[#41806](https://github.com/pingcap/tidb/issues/41806) @ [ジョッカウ](https://github.com/joccau)

    -   TiCDC

        -   TiKV または TiCDC ノード[#8174](https://github.com/pingcap/tiflow/issues/8174) @ [ひっくり返る](https://github.com/hicqu)をスケールインまたはスケールアウトするときなど、特殊なシナリオで変更フィードが停止する可能性がある問題を修正します。
        -   REDOログ[#6335](https://github.com/pingcap/tiflow/issues/6335) @ [CharlesCheung96](https://github.com/CharlesCheung96)のstorageパスで事前チェ​​ックが行われない問題を修正
        -   S3storage障害[#8089](https://github.com/pingcap/tiflow/issues/8089) @ [CharlesCheung96](https://github.com/CharlesCheung96)に対して REDO ログが許容できる期間が不十分である問題を修正
        -   設定ファイル[#7935](https://github.com/pingcap/tiflow/issues/7935) @ [CharlesCheung96](https://github.com/CharlesCheung96)から`transaction_atomicity`と`protocol`を更新できない問題を修正
        -   TiCDC が過度に多数のテーブル[#8004](https://github.com/pingcap/tiflow/issues/8004) @ [オーバーヴィーナス](https://github.com/overvenus)をレプリケートするとチェックポイントが進められない問題を修正
        -   レプリケーション ラグが過度に高い場合に REDO ログを適用すると OOM が発生する可能性がある問題を修正[#8085](https://github.com/pingcap/tiflow/issues/8085) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   REDO ログがメタ[#8074](https://github.com/pingcap/tiflow/issues/8074) @ [CharlesCheung96](https://github.com/CharlesCheung96)への書き込みを有効にするとパフォーマンスが低下する問題を修正
        -   TiCDC が大規模なトランザクション[#7982](https://github.com/pingcap/tiflow/issues/7982) @ [こんにちはラスティン](https://github.com/hi-rustin)を分割せずにデータをレプリケートするとコンテキスト期限を超過するバグを修正
        -   PD が異常なときにチェンジフィードを一時停止すると、不正なステータス[#8330](https://github.com/pingcap/tiflow/issues/8330) @ [スドジ](https://github.com/sdojjy)が発生する問題を修正
        -   TiDB または MySQL シンクにデータをレプリケートするとき、および主キー[#8420](https://github.com/pingcap/tiflow/issues/8420) @ [東門](https://github.com/asddongmen)のない非 null の一意のインデックスを持つ列に`CHARACTER SET`が指定されているときに発生するデータの不整合を修正します。
        -   テーブルのスケジューリングとブラックホール シンク[#8024](https://github.com/pingcap/tiflow/issues/8024) [#8142](https://github.com/pingcap/tiflow/issues/8142) @ [ひっくり返る](https://github.com/hicqu)のpanicの問題を修正しました。

    -   TiDB データ移行 (DM)

        -   `binlog-schema delete`コマンドの実行に失敗する問題を修正[#7373](https://github.com/pingcap/tiflow/issues/7373) @ [リウメンギャ94](https://github.com/liumengya94)
        -   最後のbinlogがスキップされた DDL [#8175](https://github.com/pingcap/tiflow/issues/8175) @ [D3ハンター](https://github.com/D3Hunter)である場合、チェックポイントが進められない問題を修正します。
        -   1つのテーブルに「更新」タイプと「非更新」タイプの両方の式フィルタを指定した場合、 `UPDATE`ステートメントがすべてスキップされるバグを修正[#7831](https://github.com/pingcap/tiflow/issues/7831) @ [ランス6716](https://github.com/lance6716)

    -   TiDB Lightning

        -   TiDB Lightning事前チェックが、以前に失敗したインポート[#39477](https://github.com/pingcap/tidb/issues/39477) @ [dsダシュン](https://github.com/dsdashun)によって残されたダーティ データを見つけられない問題を修正
        -   TiDB Lightning が分割リージョン フェーズ[#40934](https://github.com/pingcap/tidb/issues/40934) @ [ランス6716](https://github.com/lance6716)でパニックになる問題を修正
        -   競合解決ロジック ( `duplicate-resolution` ) によってチェックサムの不一致が生じる可能性がある問題を修正します[#40657](https://github.com/pingcap/tidb/issues/40657) @ [ゴズスキー](https://github.com/gozssky)
        -   並列インポート[#40923](https://github.com/pingcap/tidb/issues/40923) @ [リチュンジュ](https://github.com/lichunzhu)中に、最後の TiDB Lightning インスタンスを除くすべてのTiDB Lightningインスタンスでローカルの重複レコードが検出された場合、 TiDB Lightning が誤って競合解決をスキップする可能性がある問題を修正します。
        -   ローカル バックエンド モードでデータをインポートするときに、インポートされたターゲット テーブルの複合主キーに`auto_random`列があり、その列の値がソース データ[#41454](https://github.com/pingcap/tidb/issues/41454) @ [D3ハンター](https://github.com/D3Hunter)で指定されていない場合、ターゲット列でデータが自動的に生成されない問題を修正します。
