---
title: TiDB 6.5.2 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 6.5.2.
---

# TiDB 6.5.2 リリースノート {#tidb-6-5-2-release-notes}

発売日：2023年4月21日

TiDB バージョン: 6.5.2

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [本番展開](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup) | [インストールパッケージ](https://www.pingcap.com/download/?version=v6.5.2#version-list)

## 互換性の変更 {#compatibility-changes}

-   TiCDC は、Avro [#8490](https://github.com/pingcap/tiflow/issues/8490) @ [3エースショーハンド](https://github.com/3AceShowHand)の`FLOAT`データの誤ったエンコードの問題を修正しました

    TiCDC クラスターを v6.5.2 以降の v6.5.x バージョンにアップグレードするときに、Avro を使用してレプリケートされたテーブルに`FLOAT`データ型が含まれている場合は、アップグレードする前に Confluent Schema Registry の互換性ポリシーを手動で`None`に調整する必要があります。 Changefeed はスキーマを正常に更新できます。そうしないと、アップグレード後に変更フィードがスキーマを更新できなくなり、エラー状態になります。

-   storageサービスへのパーティション テーブルのレプリケーション中のデータ損失の潜在的な問題を修正するために、TiCDC [`sink.enable-partition-separator`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)構成項目のデフォルト値が`false`から`true`に変更されました。これは、テーブル内のパーティションがデフォルトで別のディレクトリに保存されることを意味します。データ損失の問題を避けるために、値を`true`のままにすることをお勧めします。 [#8724](https://github.com/pingcap/tiflow/issues/8724) @ [CharlesCheung96](https://github.com/CharlesCheung96)

## 改善点 {#improvements}

-   TiDB

    -   プリペアドプランキャッシュ [#42125](https://github.com/pingcap/tidb/issues/42125) @ [qw4990](https://github.com/qw4990)で`BatchPointGet`の実行プランのキャッシュをサポート
    -   インデックス結合[#40505](https://github.com/pingcap/tidb/issues/40505) @ [イーサール](https://github.com/Yisaer)でより多くの SQL 形式をサポート
    -   一部の Index Merge リーダーのログ レベルを`"info"`から`"debug"` [#41949](https://github.com/pingcap/tidb/issues/41949) @ [イービン87](https://github.com/yibin87)に変更します。
    -   制限を使用してレンジ パーティション テーブルの`distsql_concurrency`設定を最適化し、クエリレイテンシー[#41480](https://github.com/pingcap/tidb/issues/41480) @ [あなた06](https://github.com/you06)を削減します。

-   TiFlash

    -   TiFlash読み取り[#6495](https://github.com/pingcap/tiflash/issues/6495) @ [ジンヘリン](https://github.com/JinheLin)中のタスク スケジューリングの CPU 消費量を削減します。
    -   デフォルト設定[#7272](https://github.com/pingcap/tiflash/issues/7272) @ [ブリーズウィッシュ](https://github.com/breezewish)でBRおよびTiDB LightningからTiFlashへのデータ インポートのパフォーマンスが向上しました。

-   ツール

    -   TiCDC

        -   TiCDC オープン API v2.0 [#8743](https://github.com/pingcap/tiflow/issues/8743) @ [スドジ](https://github.com/sdojjy)をリリース
        -   TiCDC による OOM 問題を防ぐために`gomemlimit`を導入します[#8675](https://github.com/pingcap/tiflow/issues/8675) @ [咸陽飛](https://github.com/amyangfei)
        -   複数ステートメントのアプローチを使用して、 `UPDATE`ステートメント[#8057](https://github.com/pingcap/tiflow/issues/8057) @ [咸陽飛](https://github.com/amyangfei)のバッチ実行を含むシナリオでレプリケーションのパフォーマンスを最適化します。
        -   REDO アプライアでのトランザクションの分割をサポートして、スループットを向上させ、災害復旧シナリオでの RTO を削減します[#8318](https://github.com/pingcap/tiflow/issues/8318) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   REDO ログ[#8361](https://github.com/pingcap/tiflow/issues/8361) @ [CharlesCheung96](https://github.com/CharlesCheung96)での DDL イベントの適用のサポート

    -   TiDB Lightning

        -   BOM ヘッダー[#40744](https://github.com/pingcap/tidb/issues/40744) @ [dsダシュン](https://github.com/dsdashun)を含む CSV データ ファイルのインポートをサポート

## バグの修正 {#bug-fixes}

-   TiDB
    -   キャッシュ テーブルに新しい列が追加された後、値が列のデフォルト値[#42928](https://github.com/pingcap/tidb/issues/42928) @ [lqs](https://github.com/lqs)ではなく`NULL`になる問題を修正します。
    -   多くのパーティションとTiFlashレプリカを含むパーティション テーブルに対して`TRUNCATE TABLE`を実行するときに、書き込み競合によって引き起こされる DDL 再試行の問題を修正します[#42940](https://github.com/pingcap/tidb/issues/42940) @ [むじょん](https://github.com/mjonss)
    -   `DROP TABLE`操作の実行時に`ADMIN SHOW DDL JOBS`の結果でテーブル名が欠落する問題を修正[#42268](https://github.com/pingcap/tidb/issues/42268) @ [ティエンチャイアマオ](https://github.com/tiancaiamao)
    -   cgroup 情報の読み取りエラーにより TiDBサーバーが起動できず、エラー メッセージ「cgroup v1 からファイルメモリ.stat を読み取れません: /sys/メモリ.stat を開きます。そのようなファイルまたはディレクトリはありません」 [#42659](https://github.com/pingcap/tidb/issues/42659) @ [ホーキングレイ](https://github.com/hawkingrei)が表示される問題を修正します。
    -   DDL データ バックフィル[#24427](https://github.com/pingcap/tidb/issues/24427) @ [むじょん](https://github.com/mjonss)を実行するときにトランザクションで頻繁に発生する書き込み競合を修正しました。
    -   実行プラン[#41622](https://github.com/pingcap/tidb/issues/41622) @ [ティエンチャイアマオ](https://github.com/tiancaiamao)の生成時に取得される InfoSchema の不整合により TiDBpanicが発生する問題を修正
    -   DDL を使用して浮動小数点型を変更して長さを変更せずに小数点以下の桁数を減らすと、古いデータが同じままになる問題を修正します[#41281](https://github.com/pingcap/tidb/issues/41281) @ [ジムララ](https://github.com/zimulala)
    -   トランザクション内で`PointUpdate`実行した後、TiDB が`SELECT`ステートメント[#28011](https://github.com/pingcap/tidb/issues/28011) @ [ジグアン](https://github.com/zyguan)に対して誤った結果を返す問題を修正します。
    -   Cursor Fetch を使用し、Execute、Fetch、Close の他のステートメントを実行すると、Fetch および Close コマンドが誤った結果を返したり、TiDB がpanicを起こしたりする可能性がある問題を修正します[#40094](https://github.com/pingcap/tidb/issues/40094) @ [ヤンケオ](https://github.com/YangKeao)
    -   `INSERT IGNORE`および`REPLACE`ステートメントが、値[#42121](https://github.com/pingcap/tidb/issues/42121) @ [ジグアン](https://github.com/zyguan)を変更しないキーをロックしない問題を修正します。
    -   TiFlash が実行中に生成された列のエラーを報告する問題を修正[#40663](https://github.com/pingcap/tidb/issues/40663) @ [グオシャオゲ](https://github.com/guo-shaoge)
    -   単一の SQL ステートメント[#42135](https://github.com/pingcap/tidb/issues/42135) @ [むじょん](https://github.com/mjonss)に異なるパーティション分割テーブルが含まれる場合、TiDB が誤った結果を生成する可能性がある問題を修正します。
    -   準備されたプラン キャッシュが有効になっている場合にフル インデックス スキャンでエラーが発生する可能性がある問題を修正します[#42150](https://github.com/pingcap/tidb/issues/42150) @ [fzzf678](https://github.com/fzzf678)
    -   プラン キャッシュの準備が有効になっている場合に IndexMerge が誤った結果を生成する可能性がある問題を修正します[#41828](https://github.com/pingcap/tidb/issues/41828) @ [qw4990](https://github.com/qw4990)
    -   `max_prepared_stmt_count`の設定が反映されない問題を修正[#39735](https://github.com/pingcap/tidb/issues/39735) @ [シュイファングリーンアイズ](https://github.com/xuyifangreeneyes)
    -   プラン キャッシュの準備が有効になっている場合に IndexMerge が誤った結果を生成する可能性がある問題を修正します[#41828](https://github.com/pingcap/tidb/issues/41828) @ [qw4990](https://github.com/qw4990) @ [徐淮嶼](https://github.com/XuHuaiyu)
    -   パーティションテーブル[#40596](https://github.com/pingcap/tidb/issues/40596) @ [ティエンチャイアマオ](https://github.com/tiancaiamao)の動的トリミングモードでインデックス結合によりpanicが発生する可能性がある問題を修正

-   TiKV

    -   TiKV が cgroup path [#14538](https://github.com/tikv/tikv/issues/14538) @ [SpadeA-Tang](https://github.com/SpadeA-Tang)を処理するときに`:`文字を正しく解析しない問題を修正します。

-   PD

    -   PD が予期せず複数の学習者をリージョン[#5786](https://github.com/tikv/pd/issues/5786) @ [フンドゥンDM](https://github.com/HunDunDM)に追加する可能性がある問題を修正
    -   配置ルールを切り替えると、引出線[#6195](https://github.com/tikv/pd/issues/6195) @ [バッファフライ](https://github.com/bufferflies)の分布が不均一になる可能性がある問題を修正

-   TiFlash

    -   TiFlash が生成された列[#6801](https://github.com/pingcap/tiflash/issues/6801) @ [グオシャオゲ](https://github.com/guo-shaoge)を認識できない問題を修正
    -   特定の場合に 10 進数の除算で最後の桁が切り上げられない問題を修正[#7022](https://github.com/pingcap/tiflash/issues/7022) @ [リトルフォール](https://github.com/LittleFall)
    -   特定の場合に Decimal キャストが誤って切り上げられる問題を修正[#6994](https://github.com/pingcap/tiflash/issues/6994) @ [ウィンドトーカー](https://github.com/windtalker)
    -   新しい照合順序[#6807](https://github.com/pingcap/tiflash/issues/6807) @ [xzhangxian1008](https://github.com/xzhangxian1008)を有効にした後、TopN/Sort 演算子が誤った結果を生成する問題を修正します。
    -   TiCDC の非互換性によるTiFlashプロセスの失敗の問題を修正[#7212](https://github.com/pingcap/tiflash/issues/7212) @ [ホンユニャン](https://github.com/hongyunyan)

-   ツール

    -   バックアップと復元 (BR)

        -   TiDB クラスター[#40759](https://github.com/pingcap/tidb/issues/40759) @ [ジョッカウ](https://github.com/joccau)に PITR バックアップ タスクがない場合、 `resolve lock`の頻度が高すぎる問題を修正
        -   PITR リカバリ プロセス[#42001](https://github.com/pingcap/tidb/issues/42001) @ [ジョッカウ](https://github.com/joccau)中にリージョンを分割するための待ち時間が不十分である問題を修正します。

    -   TiCDC

        -   TiCDC がデータをオブジェクトstorage[#8581](https://github.com/pingcap/tiflow/issues/8581) @ [CharlesCheung96](https://github.com/CharlesCheung96) @ [こんにちはラスティン](https://github.com/hi-rustin)にレプリケートするときにパーティション セパレーターが機能しない問題を修正します。
        -   TiCDC がデータをオブジェクトstorage[#8256](https://github.com/pingcap/tiflow/issues/8256) @ [ジャオシンユ](https://github.com/zhaoxinyu)にレプリケートするときに、テーブル スケジューリングによってデータ損失が発生する可能性がある問題を修正します。
        -   非再入可能 DDL ステートメント[#8662](https://github.com/pingcap/tiflow/issues/8662) @ [ひっくり返る](https://github.com/hicqu)が原因でレプリケーションが停止する問題を修正します。
        -   TiCDC がデータをオブジェクトstorage[#8666](https://github.com/pingcap/tiflow/issues/8666) @ [CharlesCheung96](https://github.com/CharlesCheung96)にレプリケートするときに、TiCDC スケーリングによってデータ損失が発生する可能性がある問題を修正します。
        -   `db sorter`のメモリ使用量が`cgroup memory limit` [#8588](https://github.com/pingcap/tiflow/issues/8588) @ [咸陽飛](https://github.com/amyangfei)によって制御されない問題を修正
        -   REDO ログ[#8591](https://github.com/pingcap/tiflow/issues/8591) @ [CharlesCheung96](https://github.com/CharlesCheung96)の適用中に特殊なケースでデータ損失が発生する可能性がある問題を修正
        -   `db sorter`のメモリ使用量が`cgroup memory limit` [#8588](https://github.com/pingcap/tiflow/issues/8588) @ [咸陽飛](https://github.com/amyangfei)によって制御されない問題を修正
        -   データ レプリケーション中の`UPDATE`と`INSERT`ステートメントの不規則性により、 `Duplicate entry`エラー[#8597](https://github.com/pingcap/tiflow/issues/8597) @ [スドジ](https://github.com/sdojjy)が発生する可能性がある問題を修正します。
        -   PD と TiCDC [#8562](https://github.com/pingcap/tiflow/issues/8562) @ [オーバーヴィーナス](https://github.com/overvenus)の間のネットワーク分離によって引き起こされる TiCDC サービスの異常終了の問題を修正します。
        -   Kubernetes [#8484](https://github.com/pingcap/tiflow/issues/8484) @ [オーバーヴィーナス](https://github.com/overvenus)で TiCDC クラスターの正常なアップグレードが失敗する問題を修正
        -   すべてのダウンストリーム Kafka サーバーが利用できない場合に TiCDCサーバーがパニックになる問題を修正[#8523](https://github.com/pingcap/tiflow/issues/8523) @ [3エースショーハンド](https://github.com/3AceShowHand)
        -   変更フィードを再開するとデータが失われる可能性がある、またはチェックポイントが[#8242](https://github.com/pingcap/tiflow/issues/8242) @ [オーバーヴィーナス](https://github.com/overvenus)進むことができないという問題を修正します。
