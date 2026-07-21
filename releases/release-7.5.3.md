---
title: TiDB 7.5.3 Release Notes
summary: TiDB 7.5.3 における互換性の変更、改善、およびバグ修正について説明します。
---

# TiDB 7.5.3 リリースノート {#tidb-7-5-3-release-notes}

発売日：2024年8月5日

TiDB バージョン: 7.5.3

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v7.5/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v7.5/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   TiDB でサポートされているすべてのキーワードの情報を表示するための新しいシステムテーブル[`INFORMATION_SCHEMA.KEYWORDS`](/information-schema/information-schema-keywords.md)を追加します。 [＃48801](https://github.com/pingcap/tidb/issues/48801) @ [dveeden](https://github.com/dveeden)
-   TiKV構成項目[`server.grpc-compression-type`](/tikv-configuration-file.md#grpc-compression-type)のスコープを変更します。

    -   v7.5.3 より前の v7.5.x バージョンでは、この構成項目は TiKV ノード間の gRPC メッセージの圧縮アルゴリズムにのみ影響します。
    -   v7.5.3以降、この設定項目はTiKVからTiDBに送信されるgRPC応答メッセージの圧縮アルゴリズムにも影響します。圧縮を有効にすると、CPUリソースの消費量が増加する可能性があります[＃17176](https://github.com/tikv/tikv/issues/17176) @ [ekexium](https://github.com/ekexium)

## 改善点 {#improvements}

-   TiDB

    -   TiFlash配置ルールを一括削除することで、パーティションテーブルで`TRUNCATE`または`DROP`操作を実行した後のデータGCの処理速度が向上します。 [＃54068](https://github.com/pingcap/tidb/issues/54068) @ [Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)

-   TiFlash

    -   TLS を有効にした後に証明書を更新することでTiFlash がpanic可能性がある問題を軽減します[＃8535](https://github.com/pingcap/tiflash/issues/8535) @ [windtalker](https://github.com/windtalker)
    -   同時実行性の高いデータ読み取り操作におけるロック競合を減らし、短いクエリのパフォーマンスを最適化します[＃9125](https://github.com/pingcap/tiflash/issues/9125) @ [JinheLin](https://github.com/JinheLin)

-   ツール

    -   Backup & Restore (BR)

        -   `br log restore`サブコマンドを除き、他の`br log`サブコマンドはすべて、メモリ消費量を削減するために TiDB `domain`データ構造のロードをスキップすることをサポートしています[＃52088](https://github.com/pingcap/tidb/issues/52088) @ [Leavrth](https://github.com/Leavrth)
        -   チェックポイントの遅延が大きい場合にログ バックアップ タスクを自動的に中止し、GC の長時間のブロッキングや潜在的なクラスターの問題を回避することをサポートします[＃50803](https://github.com/pingcap/tidb/issues/50803) @ [RidRisR](https://github.com/RidRisR)
        -   DNSエラーによる失敗の再試行回数を[＃53029](https://github.com/pingcap/tidb/issues/53029) / @ [YuJuncen](https://github.com/YuJuncen)に増やす
        -   ログバックアップの互換性テストとインデックスアクセラレーションの追加をカバーするPITR統合テストケースを追加します。 [＃51987](https://github.com/pingcap/tidb/issues/51987) @ [Leavrth](https://github.com/Leavrth)
        -   リージョンのリーダー不在による失敗の再試行回数を@ [Leavrth](https://github.com/Leavrth)に増やす [＃54017](https://github.com/pingcap/tidb/issues/54017)
        -   環境変数を介した Alibaba Cloud アクセス資格情報の設定をサポート [＃45551](https://github.com/pingcap/tidb/issues/45551) @ [RidRisR](https://github.com/RidRisR)

    -   TiCDC

        -   ダウンストリームがメッセージキュー（MQ）またはクラウドストレージの場合、生のイベントを直接出力することをサポート[＃11211](https://github.com/pingcap/tiflow/issues/11211) @ [CharlesCheung96](https://github.com/CharlesCheung96)

## バグ修正 {#bug-fixes}

-   TiDB

    -   インデックス統計の読み込み時にメモリリークが発生する可能性がある問題を修正[＃54022](https://github.com/pingcap/tidb/issues/54022) @ [Rustin170506](https://github.com/Rustin170506)
    -   `UPDATE`操作で複数テーブルシナリオで TiDB OOM が発生する可能性がある問題を修正 [＃53742](https://github.com/pingcap/tidb/issues/53742) @ [hawkingrei](https://github.com/hawkingrei)
    -   `GROUP BY`ステートメント内の間接プレースホルダ`?`参照が列を見つけられない問題を修正しました [＃53872](https://github.com/pingcap/tidb/issues/53872) @ [qw4990](https://github.com/qw4990)
    -   照合順序が`utf8_bin`または`utf8mb4_bin` の場合に`LENGTH()`条件が予期せず削除される問題を修正しました [＃53730](https://github.com/pingcap/tidb/issues/53730) @ [elsa0520](https://github.com/elsa0520)
    -   科学表記法で大きすぎる数値を挿入するとエラーではなく警告が返される問題を修正し、MySQL と一貫性を保ちます。 [＃47787](https://github.com/pingcap/tidb/issues/47787) @ [qw4990](https://github.com/qw4990)
    -   再帰CTEクエリが無効なポインタを生成する可能性がある問題を修正しました [＃54449](https://github.com/pingcap/tidb/issues/54449) @ [hawkingrei](https://github.com/hawkingrei)
    -   重複する主キーに遭遇したときに統計収集で`stats_history`テーブルが更新されない問題を修正しました [＃47539](https://github.com/pingcap/tidb/issues/47539) @ [Defined2014](https://github.com/Defined2014)
    -   クエリに非相関サブクエリと`LIMIT`句が含まれている場合、列のプルーニングが不完全になり、最適でないプランになる可能性がある問題を修正しました。 [＃54213](https://github.com/pingcap/tidb/issues/54213) @ [qw4990](https://github.com/qw4990)
    -   `HashJoin`または`IndexLookUp`演算子が`Apply`演算子の駆動側サブノードである場合に`memTracker`切り離されないことで発生する異常に高いメモリ使用量の問題を修正しました。 [＃54005](https://github.com/pingcap/tidb/issues/54005) @ [XuHuaiyu](https://github.com/XuHuaiyu)
    -   再帰CTE演算子がメモリ使用量を誤って追跡する問題を修正しました [＃54181](https://github.com/pingcap/tidb/issues/54181) @ [guo-shaoge](https://github.com/guo-shaoge)
    -   トランザクションで使用されるメモリが複数回追跡される可能性がある問題を修正[＃53984](https://github.com/pingcap/tidb/issues/53984) @ [ekexium](https://github.com/ekexium)
    -   `SHOW WARNINGS;`を使用して警告を取得するとpanicが発生する可能性がある問題を修正しました [＃48756](https://github.com/pingcap/tidb/issues/48756) @ [xhebox](https://github.com/xhebox)
    -   `sql_mode=''` の場合に、フィールドの`UNSIGNED`型を`-1`に更新すると`0`ではなく`null`が返される問題を修正しました。 [＃47816](https://github.com/pingcap/tidb/issues/47816) @ [lcwangchao](https://github.com/lcwangchao)
    -   最初の引数が`month`で、2番目の引数が負の場合に`TIMESTAMPADD()`関数が無限ループに入る問題を修正しました。 [＃54908](https://github.com/pingcap/tidb/issues/54908) @ [xzhangxian1008](https://github.com/xzhangxian1008)
    -   ハンドシェイクが完了する前に一部の接続が終了した場合に、Grafana の接続数監視メトリックが正しくない問題を修正しました[＃54428](https://github.com/pingcap/tidb/issues/54428) @ [YangKeao](https://github.com/YangKeao)
    -   TiProxy とリソース グループを使用するときに、各リソース グループの接続数が正しくない問題を修正しました。 [＃54545](https://github.com/pingcap/tidb/issues/54545) @ [YangKeao](https://github.com/YangKeao)
    -   `CREATE OR REPLACE VIEW`同時に実行すると`table doesn't exist`エラーが発生する可能性がある問題を修正 [＃53673](https://github.com/pingcap/tidb/issues/53673) @ [tangenta](https://github.com/tangenta)
    -   データ変更操作を含むトランザクションで仮想列を持つテーブルをクエリすると、TiDB が誤ったクエリ結果を返す可能性がある問題を修正しました [＃53951](https://github.com/pingcap/tidb/issues/53951) @ [qw4990](https://github.com/qw4990)
    -   `SELECT DISTINCT CAST(col AS DECIMAL), CAST(col AS SIGNED) FROM ...`クエリを実行すると誤った結果が返される可能性がある問題を修正[＃53726](https://github.com/pingcap/tidb/issues/53726) @ [hawkingrei](https://github.com/hawkingrei)
    -   オプティマイザーヒント使用時に誤った警告情報が表示される問題を修正しました [＃53767](https://github.com/pingcap/tidb/issues/53767) @ [hawkingrei](https://github.com/hawkingrei)
    -   場合によっては無効な列タイプ`DECIMAL(0,0)`が作成される可能性がある問題を修正[＃53779](https://github.com/pingcap/tidb/issues/53779) @ [tangenta](https://github.com/tangenta)
    -   `memory_quota`ヒントがサブクエリで機能しない可能性がある問題を修正しました [＃53834](https://github.com/pingcap/tidb/issues/53834) @ [qw4990](https://github.com/qw4990)
    -   JSON関連の関数がMySQLと矛盾するエラーを返す場合がある問題を修正[＃53799](https://github.com/pingcap/tidb/issues/53799) @ [dveeden](https://github.com/dveeden)
    -   特定の状況下でプランキャッシュを使用する際に、メタデータロックの不適切な使用によって異常なデータが書き込まれる可能性がある問題を修正しました[＃53634](https://github.com/pingcap/tidb/issues/53634) @ [zimulala](https://github.com/zimulala)
    -   クエリ内の特定のフィルター条件により、プランナーモジュールが`invalid memory address or nil pointer dereference`エラー[＃53582](https://github.com/pingcap/tidb/issues/53582) [＃53580](https://github.com/pingcap/tidb/issues/53580) を報告する可能性がある問題を修正しました [＃53603](https://github.com/pingcap/tidb/issues/53603) @ [YangKeao](https://github.com/YangKeao) [＃53594](https://github.com/pingcap/tidb/issues/53594)
    -   トランザクション内のステートメントが OOM によって強制終了された後、TiDB が同じトランザクション内で次のステートメントの実行を継続すると、エラー`Trying to start aggressive locking while it's already started`が発生し、panicが発生する可能性がある問題を修正しました。 [＃53540](https://github.com/pingcap/tidb/issues/53540) @ [MyonKeminta](https://github.com/MyonKeminta)
    -   `ALTER TABLE ... REMOVE PARTITIONING`実行するとでデータが失われる可能性がある問題を修正 [＃53385](https://github.com/pingcap/tidb/issues/53385) @ [mjonss](https://github.com/mjonss)
    -   `?`の引数を含む`CONV`の式を持つ`PREPARE` `EXECUTE`ステートメントを複数回実行すると、誤ったクエリ結果が返される可能性がある問題を修正しました[＃53505](https://github.com/pingcap/tidb/issues/53505) @ [qw4990](https://github.com/qw4990)
    -   `auth_socket`認証プラグインを使用しているときに、TiDB が認証されていないユーザーの接続を拒否できないことがある問題を修正しました。 [＃54031](https://github.com/pingcap/tidb/issues/54031) @ [lcwangchao](https://github.com/lcwangchao)
    -   情報スキーマキャッシュミスにより、古い読み取りのクエリレイテンシーが増加する問題を修正しました。 [＃53428](https://github.com/pingcap/tidb/issues/53428) @ [crazycs520](https://github.com/crazycs520)
    -   `STATE`フィールドのうち`size`が定義されていないため、 `INFORMATION_SCHEMA.TIDB_TRX`テーブルの`STATE`フィールドが空になる問題を修正しました[＃53026](https://github.com/pingcap/tidb/issues/53026) @ [cfzjywxk](https://github.com/cfzjywxk)
    -   自動統計収集中にシステム変数`tidb_enable_async_merge_global_stats`と`tidb_analyze_partition_concurrency`有効にならない問題を修正[＃53972](https://github.com/pingcap/tidb/issues/53972) @ [Rustin170506](https://github.com/Rustin170506)
    -   列のデフォルト値として`CURRENT_DATE()`使用すると、クエリ結果が正しくなくなる問題を修正しました [＃53746](https://github.com/pingcap/tidb/issues/53746) @ [tangenta](https://github.com/tangenta)
    -   `SELECT ... FOR UPDATE` の間違ったPointGetプランを再利用する問題を修正しました [＃54652](https://github.com/pingcap/tidb/issues/54652) @ [qw4990](https://github.com/qw4990)

-   TiKV

    -   gRPC メッセージ圧縮方式を`grpc-compression-type`で設定しても、TiKV から TiDB に送信されるメッセージには反映されない問題を修正しました。 [＃17176](https://github.com/tikv/tikv/issues/17176) @ [ekexium](https://github.com/ekexium)
    -   同時実行性の高いコプロセッサー要求により TiKV OOM が発生する可能性がある問題を修正しました [＃16653](https://github.com/tikv/tikv/issues/16653) @ [overvenus](https://github.com/overvenus)
    -   CDC とログバックアップが`advance-ts-interval`構成を使用して`check_leader`のタイムアウトを制限しないため、TiKV が正常に再起動したときに`resolved_ts`遅延が大きくなる場合がある問題を修正しました[＃17107](https://github.com/tikv/tikv/issues/17107) @ [MyonKeminta](https://github.com/MyonKeminta)
    -   破損したRaftデータ スナップショットを適用すると TiKV が繰り返しpanic可能性がある問題を修正しました。 [＃15292](https://github.com/tikv/tikv/issues/15292) @ [LykxSassinator](https://github.com/LykxSassinator)

-   PD

    -   リソース グループ クライアントでスロットが完全に削除されず、割り当てられたトークンの数が指定された値より少なくなる問題を修正しました。 [＃7346](https://github.com/tikv/pd/issues/7346) @ [guo-shaoge](https://github.com/guo-shaoge)
    -   500 ミリ秒を超えるトークンをリクエストするとリソース グループがクォータ制限に達する問題を修正[＃8349](https://github.com/tikv/pd/issues/8349) @ [nolouch](https://github.com/nolouch)
    -   リソースグループのデータ競合問題を修正 [＃8267](https://github.com/tikv/pd/issues/8267) @ [HuSharp](https://github.com/HuSharp)
    -   PD がオペレータ チェック中に遭遇するデータ競合問題を修正しました [＃8263](https://github.com/tikv/pd/issues/8263) @ [lhy1024](https://github.com/lhy1024)
    -   削除されたノードがetcdクライアントの候補接続リストにまだ表示される問題を修正 [＃8286](https://github.com/tikv/pd/issues/8286) @ [JmPotato](https://github.com/JmPotato)
    -   TiKV構成項目[`coprocessor.region-split-size`](/tikv-configuration-file.md#region-split-size) 1 MiB未満の値に設定するとPD panicが発生する問題を修正しました [＃8323](https://github.com/tikv/pd/issues/8323) @ [JmPotato](https://github.com/JmPotato)
    -   暗号化マネージャーが使用前に初期化されない問題を修正[＃8384](https://github.com/tikv/pd/issues/8384) @ [releungx](https://github.com/releungx)
    -   PD構成項目[`security.redact-info-log`](/pd-configuration-file.md#redact-info-log-new-in-v50)が有効になっているときにPDログが完全に編集されない問題を修正[＃8419](https://github.com/tikv/pd/issues/8419) @ [releungx](https://github.com/releungx)
    -   ロールをリソースグループにバインドするときにエラーが報告されない問題を修正しました [＃54417](https://github.com/pingcap/tidb/issues/54417) @ [JmPotato](https://github.com/JmPotato)

-   TiFlash

    -   BRまたはTiDB Lightning 経由でデータをインポートした後、FastScanモードで多数の重複行が読み取られる可能性がある問題を修正しました。 [＃9118](https://github.com/pingcap/tiflash/issues/9118) @ [JinheLin](https://github.com/JinheLin)
    -   `SUBSTRING_INDEX()`関数が一部のコーナーケースでTiFlash のクラッシュを引き起こす可能性がある問題を修正[＃9116](https://github.com/pingcap/tiflash/issues/9116) @ [wshwsh12](https://github.com/wshwsh12)
    -   TiFlashで SSL 証明書の構成を空の文字列に設定すると、誤って TLS が有効になり、 TiFlash が起動しなくなる問題を修正しました[＃9235](https://github.com/pingcap/tiflash/issues/9235) @ [JaySon-Huang](https://github.com/JaySon-Huang)
    -   遅延マテリアライゼーションが有効になった後に、一部のクエリで列タイプの不一致エラーが報告される可能性がある問題を修正[＃9175](https://github.com/pingcap/tiflash/issues/9175) @ [JinheLin](https://github.com/JinheLin)
    -   遅延マテリアライゼーションが有効になった後、仮想生成列を含むクエリが誤った結果を返す可能性がある問題を修正[＃9188](https://github.com/pingcap/tiflash/issues/9188) @ [JinheLin](https://github.com/JinheLin)
    -   データベースにまたがる空のパーティションを持つパーティションテーブルで`RENAME TABLE ... TO ...`実行した後にTiFlash がpanic可能性がある問題を修正しました。 [＃9132](https://github.com/pingcap/tiflash/issues/9132) @ [JaySon-Huang](https://github.com/JaySon-Huang)
    -   データベースが作成直後に削除されるとTiFlash がpanic可能性がある問題を修正[＃9266](https://github.com/pingcap/tiflash/issues/9266) @ [JaySon-Huang](https://github.com/JaySon-Huang)

-   ツール

    -   Backup & Restore (BR)

        -   アドバンサーオーナーの移行後にログバックアップが一時停止される可能性がある問題を修正しました [＃53561](https://github.com/pingcap/tidb/issues/53561) @ [RidRisR](https://github.com/RidRisR)
        -   復元プロセス中に複数のネストされた再試行によりBR がエラーを正しく識別できない問題を修正[＃54053](https://github.com/pingcap/tidb/issues/54053) @ [RidRisR](https://github.com/RidRisR)
        -   増分バックアップ中の DDL ジョブのスキャンの非効率性の問題を修正 [＃54139](https://github.com/pingcap/tidb/issues/54139) @ [3pointer](https://github.com/3pointer)
        -   リージョンリーダーの探索の中断により、チェックポイントバックアップ中のバックアップパフォーマンスが影響を受ける問題を修正しました。 [＃17168](https://github.com/tikv/tikv/issues/17168) @ [Leavrth](https://github.com/Leavrth)
        -   ログバックアップタスクを一時停止、停止、再構築した後、タスクの状態は正常であるが、チェックポイントがに進まない問題を修正しました。 [＃53047](https://github.com/pingcap/tidb/issues/53047) @ [RidRisR](https://github.com/RidRisR)
        -   `ADD INDEX`や`MODIFY COLUMN`などのバックフィルを必要とする DDL が、増分リストア中に正しく回復されない可能性がある問題を修正しました。 [＃54426](https://github.com/pingcap/tidb/issues/54426) @ [3pointer](https://github.com/3pointer)

    -   TiCDC

        -   `UPDATE`イベントをに分割した後、チェックサムが正しく`0`に設定されない問題を修正しました。 [＃11402](https://github.com/pingcap/tiflow/issues/11402) @ [3AceShowHand](https://github.com/3AceShowHand)
        -   下流の Kafka にアクセスできない場合にプロセッサモジュールがスタックする可能性がある問題を修正[＃11340](https://github.com/pingcap/tiflow/issues/11340) @ [asddongmen](https://github.com/asddongmen)

    -   Dumpling

        -   テーブルとビューを同時にエクスポートするとDumpling がエラーを報告する問題を修正[＃53682](https://github.com/pingcap/tidb/issues/53682) @ [tangenta](https://github.com/tangenta)
