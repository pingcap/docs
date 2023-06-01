---
title: TiDB 6.5.2 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 6.5.2.
---

# TiDB 6.5.2 リリースノート {#tidb-6-5-2-release-notes}

発売日：2023年4月21日

TiDB バージョン: 6.5.2

クイックアクセス: [<a href="https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb">クイックスタート</a>](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [<a href="https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup">本番展開</a>](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup) | [<a href="https://www.pingcap.com/download/?version=v6.5.2#version-list">インストールパッケージ</a>](https://www.pingcap.com/download/?version=v6.5.2#version-list)

## 互換性の変更 {#compatibility-changes}

-   TiCDC は、Avro [<a href="https://github.com/pingcap/tiflow/issues/8490">#8490</a>](https://github.com/pingcap/tiflow/issues/8490) @ [<a href="https://github.com/3AceShowHand">3エースショーハンド</a>](https://github.com/3AceShowHand)の`FLOAT`データの誤ったエンコードの問題を修正しました

    TiCDC クラスターを v6.5.2 以降の v6.5.x バージョンにアップグレードするときに、Avro を使用してレプリケートされたテーブルに`FLOAT`データ型が含まれている場合は、アップグレードする前に Confluent Schema Registry の互換性ポリシーを手動で`None`に調整する必要があります。 Changefeed はスキーマを正常に更新できます。そうしないと、アップグレード後に変更フィードがスキーマを更新できなくなり、エラー状態になります。

-   storageサービスへのパーティション テーブルのレプリケーション中のデータ損失の潜在的な問題を修正するために、TiCDC [<a href="/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters">`sink.enable-partition-separator`</a>](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)構成項目のデフォルト値が`false`から`true`に変更されました。これは、テーブル内のパーティションがデフォルトで別のディレクトリに保存されることを意味します。データ損失の問題を避けるために、値を`true`のままにすることをお勧めします。 [<a href="https://github.com/pingcap/tiflow/issues/8724">#8724</a>](https://github.com/pingcap/tiflow/issues/8724) @ [<a href="https://github.com/CharlesCheung96">CharlesCheung96</a>](https://github.com/CharlesCheung96)

## 改善点 {#improvements}

-   TiDB

    -   プリペアドプランキャッシュ [<a href="https://github.com/pingcap/tidb/issues/42125">#42125</a>](https://github.com/pingcap/tidb/issues/42125) @ [<a href="https://github.com/qw4990">qw4990</a>](https://github.com/qw4990)で`BatchPointGet`の実行プランのキャッシュをサポート
    -   インデックス結合[<a href="https://github.com/pingcap/tidb/issues/40505">#40505</a>](https://github.com/pingcap/tidb/issues/40505) @ [<a href="https://github.com/Yisaer">イーサール</a>](https://github.com/Yisaer)でより多くの SQL 形式をサポート
    -   一部の Index Merge リーダーのログ レベルを`"info"`から`"debug"` [<a href="https://github.com/pingcap/tidb/issues/41949">#41949</a>](https://github.com/pingcap/tidb/issues/41949) @ [<a href="https://github.com/yibin87">イービン87</a>](https://github.com/yibin87)に変更します。
    -   制限を使用してレンジ パーティション テーブルの`distsql_concurrency`設定を最適化し、クエリレイテンシー[<a href="https://github.com/pingcap/tidb/issues/41480">#41480</a>](https://github.com/pingcap/tidb/issues/41480) @ [<a href="https://github.com/you06">あなた06</a>](https://github.com/you06)を削減します。

-   TiFlash

    -   TiFlash読み取り[<a href="https://github.com/pingcap/tiflash/issues/6495">#6495</a>](https://github.com/pingcap/tiflash/issues/6495) @ [<a href="https://github.com/JinheLin">ジンヘリン</a>](https://github.com/JinheLin)中のタスク スケジューリングの CPU 消費量を削減します。
    -   デフォルト設定[<a href="https://github.com/pingcap/tiflash/issues/7272">#7272</a>](https://github.com/pingcap/tiflash/issues/7272) @ [<a href="https://github.com/breezewish">ブリーズウィッシュ</a>](https://github.com/breezewish)でBRおよびTiDB LightningからTiFlashへのデータ インポートのパフォーマンスが向上しました。

-   ツール

    -   TiCDC

        -   TiCDC オープン API v2.0 [<a href="https://github.com/pingcap/tiflow/issues/8743">#8743</a>](https://github.com/pingcap/tiflow/issues/8743) @ [<a href="https://github.com/sdojjy">スドジ</a>](https://github.com/sdojjy)をリリース
        -   TiCDC による OOM 問題を防ぐために`gomemlimit`を導入します[<a href="https://github.com/pingcap/tiflow/issues/8675">#8675</a>](https://github.com/pingcap/tiflow/issues/8675) @ [<a href="https://github.com/amyangfei">咸陽飛</a>](https://github.com/amyangfei)
        -   複数ステートメントのアプローチを使用して、 `UPDATE`ステートメント[<a href="https://github.com/pingcap/tiflow/issues/8057">#8057</a>](https://github.com/pingcap/tiflow/issues/8057) @ [<a href="https://github.com/amyangfei">咸陽飛</a>](https://github.com/amyangfei)のバッチ実行を含むシナリオでレプリケーションのパフォーマンスを最適化します。
        -   REDO アプライアでのトランザクションの分割をサポートして、スループットを向上させ、災害復旧シナリオでの RTO を削減します[<a href="https://github.com/pingcap/tiflow/issues/8318">#8318</a>](https://github.com/pingcap/tiflow/issues/8318) @ [<a href="https://github.com/CharlesCheung96">CharlesCheung96</a>](https://github.com/CharlesCheung96)
        -   REDO ログ[<a href="https://github.com/pingcap/tiflow/issues/8361">#8361</a>](https://github.com/pingcap/tiflow/issues/8361) @ [<a href="https://github.com/CharlesCheung96">CharlesCheung96</a>](https://github.com/CharlesCheung96)での DDL イベントの適用のサポート

    -   TiDB Lightning

        -   BOM ヘッダー[<a href="https://github.com/pingcap/tidb/issues/40744">#40744</a>](https://github.com/pingcap/tidb/issues/40744) @ [<a href="https://github.com/dsdashun">dsダシュン</a>](https://github.com/dsdashun)を含む CSV データ ファイルのインポートをサポート

## バグの修正 {#bug-fixes}

-   TiDB
    -   キャッシュ テーブルに新しい列が追加された後、値が列のデフォルト値[<a href="https://github.com/pingcap/tidb/issues/42928">#42928</a>](https://github.com/pingcap/tidb/issues/42928) @ [<a href="https://github.com/lqs">lqs</a>](https://github.com/lqs)ではなく`NULL`になる問題を修正します。
    -   多くのパーティションとTiFlashレプリカを含むパーティション テーブルに対して`TRUNCATE TABLE`を実行するときに、書き込み競合によって引き起こされる DDL 再試行の問題を修正します[<a href="https://github.com/pingcap/tidb/issues/42940">#42940</a>](https://github.com/pingcap/tidb/issues/42940) @ [<a href="https://github.com/mjonss">むじょん</a>](https://github.com/mjonss)
    -   `DROP TABLE`操作の実行時に`ADMIN SHOW DDL JOBS`結果でテーブル名が欠落する問題を修正[<a href="https://github.com/pingcap/tidb/issues/42268">#42268</a>](https://github.com/pingcap/tidb/issues/42268) @ [<a href="https://github.com/tiancaiamao">ティエンチャイアマオ</a>](https://github.com/tiancaiamao)
    -   cgroup 情報の読み取りエラーにより TiDBサーバーが起動できず、エラー メッセージ「cgroup v1 からファイルメモリ.stat を読み取れません: /sys/メモリ.stat を開きます。そのようなファイルまたはディレクトリはありません」 [<a href="https://github.com/pingcap/tidb/issues/42659">#42659</a>](https://github.com/pingcap/tidb/issues/42659) @ [<a href="https://github.com/hawkingrei">ホーキングレイ</a>](https://github.com/hawkingrei)が表示される問題を修正します。
    -   DDL データ バックフィル[<a href="https://github.com/pingcap/tidb/issues/24427">#24427</a>](https://github.com/pingcap/tidb/issues/24427) @ [<a href="https://github.com/mjonss">むじょん</a>](https://github.com/mjonss)を実行するときにトランザクションで頻繁に発生する書き込み競合を修正しました。
    -   実行プラン生成時に取得した InfoSchema の不整合により TiDBpanicが発生する問題を修正[<a href="https://github.com/pingcap/tidb/issues/41622">#41622</a>](https://github.com/pingcap/tidb/issues/41622) [<a href="https://github.com/tiancaiamao">@tiancaiamao</a>](https://github.com/tiancaiamao)
    -   DDL を使用して浮動小数点型を変更し、長さを変更せずに小数点以下の桁数を減らすと、古いデータが同じままになる問題を修正します[<a href="https://github.com/pingcap/tidb/issues/41281">#41281</a>](https://github.com/pingcap/tidb/issues/41281) [<a href="https://github.com/zimulala">@zimulala</a>](https://github.com/zimulala)
    -   トランザクション内で`PointUpdate`実行した後、TiDB が`SELECT`ステートメント[<a href="https://github.com/pingcap/tidb/issues/28011">#28011</a>](https://github.com/pingcap/tidb/issues/28011) @ [<a href="https://github.com/zyguan">ジグアン</a>](https://github.com/zyguan)に対して誤った結果を返す問題を修正します。
    -   Cursor Fetch を使用し、Execute、Fetch、Close の他のステートメントを実行すると、Fetch および Close コマンドが誤った結果を返したり、TiDB がpanicを引き起こす可能性がある問題を修正します[<a href="https://github.com/pingcap/tidb/issues/40094">#40094</a>](https://github.com/pingcap/tidb/issues/40094) [<a href="https://github.com/YangKeao">@YangKeao</a>](https://github.com/YangKeao)
    -   `INSERT IGNORE`および`REPLACE`ステートメントが、値[<a href="https://github.com/pingcap/tidb/issues/42121">#42121</a>](https://github.com/pingcap/tidb/issues/42121) @ [<a href="https://github.com/zyguan">ジグアン</a>](https://github.com/zyguan)を変更しないキーをロックしない問題を修正します。
    -   TiFlash が実行中に生成された列のエラーを報告する問題を修正[<a href="https://github.com/pingcap/tidb/issues/40663">#40663</a>](https://github.com/pingcap/tidb/issues/40663) @ [<a href="https://github.com/guo-shaoge">グオシャオゲ</a>](https://github.com/guo-shaoge)
    -   単一の SQL ステートメント[<a href="https://github.com/pingcap/tidb/issues/42135">#42135</a>](https://github.com/pingcap/tidb/issues/42135) @ [<a href="https://github.com/mjonss">むじょん</a>](https://github.com/mjonss)に異なるパーティション分割テーブルが含まれる場合、TiDB が誤った結果を生成する可能性がある問題を修正します。
    -   準備されたプラン キャッシュが有効になっている場合にフル インデックス スキャンでエラーが発生する可能性がある問題を修正します[<a href="https://github.com/pingcap/tidb/issues/42150">#42150</a>](https://github.com/pingcap/tidb/issues/42150) @ [<a href="https://github.com/fzzf678">fzzf678</a>](https://github.com/fzzf678)
    -   プラン キャッシュの準備が有効になっている場合に IndexMerge が誤った結果を生成する可能性がある問題を修正します[<a href="https://github.com/pingcap/tidb/issues/41828">#41828</a>](https://github.com/pingcap/tidb/issues/41828) @ [<a href="https://github.com/qw4990">qw4990</a>](https://github.com/qw4990)
    -   `max_prepared_stmt_count`の設定が反映されない問題を修正[<a href="https://github.com/pingcap/tidb/issues/39735">#39735</a>](https://github.com/pingcap/tidb/issues/39735) @ [<a href="https://github.com/xuyifangreeneyes">シュイファングリーンアイズ</a>](https://github.com/xuyifangreeneyes)
    -   プラン キャッシュの準備が有効になっている場合に IndexMerge が誤った結果を生成する可能性がある問題を修正します[<a href="https://github.com/pingcap/tidb/issues/41828">#41828</a>](https://github.com/pingcap/tidb/issues/41828) @ [<a href="https://github.com/qw4990">qw4990</a>](https://github.com/qw4990) @ [<a href="https://github.com/XuHuaiyu">徐淮嶼</a>](https://github.com/XuHuaiyu)
    -   パーティションテーブル[<a href="https://github.com/pingcap/tidb/issues/40596">#40596</a>](https://github.com/pingcap/tidb/issues/40596) @ [<a href="https://github.com/tiancaiamao">ティエンチャイアマオ</a>](https://github.com/tiancaiamao)の動的トリミングモードでインデックス結合によりpanicが発生する可能性がある問題を修正

-   TiKV

    -   cgroup path [<a href="https://github.com/tikv/tikv/issues/14538">#14538</a>](https://github.com/tikv/tikv/issues/14538) @ [<a href="https://github.com/SpadeA-Tang">SpadeA-Tang</a>](https://github.com/SpadeA-Tang)を処理するときに TiKV が`:`文字を正しく解析しない問題を修正

-   PD

    -   PD が予期せず複数の学習者をリージョン[<a href="https://github.com/tikv/pd/issues/5786">#5786</a>](https://github.com/tikv/pd/issues/5786) @ [<a href="https://github.com/HunDunDM">フンドゥンDM</a>](https://github.com/HunDunDM)に追加する可能性がある問題を修正
    -   配置ルールを切り替えると、引出線[<a href="https://github.com/tikv/pd/issues/6195">#6195</a>](https://github.com/tikv/pd/issues/6195) @ [<a href="https://github.com/bufferflies">バッファフライ</a>](https://github.com/bufferflies)の分布が不均一になる可能性がある問題を修正

-   TiFlash

    -   TiFlash が生成された列[<a href="https://github.com/pingcap/tiflash/issues/6801">#6801</a>](https://github.com/pingcap/tiflash/issues/6801) @ [<a href="https://github.com/guo-shaoge">グオシャオゲ</a>](https://github.com/guo-shaoge)を認識できない問題を修正
    -   特定の場合に 10 進数の除算で最後の桁が切り上げられない問題を修正[<a href="https://github.com/pingcap/tiflash/issues/7022">#7022</a>](https://github.com/pingcap/tiflash/issues/7022) @ [<a href="https://github.com/LittleFall">リトルフォール</a>](https://github.com/LittleFall)
    -   特定の場合に Decimal キャストが誤って切り上げられる問題を修正[<a href="https://github.com/pingcap/tiflash/issues/6994">#6994</a>](https://github.com/pingcap/tiflash/issues/6994) @ [<a href="https://github.com/windtalker">ウィンドトーカー</a>](https://github.com/windtalker)
    -   新しい照合順序[<a href="https://github.com/pingcap/tiflash/issues/6807">#6807</a>](https://github.com/pingcap/tiflash/issues/6807) @ [<a href="https://github.com/xzhangxian1008">xzhangxian1008</a>](https://github.com/xzhangxian1008)を有効にした後、TopN/Sort 演算子が誤った結果を生成する問題を修正します。
    -   TiCDC の非互換性によるTiFlashプロセスの失敗の問題を修正[<a href="https://github.com/pingcap/tiflash/issues/7212">#7212</a>](https://github.com/pingcap/tiflash/issues/7212) @ [<a href="https://github.com/hongyunyan">ホンユニャン</a>](https://github.com/hongyunyan)

-   ツール

    -   バックアップと復元 (BR)

        -   TiDB クラスター[<a href="https://github.com/pingcap/tidb/issues/40759">#40759</a>](https://github.com/pingcap/tidb/issues/40759) @ [<a href="https://github.com/joccau">ジョッカウ</a>](https://github.com/joccau)に PITR バックアップ タスクがない場合、 `resolve lock`の頻度が高すぎる問題を修正
        -   PITR リカバリ プロセス[<a href="https://github.com/pingcap/tidb/issues/42001">#42001</a>](https://github.com/pingcap/tidb/issues/42001) @ [<a href="https://github.com/joccau">ジョッカウ</a>](https://github.com/joccau)中にリージョンを分割するための待ち時間が不十分である問題を修正します。

    -   TiCDC

        -   TiCDC がデータをオブジェクトstorage[<a href="https://github.com/pingcap/tiflow/issues/8581">#8581</a>](https://github.com/pingcap/tiflow/issues/8581) @ [<a href="https://github.com/CharlesCheung96">CharlesCheung96</a>](https://github.com/CharlesCheung96) @ [<a href="https://github.com/hi-rustin">こんにちはラスティン</a>](https://github.com/hi-rustin)にレプリケートするときにパーティション セパレーターが機能しない問題を修正します。
        -   TiCDC がデータをオブジェクトstorage[<a href="https://github.com/pingcap/tiflow/issues/8256">#8256</a>](https://github.com/pingcap/tiflow/issues/8256) @ [<a href="https://github.com/zhaoxinyu">ジャオシンユ</a>](https://github.com/zhaoxinyu)にレプリケートするときに、テーブル スケジューリングによってデータ損失が発生する可能性がある問題を修正します。
        -   非再入可能 DDL ステートメント[<a href="https://github.com/pingcap/tiflow/issues/8662">#8662</a>](https://github.com/pingcap/tiflow/issues/8662) @ [<a href="https://github.com/hicqu">ひっくり返る</a>](https://github.com/hicqu)が原因でレプリケーションが停止する問題を修正します。
        -   TiCDC がデータをオブジェクトstorage[<a href="https://github.com/pingcap/tiflow/issues/8666">#8666</a>](https://github.com/pingcap/tiflow/issues/8666) @ [<a href="https://github.com/CharlesCheung96">CharlesCheung96</a>](https://github.com/CharlesCheung96)にレプリケートするときに、TiCDC スケーリングによってデータ損失が発生する可能性がある問題を修正します。
        -   `db sorter`のメモリ使用量が`cgroup memory limit` [<a href="https://github.com/pingcap/tiflow/issues/8588">#8588</a>](https://github.com/pingcap/tiflow/issues/8588) @ [<a href="https://github.com/amyangfei">咸陽飛</a>](https://github.com/amyangfei)によって制御されない問題を修正
        -   REDO ログ[<a href="https://github.com/pingcap/tiflow/issues/8591">#8591</a>](https://github.com/pingcap/tiflow/issues/8591) @ [<a href="https://github.com/CharlesCheung96">CharlesCheung96</a>](https://github.com/CharlesCheung96)の適用中に特殊なケースでデータ損失が発生する可能性がある問題を修正
        -   `db sorter`のメモリ使用量が`cgroup memory limit` [<a href="https://github.com/pingcap/tiflow/issues/8588">#8588</a>](https://github.com/pingcap/tiflow/issues/8588) @ [<a href="https://github.com/amyangfei">咸陽飛</a>](https://github.com/amyangfei)によって制御されない問題を修正
        -   データ レプリケーション中の`UPDATE`と`INSERT`ステートメントの不規則性により、 `Duplicate entry`エラー[<a href="https://github.com/pingcap/tiflow/issues/8597">#8597</a>](https://github.com/pingcap/tiflow/issues/8597) @ [<a href="https://github.com/sojjy">スドジ</a>](https://github.com/sojjy)が発生する可能性がある問題を修正します。
        -   PD と TiCDC [<a href="https://github.com/pingcap/tiflow/issues/8562">#8562</a>](https://github.com/pingcap/tiflow/issues/8562) @ [<a href="https://github.com/overvenus">オーバーヴィーナス</a>](https://github.com/overvenus)の間のネットワーク分離によって引き起こされる TiCDC サービスの異常終了の問題を修正します。
        -   Kubernetes [<a href="https://github.com/pingcap/tiflow/issues/8484">#8484</a>](https://github.com/pingcap/tiflow/issues/8484) @ [<a href="https://github.com/overvenus">オーバーヴィーナス</a>](https://github.com/overvenus)で TiCDC クラスターの正常なアップグレードが失敗する問題を修正
        -   すべてのダウンストリーム Kafka サーバーが利用できない場合に TiCDCサーバーがパニックになる問題を修正[<a href="https://github.com/pingcap/tiflow/issues/8523">#8523</a>](https://github.com/pingcap/tiflow/issues/8523) @ [<a href="https://github.com/3AceShowHand">3エースショーハンド</a>](https://github.com/3AceShowHand)
        -   変更フィードを再開するとデータが失われる可能性がある、またはチェックポイントが[<a href="https://github.com/pingcap/tiflow/issues/8242">#8242</a>](https://github.com/pingcap/tiflow/issues/8242) @ [<a href="https://github.com/overvenus">オーバーヴィーナス</a>](https://github.com/overvenus)進むことができないという問題を修正します。
