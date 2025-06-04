---
title: TiDB 7.5.3 Release Notes
summary: TiDB 7.5.3 における互換性の変更、改善、およびバグ修正について説明します。
---

# TiDB 7.5.3 リリースノート {#tidb-7-5-3-release-notes}

発売日：2024年8月5日

TiDB バージョン: 7.5.3

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v7.5/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v7.5/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   TiDB [＃48801](https://github.com/pingcap/tidb/issues/48801) @ [ドヴェーデン](https://github.com/dveeden)でサポートされているすべてのキーワードの情報を表示するための新しいシステムテーブル[`INFORMATION_SCHEMA.KEYWORDS`](/information-schema/information-schema-keywords.md)を追加します。
-   TiKV構成項目[`server.grpc-compression-type`](/tikv-configuration-file.md#grpc-compression-type)のスコープを変更します。

    -   v7.5.3 より前の v7.5.x バージョンでは、この構成項目は TiKV ノード間の gRPC メッセージの圧縮アルゴリズムにのみ影響します。
    -   v7.5.3以降、この設定項目はTiKVからTiDBに送信されるgRPC応答メッセージの圧縮アルゴリズムにも影響します。圧縮を有効にすると、CPUリソースの消費量が増加する可能性があります[＃17176](https://github.com/tikv/tikv/issues/17176) @ [エキシウム](https://github.com/ekexium)

## 改善点 {#improvements}

-   TiDB

    -   TiFlash配置ルールを一括削除することで、パーティションテーブル[＃54068](https://github.com/pingcap/tidb/issues/54068) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)で`TRUNCATE`または`DROP`操作を実行した後のデータGCの処理速度が向上します。

-   TiFlash

    -   TLS を有効にした後に証明書を更新することでTiFlash がpanic可能性がある問題を軽減します[＃8535](https://github.com/pingcap/tiflash/issues/8535) @ [ウィンドトーカー](https://github.com/windtalker)
    -   同時実行性の高いデータ読み取り操作におけるロック競合を削減し、短いクエリのパフォーマンスを最適化します[＃9125](https://github.com/pingcap/tiflash/issues/9125) @ [ジンヘリン](https://github.com/JinheLin)

-   ツール

    -   バックアップと復元 (BR)

        -   `br log restore`サブコマンドを除き、他の`br log`サブコマンドはすべて、メモリ消費量を削減するために TiDB `domain`データ構造のロードをスキップすることをサポートしています[＃52088](https://github.com/pingcap/tidb/issues/52088) @ [リーヴルス](https://github.com/Leavrth)
        -   チェックポイントの遅延が大きい場合にログ バックアップ タスクを自動的に中止する機能をサポートし、GC の長時間のブロッキングや潜在的なクラスターの問題を回避します[＃50803](https://github.com/pingcap/tidb/issues/50803) @ [リドリスR](https://github.com/RidRisR)
        -   DNSエラーによる失敗の再試行回数を[＃53029](https://github.com/pingcap/tidb/issues/53029)から[ユジュンセン](https://github.com/YuJuncen)増やす
        -   ログバックアップの互換性テストとインデックスアクセラレーション[＃51987](https://github.com/pingcap/tidb/issues/51987) @ [リーヴルス](https://github.com/Leavrth)をカバーするPITR統合テストケースを追加します。
        -   リージョン[＃54017](https://github.com/pingcap/tidb/issues/54017)のリーダーの不在によって発生した失敗の再試行回数を[リーヴルス](https://github.com/Leavrth)に増やす
        -   環境変数[＃45551](https://github.com/pingcap/tidb/issues/45551) @ [リドリスR](https://github.com/RidRisR)による Alibaba Cloud アクセス資格情報の設定をサポート

    -   TiCDC

        -   ダウンストリームがメッセージキュー（MQ）またはクラウドstorageの場合に生のイベントを直接出力することをサポートします[＃11211](https://github.com/pingcap/tiflow/issues/11211) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)

## バグ修正 {#bug-fixes}

-   TiDB

    -   インデックス統計の読み込み時にメモリリークが発生する可能性がある問題を修正[＃54022](https://github.com/pingcap/tidb/issues/54022) @ [ハイラスティン](https://github.com/Rustin170506)
    -   `UPDATE`操作で複数テーブルシナリオ[＃53742](https://github.com/pingcap/tidb/issues/53742) @ [ホーキングレイ](https://github.com/hawkingrei)で TiDB OOM が発生する可能性がある問題を修正
    -   `GROUP BY`ステートメント内の間接プレースホルダ`?`参照が列[＃53872](https://github.com/pingcap/tidb/issues/53872) @ [qw4990](https://github.com/qw4990)を見つけられない問題を修正しました
    -   照合順序が`utf8_bin`または`utf8mb4_bin` [＃53730](https://github.com/pingcap/tidb/issues/53730) @ [エルサ0520](https://github.com/elsa0520)の場合に`LENGTH()`条件が予期せず削除される問題を修正しました
    -   科学表記法で大きすぎる数値を挿入するとエラーではなく警告が返される問題を修正し、MySQL [＃47787](https://github.com/pingcap/tidb/issues/47787) @ [qw4990](https://github.com/qw4990)と一貫性を保ちます。
    -   再帰CTEクエリが無効なポインタ[＃54449](https://github.com/pingcap/tidb/issues/54449) @ [ホーキングレイ](https://github.com/hawkingrei)を生成する可能性がある問題を修正しました
    -   重複した主キー[＃47539](https://github.com/pingcap/tidb/issues/47539) @ [定義2014](https://github.com/Defined2014)に遭遇したときに統計収集で`stats_history`テーブルが更新されない問題を修正しました
    -   クエリに非相関サブクエリと`LIMIT`句が含まれている場合、列のプルーニングが不完全になり、最適でないプラン[＃54213](https://github.com/pingcap/tidb/issues/54213) @ [qw4990](https://github.com/qw4990)になる可能性がある問題を修正しました。
    -   `HashJoin`または`IndexLookUp`演算子が`Apply`演算子[＃54005](https://github.com/pingcap/tidb/issues/54005) @ [徐淮嶼](https://github.com/XuHuaiyu)の駆動側サブノードである場合に`memTracker`切り離されないことで発生する異常に高いメモリ使用量の問題を修正しました。
    -   再帰 CTE 演算子がメモリ使用量[＃54181](https://github.com/pingcap/tidb/issues/54181) @ [グオシャオゲ](https://github.com/guo-shaoge)を誤って追跡する問題を修正しました
    -   トランザクションで使用されるメモリが複数回追跡される可能性がある問題を修正[＃53984](https://github.com/pingcap/tidb/issues/53984) @ [エキシウム](https://github.com/ekexium)
    -   `SHOW WARNINGS;`使用して警告を取得するとpanicが発生する可能性がある問題を修正[＃48756](https://github.com/pingcap/tidb/issues/48756) @ [xhebox](https://github.com/xhebox)
    -   `sql_mode=''` [＃47816](https://github.com/pingcap/tidb/issues/47816) @ [lcwangchao](https://github.com/lcwangchao)の場合に、フィールドの`UNSIGNED`型を`-1`に更新すると`0`ではなく`null`返される問題を修正しました。
    -   最初の引数が`month`で、2番目の引数が負の[＃54908](https://github.com/pingcap/tidb/issues/54908) @ [xzhangxian1008](https://github.com/xzhangxian1008)場合に`TIMESTAMPADD()`関数が無限ループに入る問題を修正しました。
    -   ハンドシェイクが完了する前に一部の接続が終了した場合に、Grafana の接続数監視メトリックが正しく表示されない問題を修正しました[＃54428](https://github.com/pingcap/tidb/issues/54428) @ [ヤンケオ](https://github.com/YangKeao)
    -   TiProxy とリソース グループ[＃54545](https://github.com/pingcap/tidb/issues/54545) @ [ヤンケオ](https://github.com/YangKeao)の使用時に各リソース グループの接続数が正しくない問題を修正しました
    -   `CREATE OR REPLACE VIEW`同時に実行すると`table doesn't exist`エラー[＃53673](https://github.com/pingcap/tidb/issues/53673) @ [接線](https://github.com/tangenta)が発生する可能性がある問題を修正
    -   データ変更操作[＃53951](https://github.com/pingcap/tidb/issues/53951) @ [qw4990](https://github.com/qw4990)を含むトランザクションで仮想列を含むテーブルをクエリすると、TiDB が誤ったクエリ結果を返す可能性がある問題を修正しました
    -   `SELECT DISTINCT CAST(col AS DECIMAL), CAST(col AS SIGNED) FROM ...`クエリを実行すると誤った結果が返される可能性がある問題を修正[＃53726](https://github.com/pingcap/tidb/issues/53726) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   オプティマイザーヒント[＃53767](https://github.com/pingcap/tidb/issues/53767) @ [ホーキングレイ](https://github.com/hawkingrei)使用時に誤った警告情報が表示される問題を修正しました
    -   不正な列タイプ`DECIMAL(0,0)`場合によっては作成される可能性がある問題を修正[＃53779](https://github.com/pingcap/tidb/issues/53779) @ [接線](https://github.com/tangenta)
    -   `memory_quota`ヒントがサブクエリ[＃53834](https://github.com/pingcap/tidb/issues/53834) @ [qw4990](https://github.com/qw4990)で機能しない可能性がある問題を修正しました
    -   JSON関連の関数がMySQLと矛盾するエラーを返す場合がある問題を修正[＃53799](https://github.com/pingcap/tidb/issues/53799) @ [ドヴェーデン](https://github.com/dveeden)
    -   特定の状況下でプランキャッシュを使用する際に、メタデータロックの不適切な使用によって異常なデータが書き込まれる可能性がある問題を修正[＃53634](https://github.com/pingcap/tidb/issues/53634) @ [ジムララ](https://github.com/zimulala)
    -   クエリ内の特定のフィルター条件により、プランナーモジュールが`invalid memory address or nil pointer dereference`エラー[＃53582](https://github.com/pingcap/tidb/issues/53582) [＃53580](https://github.com/pingcap/tidb/issues/53580) [＃53594](https://github.com/pingcap/tidb/issues/53594) [＃53603](https://github.com/pingcap/tidb/issues/53603) @ [ヤンケオ](https://github.com/YangKeao)を報告する可能性がある問題を修正しました
    -   トランザクション内のステートメントが OOM によって強制終了された後、TiDB が同じトランザクション内で次のステートメントの実行を継続すると、エラー`Trying to start aggressive locking while it's already started`が発生し、panic[＃53540](https://github.com/pingcap/tidb/issues/53540) @ [ミョンケミンタ](https://github.com/MyonKeminta)が発生する可能性がある問題を修正しました。
    -   `ALTER TABLE ... REMOVE PARTITIONING`実行すると[＃53385](https://github.com/pingcap/tidb/issues/53385) @ [ミョンス](https://github.com/mjonss)のデータ損失が発生する可能性がある問題を修正しました
    -   `?`引数を含む`CONV` `EXECUTE` `PREPARE`を複数回実行すると、誤ったクエリ結果が返される可能性がある問題を修正しました[＃53505](https://github.com/pingcap/tidb/issues/53505) @ [qw4990](https://github.com/qw4990)
    -   `auth_socket`認証プラグイン[＃54031](https://github.com/pingcap/tidb/issues/54031) @ [lcwangchao](https://github.com/lcwangchao)を使用しているときに、TiDB が認証されていないユーザーの接続を拒否できないことがある問題を修正しました。
    -   情報スキーマキャッシュミス[＃53428](https://github.com/pingcap/tidb/issues/53428) @ [crazycs520](https://github.com/crazycs520)により、古い読み取りのクエリレイテンシーが増加する問題を修正しました。
    -   `STATE`のフィールドのうち`size`番目が定義されていないため、 `INFORMATION_SCHEMA.TIDB_TRX`のテーブルの`STATE`フィールドが空になる問題を修正しました[＃53026](https://github.com/pingcap/tidb/issues/53026) @ [cfzjywxk](https://github.com/cfzjywxk)
    -   自動統計収集中にシステム変数`tidb_enable_async_merge_global_stats`と`tidb_analyze_partition_concurrency`有効にならない問題を修正[＃53972](https://github.com/pingcap/tidb/issues/53972) @ [ハイラスティン](https://github.com/Rustin170506)
    -   列のデフォルト値として`CURRENT_DATE()`使用するとクエリ結果が不正確になる問題を修正[＃53746](https://github.com/pingcap/tidb/issues/53746) @ [接線](https://github.com/tangenta)
    -   `SELECT ... FOR UPDATE` [＃54652](https://github.com/pingcap/tidb/issues/54652) @ [qw4990](https://github.com/qw4990)の間違ったポイント取得プランを再利用する問題を修正しました

-   TiKV

    -   gRPC メッセージ圧縮方式を`grpc-compression-type`で設定しても、TiKV から TiDB [＃17176](https://github.com/tikv/tikv/issues/17176) @ [エキシウム](https://github.com/ekexium)に送信されるメッセージには反映されない問題を修正しました。
    -   同時実行性の高いコプロセッサー要求により TiKV OOM [＃16653](https://github.com/tikv/tikv/issues/16653) @ [金星の上](https://github.com/overvenus)が発生する可能性がある問題を修正しました
    -   CDC とログバックアップが`advance-ts-interval`構成を使用して`check_leader`のタイムアウトを制限しないため、TiKV が正常に再起動したときに`resolved_ts`遅延が大きくなる場合がある問題を修正しました[＃17107](https://github.com/tikv/tikv/issues/17107) @ [ミョンケミンタ](https://github.com/MyonKeminta)
    -   破損したRaftデータ スナップショット[＃15292](https://github.com/tikv/tikv/issues/15292) @ [LykxSassinator](https://github.com/LykxSassinator)を適用すると TiKV が繰り返しpanic可能性がある問題を修正しました。

-   PD

    -   リソース グループ クライアントでスロットが完全に削除されず、割り当てられたトークンの数が指定された値[＃7346](https://github.com/tikv/pd/issues/7346) @ [グオシャオゲ](https://github.com/guo-shaoge)より少なくなる問題を修正しました。
    -   500 ミリ秒を超えるトークンをリクエストするとリソース グループがクォータ制限に達する問題を修正[＃8349](https://github.com/tikv/pd/issues/8349) @ [ノルーシュ](https://github.com/nolouch)
    -   リソースグループ[＃8267](https://github.com/tikv/pd/issues/8267) @ [HuSharp](https://github.com/HuSharp)のデータ競合問題を修正
    -   PD がオペレータ チェック[＃8263](https://github.com/tikv/pd/issues/8263) @ [lhy1024](https://github.com/lhy1024)中に遭遇するデータ競合問題を修正しました
    -   削除されたノードがetcdクライアント[＃8286](https://github.com/tikv/pd/issues/8286) @ [Jmポテト](https://github.com/JmPotato)の候補接続リストにまだ表示される問題を修正
    -   TiKV構成項目[`coprocessor.region-split-size`](/tikv-configuration-file.md#region-split-size) 1 MiB未満の値に設定するとPDpanic[＃8323](https://github.com/tikv/pd/issues/8323) @ [Jmポテト](https://github.com/JmPotato)が発生する問題を修正しました
    -   暗号化マネージャーが使用前に初期化されない問題を修正[＃8384](https://github.com/tikv/pd/issues/8384) @ [再帰x](https://github.com/releungx)
    -   PD構成項目[`security.redact-info-log`](/pd-configuration-file.md#redact-info-log-new-in-v50)有効になっているときにPDログが完全に編集されない問題を修正[＃8419](https://github.com/tikv/pd/issues/8419) @ [再帰x](https://github.com/releungx)
    -   ロールをリソースグループ[＃54417](https://github.com/pingcap/tidb/issues/54417) @ [Jmポテト](https://github.com/JmPotato)にバインドするときにエラーが報告されない問題を修正しました

-   TiFlash

    -   BRまたはTiDB Lightning [＃9118](https://github.com/pingcap/tiflash/issues/9118) @ [ジンヘリン](https://github.com/JinheLin)経由でデータをインポートした後、FastScanモードで多数の重複行が読み取られる可能性がある問題を修正しました。
    -   `SUBSTRING_INDEX()`関数が一部のコーナーケースでTiFlashをクラッシュさせる可能性がある問題を修正[＃9116](https://github.com/pingcap/tiflash/issues/9116) @ [wshwsh12](https://github.com/wshwsh12)
    -   TiFlashで SSL 証明書の構成を空の文字列に設定すると、誤って TLS が有効になり、 TiFlashが起動しなくなる問題を修正しました[＃9235](https://github.com/pingcap/tiflash/issues/9235) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)
    -   遅延マテリアライゼーションが有効になった後に、一部のクエリで列タイプの不一致エラーが報告される可能性がある問題を修正[＃9175](https://github.com/pingcap/tiflash/issues/9175) @ [ジンヘリン](https://github.com/JinheLin)
    -   遅延マテリアライゼーションが有効になった後、仮想生成列を含むクエリが誤った結果を返す可能性がある問題を修正[＃9188](https://github.com/pingcap/tiflash/issues/9188) @ [ジンヘリン](https://github.com/JinheLin)
    -   データベース[＃9132](https://github.com/pingcap/tiflash/issues/9132) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)にまたがる空のパーティションを持つパーティションテーブルで`RENAME TABLE ... TO ...`実行した後にTiFlash がpanic可能性がある問題を修正しました。
    -   データベースの作成直後に削除されるとTiFlash がpanic可能性がある問題を修正[＃9266](https://github.com/pingcap/tiflash/issues/9266) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)

-   ツール

    -   バックアップと復元 (BR)

        -   アドバンサー所有者の移行[＃53561](https://github.com/pingcap/tidb/issues/53561) @ [リドリスR](https://github.com/RidRisR)後にログバックアップが一時停止される可能性がある問題を修正しました
        -   復元プロセス中に複数のネストされた再試行によりBR がエラーを正しく識別できない問題を修正[＃54053](https://github.com/pingcap/tidb/issues/54053) @ [リドリスR](https://github.com/RidRisR)
        -   増分バックアップ[＃54139](https://github.com/pingcap/tidb/issues/54139) @ [3ポイントシュート](https://github.com/3pointer)中の DDL ジョブのスキャンの非効率性の問題を修正
        -   リージョンリーダー[＃17168](https://github.com/tikv/tikv/issues/17168) @ [リーヴルス](https://github.com/Leavrth)の探索の中断により、チェックポイントバックアップ中のバックアップパフォーマンスが影響を受ける問題を修正しました。
        -   ログバックアップタスクを一時停止、停止、再構築した後、タスクの状態は正常であるが、チェックポイントが[＃53047](https://github.com/pingcap/tidb/issues/53047) @ [リドリスR](https://github.com/RidRisR)に進まない問題を修正しました。
        -   `ADD INDEX`や`MODIFY COLUMN`などのバックフィルを必要とする DDL が、増分リストア[＃54426](https://github.com/pingcap/tidb/issues/54426) @ [3ポイントシュート](https://github.com/3pointer)中に正しく回復されない可能性がある問題を修正しました。

    -   TiCDC

        -   `UPDATE`イベントを[＃11402](https://github.com/pingcap/tiflow/issues/11402) @ [3エースショーハンド](https://github.com/3AceShowHand)に分割した後、チェックサムが正しく`0`に設定されない問題を修正しました。
        -   下流の Kafka にアクセスできない場合にプロセッサモジュールがスタックする可能性がある問題を修正[＃11340](https://github.com/pingcap/tiflow/issues/11340) @ [アズドンメン](https://github.com/asddongmen)

    -   Dumpling

        -   テーブルとビューを同時にエクスポートするとDumpling がエラーを報告する問題を修正[＃53682](https://github.com/pingcap/tidb/issues/53682) @ [接線](https://github.com/tangenta)
