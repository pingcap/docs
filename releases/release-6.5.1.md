---
title: TiDB 6.5.1 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 6.5.1.
---

# TiDB 6.5.1 リリースノート {#tidb-6-5-1-release-notes}

発売日：2023年3月10日

TiDB バージョン: 6.5.1

クイックアクセス: [<a href="https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb">クイックスタート</a>](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [<a href="https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup">本番展開</a>](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup) | [<a href="https://www.pingcap.com/download/?version=v6.5.1#version-list">インストールパッケージ</a>](https://www.pingcap.com/download/?version=v6.5.1#version-list)

## 互換性の変更 {#compatibility-changes}

-   2023 年 2 月 20 日以降、v6.5.1 を含む TiDB および TiDB ダッシュボードの新しいバージョンでは[<a href="/telemetry.md">テレメトリー機能</a>](/telemetry.md)がデフォルトで無効になり、使用状況情報は収集されず、PingCAP と共有されません。これらのバージョンにアップグレードする前に、クラスターでデフォルトのテレメトリ構成が使用されている場合、アップグレード後にテレメトリ機能は無効になります。特定のバージョンについては[<a href="/releases/release-timeline.md">TiDB リリース タイムライン</a>](/releases/release-timeline.md)参照してください。

    -   [<a href="/system-variables.md#tidb_enable_telemetry-new-in-v402">`tidb_enable_telemetry`</a>](/system-variables.md#tidb_enable_telemetry-new-in-v402)システム変数のデフォルト値が`ON`から`OFF`に変更されました。
    -   TiDB [<a href="/tidb-configuration-file.md#enable-telemetry-new-in-v402">`enable-telemetry`</a>](/tidb-configuration-file.md#enable-telemetry-new-in-v402)構成項目のデフォルト値が`true`から`false`に変更されました。
    -   PD [<a href="/pd-configuration-file.md#enable-telemetry">`enable-telemetry`</a>](/pd-configuration-file.md#enable-telemetry)設定項目のデフォルト値が`true`から`false`に変更されます。

-   v1.11.3 以降、新しく展開されたTiUPではテレメトリ機能がデフォルトで無効になっており、使用状況情報は収集されません。 TiUP のv1.11.3 より前のバージョンから v1.11.3 以降のバージョンにアップグレードすると、テレメトリ機能はアップグレード前と同じステータスを維持します。

-   正確性の問題が発生する可能性があるため、パーティション テーブルの列タイプの変更はサポートされなくなりました。 [<a href="https://github.com/pingcap/tidb/issues/40620">#40620</a>](https://github.com/pingcap/tidb/issues/40620) @ [<a href="https://github.com/mjonss">むじょん</a>](https://github.com/mjonss)

-   TiKV [<a href="/tikv-configuration-file.md#advance-ts-interval">`advance-ts-interval`</a>](/tikv-configuration-file.md#advance-ts-interval)構成項目のデフォルト値が`1s`から`20s`に変更されます。この構成項目を変更して、レイテンシーを短縮し、 ステイル読み取りデータの適時性を向上させることができます。詳細は[<a href="/stale-read.md#reduce-stale-read-latency">ステイル読み取りレイテンシーを削減する</a>](/stale-read.md#reduce-stale-read-latency)を参照してください。

## 改善点 {#improvements}

-   TiDB

    -   v6.5.1 以降、 TiDB Operator v1.4.3 以降によってデプロイされた TiDB クラスターは IPv6 アドレスをサポートします。これは、TiDB がより大きなアドレス空間をサポートし、より優れたセキュリティとネットワーク パフォーマンスを実現できることを意味します。

        -   IPv6 アドレス指定の完全サポート: TiDB は、クライアント接続、ノード間の内部通信、外部システムとの通信を含むすべてのネットワーク接続で IPv6 アドレスの使用をサポートします。
        -   デュアルスタックのサポート: まだ IPv6 に完全に切り替える準備ができていない場合は、TiDB はデュアルスタック ネットワークもサポートします。これは、同じ TiDB クラスター内で IPv4 アドレスと IPv6 アドレスの両方を使用でき、構成によって IPv6 を優先するネットワーク展開モードを選択できることを意味します。

        IPv6 展開の詳細については、 [<a href="https://docs.pingcap.com/tidb-in-kubernetes/stable/configure-a-tidb-cluster#ipv6-support">Kubernetes 上の TiDB ドキュメント</a>](https://docs.pingcap.com/tidb-in-kubernetes/stable/configure-a-tidb-cluster#ipv6-support)を参照してください。

    -   TiDB クラスターの初期化時に実行される SQL スクリプトの指定をサポート[<a href="https://github.com/pingcap/tidb/issues/35624">#35624</a>](https://github.com/pingcap/tidb/issues/35624) @ [<a href="https://github.com/morgo">モルゴ</a>](https://github.com/morgo)

        TiDB v6.5.1 では、新しい構成項目[<a href="https://docs.pingcap.com/tidb/v6.5/tidb-configuration-file#initialize-sql-file-new-in-v651">`initialize-sql-file`</a>](https://docs.pingcap.com/tidb/v6.5/tidb-configuration-file#initialize-sql-file-new-in-v651)が追加されています。 TiDB クラスターを初めて起動するときは、コマンド ライン パラメーター`--initialize-sql-file`を構成することで、実行する SQL スクリプトを指定できます。この機能は、システム変数の値の変更、ユーザーの作成、権限の権限などの操作を実行する必要がある場合に使用できます。詳細については、 [<a href="https://docs.pingcap.com/tidb/v6.5/tidb-configuration-file#initialize-sql-file-new-in-v651">ドキュメンテーション</a>](https://docs.pingcap.com/tidb/v6.5/tidb-configuration-file#initialize-sql-file-new-in-v651)を参照してください。

    -   期限切れの領域キャッシュを定期的にクリアして、メモリリークとパフォーマンスの低下を回避します[<a href="https://github.com/pingcap/tidb/issues/40461">#40461</a>](https://github.com/pingcap/tidb/issues/40461) @ [<a href="https://github.com/sticnarf">スティックナーフ</a>](https://github.com/sticnarf)

    -   新しい構成項目`--proxy-protocol-fallbackable`を追加して、PROXY プロトコル フォールバック モードを有効にするかどうかを制御します。このパラメータが`true`に設定されている場合、TiDB は PROXY クライアント接続および PROXY プロトコル ヘッダーなしのクライアント接続を受け入れます[<a href="https://github.com/pingcap/tidb/issues/41409">#41409</a>](https://github.com/pingcap/tidb/issues/41409) @ [<a href="https://github.com/blacktear23">ブラックティア23</a>](https://github.com/blacktear23)

    -   Memory Tracker [<a href="https://github.com/pingcap/tidb/issues/40900">#40900</a>](https://github.com/pingcap/tidb/issues/40900) [<a href="https://github.com/pingcap/tidb/issues/40500">#40500</a>](https://github.com/pingcap/tidb/issues/40500) @ [<a href="https://github.com/wshwsh12">wshwsh12</a>](https://github.com/wshwsh12)の精度を向上させます。

    -   プラン キャッシュが有効にならない場合、システムはその理由を警告[<a href="https://github.com/pingcap/tidb/pull/40210">#40210</a>](https://github.com/pingcap/tidb/pull/40210) @ [<a href="https://github.com/qw4990">qw4990</a>](https://github.com/qw4990)として返します。

    -   範囲外の推定[<a href="https://github.com/pingcap/tidb/issues/39008">#39008</a>](https://github.com/pingcap/tidb/issues/39008) @ [<a href="https://github.com/time-and-fate">時間と運命</a>](https://github.com/time-and-fate)に対するオプティマイザ戦略を改善します。

-   TiKV

    -   1 コア未満の CPU での TiKV の起動をサポート[<a href="https://github.com/tikv/tikv/issues/13586">#13586</a>](https://github.com/tikv/tikv/issues/13586) [<a href="https://github.com/tikv/tikv/issues/13752">#13752</a>](https://github.com/tikv/tikv/issues/13752) [<a href="https://github.com/tikv/tikv/issues/14017">#14017</a>](https://github.com/tikv/tikv/issues/14017) @ [<a href="https://github.com/andreid-db">アンドロイドデータベース</a>](https://github.com/andreid-db)
    -   統合読み取りプール ( `readpool.unified.max-thread-count` ) のスレッド制限を CPU クォータの 10 倍に増やし、同時実行性の高いクエリの処理を改善します[<a href="https://github.com/tikv/tikv/issues/13690">#13690</a>](https://github.com/tikv/tikv/issues/13690) @ [<a href="https://github.com/v01dstar">v01dstar</a>](https://github.com/v01dstar)
    -   リージョン間のトラフィック[<a href="https://github.com/tikv/tikv/issues/14100">#14100</a>](https://github.com/tikv/tikv/issues/14100) @ [<a href="https://github.com/overvenus">オーバーヴィーナス</a>](https://github.com/overvenus)を減らすために、デフォルト値`resolved-ts.advance-ts-interval`を`"1s"`から`"20s"`に変更します。

-   TiFlash

    -   データ量が多い場合にTiFlash の起動を大幅に高速化[<a href="https://github.com/pingcap/tiflash/issues/6395">#6395</a>](https://github.com/pingcap/tiflash/issues/6395) @ [<a href="https://github.com/hehechen">へへへん</a>](https://github.com/hehechen)

-   ツール

    -   バックアップと復元 (BR)

        -   TiKV 側でのログ バックアップ ファイルのダウンロードの同時実行性を最適化し、通常のシナリオ[<a href="https://github.com/tikv/tikv/issues/14206">#14206</a>](https://github.com/tikv/tikv/issues/14206) @ [<a href="https://github.com/YuJuncen">ユジュンセン</a>](https://github.com/YuJuncen)での PITR のパフォーマンスを向上させます。

    -   TiCDC

        -   プルベースのシンクを有効にしてシステム スループットを最適化[<a href="https://github.com/pingcap/tiflow/issues/8232">#8232</a>](https://github.com/pingcap/tiflow/issues/8232) @ [<a href="https://github.com/hi-rustin">こんにちはラスティン</a>](https://github.com/hi-rustin)
        -   GCS 互換または Azure 互換のオブジェクトstorage[<a href="https://github.com/pingcap/tiflow/issues/7987">#7987</a>](https://github.com/pingcap/tiflow/issues/7987) @ [<a href="https://github.com/CharlesCheung96">CharlesCheung96</a>](https://github.com/CharlesCheung96)への REDO ログの保存のサポート
        -   MQ シンクと MySQL シンクを非同期モードで実装して、シンクのスループットを向上させます[<a href="https://github.com/pingcap/tiflow/issues/5928">#5928</a>](https://github.com/pingcap/tiflow/issues/5928) @ [<a href="https://github.com/amyangfei">咸陽飛</a>](https://github.com/amyangfei) @ [<a href="https://github.com/CharlesCheung96">CharlesCheung96</a>](https://github.com/CharlesCheung96)

## バグの修正 {#bug-fixes}

-   TiDB

    -   ポイント取得クエリ[<a href="https://github.com/pingcap/tidb/issues/39928">#39928</a>](https://github.com/pingcap/tidb/issues/39928) @ [<a href="https://github.com/zyguan">ジグアン</a>](https://github.com/zyguan)で設定項目[<a href="/tidb-configuration-file.md#pessimistic-auto-commit-new-in-v600">`pessimistic-auto-commit`</a>](/tidb-configuration-file.md#pessimistic-auto-commit-new-in-v600)が有効にならない問題を修正
    -   長いセッション接続[<a href="https://github.com/pingcap/tidb/issues/40351">#40351</a>](https://github.com/pingcap/tidb/issues/40351) @ [<a href="https://github.com/winoros">ウィノロス</a>](https://github.com/winoros)で`INSERT`または`REPLACE`ステートメントがpanicになる可能性がある問題を修正
    -   `auto analyze`により正常なシャットダウンに時間がかかる問題を修正[<a href="https://github.com/pingcap/tidb/issues/40038">#40038</a>](https://github.com/pingcap/tidb/issues/40038) @ [<a href="https://github.com/xuyifangreeneyes">シュイファングリーンアイズ</a>](https://github.com/xuyifangreeneyes)
    -   DDL 取り込み[<a href="https://github.com/pingcap/tidb/issues/40970">#40970</a>](https://github.com/pingcap/tidb/issues/40970) @ [<a href="https://github.com/tangenta">タンジェンタ</a>](https://github.com/tangenta)中にデータ競合が発生する可能性がある問題を修正
    -   インデックス[<a href="https://github.com/pingcap/tidb/issues/40879">#40879</a>](https://github.com/pingcap/tidb/issues/40879) @ [<a href="https://github.com/tangenta">タンジェンタ</a>](https://github.com/tangenta)を追加するとデータ競合が発生する可能性がある問題を修正
    -   テーブル[<a href="https://github.com/pingcap/tidb/issues/38436">#38436</a>](https://github.com/pingcap/tidb/issues/38436) @ [<a href="https://github.com/tangenta">タンジェンタ</a>](https://github.com/tangenta)に多数のリージョンがある場合、無効なリージョンキャッシュによりインデックスの追加操作が非効率になる問題を修正
    -   TiDB が初期化[<a href="https://github.com/pingcap/tidb/issues/40408">#40408</a>](https://github.com/pingcap/tidb/issues/40408) @ [<a href="https://github.com/Defined2014">定義2014</a>](https://github.com/Defined2014)中にデッドロックする可能性がある問題を修正
    -   キー範囲[<a href="https://github.com/pingcap/tidb/issues/40158">#40158</a>](https://github.com/pingcap/tidb/issues/40158) @ [<a href="https://github.com/tiancaiamao">ティエンチャイアマオ</a>](https://github.com/tiancaiamao)を構築するときに TiDB が`NULL`値を適切に処理しないため、予期しないデータが読み取られる問題を修正
    -   メモリの再利用によりシステム変数の値が誤って変更される場合がある問題を修正[<a href="https://github.com/pingcap/tidb/issues/40979">#40979</a>](https://github.com/pingcap/tidb/issues/40979) @ [<a href="https://github.com/lcwangchao">ルクワンチャオ</a>](https://github.com/lcwangchao)
    -   テーブルの主キーに`ENUM`カラム[<a href="https://github.com/pingcap/tidb/issues/40456">#40456</a>](https://github.com/pingcap/tidb/issues/40456) @ [<a href="https://github.com/lcwangchao">ルクワンチャオ</a>](https://github.com/lcwangchao)が含まれる場合、TTL タスクが失敗する問題を修正します。
    -   一意のインデックス[<a href="https://github.com/pingcap/tidb/issues/40592">#40592</a>](https://github.com/pingcap/tidb/issues/40592) @ [<a href="https://github.com/tangenta">タンジェンタ</a>](https://github.com/tangenta)を追加するときに TiDB がパニックになる問題を修正
    -   同じテーブルを同時に切り捨てる場合、一部の切り捨て操作が MDL によってブロックされない問題を修正します[<a href="https://github.com/pingcap/tidb/issues/40484">#40484</a>](https://github.com/pingcap/tidb/issues/40484) @ [<a href="https://github.com/wjhuang2016">wjhuang2016</a>](https://github.com/wjhuang2016)
    -   動的トリミング モード[<a href="https://github.com/pingcap/tidb/issues/40368">#40368</a>](https://github.com/pingcap/tidb/issues/40368) @ [<a href="https://github.com/Yisaer">イーサール</a>](https://github.com/Yisaer)でパーティション テーブルのグローバル バインディングが作成された後、TiDB が再起動できない問題を修正します。
    -   「カーソル読み取り」メソッドを使用してデータを読み取ると、GC [<a href="https://github.com/pingcap/tidb/issues/39447">#39447</a>](https://github.com/pingcap/tidb/issues/39447) @ [<a href="https://github.com/zyguan">ジグアン</a>](https://github.com/zyguan)が原因でエラーが返される場合がある問題を修正
    -   `SHOW PROCESSLIST` [<a href="https://github.com/pingcap/tidb/issues/41156">#41156</a>](https://github.com/pingcap/tidb/issues/41156) @ [<a href="https://github.com/YangKeao">ヤンケオ</a>](https://github.com/YangKeao)の結果で`EXECUTE`情報が null になる問題を修正
    -   `globalMemoryControl`がクエリを強制終了しているときに、 `KILL`操作が[<a href="https://github.com/pingcap/tidb/issues/41057">#41057</a>](https://github.com/pingcap/tidb/issues/41057) @ [<a href="https://github.com/wshwsh12">wshwsh12</a>](https://github.com/wshwsh12)で終了しない可能性がある問題を修正します。
    -   `indexMerge`エラー[<a href="https://github.com/pingcap/tidb/issues/41047">#41047</a>](https://github.com/pingcap/tidb/issues/41047) [<a href="https://github.com/pingcap/tidb/issues/40877">#40877</a>](https://github.com/pingcap/tidb/issues/40877) @ [<a href="https://github.com/guo-shaoge">グオシャオゲ</a>](https://github.com/guo-shaoge) @ [<a href="https://github.com/windtalker">ウィンドトーカー</a>](https://github.com/windtalker)が発生した後に TiDB がpanicになる可能性がある問題を修正
    -   `ANALYZE`ステートメントが`KILL` [<a href="https://github.com/pingcap/tidb/issues/41825">#41825</a>](https://github.com/pingcap/tidb/issues/41825) @ [<a href="https://github.com/XuHuaiyu">徐淮嶼</a>](https://github.com/XuHuaiyu)で終了する可能性がある問題を修正
    -   `indexMerge` [<a href="https://github.com/pingcap/tidb/issues/41545">#41545</a>](https://github.com/pingcap/tidb/issues/41545) [<a href="https://github.com/pingcap/tidb/issues/41605">#41605</a>](https://github.com/pingcap/tidb/issues/41605) @ [<a href="https://github.com/guo-shaoge">グオシャオゲ</a>](https://github.com/guo-shaoge)で goroutine リークが発生する可能性がある問題を修正
    -   符号なし`TINYINT` / `SMALLINT` / `INT`の値を`0` [<a href="https://github.com/pingcap/tidb/issues/41736">#41736</a>](https://github.com/pingcap/tidb/issues/41736) @ [<a href="https://github.com/LittleFall">リトルフォール</a>](https://github.com/LittleFall)より小さい`DECIMAL` / `FLOAT` / `DOUBLE`の値と比較するときに誤った結果が生じる可能性がある問題を修正
    -   `tidb_enable_reuse_chunk`を有効にするとメモリリーク[<a href="https://github.com/pingcap/tidb/issues/40987">#40987</a>](https://github.com/pingcap/tidb/issues/40987) @ [<a href="https://github.com/guo-shaoge">グオシャオゲ</a>](https://github.com/guo-shaoge)が発生する可能性がある問題を修正
    -   タイムゾーン内のデータ競合によりデータインデックスの不整合が発生する可能性がある問題を修正[<a href="https://github.com/pingcap/tidb/issues/40710">#40710</a>](https://github.com/pingcap/tidb/issues/40710) @ [<a href="https://github.com/wjhuang2016">wjhuang2016</a>](https://github.com/wjhuang2016)
    -   `batch cop`の実行時のスキャン詳細情報が不正確になる場合がある問題を修正[<a href="https://github.com/pingcap/tidb/issues/41582">#41582</a>](https://github.com/pingcap/tidb/issues/41582) @ [<a href="https://github.com/you06">あなた06</a>](https://github.com/you06)
    -   `cop`の同時実行数の上限が[<a href="https://github.com/pingcap/tidb/issues/41134">#41134</a>](https://github.com/pingcap/tidb/issues/41134) @ [<a href="https://github.com/you06">あなた06</a>](https://github.com/you06)に制限されない問題を修正
    -   `cursor read`の`statement context`誤って[<a href="https://github.com/pingcap/tidb/issues/39998">#39998</a>](https://github.com/pingcap/tidb/issues/39998) @ [<a href="https://github.com/zyguan">ジグアン</a>](https://github.com/zyguan)にキャッシュされる問題を修正
    -   メモリリークとパフォーマンスの低下を避けるために、古いリージョンキャッシュを定期的にクリーンアップします[<a href="https://github.com/pingcap/tidb/issues/40355">#40355</a>](https://github.com/pingcap/tidb/issues/40355) @ [<a href="https://github.com/sticnarf">スティックナーフ</a>](https://github.com/sticnarf)
    -   `year <cmp> const`を含むクエリでプラン キャッシュを使用すると、間違った結果[<a href="https://github.com/pingcap/tidb/issues/41626">#41626</a>](https://github.com/pingcap/tidb/issues/41626) @ [<a href="https://github.com/qw4990">qw4990</a>](https://github.com/qw4990)が得られる可能性がある問題を修正します。
    -   広い範囲と大量のデータ変更を伴うクエリ時に大きな推定エラーが発生する問題を修正[<a href="https://github.com/pingcap/tidb/issues/39593">#39593</a>](https://github.com/pingcap/tidb/issues/39593) @ [<a href="https://github.com/time-and-fate">時間と運命</a>](https://github.com/time-and-fate)
    -   Plan Cache [<a href="https://github.com/pingcap/tidb/issues/40093">#40093</a>](https://github.com/pingcap/tidb/issues/40093) [<a href="https://github.com/pingcap/tidb/issues/38205">#38205</a>](https://github.com/pingcap/tidb/issues/38205) @ [<a href="https://github.com/qw4990">qw4990</a>](https://github.com/qw4990)を使用する場合、結合演算子を使用して一部の条件をプッシュダウンできない問題を修正します。
    -   IndexMerge プランが SET タイプの列[<a href="https://github.com/pingcap/tidb/issues/41273">#41273</a>](https://github.com/pingcap/tidb/issues/41273) [<a href="https://github.com/pingcap/tidb/issues/41293">#41293</a>](https://github.com/pingcap/tidb/issues/41293) @ [<a href="https://github.com/time-and-fate">時間と運命</a>](https://github.com/time-and-fate)に不正な範囲を生成する可能性がある問題を修正します。
    -   `int_col <cmp> decimal`条件[<a href="https://github.com/pingcap/tidb/issues/40679">#40679</a>](https://github.com/pingcap/tidb/issues/40679) [<a href="https://github.com/pingcap/tidb/issues/41032">#41032</a>](https://github.com/pingcap/tidb/issues/41032) @ [<a href="https://github.com/qw4990">qw4990</a>](https://github.com/qw4990)を処理するときにプラン キャッシュがフルスキャン プランをキャッシュする可能性がある問題を修正
    -   `int_col in (decimal...)`条件[<a href="https://github.com/pingcap/tidb/issues/40224">#40224</a>](https://github.com/pingcap/tidb/issues/40224) @ [<a href="https://github.com/qw4990">qw4990</a>](https://github.com/qw4990)を処理するときにプラン キャッシュがフルスキャン プランをキャッシュする可能性がある問題を修正
    -   `ignore_plan_cache`ヒントが`INSERT`ステートメント[<a href="https://github.com/pingcap/tidb/issues/40079">#40079</a>](https://github.com/pingcap/tidb/issues/40079) [<a href="https://github.com/pingcap/tidb/issues/39717">#39717</a>](https://github.com/pingcap/tidb/issues/39717) @ [<a href="https://github.com/qw4990">qw4990</a>](https://github.com/qw4990)に対して機能しない可能性がある問題を修正
    -   自動分析により TiDB の終了が妨げられる可能性がある問題を修正[<a href="https://github.com/pingcap/tidb/issues/40038">#40038</a>](https://github.com/pingcap/tidb/issues/40038) @ [<a href="https://github.com/xuyifangreeneyes">シュイファングリーンアイズ</a>](https://github.com/xuyifangreeneyes)
    -   パーティションテーブル[<a href="https://github.com/pingcap/tidb/issues/40309">#40309</a>](https://github.com/pingcap/tidb/issues/40309) @ [<a href="https://github.com/winoros">ウィノロス</a>](https://github.com/winoros)の署名なし主キーに対して不正なアクセス間隔が構築される可能性がある問題を修正
    -   プラン キャッシュがシャッフル演算子をキャッシュし、誤った結果[<a href="https://github.com/pingcap/tidb/issues/38335">#38335</a>](https://github.com/pingcap/tidb/issues/38335) @ [<a href="https://github.com/qw4990">qw4990</a>](https://github.com/qw4990)を返す可能性がある問題を修正します。
    -   パーティション化されたテーブルにグローバル バインディングを作成すると、TiDB の起動に失敗する可能性がある問題を修正します[<a href="https://github.com/pingcap/tidb/issues/40368">#40368</a>](https://github.com/pingcap/tidb/issues/40368) @ [<a href="https://github.com/Yisaer">イーサール</a>](https://github.com/Yisaer)
    -   低速ログ[<a href="https://github.com/pingcap/tidb/issues/41458">#41458</a>](https://github.com/pingcap/tidb/issues/41458) @ [<a href="https://github.com/time-and-fate">時間と運命</a>](https://github.com/time-and-fate)でクエリ プラン演算子が欠落する可能性がある問題を修正
    -   仮想列を持つ TopN オペレーターが誤って TiKV またはTiFlash [<a href="https://github.com/pingcap/tidb/issues/41355">#41355</a>](https://github.com/pingcap/tidb/issues/41355) @ [<a href="https://github.com/Dousir9">ドゥーシール9</a>](https://github.com/Dousir9)にプッシュダウンすると、誤った結果が返される可能性がある問題を修正
    -   インデックス[<a href="https://github.com/pingcap/tidb/issues/40698">#40698</a>](https://github.com/pingcap/tidb/issues/40698) [<a href="https://github.com/pingcap/tidb/issues/40730">#40730</a>](https://github.com/pingcap/tidb/issues/40730) [<a href="https://github.com/pingcap/tidb/issues/41459">#41459</a>](https://github.com/pingcap/tidb/issues/41459) [<a href="https://github.com/pingcap/tidb/issues/40464">#40464</a>](https://github.com/pingcap/tidb/issues/40464) [<a href="https://github.com/pingcap/tidb/issues/40217">#40217</a>](https://github.com/pingcap/tidb/issues/40217) @ [<a href="https://github.com/tangenta">タンジェンタ</a>](https://github.com/tangenta)を追加する際のデータの不整合の問題を修正
    -   インデックス[<a href="https://github.com/pingcap/tidb/issues/41515">#41515</a>](https://github.com/pingcap/tidb/issues/41515) @ [<a href="https://github.com/tangenta">タンジェンタ</a>](https://github.com/tangenta)を追加するときに`Pessimistic lock not found`エラーが発生する問題を修正
    -   一意のインデックス[<a href="https://github.com/pingcap/tidb/issues/41630">#41630</a>](https://github.com/pingcap/tidb/issues/41630) @ [<a href="https://github.com/tangenta">タンジェンタ</a>](https://github.com/tangenta)を追加するときに重複キー エラーが誤って報告される問題を修正
    -   TiDB [<a href="https://github.com/pingcap/tidb/issues/40741">#40741</a>](https://github.com/pingcap/tidb/issues/40741) @ [<a href="https://github.com/solotzg">ソロッツグ</a>](https://github.com/solotzg)で`paging`を使用するとパフォーマンスが低下する問題を修正

-   TiKV

    -   解決された TS によりネットワーク トラフィックが増加する問題を修正[<a href="https://github.com/tikv/tikv/issues/14092">#14092</a>](https://github.com/tikv/tikv/issues/14092) @ [<a href="https://github.com/overvenus">オーバーヴィーナス</a>](https://github.com/overvenus)
    -   悲観的DML [<a href="https://github.com/tikv/tikv/issues/14038">#14038</a>](https://github.com/tikv/tikv/issues/14038) @ [<a href="https://github.com/MyonKeminta">ミョンケミンタ</a>](https://github.com/MyonKeminta)が失敗した後の DML の実行中に、TiDB と TiKV の間のネットワーク障害によって引き起こされるデータの不整合の問題を修正しました。
    -   `const Enum`型を他の型[<a href="https://github.com/tikv/tikv/issues/14156">#14156</a>](https://github.com/tikv/tikv/issues/14156) @ [<a href="https://github.com/wshwsh12">wshwsh12</a>](https://github.com/wshwsh12)にキャストするときに発生するエラーを修正
    -   cop タスクのページングが不正確である問題を修正[<a href="https://github.com/tikv/tikv/issues/14254">#14254</a>](https://github.com/tikv/tikv/issues/14254) @ [<a href="https://github.com/you06">あなた06</a>](https://github.com/you06)
    -   `batch_cop`モード[<a href="https://github.com/tikv/tikv/issues/14109">#14109</a>](https://github.com/tikv/tikv/issues/14109) @ [<a href="https://github.com/you06">あなた06</a>](https://github.com/you06)で`scan_detail`フィールドが不正確になる問題を修正
    -   TiKV がRaftデータの破損を検出し、 [<a href="https://github.com/tikv/tikv/issues/14338">#14338</a>](https://github.com/tikv/tikv/issues/14338) @ [<a href="https://github.com/tonyxuqqi">トニーシュクキ</a>](https://github.com/tonyxuqqi)の再起動に失敗する可能性があるRaft Engineの潜在的なエラーを修正しました。

-   PD

    -   特定の条件下で実行`replace-down-peer`が遅くなる問題を修正[<a href="https://github.com/tikv/pd/issues/5788">#5788</a>](https://github.com/tikv/pd/issues/5788) @ [<a href="https://github.com/HunDunDM">フンドゥンDM</a>](https://github.com/HunDunDM)
    -   PD が予期せず複数の学習者をリージョン[<a href="https://github.com/tikv/pd/issues/5786">#5786</a>](https://github.com/tikv/pd/issues/5786) @ [<a href="https://github.com/HunDunDM">フンドゥンDM</a>](https://github.com/HunDunDM)に追加する可能性がある問題を修正
    -   リージョン分散タスクが予期せず冗長レプリカを生成する問題を修正します[<a href="https://github.com/tikv/pd/issues/5909">#5909</a>](https://github.com/tikv/pd/issues/5909) @ [<a href="https://github.com/HunDunDM">フンドゥンDM</a>](https://github.com/HunDunDM)
    -   `ReportMinResolvedTS` [<a href="https://github.com/tikv/pd/issues/5965">#5965</a>](https://github.com/tikv/pd/issues/5965) @ [<a href="https://github.com/HunDunDM">フンドゥンDM</a>](https://github.com/HunDunDM)の呼び出しが頻繁すぎる場合に発生する PD OOM 問題を修正します。
    -   リージョン分散によりリーダー[<a href="https://github.com/tikv/pd/issues/6017">#6017</a>](https://github.com/tikv/pd/issues/6017) @ [<a href="https://github.com/HunDunDM">フンドゥンDM</a>](https://github.com/HunDunDM)が不均一に分布する可能性がある問題を修正

-   TiFlash

    -   デカルト積[<a href="https://github.com/pingcap/tiflash/issues/6730">#6730</a>](https://github.com/pingcap/tiflash/issues/6730) @ [<a href="https://github.com/gengliqi">ゲンリキ</a>](https://github.com/gengliqi)を計算するときにセミ結合が過剰なメモリを使用する問題を修正
    -   TiFlashログ検索が遅すぎる問題を修正[<a href="https://github.com/pingcap/tiflash/issues/6829">#6829</a>](https://github.com/pingcap/tiflash/issues/6829) @ [<a href="https://github.com/hehechen">へへへん</a>](https://github.com/hehechen)
    -   再起動を繰り返すと誤ってファイルが削除されてしまい、 TiFlashが起動できない問題を修正[<a href="https://github.com/pingcap/tiflash/issues/6486">#6486</a>](https://github.com/pingcap/tiflash/issues/6486) @ [<a href="https://github.com/JaySon-Huang">ジェイ・ソン・ファン</a>](https://github.com/JaySon-Huang)
    -   新しい列[<a href="https://github.com/pingcap/tiflash/issues/6726">#6726</a>](https://github.com/pingcap/tiflash/issues/6726) @ [<a href="https://github.com/JaySon-Huang">ジェイ・ソン・ファン</a>](https://github.com/JaySon-Huang)を追加した後にクエリを実行すると、 TiFlash がエラーを報告する可能性がある問題を修正
    -   TiFlash がIPv6 構成[<a href="https://github.com/pingcap/tiflash/issues/6734">#6734</a>](https://github.com/pingcap/tiflash/issues/6734) @ [<a href="https://github.com/ywqzzy">ywqzzy</a>](https://github.com/ywqzzy)をサポートしていない問題を修正

-   ツール

    -   バックアップと復元 (BR)

        -   PD と tidb-server の間の接続障害により、PITR バックアップの進行状況が[<a href="https://github.com/pingcap/tidb/issues/41082">#41082</a>](https://github.com/pingcap/tidb/issues/41082) @ [<a href="https://github.com/YuJuncen">ユジュンセン</a>](https://github.com/YuJuncen)進まない問題を修正
        -   PD と TiKV [<a href="https://github.com/tikv/tikv/issues/14159">#14159</a>](https://github.com/tikv/tikv/issues/14159) @ [<a href="https://github.com/YuJuncen">ユジュンセン</a>](https://github.com/YuJuncen)間の接続障害により、TiKV が PITR タスクをリッスンできない問題を修正
        -   PITR が PD クラスター[<a href="https://github.com/tikv/tikv/issues/14165">#14165</a>](https://github.com/tikv/tikv/issues/14165) @ [<a href="https://github.com/YuJuncen">ユジュンセン</a>](https://github.com/YuJuncen)の構成変更をサポートしていない問題を修正
        -   PITR 機能が CA バンドル[<a href="https://github.com/pingcap/tidb/issues/38775">#38775</a>](https://github.com/pingcap/tidb/issues/38775) @ [<a href="https://github.com/3pointer">3ポインター</a>](https://github.com/3pointer)をサポートしない問題を修正
        -   PITR バックアップ タスクが削除されると、残ったバックアップ データにより新しいタスク[<a href="https://github.com/pingcap/tidb/issues/40403">#40403</a>](https://github.com/pingcap/tidb/issues/40403) @ [<a href="https://github.com/joccau">ジョッカウ</a>](https://github.com/joccau)でデータの不整合が発生する問題を修正します。
        -   BR が`backupmeta`ファイル[<a href="https://github.com/pingcap/tidb/issues/40878">#40878</a>](https://github.com/pingcap/tidb/issues/40878) @ [<a href="https://github.com/MoCuishle28">モクイシュル28</a>](https://github.com/MoCuishle28)を解析するときにpanicを引き起こす問題を修正します。
        -   リージョンサイズ[<a href="https://github.com/pingcap/tidb/issues/36053">#36053</a>](https://github.com/pingcap/tidb/issues/36053) @ [<a href="https://github.com/YuJuncen">ユジュンセン</a>](https://github.com/YuJuncen)の取得に失敗して復元が中断される問題を修正
        -   TiDB クラスター[<a href="https://github.com/pingcap/tidb/issues/40759">#40759</a>](https://github.com/pingcap/tidb/issues/40759) @ [<a href="https://github.com/joccau">ジョッカウ</a>](https://github.com/joccau)に PITR バックアップ タスクがない場合、 `resolve lock`の頻度が高すぎる問題を修正
        -   ログ バックアップが実行されているクラスターにデータを復元すると、ログ バックアップ ファイルを復元できなくなる問題を修正します[<a href="https://github.com/pingcap/tidb/issues/40797">#40797</a>](https://github.com/pingcap/tidb/issues/40797) @ [<a href="https://github.com/Leavrth">レヴルス</a>](https://github.com/Leavrth)
        -   完全バックアップの失敗後にチェックポイントからバックアップを再開しようとすると発生するpanicの問題を修正[<a href="https://github.com/pingcap/tidb/issues/40704">#40704</a>](https://github.com/pingcap/tidb/issues/40704) @ [<a href="https://github.com/Leavrth">レヴルス</a>](https://github.com/Leavrth)
        -   PITR エラーが上書きされる問題を修正[<a href="https://github.com/pingcap/tidb/issues/40576">#40576</a>](https://github.com/pingcap/tidb/issues/40576) @ [<a href="https://github.com/Leavrth">レヴルス</a>](https://github.com/Leavrth)
        -   事前所有者と gc 所有者が異なる場合、PITR バックアップ タスクでチェックポイントが進められない問題を修正[<a href="https://github.com/pingcap/tidb/issues/41806">#41806</a>](https://github.com/pingcap/tidb/issues/41806) @ [<a href="https://github.com/joccau">ジョッカウ</a>](https://github.com/joccau)

    -   TiCDC

        -   TiKV または TiCDC ノード[<a href="https://github.com/pingcap/tiflow/issues/8174">#8174</a>](https://github.com/pingcap/tiflow/issues/8174) @ [<a href="https://github.com/hicqu">ひっくり返る</a>](https://github.com/hicqu)をスケールインまたはスケールアウトするときなど、特殊なシナリオで変更フィードが停止する可能性がある問題を修正します。
        -   REDOログ[<a href="https://github.com/pingcap/tiflow/issues/6335">#6335</a>](https://github.com/pingcap/tiflow/issues/6335) @ [<a href="https://github.com/CharlesCheung96">CharlesCheung96</a>](https://github.com/CharlesCheung96)のstorageパスで事前チェックが行われない問題を修正
        -   S3storage障害[<a href="https://github.com/pingcap/tiflow/issues/8089">#8089</a>](https://github.com/pingcap/tiflow/issues/8089) @ [<a href="https://github.com/CharlesCheung96">CharlesCheung96</a>](https://github.com/CharlesCheung96)に対して REDO ログが許容できる期間が不十分である問題を修正
        -   設定ファイル[<a href="https://github.com/pingcap/tiflow/issues/7935">#7935</a>](https://github.com/pingcap/tiflow/issues/7935) @ [<a href="https://github.com/CharlesCheung96">CharlesCheung96</a>](https://github.com/CharlesCheung96)から`transaction_atomicity`と`protocol`を更新できない問題を修正
        -   TiCDC が過度に多数のテーブル[<a href="https://github.com/pingcap/tiflow/issues/8004">#8004</a>](https://github.com/pingcap/tiflow/issues/8004) @ [<a href="https://github.com/overvenus">オーバーヴィーナス</a>](https://github.com/overvenus)をレプリケートするとチェックポイントが進められない問題を修正
        -   レプリケーション ラグが過度に高い場合に REDO ログを適用すると OOM が発生する可能性がある問題を修正[<a href="https://github.com/pingcap/tiflow/issues/8085">#8085</a>](https://github.com/pingcap/tiflow/issues/8085) @ [<a href="https://github.com/CharlesCheung96">CharlesCheung96</a>](https://github.com/CharlesCheung96)
        -   REDO ログがメタ[<a href="https://github.com/pingcap/tiflow/issues/8074">#8074</a>](https://github.com/pingcap/tiflow/issues/8074) @ [<a href="https://github.com/CharlesCheung96">CharlesCheung96</a>](https://github.com/CharlesCheung96)への書き込みを有効にするとパフォーマンスが低下する問題を修正
        -   TiCDC が大規模なトランザクション[<a href="https://github.com/pingcap/tiflow/issues/7982">#7982</a>](https://github.com/pingcap/tiflow/issues/7982) @ [<a href="https://github.com/hi-rustin">こんにちはラスティン</a>](https://github.com/hi-rustin)を分割せずにデータをレプリケートするとコンテキスト期限を超過するバグを修正
        -   PD が異常なときにチェンジフィードを一時停止すると、不正なステータス[<a href="https://github.com/pingcap/tiflow/issues/8330">#8330</a>](https://github.com/pingcap/tiflow/issues/8330) @ [<a href="https://github.com/sdojjy">スドジ</a>](https://github.com/sdojjy)が発生する問題を修正
        -   TiDB または MySQL シンクにデータをレプリケートするとき、および主キー[<a href="https://github.com/pingcap/tiflow/issues/8420">#8420</a>](https://github.com/pingcap/tiflow/issues/8420) @ [<a href="https://github.com/asddongmen">東門</a>](https://github.com/asddongmen)のない非 null の一意のインデックスを持つ列に`CHARACTER SET`が指定されているときに発生するデータの不整合を修正します。
        -   テーブルのスケジューリングとブラックホール シンク[<a href="https://github.com/pingcap/tiflow/issues/8024">#8024</a>](https://github.com/pingcap/tiflow/issues/8024) [<a href="https://github.com/pingcap/tiflow/issues/8142">#8142</a>](https://github.com/pingcap/tiflow/issues/8142) @ [<a href="https://github.com/hicqu">ひっくり返る</a>](https://github.com/hicqu)のpanicの問題を修正しました。

    -   TiDB データ移行 (DM)

        -   `binlog-schema delete`コマンドの実行に失敗する問題を修正[<a href="https://github.com/pingcap/tiflow/issues/7373">#7373</a>](https://github.com/pingcap/tiflow/issues/7373) @ [<a href="https://github.com/liumengya94">リウメンギャ94</a>](https://github.com/liumengya94)
        -   最後のbinlogがスキップされた DDL [<a href="https://github.com/pingcap/tiflow/issues/8175">#8175</a>](https://github.com/pingcap/tiflow/issues/8175) @ [<a href="https://github.com/D3Hunter">D3ハンター</a>](https://github.com/D3Hunter)である場合、チェックポイントが進められない問題を修正します。
        -   1つのテーブルに「更新」タイプと「非更新」タイプの両方の式フィルタを指定した場合、 `UPDATE`ステートメントがすべてスキップされるバグを修正[<a href="https://github.com/pingcap/tiflow/issues/7831">#7831</a>](https://github.com/pingcap/tiflow/issues/7831) @ [<a href="https://github.com/lance6716">ランス6716</a>](https://github.com/lance6716)

    -   TiDB Lightning

        -   TiDB Lightning事前チェックが、以前に失敗したインポート[<a href="https://github.com/pingcap/tidb/issues/39477">#39477</a>](https://github.com/pingcap/tidb/issues/39477) @ [<a href="https://github.com/dsdashun">dsダシュン</a>](https://github.com/dsdashun)によって残されたダーティ データを見つけられない問題を修正
        -   TiDB Lightning が分割リージョン フェーズ[<a href="https://github.com/pingcap/tidb/issues/40934">#40934</a>](https://github.com/pingcap/tidb/issues/40934) @ [<a href="https://github.com/lance6716">ランス6716</a>](https://github.com/lance6716)でパニックになる問題を修正
        -   競合解決ロジック ( `duplicate-resolution` ) によってチェックサムの不一致が生じる可能性がある問題を修正します[<a href="https://github.com/pingcap/tidb/issues/40657">#40657</a>](https://github.com/pingcap/tidb/issues/40657) @ [<a href="https://github.com/gozssky">ゴズスキー</a>](https://github.com/gozssky)
        -   並列インポート[<a href="https://github.com/pingcap/tidb/issues/40923">#40923</a>](https://github.com/pingcap/tidb/issues/40923) @ [<a href="https://github.com/lichunzhu">リチュンジュ</a>](https://github.com/lichunzhu)中に、最後の TiDB Lightning インスタンスを除くすべてのTiDB Lightningインスタンスでローカルの重複レコードが検出された場合、 TiDB Lightning が誤って競合解決をスキップする可能性がある問題を修正します。
        -   ローカル バックエンド モードでデータをインポートするときに、インポートされたターゲット テーブルの複合主キーに`auto_random`列があり、その列の値がソース データ[<a href="https://github.com/pingcap/tidb/issues/41454">#41454</a>](https://github.com/pingcap/tidb/issues/41454) @ [<a href="https://github.com/D3Hunter">D3ハンター</a>](https://github.com/D3Hunter)で指定されていない場合、ターゲット列でデータが自動的に生成されない問題を修正します。
