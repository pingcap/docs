---
title: TiDB 6.5.2 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 6.5.2.
---

# TiDB 6.5.2 リリースノート {#tidb-6-5-2-release-notes}

発売日：2023年4月21日

TiDB バージョン: 6.5.2

クイックアクセス: [インストールパッケージ](https://www.pingcap.com/download/?version=v6.5.2#version-list)

## 互換性の変更 {#compatibility-changes}

-   TiCDC は、Avro [3エースショーハンド](https://github.com/3AceShowHand)の`FLOAT`データの誤ったエンコードの問題を修正しました

    TiCDC クラスターを v6.5.2 以降の v6.5.x バージョンにアップグレードするときに、Avro を使用してレプリケートされたテーブルに`FLOAT`データ型が含まれている場合は、アップグレードする前に Confluent Schema Registry の互換性ポリシーを手動で`None`に調整する必要があります。 Changefeed はスキーマを正常に更新できます。そうしないと、アップグレード後に変更フィードがスキーマを更新できなくなり、エラー状態になります。

-   storageサービスへのパーティション テーブルのレプリケーション中のデータ損失の潜在的な問題を修正するために、TiCDC [CharlesCheung96](https://github.com/CharlesCheung96)

## 改善点 {#improvements}

-   TiDB

    -   プリペアドプランキャッシュ [qw4990](https://github.com/qw4990)で`BatchPointGet`の実行プランのキャッシュをサポート
    -   インデックス結合[イーサール](https://github.com/Yisaer)でより多くの SQL 形式をサポート
    -   一部の Index Merge リーダーのログ レベルを`"info"`から`"debug"` [イービン87](https://github.com/yibin87)に変更します。
    -   制限を使用してレンジ パーティション テーブルの`distsql_concurrency`設定を最適化し、クエリレイテンシー[あなた06](https://github.com/you06)を削減します。

-   TiFlash

    -   TiFlash読み取り[ジンヘリン](https://github.com/JinheLin)中のタスク スケジューリングの CPU 消費量を削減します。
    -   デフォルト設定[ブリーズウィッシュ](https://github.com/breezewish)でBRおよびTiDB LightningからTiFlashへのデータ インポートのパフォーマンスが向上しました。

-   ツール

    -   TiCDC

        -   TiCDC オープン API v2.0 [スドジ](https://github.com/sdojjy)をリリース
        -   TiCDC による OOM 問題を防ぐために`gomemlimit`を導入します[咸陽飛](https://github.com/amyangfei)
        -   複数ステートメントのアプローチを使用して、 `UPDATE`ステートメント[咸陽飛](https://github.com/amyangfei)のバッチ実行を含むシナリオでレプリケーションのパフォーマンスを最適化します。
        -   REDO アプライアでのトランザクションの分割をサポートして、スループットを向上させ、災害復旧シナリオでの RTO を削減します[CharlesCheung96](https://github.com/CharlesCheung96)
        -   REDO ログ[CharlesCheung96](https://github.com/CharlesCheung96)での DDL イベントの適用のサポート

    -   TiDB Lightning

        -   BOM ヘッダー[dsダシュン](https://github.com/dsdashun)を含む CSV データ ファイルのインポートをサポート

## バグの修正 {#bug-fixes}

-   TiDB
    -   キャッシュ テーブルに新しい列が追加された後、値が列のデフォルト値[lqs](https://github.com/lqs)ではなく`NULL`になる問題を修正します。
    -   多くのパーティションとTiFlashレプリカを含むパーティション テーブルに対して`TRUNCATE TABLE`を実行するときに、書き込み競合によって引き起こされる DDL 再試行の問題を修正します[むじょん](https://github.com/mjonss)
    -   `DROP TABLE`操作の実行時に`ADMIN SHOW DDL JOBS`結果でテーブル名が欠落する問題を修正[ティエンチャイアマオ](https://github.com/tiancaiamao)
    -   cgroup 情報の読み取りエラーにより TiDBサーバーが起動できず、エラー メッセージ「cgroup v1 からファイルメモリ.stat を読み取れません: /sys/メモリ.stat を開きます。そのようなファイルまたはディレクトリはありません」 [ホーキングレイ](https://github.com/hawkingrei)が表示される問題を修正します。
    -   DDL データ バックフィル[むじょん](https://github.com/mjonss)を実行するときにトランザクションで頻繁に発生する書き込み競合を修正しました。
    -   実行プラン生成時に取得した InfoSchema の不整合により TiDBpanicが発生する問題を修正[@tiancaiamao](https://github.com/tiancaiamao)
    -   DDL を使用して浮動小数点型を変更し、長さを変更せずに小数点以下の桁数を減らすと、古いデータが同じままになる問題を修正します[@zimulala](https://github.com/zimulala)
    -   トランザクション内で`PointUpdate`実行した後、TiDB が`SELECT`ステートメント[ジグアン](https://github.com/zyguan)に対して誤った結果を返す問題を修正します。
    -   Cursor Fetch を使用し、Execute、Fetch、Close の他のステートメントを実行すると、Fetch および Close コマンドが誤った結果を返したり、TiDB がpanicを引き起こす可能性がある問題を修正します[@YangKeao](https://github.com/YangKeao)
    -   `INSERT IGNORE`および`REPLACE`ステートメントが、値[ジグアン](https://github.com/zyguan)を変更しないキーをロックしない問題を修正します。
    -   TiFlash が実行中に生成された列のエラーを報告する問題を修正[グオシャオゲ](https://github.com/guo-shaoge)
    -   単一の SQL ステートメント[むじょん](https://github.com/mjonss)に異なるパーティション分割テーブルが含まれる場合、TiDB が誤った結果を生成する可能性がある問題を修正します。
    -   準備されたプラン キャッシュが有効になっている場合にフル インデックス スキャンでエラーが発生する可能性がある問題を修正します[fzzf678](https://github.com/fzzf678)
    -   プラン キャッシュの準備が有効になっている場合に IndexMerge が誤った結果を生成する可能性がある問題を修正します[qw4990](https://github.com/qw4990)
    -   `max_prepared_stmt_count`の設定が反映されない問題を修正[シュイファングリーンアイズ](https://github.com/xuyifangreeneyes)
    -   プラン キャッシュの準備が有効になっている場合に IndexMerge が誤った結果を生成する可能性がある問題を修正します[徐淮嶼](https://github.com/XuHuaiyu)
    -   パーティションテーブル[ティエンチャイアマオ](https://github.com/tiancaiamao)の動的トリミングモードでインデックス結合によりpanicが発生する可能性がある問題を修正

-   TiKV

    -   cgroup path [SpadeA-Tang](https://github.com/SpadeA-Tang)を処理するときに TiKV が`:`文字を正しく解析しない問題を修正

-   PD

    -   PD が予期せず複数の学習者をリージョン[フンドゥンDM](https://github.com/HunDunDM)に追加する可能性がある問題を修正
    -   配置ルールを切り替えると、引出線[バッファフライ](https://github.com/bufferflies)の分布が不均一になる可能性がある問題を修正

-   TiFlash

    -   TiFlash が生成された列[グオシャオゲ](https://github.com/guo-shaoge)を認識できない問題を修正
    -   特定の場合に 10 進数の除算で最後の桁が切り上げられない問題を修正[リトルフォール](https://github.com/LittleFall)
    -   特定の場合に Decimal キャストが誤って切り上げられる問題を修正[ウィンドトーカー](https://github.com/windtalker)
    -   新しい照合順序[xzhangxian1008](https://github.com/xzhangxian1008)を有効にした後、TopN/Sort 演算子が誤った結果を生成する問題を修正します。
    -   TiCDC の非互換性によるTiFlashプロセスの失敗の問題を修正[ホンユニャン](https://github.com/hongyunyan)

-   ツール

    -   バックアップと復元 (BR)

        -   TiDB クラスター[ジョッカウ](https://github.com/joccau)に PITR バックアップ タスクがない場合、 `resolve lock`の頻度が高すぎる問題を修正
        -   PITR リカバリ プロセス[ジョッカウ](https://github.com/joccau)中にリージョンを分割するための待ち時間が不十分である問題を修正します。

    -   TiCDC

        -   TiCDC がデータをオブジェクトstorage[こんにちはラスティン](https://github.com/hi-rustin)にレプリケートするときにパーティション セパレーターが機能しない問題を修正します。
        -   TiCDC がデータをオブジェクトstorage[ジャオシンユ](https://github.com/zhaoxinyu)にレプリケートするときに、テーブル スケジューリングによってデータ損失が発生する可能性がある問題を修正します。
        -   非再入可能 DDL ステートメント[ひっくり返る](https://github.com/hicqu)が原因でレプリケーションが停止する問題を修正します。
        -   TiCDC がデータをオブジェクトstorage[CharlesCheung96](https://github.com/CharlesCheung96)にレプリケートするときに、TiCDC スケーリングによってデータ損失が発生する可能性がある問題を修正します。
        -   `db sorter`のメモリ使用量が`cgroup memory limit` [咸陽飛](https://github.com/amyangfei)によって制御されない問題を修正
        -   REDO ログ[CharlesCheung96](https://github.com/CharlesCheung96)の適用中に特殊なケースでデータ損失が発生する可能性がある問題を修正
        -   `db sorter`のメモリ使用量が`cgroup memory limit` [咸陽飛](https://github.com/amyangfei)によって制御されない問題を修正
        -   データ レプリケーション中の`UPDATE`と`INSERT`ステートメントの不規則性により、 `Duplicate entry`エラー[スドジ](https://github.com/sojjy)が発生する可能性がある問題を修正します。
        -   PD と TiCDC [オーバーヴィーナス](https://github.com/overvenus)の間のネットワーク分離によって引き起こされる TiCDC サービスの異常終了の問題を修正します。
        -   Kubernetes [オーバーヴィーナス](https://github.com/overvenus)で TiCDC クラスターの正常なアップグレードが失敗する問題を修正
        -   すべてのダウンストリーム Kafka サーバーが利用できない場合に TiCDCサーバーがパニックになる問題を修正[3エースショーハンド](https://github.com/3AceShowHand)
        -   変更フィードを再開するとデータが失われる可能性がある、またはチェックポイントが[オーバーヴィーナス](https://github.com/overvenus)進むことができないという問題を修正します。
