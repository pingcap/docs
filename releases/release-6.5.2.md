---
title: TiDB 6.5.2 Release Notes
summary: TiDB 6.5.2 における互換性の変更、改善、およびバグ修正について説明します。
---

# TiDB 6.5.2 リリースノート {#tidb-6-5-2-release-notes}

発売日：2023年4月21日

TiDB バージョン: 6.5.2

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   TiCDCは、Avro [＃8490](https://github.com/pingcap/tiflow/issues/8490) @ [3エースショーハンド](https://github.com/3AceShowHand)で`FLOAT`データのエンコードが正しくない問題を修正しました。

    TiCDC クラスターを v6.5.2 またはそれ以降の v6.5.x バージョンにアップグレードする際、Avro を使用してレプリケートされたテーブルに`FLOAT`データ型が含まれている場合は、アップグレード前に Confluent Schema Registry の互換性ポリシーを手動で`None`に調整し、changefeed がスキーマを正常に更新できるようにする必要があります。そうしないと、アップグレード後に changefeed がスキーマを更新できず、エラー状態になります。

-   パーティションテーブルをstorageサービスにレプリケーションする際にデータ損失が発生する可能性がある問題を修正するため、TiCDC [`sink.enable-partition-separator`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)構成項目のデフォルト値が`false`から`true`に変更されました。これは、テーブル内のパーティションがデフォルトで別々のディレクトリに保存されることを意味します。データ損失の問題を回避するため、この値は`true`のままにしておくことをお勧めします[＃8724](https://github.com/pingcap/tiflow/issues/8724) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)

## 改善点 {#improvements}

-   TiDB

    -   プリペアドプランキャッシュ[＃42125](https://github.com/pingcap/tidb/issues/42125) @ [qw4990](https://github.com/qw4990)で`BatchPointGet`実行プランのキャッシュをサポート
    -   インデックス結合[＃40505](https://github.com/pingcap/tidb/issues/40505) @ [イーサール](https://github.com/Yisaer)より多くの SQL 形式をサポート
    -   一部のインデックスマージリーダーのログレベルを`"info"`から`"debug"` [＃41949](https://github.com/pingcap/tidb/issues/41949) @ [イービン87](https://github.com/yibin87)に変更します
    -   範囲パーティションテーブルに Limit を設定した`distsql_concurrency`設定を最適化して、クエリのレイテンシー[＃41480](https://github.com/pingcap/tidb/issues/41480) @ [あなた06](https://github.com/you06)を削減します。

-   TiFlash

    -   TiFlash読み取り時のタスク スケジューリングの CPU 消費を削減[＃6495](https://github.com/pingcap/tiflash/issues/6495) @ [ジンヘリン](https://github.com/JinheLin)
    -   デフォルト設定[＃7272](https://github.com/pingcap/tiflash/issues/7272) @ [そよ風のような](https://github.com/breezewish)でBRおよびTiDB LightningからTiFlashへのデータインポートのパフォーマンスを向上

-   ツール

    -   TiCDC

        -   TiCDC オープン API v2.0 [＃8743](https://github.com/pingcap/tiflow/issues/8743) @ [スドジ](https://github.com/sdojjy)をリリース
        -   TiCDC の OOM 問題を防ぐために`gomemlimit`を導入する[＃8675](https://github.com/pingcap/tiflow/issues/8675) @ [アミャンフェイ](https://github.com/amyangfei)
        -   `UPDATE`ステートメントを[＃8057](https://github.com/pingcap/tiflow/issues/8057) [アミャンフェイ](https://github.com/amyangfei)つ実行するシナリオでは、マルチステートメントアプローチを使用してレプリケーションのパフォーマンスを最適化します。
        -   災害復旧シナリオにおけるスループットの向上とRTOの短縮のために、REDOアプライヤでのトランザクション分割をサポートする[＃8318](https://github.com/pingcap/tiflow/issues/8318) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)
        -   REDOログ[＃8361](https://github.com/pingcap/tiflow/issues/8361) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)へのDDLイベントの適用をサポート

    -   TiDB Lightning

        -   BOM ヘッダー[＃40744](https://github.com/pingcap/tidb/issues/40744) @ [dsdashun](https://github.com/dsdashun)を含む CSV データファイルのインポートをサポート

## バグ修正 {#bug-fixes}

-   TiDB
    -   キャッシュテーブルに新しい列が追加された後、列[＃42928](https://github.com/pingcap/tidb/issues/42928) @ [lqs](https://github.com/lqs)のデフォルト値ではなく値が`NULL`なる問題を修正しました。
    -   多数のパーティションとTiFlashレプリカ[＃42940](https://github.com/pingcap/tidb/issues/42940) @ [ミョンス](https://github.com/mjonss)を持つパーティション テーブルに対して`TRUNCATE TABLE`実行するときに書き込み競合によって発生する DDL 再試行の問題を修正しました。
    -   `DROP TABLE`操作が実行されているときに`ADMIN SHOW DDL JOBS`結果にテーブル名が表示されない問題を修正[＃42268](https://github.com/pingcap/tidb/issues/42268) @ [天菜まお](https://github.com/tiancaiamao)
    -   cgroup 情報の読み取りエラーにより、TiDBサーバーが起動できない問題を修正しました。エラー メッセージは「cgroup v1 からファイルメモリ.stat を読み取れません: /sys/メモリ.stat をオープンすると、そのようなファイルまたはディレクトリが見つかりません」です[＃42659](https://github.com/pingcap/tidb/issues/42659) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   DDLデータバックフィル[＃24427](https://github.com/pingcap/tidb/issues/24427) @ [ミョンス](https://github.com/mjonss)を実行するときにトランザクションで頻繁に発生する書き込み競合を修正
    -   実行プラン[＃41622](https://github.com/pingcap/tidb/issues/41622) @ [天菜まお](https://github.com/tiancaiamao)を生成する際に不整合な InfoSchema が取得され、TiDBpanicが発生する問題を修正しました。
    -   DDLを使用して浮動小数点型を変更し、長さを変更せずに小数点以下の桁数を減らしても、古いデータが同じままになる問題を修正しました[＃41281](https://github.com/pingcap/tidb/issues/41281) @ [ジムララ](https://github.com/zimulala)
    -   トランザクション内で`PointUpdate`実行した後、TiDB が`SELECT`文[＃28011](https://github.com/pingcap/tidb/issues/28011) @ [ジグアン](https://github.com/zyguan)に対して誤った結果を返す問題を修正しました。
    -   カーソルフェッチを使用し、実行、フェッチ、およびクローズの間に他のステートメントを実行すると、フェッチおよびクローズコマンドが誤った結果を返したり、TiDB がpanicたりする可能性がある問題を修正しました[＃40094](https://github.com/pingcap/tidb/issues/40094) @ [ヤンケオ](https://github.com/YangKeao)
    -   `INSERT IGNORE`と`REPLACE`ステートメントが値[＃42121](https://github.com/pingcap/tidb/issues/42121) @ [ジグアン](https://github.com/zyguan)を変更しないキーをロックしない問題を修正しました
    -   実行中にTiFlash が生成された列に対してエラーを報告する問題を修正[＃40663](https://github.com/pingcap/tidb/issues/40663) @ [グオシャオゲ](https://github.com/guo-shaoge)
    -   単一のSQL文に異なるパーティションテーブルが出現した場合にTiDBが誤った結果を生成する可能性がある問題を修正[＃42135](https://github.com/pingcap/tidb/issues/42135) @ [ミョンス](https://github.com/mjonss)
    -   準備済みプランキャッシュが有効な場合にフルインデックススキャンでエラーが発生する可能性がある問題を修正[＃42150](https://github.com/pingcap/tidb/issues/42150) @ [fzzf678](https://github.com/fzzf678)
    -   準備プランキャッシュが有効な場合に IndexMerge が誤った結果を生成する可能性がある問題を修正[＃41828](https://github.com/pingcap/tidb/issues/41828) @ [qw4990](https://github.com/qw4990)
    -   `max_prepared_stmt_count`の設定が[＃39735](https://github.com/pingcap/tidb/issues/39735)で[xuyifangreeneyes](https://github.com/xuyifangreeneyes)に反映されない問題を修正
    -   グローバルメモリ制御が、メモリ使用量が`tidb_server_memory_limit_sess_min_size` [＃42662](https://github.com/pingcap/tidb/issues/42662) @ [徐淮嶼](https://github.com/XuHuaiyu)未満の SQL 文を誤って強制終了する可能性がある問題を修正しました。
    -   パーティションテーブル[＃40596](https://github.com/pingcap/tidb/issues/40596) @ [天菜まお](https://github.com/tiancaiamao)の動的トリミングモードでインデックス結合によりpanicが発生する可能性がある問題を修正しました。

-   TiKV

    -   TiKVがcgroupパス[＃14538](https://github.com/tikv/tikv/issues/14538) @ [スペードA-タン](https://github.com/SpadeA-Tang)を処理するときに`:`文字目を正しく解析しない問題を修正しました

-   PD

    -   PD が予期せず複数の学習者をリージョン[＃5786](https://github.com/tikv/pd/issues/5786) @ [ハンドゥンDM](https://github.com/HunDunDM)に追加する可能性がある問題を修正しました。
    -   配置ルールの切り替えにより、リーダー[＃6195](https://github.com/tikv/pd/issues/6195) @ [バッファフライ](https://github.com/bufferflies)の分布が不均等になる可能性がある問題を修正しました。

-   TiFlash

    -   TiFlashが生成された列[＃6801](https://github.com/pingcap/tiflash/issues/6801) @ [グオシャオゲ](https://github.com/guo-shaoge)を認識できない問題を修正
    -   特定のケースで小数点以下の桁が切り上げられない問題を修正[＃7022](https://github.com/pingcap/tiflash/issues/7022) @ [リトルフォール](https://github.com/LittleFall)
    -   特定のケースで[＃6994](https://github.com/pingcap/tiflash/issues/6994) @ [ウィンドトーカー](https://github.com/windtalker) 10 進キャストが誤って切り上げられる問題を修正しました
    -   新しい照合順序[＃6807](https://github.com/pingcap/tiflash/issues/6807) @ [xzhangxian1008](https://github.com/xzhangxian1008)を有効にした後に TopN/Sort 演算子が誤った結果を生成する問題を修正しました
    -   TiCDC の非互換性によるTiFlashプロセス障害の問題を修正[＃7212](https://github.com/pingcap/tiflash/issues/7212) @ [ホンユニャン](https://github.com/hongyunyan)

-   ツール

    -   バックアップと復元 (BR)

        -   TiDBクラスタ[＃40759](https://github.com/pingcap/tidb/issues/40759) @ [ジョッカウ](https://github.com/joccau)にPITRバックアップタスクがない場合に頻度`resolve lock`が高すぎる問題を修正
        -   PITRリカバリプロセス[＃42001](https://github.com/pingcap/tidb/issues/42001) @ [ジョッカウ](https://github.com/joccau)中に分割リージョンの再試行の待機時間が不十分になる問題を修正

    -   TiCDC

        -   TiCDCがオブジェクトstorage[＃8581](https://github.com/pingcap/tiflow/issues/8581) @ [チャールズ・チュン96](https://github.com/CharlesCheung96) @ [ハイラスティン](https://github.com/Rustin170506)にデータを複製するときにパーティションセパレーターが機能しない問題を修正しました
        -   TiCDC がオブジェクトstorage[＃8256](https://github.com/pingcap/tiflow/issues/8256) @ [ジャオシンユ](https://github.com/zhaoxinyu)にデータを複製するときにテーブル スケジューリングによってデータ損失が発生する可能性がある問題を修正しました。
        -   非再入可能DDL文[＃8662](https://github.com/pingcap/tiflow/issues/8662) @ [ヒック](https://github.com/hicqu)によりレプリケーションが停止する問題を修正
        -   TiCDC がオブジェクトstorage[＃8666](https://github.com/pingcap/tiflow/issues/8666) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)にデータを複製するときに、TiCDC スケーリングによってデータ損失が発生する可能性がある問題を修正しました。
        -   `db sorter`のメモリ使用量が`cgroup memory limit` [＃8588](https://github.com/pingcap/tiflow/issues/8588) @ [アミャンフェイ](https://github.com/amyangfei)で制御されない問題を修正
        -   Redo ログ[＃8591](https://github.com/pingcap/tiflow/issues/8591) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)の適用中に特別なケースでデータ損失が発生する可能性がある問題を修正しました
        -   `db sorter`のメモリ使用量が`cgroup memory limit` [＃8588](https://github.com/pingcap/tiflow/issues/8588) @ [アミャンフェイ](https://github.com/amyangfei)で制御されない問題を修正
        -   データレプリケーション中の`UPDATE`と`INSERT`ステートメントの順序が乱れると、 `Duplicate entry`エラー[＃8597](https://github.com/pingcap/tiflow/issues/8597) @ [スドジ](https://github.com/sdojjy)が発生する可能性がある問題を修正しました。
        -   PDとTiCDC [＃8562](https://github.com/pingcap/tiflow/issues/8562) @ [金星の上](https://github.com/overvenus)間のネットワーク分離によって発生するTiCDCサービスの異常終了問題を修正
        -   Kubernetes [＃8484](https://github.com/pingcap/tiflow/issues/8484) @ [金星の上](https://github.com/overvenus)で TiCDC クラスターの正常なアップグレードが失敗する問題を修正しました
        -   すべての下流 Kafka サーバーが利用できない場合に TiCDCサーバーがパニックになる問題を修正[＃8523](https://github.com/pingcap/tiflow/issues/8523) @ [3エースショーハンド](https://github.com/3AceShowHand)
        -   変更フィードを再開するとデータが失われる可能性がある、またはチェックポイントが[＃8242](https://github.com/pingcap/tiflow/issues/8242) @ [金星の上](https://github.com/overvenus)に進めない問題を修正しました。
