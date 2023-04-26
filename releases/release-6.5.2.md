---
title: TiDB 6.5.2 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 6.5.2.
---

# TiDB 6.5.2 リリースノート {#tidb-6-5-2-release-notes}

発売日：2023年4月21日

TiDB バージョン: 6.5.2

クイック アクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [本番展開](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup) | [インストール パッケージ](https://www.pingcap.com/download/?version=v6.5.2#version-list)

## 互換性の変更 {#compatibility-changes}

-   TiCDC は、Avro [#8490](https://github.com/pingcap/tiflow/issues/8490) @ [3AceShowHand](https://github.com/3AceShowHand)の`FLOAT`データの不適切なエンコードの問題を修正します。

    TiCDC クラスターを v6.5.2 以降の v6.5.x バージョンにアップグレードするときに、Avro を使用してレプリケートされたテーブルに`FLOAT`データ型が含まれている場合、アップグレードする前に Confluent Schema Registry の互換性ポリシーを手動で`None`に調整する必要があります。 changefeed はスキーマを正常に更新できます。そうしないと、アップグレード後に変更フィードがスキーマを更新できず、エラー状態になります。

-   パーティション分割されたテーブルをstorageサービスにレプリケーションする際のデータ損失の潜在的な問題を修正するために、TiCDC [`sink.enable-partition-separator`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)構成項目の既定値が`false`から`true`に変更されました。これは、テーブル内のパーティションがデフォルトで別々のディレクトリに格納されることを意味します。データ損失の問題を回避するために、値を`true`のままにしておくことをお勧めします。 [#8724](https://github.com/pingcap/tiflow/issues/8724) @ [チャールズ・チャン96](https://github.com/CharlesCheung96)

## 改良点 {#improvements}

-   TiDB

    -   プリペアドプランキャッシュ[#42125](https://github.com/pingcap/tidb/issues/42125) @ [qw4990](https://github.com/qw4990)で`BatchPointGet`の実行プランのキャッシュをサポート
    -   Index Join [#40505](https://github.com/pingcap/tidb/issues/40505) @ [イサール](https://github.com/Yisaer)でより多くの SQL 形式をサポート
    -   一部の Index Merge リーダーのログ レベルを`"info"`から`"debug"` [#41949](https://github.com/pingcap/tidb/issues/41949) @ [イビン87](https://github.com/yibin87)に変更します
    -   範囲パーティション分割されたテーブルの`distsql_concurrency`設定を制限付きで最適化し、クエリのレイテンシーを短縮する[#41480](https://github.com/pingcap/tidb/issues/41480) @ [あなた06](https://github.com/you06)

-   TiFlash

    -   TiFlash読み取り中のタスク スケジューリングの CPU 消費を削減[#6495](https://github.com/pingcap/tiflash/issues/6495) @ [リン・ジンヘ](https://github.com/JinheLin)
    -   BRおよびTiDB LightningからTiFlashへのデフォルト構成でのデータ インポートのパフォーマンスを向上させる[#7272](https://github.com/pingcap/tiflash/issues/7272) @ [そよ風](https://github.com/breezewish)

-   ツール

    -   TiCDC

        -   TiCDC Open API v2.0 をリリース[#8743](https://github.com/pingcap/tiflow/issues/8743) @ [スドジ](https://github.com/sdojjy)
        -   OOM の問題から TiCDC を防ぐために`gomemlimit`を導入する[#8675](https://github.com/pingcap/tiflow/issues/8675) @ [アミヤンフェイ](https://github.com/amyangfei)
        -   マルチステートメント アプローチを使用して、 `UPDATE`ステートメント[#8057](https://github.com/pingcap/tiflow/issues/8057) @ [アミヤンフェイ](https://github.com/amyangfei)のバッチ実行を含むシナリオでレプリケーション パフォーマンスを最適化します。
        -   REDO アプライヤーでトランザクションの分割をサポートして、スループットを向上させ、災害復旧シナリオで RTO を削減します[#8318](https://github.com/pingcap/tiflow/issues/8318) @ [チャールズ・チャン96](https://github.com/CharlesCheung96)
        -   REDO ログ[#8361](https://github.com/pingcap/tiflow/issues/8361) @ [チャールズ・チャン96](https://github.com/CharlesCheung96)での DDL イベントの適用をサポート

    -   TiDB Lightning

        -   BOM ヘッダー[#40744](https://github.com/pingcap/tidb/issues/40744) @ [dsdashun](https://github.com/dsdashun)を含む CSV データ ファイルのインポートをサポート

## バグの修正 {#bug-fixes}

-   TiDB
    -   新しい列がキャッシュ テーブルに追加された後、値が列[#42928](https://github.com/pingcap/tidb/issues/42928) @ [lqs](https://github.com/lqs)の既定値ではなく`NULL`になる問題を修正します。
    -   多くのパーティションとTiFlashレプリカ[#42940](https://github.com/pingcap/tidb/issues/42940) @ [ミヨンス](https://github.com/mjonss)を持つパーティション化されたテーブルに対して`TRUNCATE TABLE`を実行すると、書き込みの競合によって発生する DDL 再試行の問題を修正します。
    -   `DROP TABLE`操作が実行されているときに`ADMIN SHOW DDL JOBS`結果でテーブル名が欠落する問題を修正します[#42268](https://github.com/pingcap/tidb/issues/42268) @ [ティアンカイマオ](https://github.com/tiancaiamao)
    -   cgroup 情報を読み取る際にエラー メッセージ「can&#39;t read file メモリ.stat from cgroup v1: open /sys/ メモリ .stat no such file or directory」が表示され、TiDBサーバーが起動できない問題を修正します[#42659](https://github.com/pingcap/tidb/issues/42659) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   DDL データ バックフィル[#24427](https://github.com/pingcap/tidb/issues/24427) @ [ミヨンス](https://github.com/mjonss)を実行するときにトランザクションで頻繁に発生する書き込み競合を修正します。
    -   実行計画生成時に得られる InfoSchema の不整合により TiDBpanicが発生する問題を修正[#41622](https://github.com/pingcap/tidb/issues/41622) [@tiancaiamao](https://github.com/tiancaiamao)
    -   DDL を使用して浮動小数点型を変更して長さを変更せずに小数点以下の桁数を減らすと、古いデータが同じままになるという問題を修正します[#41281](https://github.com/pingcap/tidb/issues/41281) [@zimulala](https://github.com/zimulala)
    -   トランザクション内で`PointUpdate`実行した後、TiDB が`SELECT`ステートメント[#28011](https://github.com/pingcap/tidb/issues/28011) @ [ジグアン](https://github.com/zyguan)に対して誤った結果を返す問題を修正します。
    -   Cursor Fetch を使用して Execute、Fetch、および Close の他のステートメントを実行すると、Fetch および Close コマンドが誤った結果を返したり、TiDB がpanicを引き起こしたりする可能性があるという問題を修正します[#40094](https://github.com/pingcap/tidb/issues/40094) [@ヤンケアオ](https://github.com/YangKeao)
    -   `INSERT IGNORE`および`REPLACE`ステートメントが値[#42121](https://github.com/pingcap/tidb/issues/42121) @ [ジグアン](https://github.com/zyguan)を変更しないキーをロックしないという問題を修正します。
    -   [#40663](https://github.com/pingcap/tidb/issues/40663) @ [グオシャオゲ](https://github.com/guo-shaoge)の実行中に、 TiFlash が生成された列のエラーを報告する問題を修正します。
    -   単一の SQL ステートメント[#42135](https://github.com/pingcap/tidb/issues/42135) @ [ミヨンス](https://github.com/mjonss)に異なるパーティション テーブルが表示されると、TiDB が誤った結果を生成する可能性があるという問題を修正します。
    -   準備済みプラン キャッシュが有効になっている場合に、フル インデックス スキャンでエラーが発生する可能性がある問題を修正します[#42150](https://github.com/pingcap/tidb/issues/42150) @ [fzzf678](https://github.com/fzzf678)
    -   プラン キャッシュの準備が有効になっている場合、IndexMerge が誤った結果を生成する可能性がある問題を修正します[#41828](https://github.com/pingcap/tidb/issues/41828) @ [qw4990](https://github.com/qw4990)
    -   プラン キャッシュの準備が有効になっている場合、IndexMerge が誤った結果を生成する可能性がある問題を修正します[#41828](https://github.com/pingcap/tidb/issues/41828) @ [qw4990](https://github.com/qw4990) @ [徐懐玉](https://github.com/XuHuaiyu)
    -   パーティション テーブル[#40596](https://github.com/pingcap/tidb/issues/40596) @ [ティアンカイマオ](https://github.com/tiancaiamao)の動的トリミング モードでインデックス ジョインがpanicを引き起こす可能性がある問題を修正します。

-   TiKV

    -   cgroup パス[#14538](https://github.com/tikv/tikv/issues/14538) @ [スペード・ア・タン](https://github.com/SpadeA-Tang)を処理するときに、TiKV が`:`文字を正しく解析しない問題を修正します。

-   PD

    -   PD がリージョン[#5786](https://github.com/tikv/pd/issues/5786) @ [フンドゥンDM](https://github.com/HunDunDM)に複数の学習者を予期せず追加する可能性がある問題を修正します
    -   配置ルールを切り替えると、リーダー[#6195](https://github.com/tikv/pd/issues/6195) @ [バタフライ](https://github.com/bufferflies)の分布が不均一になる可能性がある問題を修正します。

-   TiFlash

    -   TiFlash が生成された列[#6801](https://github.com/pingcap/tiflash/issues/6801) @ [グオシャオゲ](https://github.com/guo-shaoge)を認識できない問題を修正
    -   特定の場合に 10 進数の除算で最後の桁が切り上げられない問題を修正します[#7022](https://github.com/pingcap/tiflash/issues/7022) @ [リトルフォール](https://github.com/LittleFall)
    -   Decimal キャストが特定の場合に[#6994](https://github.com/pingcap/tiflash/issues/6994) @ [風の語り手](https://github.com/windtalker)で誤って切り上げられる問題を修正します。
    -   新しい照合順序[#6807](https://github.com/pingcap/tiflash/issues/6807) @ [xzhangxian1008](https://github.com/xzhangxian1008)を有効にした後、TopN/Sort 演算子が誤った結果を生成する問題を修正します。
    -   TiCDC の非互換性によるTiFlashプロセスの失敗の問題を修正します[#7212](https://github.com/pingcap/tiflash/issues/7212) @ [ホンユニャン](https://github.com/hongyunyan)

-   ツール

    -   バックアップと復元 (BR)

        -   TiDBクラスタ[#40759](https://github.com/pingcap/tidb/issues/40759) @ [ジョッカウ](https://github.com/joccau)でPITRバックアップタスクがない場合に`resolve lock`の頻度が高すぎる問題を修正
        -   PITR リカバリ プロセス[#42001](https://github.com/pingcap/tidb/issues/42001) @ [ジョッカウ](https://github.com/joccau)中の分割リージョンリトライの待機時間が不十分である問題を修正します。

    -   TiCDC

        -   TiCDC がオブジェクトstorage[#8581](https://github.com/pingcap/tiflow/issues/8581) @ [チャールズ・チャン96](https://github.com/CharlesCheung96) @ [ハイラスチン](https://github.com/hi-rustin)にデータをレプリケートするときに、パーティション セパレータが機能しない問題を修正します。
        -   TiCDC がオブジェクトstorage[#8256](https://github.com/pingcap/tiflow/issues/8256) @ [照信雨](https://github.com/zhaoxinyu)にデータをレプリケートするときに、テーブル スケジューリングによってデータが失われる可能性があるという問題を修正します。
        -   再入不可の DDL ステートメントが原因でレプリケーションが停止する問題を修正します[#8662](https://github.com/pingcap/tiflow/issues/8662) @ [ヒック](https://github.com/hicqu)
        -   TiCDC がデータをオブジェクトstorage[#8666](https://github.com/pingcap/tiflow/issues/8666) @ [チャールズ・チャン96](https://github.com/CharlesCheung96)にレプリケートするときに、TiCDC スケーリングによってデータが失われる可能性があるという問題を修正します。
        -   `db sorter`のメモリ使用量が`cgroup memory limit` [#8588](https://github.com/pingcap/tiflow/issues/8588) @ [アミヤンフェイ](https://github.com/amyangfei)によって制御されない問題を修正
        -   REDO ログ[#8591](https://github.com/pingcap/tiflow/issues/8591) @ [チャールズ・チャン96](https://github.com/CharlesCheung96)の適用中に、特殊なケースでデータ損失が発生する可能性がある問題を修正します。
        -   `db sorter`のメモリ使用量が`cgroup memory limit` [#8588](https://github.com/pingcap/tiflow/issues/8588) @ [アミヤンフェイ](https://github.com/amyangfei)によって制御されない問題を修正
        -   データのレプリケーション中に`UPDATE`と`INSERT`ステートメントが乱れると、 `Duplicate entry`エラー[#8597](https://github.com/pingcap/tiflow/issues/8597) @ [スドジ](https://github.com/sojjy)が発生する可能性がある問題を修正します。
        -   PD と TiCDC [#8562](https://github.com/pingcap/tiflow/issues/8562) @ [大静脈](https://github.com/overvenus)の間のネットワーク分離によって発生する TiCDC サービスの異常終了の問題を修正します。
        -   Kubernetes [#8484](https://github.com/pingcap/tiflow/issues/8484) @ [大静脈](https://github.com/overvenus)で TiCDC クラスターのグレースフル アップグレードが失敗する問題を修正します。
        -   すべてのダウンストリーム Kafka サーバーが使用できない場合に TiCDCサーバーがパニックになる問題を修正します[#8523](https://github.com/pingcap/tiflow/issues/8523) @ [3AceShowHand](https://github.com/3AceShowHand)
        -   変更フィードを再起動するとデータが失われる可能性がある、またはチェックポイントが[#8242](https://github.com/pingcap/tiflow/issues/8242) @ [大静脈](https://github.com/overvenus)進めない問題を修正します。
