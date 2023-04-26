---
title: TiDB 6.5.1 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 6.5.1.
---

# TiDB 6.5.1 リリースノート {#tidb-6-5-1-release-notes}

発売日：2023年3月10日

TiDB バージョン: 6.5.1

クイック アクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [本番展開](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup) | [インストール パッケージ](https://www.pingcap.com/download/?version=v6.5.1#version-list)

## 互換性の変更 {#compatibility-changes}

-   2023 年 2 月 20 日以降、v6.5.1 を含む新しいバージョンの TiDB および TiDB ダッシュボードでは[テレメトリ機能](/telemetry.md)がデフォルトで無効になり、使用状況に関する情報は収集されず、PingCAP と共有されません。これらのバージョンにアップグレードする前に、クラスタがデフォルトのテレメトリ構成を使用している場合、アップグレード後にテレメトリ機能が無効になります。特定のバージョンについては、 [TiDB リリースのタイムライン](/releases/release-timeline.md)参照してください。

    -   [`tidb_enable_telemetry`](/system-variables.md#tidb_enable_telemetry-new-in-v402)システム変数のデフォルト値が`ON`から`OFF`に変更されました。
    -   TiDB [`enable-telemetry`](/tidb-configuration-file.md#enable-telemetry-new-in-v402)構成項目のデフォルト値が`true`から`false`に変更されました。
    -   PD [`enable-telemetry`](/pd-configuration-file.md#enable-telemetry)構成アイテムのデフォルト値が`true`から`false`に変更されました。

-   v1.11.3 以降、新たに展開されたTiUPではテレメトリ機能がデフォルトで無効になり、使用状況情報は収集されません。 v1.11.3 より前のTiUPバージョンから v1.11.3 以降のバージョンにアップグレードした場合、テレメトリ機能はアップグレード前と同じ状態を維持します。

-   正確性の問題が発生する可能性があるため、分割されたテーブルの列の種類の変更はサポートされなくなりました。 [#40620](https://github.com/pingcap/tidb/issues/40620) @ [ミヨンス](https://github.com/mjonss)

-   TiKV [`advance-ts-interval`](/tikv-configuration-file.md#advance-ts-interval)構成項目のデフォルト値が`1s`から`20s`に変更されました。この構成項目を変更して、レイテンシーを短縮し、ステイル読み取りデータの適時性を向上させることができます。詳細は[ステイル読み取りのレイテンシーを減らす](/stale-read.md#reduce-stale-read-latency)を参照してください。

## 改良点 {#improvements}

-   TiDB

    -   v6.5.1 以降、 TiDB Operator v1.4.3 以降でデプロイされた TiDB クラスターは IPv6 アドレスをサポートします。これは、TiDB がより大きなアドレス空間をサポートし、より優れたセキュリティとネットワーク パフォーマンスをもたらすことを意味します。

        -   IPv6 アドレッシングの完全サポート: TiDB は、クライアント接続、ノード間の内部通信、および外部システムとの通信を含む、すべてのネットワーク接続で IPv6 アドレスの使用をサポートします。
        -   デュアルスタックのサポート: まだ IPv6 に完全に切り替える準備ができていない場合、TiDB はデュアルスタック ネットワークもサポートします。これは、同じ TiDB クラスターで IPv4 と IPv6 の両方のアドレスを使用し、構成によって IPv6 を優先するネットワーク展開モードを選択できることを意味します。

        IPv6 展開の詳細については、 [Kubernetes ドキュメント上の TiDB](https://docs.pingcap.com/tidb-in-kubernetes/stable/configure-a-tidb-cluster#ipv6-support)を参照してください。

    -   TiDB クラスタの初期化時に実行する SQL スクリプトの指定をサポート[#35624](https://github.com/pingcap/tidb/issues/35624) @ [モルゴ](https://github.com/morgo)

        TiDB v6.5.1 は、新しい構成項目[`initialize-sql-file`](https://docs.pingcap.com/tidb/v6.5/tidb-configuration-file#initialize-sql-file-new-in-v651)を追加します。初めて TiDB クラスターを起動するときに、コマンド ライン パラメーター`--initialize-sql-file`を構成することで、実行する SQL スクリプトを指定できます。システム変数の値の変更、ユーザーの作成、権限などの操作を実行する必要がある場合に、この機能を使用できます。詳細については、 [ドキュメンテーション](https://docs.pingcap.com/tidb/v6.5/tidb-configuration-file#initialize-sql-file-new-in-v651)を参照してください。

    -   有効期限が切れたリージョン キャッシュを定期的にクリアして、メモリリークとパフォーマンスの低下を回避します[#40461](https://github.com/pingcap/tidb/issues/40461) @ [スティックナーフ](https://github.com/sticnarf)

    -   PROXY プロトコル フォールバック モードを有効にするかどうかを制御する新しい構成項目`--proxy-protocol-fallbackable`を追加します。このパラメーターが`true`に設定されている場合、TiDB は PROXY クライアント接続と、PROXY プロトコル ヘッダー[#41409](https://github.com/pingcap/tidb/issues/41409) @ [ブラックティア23](https://github.com/blacktear23)なしのクライアント接続を受け入れます。

    -   メモリートラッカーの精度を向上させる[#40900](https://github.com/pingcap/tidb/issues/40900) [#40500](https://github.com/pingcap/tidb/issues/40500) @ [wshwsh12](https://github.com/wshwsh12)

    -   プラン キャッシュが有効にならない場合、システムはその理由を警告[#40210](https://github.com/pingcap/tidb/pull/40210) @ [qw4990](https://github.com/qw4990)として返します。

    -   範囲外の推定[#39008](https://github.com/pingcap/tidb/issues/39008) @ [時間と運命](https://github.com/time-and-fate)のオプティマイザー戦略を改善する

-   TiKV

    -   コア数が 1 未満の CPU での TiKV の起動をサポート[#13586](https://github.com/tikv/tikv/issues/13586) [#13752](https://github.com/tikv/tikv/issues/13752) [#14017](https://github.com/tikv/tikv/issues/14017) @ [アンドレイドデータベース](https://github.com/andreid-db)
    -   統合読み取りプール ( `readpool.unified.max-thread-count` ) のスレッド制限を CPU クォータの 10 倍に増やして、同時実行性の高いクエリ[#13690](https://github.com/tikv/tikv/issues/13690) @ [v01dstar](https://github.com/v01dstar)をより適切に処理します。
    -   デフォルト値の`resolved-ts.advance-ts-interval` `"1s"`から`"20s"`に変更して、クロスリージョン トラフィック[#14100](https://github.com/tikv/tikv/issues/14100) @ [大静脈](https://github.com/overvenus)を減らします

-   TiFlash

    -   データ量が多い場合にTiFlashの起動を大幅に高速化[#6395](https://github.com/pingcap/tiflash/issues/6395) @ [へへへん](https://github.com/hehechen)

-   ツール

    -   バックアップと復元 (BR)

        -   TiKV 側でのログ バックアップ ファイルのダウンロードの同時実行性を最適化して、通常のシナリオで PITR のパフォーマンスを向上させます[#14206](https://github.com/tikv/tikv/issues/14206) @ [ユジュンセン](https://github.com/YuJuncen)

    -   TiCDC

        -   プルベースのシンクを有効にして、システムのスループットを最適化します[#8232](https://github.com/pingcap/tiflow/issues/8232) @ [ハイラスチン](https://github.com/hi-rustin)
        -   GCS 互換または Azure 互換のオブジェクトstorageへの REDO ログの保存をサポート[#7987](https://github.com/pingcap/tiflow/issues/7987) @ [チャールズ・チャン96](https://github.com/CharlesCheung96)
        -   MQ シンクと MySQL シンクを非同期モードで実装して、シンクのスループットを向上させる[#5928](https://github.com/pingcap/tiflow/issues/5928) @ [アミヤンフェイ](https://github.com/amyangfei) @ [チャールズ・チャン96](https://github.com/CharlesCheung96)

## バグの修正 {#bug-fixes}

-   TiDB

    -   ポイント取得クエリ[#39928](https://github.com/pingcap/tidb/issues/39928) @ [ジグアン](https://github.com/zyguan)で[`pessimistic-auto-commit`](/tidb-configuration-file.md#pessimistic-auto-commit-new-in-v600)構成アイテムが有効にならない問題を修正
    -   `INSERT`つまたは`REPLACE`のステートメントが長いセッション接続でpanicになる可能性がある問題を修正します[#40351](https://github.com/pingcap/tidb/issues/40351) @ [ウィノロス](https://github.com/winoros)
    -   `auto analyze`で正常なシャットダウンに時間がかかる問題を修正[#40038](https://github.com/pingcap/tidb/issues/40038) @ [しゅいふぁんグリーンアイズ](https://github.com/xuyifangreeneyes)
    -   DDL インジェスト[#40970](https://github.com/pingcap/tidb/issues/40970) @ [接線](https://github.com/tangenta)中にデータ競合が発生する可能性がある問題を修正
    -   インデックスを[#40879](https://github.com/pingcap/tidb/issues/40879) @ [接線](https://github.com/tangenta)追加するとデータ競合が発生する可能性がある問題を修正
    -   テーブル[#38436](https://github.com/pingcap/tidb/issues/38436) @ [接線](https://github.com/tangenta)に多数のリージョンがある場合、無効なリージョンキャッシュが原因でインデックスの追加操作が非効率になる問題を修正します。
    -   TiDB が初期化中にデッドロックする可能性がある問題を修正します[#40408](https://github.com/pingcap/tidb/issues/40408) @ [定義済み2014](https://github.com/Defined2014)
    -   キー範囲[#40158](https://github.com/pingcap/tidb/issues/40158) @ [ティアンカイマオ](https://github.com/tiancaiamao)を構築するときに TiDB が`NULL`値を適切に処理しないため、予期しないデータが読み取られる問題を修正します
    -   メモリの再利用[#40979](https://github.com/pingcap/tidb/issues/40979) @ [ルクァンチャオ](https://github.com/lcwangchao)により、システム変数の値が誤って変更される場合がある問題を修正します。
    -   テーブルの主キーに`ENUM`列[#40456](https://github.com/pingcap/tidb/issues/40456) @ [ルクァンチャオ](https://github.com/lcwangchao)が含まれている場合に TTL タスクが失敗する問題を修正します
    -   一意のインデックス[#40592](https://github.com/pingcap/tidb/issues/40592) @ [接線](https://github.com/tangenta)を追加すると TiDB がパニックになる問題を修正
    -   同じテーブルを同時に切り捨てる場合、一部の切り捨て操作が MDL によってブロックされない問題を修正します[#40484](https://github.com/pingcap/tidb/issues/40484) @ [wjhuang2016](https://github.com/wjhuang2016)
    -   動的トリミング モード[#40368](https://github.com/pingcap/tidb/issues/40368) @ [イサール](https://github.com/Yisaer)でパーティション テーブルに対してグローバル バインディングが作成された後、TiDB を再起動できない問題を修正します。
    -   「カーソル読み取り」メソッドを使用してデータを読み取ると、GC [#39447](https://github.com/pingcap/tidb/issues/39447) @ [ジグアン](https://github.com/zyguan)が原因でエラーが返される可能性がある問題を修正します。
    -   `SHOW PROCESSLIST` [#41156](https://github.com/pingcap/tidb/issues/41156) @ [ヤンケアオ](https://github.com/YangKeao)の結果で`EXECUTE`情報が null になる問題を修正
    -   `globalMemoryControl`がクエリを強制終了している場合、 `KILL`操作が終了しない可能性があるという問題を修正します[#41057](https://github.com/pingcap/tidb/issues/41057) @ [wshwsh12](https://github.com/wshwsh12)
    -   `indexMerge`エラー[#41047](https://github.com/pingcap/tidb/issues/41047) [#40877](https://github.com/pingcap/tidb/issues/40877) @ [グオシャオゲ](https://github.com/guo-shaoge) @ [風の語り手](https://github.com/windtalker)に遭遇した後、TiDB がpanicになる可能性がある問題を修正します。
    -   `ANALYZE`ステートメントが`KILL` [#41825](https://github.com/pingcap/tidb/issues/41825) @ [徐懐玉](https://github.com/XuHuaiyu)で終了する可能性がある問題を修正します。
    -   `indexMerge` [#41545](https://github.com/pingcap/tidb/issues/41545) [#41605](https://github.com/pingcap/tidb/issues/41605) @ [グオシャオゲ](https://github.com/guo-shaoge)でゴルーチンリークが発生する可能性がある問題を修正
    -   符号なしの`TINYINT` / `SMALLINT` / `INT`値を`0` [#41736](https://github.com/pingcap/tidb/issues/41736) @ [リトルフォール](https://github.com/LittleFall)より小さい`DECIMAL` / `FLOAT` / `DOUBLE`値と比較すると、間違った結果になる可能性がある問題を修正
    -   `tidb_enable_reuse_chunk`を有効にするとメモリリークが発生する可能性がある問題を修正[#40987](https://github.com/pingcap/tidb/issues/40987) @ [グオシャオゲ](https://github.com/guo-shaoge)
    -   タイム ゾーンでのデータ競合がデータ インデックスの不整合を引き起こす可能性がある問題を修正します[#40710](https://github.com/pingcap/tidb/issues/40710) @ [wjhuang2016](https://github.com/wjhuang2016)
    -   `batch cop`の実行中のスキャン詳細情報が不正確になることがある問題を修正[#41582](https://github.com/pingcap/tidb/issues/41582) @ [あなた06](https://github.com/you06)
    -   `cop`の上限同時実行数が[#41134](https://github.com/pingcap/tidb/issues/41134) @ [あなた06](https://github.com/you06)に制限されない問題を修正
    -   `cursor read`分の`statement context`誤って[#39998](https://github.com/pingcap/tidb/issues/39998) @ [ジグアン](https://github.com/zyguan)にキャッシュされる問題を修正
    -   古いリージョンキャッシュを定期的にクリーンアップして、メモリリークとパフォーマンスの低下を回避する[#40355](https://github.com/pingcap/tidb/issues/40355) @ [スティックナーフ](https://github.com/sticnarf)
    -   `year <cmp> const`を含むクエリでプラン キャッシュを使用すると、間違った結果[#41626](https://github.com/pingcap/tidb/issues/41626) @ [qw4990](https://github.com/qw4990)が返される可能性があるという問題を修正します。
    -   広い範囲と大量のデータ変更[#39593](https://github.com/pingcap/tidb/issues/39593) @ [時間と運命](https://github.com/time-and-fate)でクエリを実行すると、大きな推定エラーが発生する問題を修正します。
    -   Plan Cache [#40093](https://github.com/pingcap/tidb/issues/40093) [#38205](https://github.com/pingcap/tidb/issues/38205) @ [qw4990](https://github.com/qw4990)を使用している場合、Join 演算子を使用して一部の条件をプッシュダウンできない問題を修正します。
    -   IndexMerge プランが SET タイプ列[#41273](https://github.com/pingcap/tidb/issues/41273) [#41293](https://github.com/pingcap/tidb/issues/41293) @ [時間と運命](https://github.com/time-and-fate)で誤った範囲を生成する可能性があるという問題を修正します
    -   `int_col <cmp> decimal`条件[#40679](https://github.com/pingcap/tidb/issues/40679) [#41032](https://github.com/pingcap/tidb/issues/41032) @ [qw4990](https://github.com/qw4990)を処理するときに、Plan Cache が FullScan プランをキャッシュする可能性がある問題を修正します
    -   `int_col in (decimal...)`条件[#40224](https://github.com/pingcap/tidb/issues/40224) @ [qw4990](https://github.com/qw4990)を処理するときに、Plan Cache が FullScan プランをキャッシュする可能性がある問題を修正します。
    -   `INSERT`ステートメント[#40079](https://github.com/pingcap/tidb/issues/40079) [#39717](https://github.com/pingcap/tidb/issues/39717) @ [qw4990](https://github.com/qw4990)に対して`ignore_plan_cache`ヒントが機能しない可能性がある問題を修正します。
    -   Auto Analyze が TiDB の[#40038](https://github.com/pingcap/tidb/issues/40038) @ [しゅいふぁんグリーンアイズ](https://github.com/xuyifangreeneyes)の終了を妨げる可能性がある問題を修正
    -   分割されたテーブル[#40309](https://github.com/pingcap/tidb/issues/40309) @ [ウィノロス](https://github.com/winoros)の符号なし主キーに対して、誤ったアクセス間隔が構築される可能性がある問題を修正します。
    -   Plan Cache が Shuffle 演算子をキャッシュし、誤った結果[#38335](https://github.com/pingcap/tidb/issues/38335) @ [qw4990](https://github.com/qw4990)を返す可能性がある問題を修正します。
    -   パーティション化されたテーブルでグローバル バインディングを作成すると、TiDB の起動に失敗する可能性があるという問題を修正します[#40368](https://github.com/pingcap/tidb/issues/40368) @ [イサール](https://github.com/Yisaer)
    -   低速ログ[#41458](https://github.com/pingcap/tidb/issues/41458) @ [時間と運命](https://github.com/time-and-fate)でクエリ プラン演算子が欠落している可能性がある問題を修正します
    -   仮想列を持つ TopN オペレーターが誤って TiKV またはTiFlash [#41355](https://github.com/pingcap/tidb/issues/41355) @ [ドゥジール9](https://github.com/Dousir9)にプッシュ ダウンすると、誤った結果が返されることがある問題を修正します。
    -   インデックス[#40698](https://github.com/pingcap/tidb/issues/40698) [#40730](https://github.com/pingcap/tidb/issues/40730) [#41459](https://github.com/pingcap/tidb/issues/41459) [#40464](https://github.com/pingcap/tidb/issues/40464) [#40217](https://github.com/pingcap/tidb/issues/40217) @ [接線](https://github.com/tangenta)を追加する際のデータの不整合の問題を修正
    -   インデックス[#41515](https://github.com/pingcap/tidb/issues/41515) @ [接線](https://github.com/tangenta)を追加するときに`Pessimistic lock not found`エラーが発生する問題を修正
    -   一意のインデックス[#41630](https://github.com/pingcap/tidb/issues/41630) @ [接線](https://github.com/tangenta)を追加するときに誤って報告された重複キー エラーの問題を修正します。
    -   TiDB [#40741](https://github.com/pingcap/tidb/issues/40741) @ [ソロツグ](https://github.com/solotzg)で`paging`を使用するとパフォーマンスが低下する問題を修正

-   TiKV

    -   解決済みの TS が原因でネットワーク トラフィックが高くなる問題を修正します[#14092](https://github.com/tikv/tikv/issues/14092) @ [大静脈](https://github.com/overvenus)
    -   悲観的DML [#14038](https://github.com/tikv/tikv/issues/14038) @ [みょんけみんた](https://github.com/MyonKeminta)が失敗した後の DML の実行中に、TiDB と TiKV 間のネットワーク障害によって引き起こされたデータの不整合の問題を修正します。
    -   `const Enum`型を他の型[#14156](https://github.com/tikv/tikv/issues/14156) @ [wshwsh12](https://github.com/wshwsh12)にキャストするときに発生するエラーを修正
    -   警官タスクのページングが不正確である問題を修正[#14254](https://github.com/tikv/tikv/issues/14254) @ [あなた06](https://github.com/you06)
    -   `batch_cop`モード[#14109](https://github.com/tikv/tikv/issues/14109) @ [あなた06](https://github.com/you06)で`scan_detail`フィールドが不正確になる問題を修正
    -   TiKV がRaftデータの破損を検出し、 [#14338](https://github.com/tikv/tikv/issues/14338) @ [tonyxuqqi](https://github.com/tonyxuqqi)の再起動に失敗する可能性があるRaft Engineの潜在的なエラーを修正します。

-   PD

    -   特定の条件下で実行`replace-down-peer`が遅くなる問題を修正[#5788](https://github.com/tikv/pd/issues/5788) @ [HundunDM](https://github.com/HunDunDM)
    -   PD がリージョン[#5786](https://github.com/tikv/pd/issues/5786) @ [フンドゥンDM](https://github.com/HunDunDM)に複数の学習者を予期せず追加する可能性がある問題を修正します
    -   リージョン Scatter タスクが冗長レプリカを予期せず生成する問題を修正します[#5909](https://github.com/tikv/pd/issues/5909) @ [HundunDM](https://github.com/HunDunDM)
    -   `ReportMinResolvedTS`の呼び出しが頻繁すぎる場合に発生する PD OOM の問題を修正します[#5965](https://github.com/tikv/pd/issues/5965) @ [HundunDM](https://github.com/HunDunDM)
    -   リージョン Scatter がリーダー[#6017](https://github.com/tikv/pd/issues/6017) @ [フンドゥンDM](https://github.com/HunDunDM)の不均一な分布を引き起こす可能性がある問題を修正します。

-   TiFlash

    -   デカルト積[#6730](https://github.com/pingcap/tiflash/issues/6730) @ [ゲンリキ](https://github.com/gengliqi)を計算するときに準結合が過剰なメモリを使用する問題を修正します。
    -   TiFlash のログ検索が遅すぎる問題を修正[#6829](https://github.com/pingcap/tiflash/issues/6829) @ [へへへん](https://github.com/hehechen)
    -   再起動を繰り返すと誤ってファイルが削除されてしまい、 TiFlashが起動できなくなる問題を修正[#6486](https://github.com/pingcap/tiflash/issues/6486) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)
    -   新しい列[#6726](https://github.com/pingcap/tiflash/issues/6726) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)を追加した後にクエリを実行すると、 TiFlash がエラーを報告する可能性がある問題を修正します。
    -   TiFlashが IPv6 構成[#6734](https://github.com/pingcap/tiflash/issues/6734) @ [ywqzzy](https://github.com/ywqzzy)をサポートしていない問題を修正

-   ツール

    -   バックアップと復元 (BR)

        -   PD と tidb-server 間の接続障害により、PITR バックアップの進行状況が[#41082](https://github.com/pingcap/tidb/issues/41082) @ [ユジュンセン](https://github.com/YuJuncen)進まない問題を修正
        -   PD と TiKV [#14159](https://github.com/tikv/tikv/issues/14159) @ [ユジュンセン](https://github.com/YuJuncen)間の接続障害により、TiKV が PITR タスクをリッスンできない問題を修正
        -   PITR が PD クラスター[#14165](https://github.com/tikv/tikv/issues/14165) @ [ユジュンセン](https://github.com/YuJuncen)の構成変更をサポートしていない問題を修正します。
        -   PITR 機能が CA-bundles [#38775](https://github.com/pingcap/tidb/issues/38775) @ [3ポインター](https://github.com/3pointer)をサポートしていない問題を修正
        -   PITR バックアップ タスクを削除すると、残りのバックアップ データが新しいタスク[#40403](https://github.com/pingcap/tidb/issues/40403) @ [ジョッカウ](https://github.com/joccau)でデータの不整合を引き起こす問題を修正します。
        -   BR が`backupmeta`ファイル[#40878](https://github.com/pingcap/tidb/issues/40878) @ [MoCuishle28](https://github.com/MoCuishle28)を解析するときにpanicを引き起こす問題を修正します。
        -   リージョンサイズ[#36053](https://github.com/pingcap/tidb/issues/36053) @ [ユジュンセン](https://github.com/YuJuncen)の取得に失敗して復元が中断される問題を修正
        -   TiDBクラスタ[#40759](https://github.com/pingcap/tidb/issues/40759) @ [ジョッカウ](https://github.com/joccau)でPITRバックアップタスクがない場合に`resolve lock`の頻度が高すぎる問題を修正
        -   ログ バックアップが実行されているクラスターにデータを復元すると、ログ バックアップ ファイルが復元できなくなる問題を修正します[#40797](https://github.com/pingcap/tidb/issues/40797) @ [レヴルス](https://github.com/Leavrth)
        -   フル バックアップの失敗後、チェックポイントからバックアップを再開しようとすると発生するpanicの問題を修正します[#40704](https://github.com/pingcap/tidb/issues/40704) @ [レヴルス](https://github.com/Leavrth)
        -   PITR エラーが[#40576](https://github.com/pingcap/tidb/issues/40576) @ [レヴルス](https://github.com/Leavrth)で上書きされる問題を修正
        -   事前所有者と gc 所有者が異なる場合、PITR バックアップ タスクでチェックポイントが進められない問題を修正します[#41806](https://github.com/pingcap/tidb/issues/41806) @ [ジョッカウ](https://github.com/joccau)

    -   TiCDC

        -   TiKV または TiCDC ノード[#8174](https://github.com/pingcap/tiflow/issues/8174) @ [ヒック](https://github.com/hicqu)をスケールインまたはスケールアウトする場合など、特別なシナリオで changefeed が停止する可能性がある問題を修正します
        -   REDO ログ[#6335](https://github.com/pingcap/tiflow/issues/6335) @ [チャールズ・チャン96](https://github.com/CharlesCheung96)のstorageパスで事前チェックが行われない問題を修正
        -   S3storage障害[#8089](https://github.com/pingcap/tiflow/issues/8089) @ [チャールズ・チャン96](https://github.com/CharlesCheung96)に対して REDO ログが許容できる期間が不十分であるという問題を修正します。
        -   `transaction_atomicity`と`protocol`構成ファイル[#7935](https://github.com/pingcap/tiflow/issues/7935) @ [チャールズ・チャン96](https://github.com/CharlesCheung96)経由で更新できない問題を修正
        -   TiCDC が過度に多数のテーブル[#8004](https://github.com/pingcap/tiflow/issues/8004) @ [大静脈](https://github.com/overvenus)をレプリケートすると、チェックポイントが進められない問題を修正します
        -   レプリケーション ラグが過度に大きい場合に REDO ログを適用すると OOM が発生する可能性がある問題を修正します[#8085](https://github.com/pingcap/tiflow/issues/8085) @ [チャールズ・チャン96](https://github.com/CharlesCheung96)
        -   REDO ログを有効にして meta [#8074](https://github.com/pingcap/tiflow/issues/8074) @ [チャールズ・チャン96](https://github.com/CharlesCheung96)を書き込むとパフォーマンスが低下する問題を修正
        -   TiCDC が大規模なトランザクション[#7982](https://github.com/pingcap/tiflow/issues/7982) @ [ハイラスチン](https://github.com/hi-rustin)を分割せずにデータを複製すると、コンテキストのデッドラインを超過するバグを修正
        -   PDが異常な状態でチェンジフィードを一時停止すると、ステータスが正しくない[#8330](https://github.com/pingcap/tiflow/issues/8330) @ [スドジ](https://github.com/sdojjy)になる問題を修正
        -   TiDB または MySQL シンクにデータをレプリケートするときに、主キー[#8420](https://github.com/pingcap/tiflow/issues/8420) @ [アスドンメン](https://github.com/asddongmen)なしで null 以外の一意のインデックスを持つ列に`CHARACTER SET`が指定されたときに発生するデータの不整合を修正します。
        -   テーブル スケジューリングとブラックホール シンクでのpanicの問題を修正します[#8024](https://github.com/pingcap/tiflow/issues/8024) [#8142](https://github.com/pingcap/tiflow/issues/8142) @ [ヒック](https://github.com/hicqu)

    -   TiDB データ移行 (DM)

        -   `binlog-schema delete`コマンドが[#7373](https://github.com/pingcap/tiflow/issues/7373) @ [リウメンギャ94](https://github.com/liumengya94)の実行に失敗する問題を修正
        -   最後のbinlogがスキップされた DDL [#8175](https://github.com/pingcap/tiflow/issues/8175) @ [D3ハンター](https://github.com/D3Hunter)の場合、チェックポイントが進まない問題を修正
        -   1つのテーブルに「更新」タイプと「非更新」タイプの両方の式フィルターを指定すると、 `UPDATE`ステートメントがすべてスキップされるバグを修正[#7831](https://github.com/pingcap/tiflow/issues/7831) @ [ランス6716](https://github.com/lance6716)

    -   TiDB Lightning

        -   以前に失敗したインポート[#39477](https://github.com/pingcap/tidb/issues/39477) @ [dsdashun](https://github.com/dsdashun)によって残されたダーティ データをTiDB Lightningプリチェックが見つけられないという問題を修正します。
        -   分割領域フェーズ[#40934](https://github.com/pingcap/tidb/issues/40934) @ [ランス6716](https://github.com/lance6716)でTiDB Lightning がパニックになる問題を修正
        -   競合解決ロジック ( `duplicate-resolution` ) が不整合なチェックサム[#40657](https://github.com/pingcap/tidb/issues/40657) @ [ゴズスキー](https://github.com/gozssky)を引き起こす可能性があるという問題を修正します。
        -   並列インポート[#40923](https://github.com/pingcap/tidb/issues/40923) @ [リチュンジュ](https://github.com/lichunzhu)中に、最後のTiDB Lightningインスタンス以外のすべてのインスタンスがローカルの重複レコードに遭遇した場合、 TiDB Lightning が競合解決を誤ってスキップする可能性があるという問題を修正します。
        -   ローカル バックエンド モードでデータをインポートするときに、インポートされたターゲット テーブルの複合主キーに`auto_random`列があり、その列の値がソース データで指定されていない場合、ターゲット列が自動的にデータを生成しないという問題を修正します[#41454](https://github.com/pingcap/tidb/issues/41454) @ [D3ハンター](https://github.com/D3Hunter)
