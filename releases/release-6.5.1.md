---
title: TiDB 6.5.1 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 6.5.1.
---

# TiDB 6.5.1 リリースノート {#tidb-6-5-1-release-notes}

発売日：2023年3月10日

TiDB バージョン: 6.5.1

クイックアクセス: [インストールパッケージ](https://www.pingcap.com/download/?version=v6.5.1#version-list)

## 互換性の変更 {#compatibility-changes}

-   2023 年 2 月 20 日以降、v6.5.1 を含む TiDB および TiDB ダッシュボードの新しいバージョンでは[TiDB リリース タイムライン](/releases/release-timeline.md)参照してください。

    -   [`tidb_enable_telemetry`](/system-variables.md#tidb_enable_telemetry-new-in-v402)システム変数のデフォルト値が`ON`から`OFF`に変更されました。
    -   TiDB [`enable-telemetry`](/tidb-configuration-file.md#enable-telemetry-new-in-v402)構成項目のデフォルト値が`true`から`false`に変更されました。
    -   PD [`enable-telemetry`](/pd-configuration-file.md#enable-telemetry)設定項目のデフォルト値が`true`から`false`に変更されます。

-   v1.11.3 以降、新しく展開されたTiUPではテレメトリ機能がデフォルトで無効になっており、使用状況情報は収集されません。 TiUP のv1.11.3 より前のバージョンから v1.11.3 以降のバージョンにアップグレードすると、テレメトリ機能はアップグレード前と同じステータスを維持します。

-   正確性の問題が発生する可能性があるため、パーティション テーブルの列タイプの変更はサポートされなくなりました。 [むじょん](https://github.com/mjonss)

-   TiKV [ステイル読み取りレイテンシーを削減する](/stale-read.md#reduce-stale-read-latency)を参照してください。

## 改善点 {#improvements}

-   TiDB

    -   v6.5.1 以降、 TiDB Operator v1.4.3 以降によってデプロイされた TiDB クラスターは IPv6 アドレスをサポートします。これは、TiDB がより大きなアドレス空間をサポートし、より優れたセキュリティとネットワーク パフォーマンスを実現できることを意味します。

        -   IPv6 アドレス指定の完全サポート: TiDB は、クライアント接続、ノード間の内部通信、外部システムとの通信を含むすべてのネットワーク接続で IPv6 アドレスの使用をサポートします。
        -   デュアルスタックのサポート: まだ IPv6 に完全に切り替える準備ができていない場合は、TiDB はデュアルスタック ネットワークもサポートします。これは、同じ TiDB クラスター内で IPv4 アドレスと IPv6 アドレスの両方を使用でき、構成によって IPv6 を優先するネットワーク展開モードを選択できることを意味します。

        IPv6 展開の詳細については、 [Kubernetes 上の TiDB ドキュメント](https://docs.pingcap.com/tidb-in-kubernetes/stable/configure-a-tidb-cluster#ipv6-support)を参照してください。

    -   TiDB クラスターの初期化時に実行される SQL スクリプトの指定をサポート[モルゴ](https://github.com/morgo)

        TiDB v6.5.1 では、新しい構成項目[ドキュメンテーション](https://docs.pingcap.com/tidb/v6.5/tidb-configuration-file#initialize-sql-file-new-in-v651)を参照してください。

    -   期限切れの領域キャッシュを定期的にクリアして、メモリリークとパフォーマンスの低下を回避します[スティックナーフ](https://github.com/sticnarf)

    -   新しい構成項目`--proxy-protocol-fallbackable`を追加して、PROXY プロトコル フォールバック モードを有効にするかどうかを制御します。このパラメータが`true`に設定されている場合、TiDB は PROXY クライアント接続および PROXY プロトコル ヘッダーなしのクライアント接続を受け入れます[ブラックティア23](https://github.com/blacktear23)

    -   Memory Tracker [wshwsh12](https://github.com/wshwsh12)の精度を向上させます。

    -   プラン キャッシュが有効にならない場合、システムはその理由を警告[qw4990](https://github.com/qw4990)として返します。

    -   範囲外の推定[時間と運命](https://github.com/time-and-fate)に対するオプティマイザ戦略を改善します。

-   TiKV

    -   1 コア未満の CPU での TiKV の起動をサポート[アンドロイドデータベース](https://github.com/andreid-db)
    -   統合読み取りプール ( `readpool.unified.max-thread-count` ) のスレッド制限を CPU クォータの 10 倍に増やし、同時実行性の高いクエリの処理を改善します[v01dstar](https://github.com/v01dstar)
    -   リージョン間のトラフィック[オーバーヴィーナス](https://github.com/overvenus)を減らすために、デフォルト値`resolved-ts.advance-ts-interval`を`"1s"`から`"20s"`に変更します。

-   TiFlash

    -   データ量が多い場合にTiFlash の起動を大幅に高速化[へへへん](https://github.com/hehechen)

-   ツール

    -   バックアップと復元 (BR)

        -   TiKV 側でのログ バックアップ ファイルのダウンロードの同時実行性を最適化し、通常のシナリオ[ユジュンセン](https://github.com/YuJuncen)での PITR のパフォーマンスを向上させます。

    -   TiCDC

        -   プルベースのシンクを有効にしてシステム スループットを最適化[こんにちはラスティン](https://github.com/hi-rustin)
        -   GCS 互換または Azure 互換のオブジェクトstorage[CharlesCheung96](https://github.com/CharlesCheung96)への REDO ログの保存のサポート
        -   MQ シンクと MySQL シンクを非同期モードで実装して、シンクのスループットを向上させます[CharlesCheung96](https://github.com/CharlesCheung96)

## バグの修正 {#bug-fixes}

-   TiDB

    -   ポイント取得クエリ[`pessimistic-auto-commit`](/tidb-configuration-file.md#pessimistic-auto-commit-new-in-v600)が有効にならない問題を修正
    -   長いセッション接続[ウィノロス](https://github.com/winoros)で`INSERT`または`REPLACE`ステートメントがpanicになる可能性がある問題を修正
    -   `auto analyze`により正常なシャットダウンに時間がかかる問題を修正[シュイファングリーンアイズ](https://github.com/xuyifangreeneyes)
    -   DDL 取り込み[タンジェンタ](https://github.com/tangenta)中にデータ競合が発生する可能性がある問題を修正
    -   インデックス[タンジェンタ](https://github.com/tangenta)を追加するとデータ競合が発生する可能性がある問題を修正
    -   テーブル[タンジェンタ](https://github.com/tangenta)に多数のリージョンがある場合、無効なリージョンキャッシュによりインデックスの追加操作が非効率になる問題を修正
    -   TiDB が初期化[定義2014](https://github.com/Defined2014)中にデッドロックする可能性がある問題を修正
    -   キー範囲[ティエンチャイアマオ](https://github.com/tiancaiamao)を構築するときに TiDB が`NULL`値を適切に処理しないため、予期しないデータが読み取られる問題を修正
    -   メモリの再利用によりシステム変数の値が誤って変更される場合がある問題を修正[ルクワンチャオ](https://github.com/lcwangchao)
    -   テーブルの主キーに`ENUM`カラム[ルクワンチャオ](https://github.com/lcwangchao)が含まれる場合、TTL タスクが失敗する問題を修正します。
    -   一意のインデックス[タンジェンタ](https://github.com/tangenta)を追加するときに TiDB がパニックになる問題を修正
    -   同じテーブルを同時に切り捨てる場合、一部の切り捨て操作が MDL によってブロックされない問題を修正します[wjhuang2016](https://github.com/wjhuang2016)
    -   動的トリミング モード[イーサール](https://github.com/Yisaer)でパーティション テーブルのグローバル バインディングが作成された後、TiDB が再起動できない問題を修正します。
    -   「カーソル読み取り」メソッドを使用してデータを読み取ると、GC [ジグアン](https://github.com/zyguan)が原因でエラーが返される場合がある問題を修正
    -   `SHOW PROCESSLIST` [ヤンケオ](https://github.com/YangKeao)の結果で`EXECUTE`情報が null になる問題を修正
    -   `globalMemoryControl`がクエリを強制終了しているときに、 `KILL`操作が[wshwsh12](https://github.com/wshwsh12)で終了しない可能性がある問題を修正します。
    -   `indexMerge`エラー[ウィンドトーカー](https://github.com/windtalker)が発生した後に TiDB がpanicになる可能性がある問題を修正
    -   `ANALYZE`ステートメントが`KILL` [徐淮嶼](https://github.com/XuHuaiyu)で終了する可能性がある問題を修正
    -   `indexMerge` [グオシャオゲ](https://github.com/guo-shaoge)で goroutine リークが発生する可能性がある問題を修正
    -   符号なし`TINYINT` / `SMALLINT` / `INT`の値を`0` [リトルフォール](https://github.com/LittleFall)より小さい`DECIMAL` / `FLOAT` / `DOUBLE`の値と比較するときに誤った結果が生じる可能性がある問題を修正
    -   `tidb_enable_reuse_chunk`を有効にするとメモリリーク[グオシャオゲ](https://github.com/guo-shaoge)が発生する可能性がある問題を修正
    -   タイムゾーン内のデータ競合によりデータインデックスの不整合が発生する可能性がある問題を修正[wjhuang2016](https://github.com/wjhuang2016)
    -   `batch cop`の実行時のスキャン詳細情報が不正確になる場合がある問題を修正[あなた06](https://github.com/you06)
    -   `cop`の同時実行数の上限が[あなた06](https://github.com/you06)に制限されない問題を修正
    -   `cursor read`の`statement context`誤って[ジグアン](https://github.com/zyguan)にキャッシュされる問題を修正
    -   メモリリークとパフォーマンスの低下を避けるために、古いリージョンキャッシュを定期的にクリーンアップします[スティックナーフ](https://github.com/sticnarf)
    -   `year <cmp> const`を含むクエリでプラン キャッシュを使用すると、間違った結果[qw4990](https://github.com/qw4990)が得られる可能性がある問題を修正します。
    -   広い範囲と大量のデータ変更を伴うクエリ時に大きな推定エラーが発生する問題を修正[時間と運命](https://github.com/time-and-fate)
    -   Plan Cache [qw4990](https://github.com/qw4990)を使用する場合、結合演算子を使用して一部の条件をプッシュダウンできない問題を修正します。
    -   IndexMerge プランが SET タイプの列[時間と運命](https://github.com/time-and-fate)に不正な範囲を生成する可能性がある問題を修正します。
    -   `int_col <cmp> decimal`条件[qw4990](https://github.com/qw4990)を処理するときにプラン キャッシュがフルスキャン プランをキャッシュする可能性がある問題を修正
    -   `int_col in (decimal...)`条件[qw4990](https://github.com/qw4990)を処理するときにプラン キャッシュがフルスキャン プランをキャッシュする可能性がある問題を修正
    -   `ignore_plan_cache`ヒントが`INSERT`ステートメント[qw4990](https://github.com/qw4990)に対して機能しない可能性がある問題を修正
    -   自動分析により TiDB の終了が妨げられる可能性がある問題を修正[シュイファングリーンアイズ](https://github.com/xuyifangreeneyes)
    -   パーティションテーブル[ウィノロス](https://github.com/winoros)の署名なし主キーに対して不正なアクセス間隔が構築される可能性がある問題を修正
    -   プラン キャッシュがシャッフル演算子をキャッシュし、誤った結果[qw4990](https://github.com/qw4990)を返す可能性がある問題を修正します。
    -   パーティション化されたテーブルにグローバル バインディングを作成すると、TiDB の起動に失敗する可能性がある問題を修正します[イーサール](https://github.com/Yisaer)
    -   低速ログ[時間と運命](https://github.com/time-and-fate)でクエリ プラン演算子が欠落する可能性がある問題を修正
    -   仮想列を持つ TopN オペレーターが誤って TiKV またはTiFlash [ドゥーシール9](https://github.com/Dousir9)にプッシュダウンすると、誤った結果が返される可能性がある問題を修正
    -   インデックス[タンジェンタ](https://github.com/tangenta)を追加する際のデータの不整合の問題を修正
    -   インデックス[タンジェンタ](https://github.com/tangenta)を追加するときに`Pessimistic lock not found`エラーが発生する問題を修正
    -   一意のインデックス[タンジェンタ](https://github.com/tangenta)を追加するときに重複キー エラーが誤って報告される問題を修正
    -   TiDB [ソロッツグ](https://github.com/solotzg)で`paging`を使用するとパフォーマンスが低下する問題を修正

-   TiKV

    -   解決された TS によりネットワーク トラフィックが増加する問題を修正[オーバーヴィーナス](https://github.com/overvenus)
    -   悲観的DML [ミョンケミンタ](https://github.com/MyonKeminta)が失敗した後の DML の実行中に、TiDB と TiKV の間のネットワーク障害によって引き起こされるデータの不整合の問題を修正しました。
    -   `const Enum`型を他の型[wshwsh12](https://github.com/wshwsh12)にキャストするときに発生するエラーを修正
    -   cop タスクのページングが不正確である問題を修正[あなた06](https://github.com/you06)
    -   `batch_cop`モード[あなた06](https://github.com/you06)で`scan_detail`フィールドが不正確になる問題を修正
    -   TiKV がRaftデータの破損を検出し、 [トニーシュクキ](https://github.com/tonyxuqqi)の再起動に失敗する可能性があるRaft Engineの潜在的なエラーを修正しました。

-   PD

    -   特定の条件下で実行`replace-down-peer`が遅くなる問題を修正[フンドゥンDM](https://github.com/HunDunDM)
    -   PD が予期せず複数の学習者をリージョン[フンドゥンDM](https://github.com/HunDunDM)に追加する可能性がある問題を修正
    -   リージョン分散タスクが予期せず冗長レプリカを生成する問題を修正します[フンドゥンDM](https://github.com/HunDunDM)
    -   `ReportMinResolvedTS` [フンドゥンDM](https://github.com/HunDunDM)の呼び出しが頻繁すぎる場合に発生する PD OOM 問題を修正します。
    -   リージョン分散によりリーダー[フンドゥンDM](https://github.com/HunDunDM)が不均一に分布する可能性がある問題を修正

-   TiFlash

    -   デカルト積[ゲンリキ](https://github.com/gengliqi)を計算するときにセミ結合が過剰なメモリを使用する問題を修正
    -   TiFlashログ検索が遅すぎる問題を修正[へへへん](https://github.com/hehechen)
    -   再起動を繰り返すと誤ってファイルが削除されてしまい、 TiFlashが起動できない問題を修正[ジェイ・ソン・ファン](https://github.com/JaySon-Huang)
    -   新しい列[ジェイ・ソン・ファン](https://github.com/JaySon-Huang)を追加した後にクエリを実行すると、 TiFlash がエラーを報告する可能性がある問題を修正
    -   TiFlash がIPv6 構成[ywqzzy](https://github.com/ywqzzy)をサポートしていない問題を修正

-   ツール

    -   バックアップと復元 (BR)

        -   PD と tidb-server の間の接続障害により、PITR バックアップの進行状況が[ユジュンセン](https://github.com/YuJuncen)進まない問題を修正
        -   PD と TiKV [ユジュンセン](https://github.com/YuJuncen)間の接続障害により、TiKV が PITR タスクをリッスンできない問題を修正
        -   PITR が PD クラスター[ユジュンセン](https://github.com/YuJuncen)の構成変更をサポートしていない問題を修正
        -   PITR 機能が CA バンドル[3ポインター](https://github.com/3pointer)をサポートしない問題を修正
        -   PITR バックアップ タスクが削除されると、残ったバックアップ データにより新しいタスク[ジョッカウ](https://github.com/joccau)でデータの不整合が発生する問題を修正します。
        -   BR が`backupmeta`ファイル[モクイシュル28](https://github.com/MoCuishle28)を解析するときにpanicを引き起こす問題を修正します。
        -   リージョンサイズ[ユジュンセン](https://github.com/YuJuncen)の取得に失敗して復元が中断される問題を修正
        -   TiDB クラスター[ジョッカウ](https://github.com/joccau)に PITR バックアップ タスクがない場合、 `resolve lock`の頻度が高すぎる問題を修正
        -   ログ バックアップが実行されているクラスターにデータを復元すると、ログ バックアップ ファイルを復元できなくなる問題を修正します[レヴルス](https://github.com/Leavrth)
        -   完全バックアップの失敗後にチェックポイントからバックアップを再開しようとすると発生するpanicの問題を修正[レヴルス](https://github.com/Leavrth)
        -   PITR エラーが上書きされる問題を修正[レヴルス](https://github.com/Leavrth)
        -   事前所有者と gc 所有者が異なる場合、PITR バックアップ タスクでチェックポイントが進められない問題を修正[ジョッカウ](https://github.com/joccau)

    -   TiCDC

        -   TiKV または TiCDC ノード[ひっくり返る](https://github.com/hicqu)をスケールインまたはスケールアウトするときなど、特殊なシナリオで変更フィードが停止する可能性がある問題を修正します。
        -   REDOログ[CharlesCheung96](https://github.com/CharlesCheung96)のstorageパスで事前チェックが行われない問題を修正
        -   S3storage障害[CharlesCheung96](https://github.com/CharlesCheung96)に対して REDO ログが許容できる期間が不十分である問題を修正
        -   設定ファイル[CharlesCheung96](https://github.com/CharlesCheung96)から`transaction_atomicity`と`protocol`を更新できない問題を修正
        -   TiCDC が過度に多数のテーブル[オーバーヴィーナス](https://github.com/overvenus)をレプリケートするとチェックポイントが進められない問題を修正
        -   レプリケーション ラグが過度に高い場合に REDO ログを適用すると OOM が発生する可能性がある問題を修正[CharlesCheung96](https://github.com/CharlesCheung96)
        -   REDO ログがメタ[CharlesCheung96](https://github.com/CharlesCheung96)への書き込みを有効にするとパフォーマンスが低下する問題を修正
        -   TiCDC が大規模なトランザクション[こんにちはラスティン](https://github.com/hi-rustin)を分割せずにデータをレプリケートするとコンテキスト期限を超過するバグを修正
        -   PD が異常なときにチェンジフィードを一時停止すると、不正なステータス[スドジ](https://github.com/sdojjy)が発生する問題を修正
        -   TiDB または MySQL シンクにデータをレプリケートするとき、および主キー[東門](https://github.com/asddongmen)のない非 null の一意のインデックスを持つ列に`CHARACTER SET`が指定されているときに発生するデータの不整合を修正します。
        -   テーブルのスケジューリングとブラックホール シンク[ひっくり返る](https://github.com/hicqu)のpanicの問題を修正しました。

    -   TiDB データ移行 (DM)

        -   `binlog-schema delete`コマンドの実行に失敗する問題を修正[リウメンギャ94](https://github.com/liumengya94)
        -   最後のbinlogがスキップされた DDL [D3ハンター](https://github.com/D3Hunter)である場合、チェックポイントが進められない問題を修正します。
        -   1つのテーブルに「更新」タイプと「非更新」タイプの両方の式フィルタを指定した場合、 `UPDATE`ステートメントがすべてスキップされるバグを修正[ランス6716](https://github.com/lance6716)

    -   TiDB Lightning

        -   TiDB Lightning事前チェックが、以前に失敗したインポート[dsダシュン](https://github.com/dsdashun)によって残されたダーティ データを見つけられない問題を修正
        -   TiDB Lightning が分割リージョン フェーズ[ランス6716](https://github.com/lance6716)でパニックになる問題を修正
        -   競合解決ロジック ( `duplicate-resolution` ) によってチェックサムの不一致が生じる可能性がある問題を修正します[ゴズスキー](https://github.com/gozssky)
        -   並列インポート[リチュンジュ](https://github.com/lichunzhu)中に、最後の TiDB Lightning インスタンスを除くすべてのTiDB Lightningインスタンスでローカルの重複レコードが検出された場合、 TiDB Lightning が誤って競合解決をスキップする可能性がある問題を修正します。
        -   ローカル バックエンド モードでデータをインポートするときに、インポートされたターゲット テーブルの複合主キーに`auto_random`列があり、その列の値がソース データ[D3ハンター](https://github.com/D3Hunter)で指定されていない場合、ターゲット列でデータが自動的に生成されない問題を修正します。
