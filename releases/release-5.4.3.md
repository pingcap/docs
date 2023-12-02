---
title: TiDB 5.4.3 Release Notes
---

# TiDB 5.4.3 リリースノート {#tidb-5-4-3-release-notes}

発売日：2022年10月13日

TiDB バージョン: 5.4.3

## 改善点 {#improvements}

-   TiKV

    -   RocksDB 書き込み停止設定をフロー制御しきい値[#13467](https://github.com/tikv/tikv/issues/13467)よりも小さい値に構成することをサポート
    -   1 つのピアが到達不能になった後にRaftstore が大量のメッセージをブロードキャストすることを避けるための`unreachable_backoff`項目の設定をサポートします[#13054](https://github.com/tikv/tikv/issues/13054)

-   ツール

    -   TiDB Lightning

        -   散乱リージョンをバッチ モードに最適化して、散乱リージョンプロセスの安定性を向上させます[#33618](https://github.com/pingcap/tidb/issues/33618)

    -   TiCDC

        -   マルチリージョン シナリオでのランタイム コンテキストの切り替えによって生じるパフォーマンスのオーバーヘッドを削減します[#5610](https://github.com/pingcap/tiflow/issues/5610)

## バグの修正 {#bug-fixes}

-   TiDB

    -   `SHOW CREATE PLACEMENT POLICY` [#37526](https://github.com/pingcap/tidb/issues/37526)の誤った出力を修正
    -   クラスターの PD ノードが交換された後、一部の DDL ステートメントが一定期間スタックすることがある問題を修正します[#33908](https://github.com/pingcap/tidb/issues/33908)
    -   アイドル状態の接続で`KILL TIDB`がすぐに有効にならない問題を修正[#24031](https://github.com/pingcap/tidb/issues/24031)
    -   `INFORMSTION_SCHEMA.COLUMNS`システム テーブルをクエリすると、 `DATA_TYPE`と`COLUMN_TYPE`列に誤った結果が返される問題を修正します[#36496](https://github.com/pingcap/tidb/issues/36496)
    -   TiDB Binlogが有効な場合、 `ALTER SEQUENCE`ステートメントを実行するとメタデータ バージョンが間違ってDrainerが終了する可能性がある問題を修正します[#36276](https://github.com/pingcap/tidb/issues/36276)
    -   `UNION`演算子が予期しない空の結果を返す可能性がある問題を修正します[#36903](https://github.com/pingcap/tidb/issues/36903)
    -   TiFlash [#37254](https://github.com/pingcap/tidb/issues/37254)のパーティション化されたテーブルで動的モードを有効にしたときに発生する間違った結果を修正しました。
    -   `LIMIT` [#35638](https://github.com/pingcap/tidb/issues/35638)と一緒に使用すると`INL_HASH_JOIN`ハングする可能性がある問題を修正
    -   `SHOW WARNINGS`ステートメントの実行時に TiDB が`invalid memory address or nil pointer dereference`エラーを返す可能性がある問題を修正します[#31569](https://github.com/pingcap/tidb/issues/31569)
    -   RC分離レベル[#30872](https://github.com/pingcap/tidb/issues/30872)でステイル読み取りを実行すると発生する`invalid transaction`エラーを修正
    -   DML エグゼキュータを使用した`EXPLAIN ANALYZE`ステートメントが、トランザクションのコミットが完了する前に結果を返す可能性がある問題を修正します[#37373](https://github.com/pingcap/tidb/issues/37373)
    -   TiDB Binlogを有効にして重複した値を挿入すると発生する`data and columnID count not match`エラーの問題を修正します[#33608](https://github.com/pingcap/tidb/issues/33608)
    -   静的パーティション プルーン モードで、テーブルが空の場合に集計条件を含む SQL ステートメントが間違った結果を返す可能性がある問題を修正します[#35295](https://github.com/pingcap/tidb/issues/35295)
    -   `UPDATE`ステートメント[#32311](https://github.com/pingcap/tidb/issues/32311)の実行時に TiDB がpanicになる可能性がある問題を修正
    -   `UnionScan`演算子が順序[#33175](https://github.com/pingcap/tidb/issues/33175)を維持できないため、間違ったクエリ結果が表示される問題を修正
    -   場合によっては UPDATE ステートメントが誤って投影を削除し、 `Can't find column`エラー[#37568](https://github.com/pingcap/tidb/issues/37568)が発生する問題を修正します。
    -   場合によっては、パーティション化されたテーブルがインデックスを完全に使用してデータをスキャンできない問題を修正します[#33966](https://github.com/pingcap/tidb/issues/33966)
    -   特定のシナリオで`EXECUTE`予期しないエラーをスローする可能性がある問題を修正します[#37187](https://github.com/pingcap/tidb/issues/37187)
    -   準備済みプラン キャッシュが有効になっている`BIT`タイプのインデックスを使用すると、TiDB が間違った結果を返す可能性がある問題を修正します[#33067](https://github.com/pingcap/tidb/issues/33067)

-   TiKV

    -   PD リーダーが切り替わった後、または PD が再起動された後、クラスター内で継続的に SQL 実行エラーが発生する問題を修正します[#12934](https://github.com/tikv/tikv/issues/12934)
        -   原因: この問題は、ハートビート要求が失敗した後、TiKV が PD クライアントに再接続するまで、TiKV が PD クライアントへのハートビート情報の送信を再試行しないという TiKV のバグによって発生します。その結果、障害が発生した TiKV ノードのリージョン情報が古くなり、TiDB は最新のリージョン情報を取得できなくなり、SQL 実行エラーが発生します。
        -   影響を受けるバージョン: v5.3.2 および v5.4.2。この問題は v5.3.3 および v5.4.3 で修正されました。 v5.4.2 を使用している場合は、クラスターを v5.4.3 にアップグレードできます。
        -   回避策: アップグレードに加えて、送信するリージョンハートビートがなくなるまで、リージョンハートビートを PD に送信できない TiKV ノードを再起動することもできます。
    -   TiKV が Web ID プロバイダーからエラーを受け取り、デフォルトのプロバイダー[#13122](https://github.com/tikv/tikv/issues/13122)にフェイルバックすると、アクセス許可拒否エラーが発生する問題を修正します。
    -   PD クライアントがデッドロックを引き起こす可能性がある問題を修正[#13191](https://github.com/tikv/tikv/issues/13191)
    -   Raftstoreがビジー状態の場合にリージョンが重なる可能性がある問題を修正[#13160](https://github.com/tikv/tikv/issues/13160)

-   PD

    -   PD がダッシュボード プロキシ リクエストを正しく処理できない問題を修正します[#5321](https://github.com/tikv/pd/issues/5321)
    -   PDリーダー移転後、削除された墓石ストアが再び表示される問題を修正[#4941](https://github.com/tikv/pd/issues/4941)
    -   TiFlash学習者のレプリカが作成されない場合がある問題を修正[#5401](https://github.com/tikv/pd/issues/5401)

-   TiFlash

    -   `format`関数が`Data truncated`エラー[#4891](https://github.com/pingcap/tiflash/issues/4891)を返す可能性がある問題を修正します。
    -   並列集計[#5356](https://github.com/pingcap/tiflash/issues/5356)のエラーによりTiFlash がクラッシュする可能性がある問題を修正
    -   `NULL`値[#5859](https://github.com/pingcap/tiflash/issues/5859)を含む列でプライマリ インデックスを作成した後に発生するpanicを修正します。

-   ツール

    -   TiDB Lightning

        -   タイプ`BIGINT`の自動インクリメント列が範囲[#27397](https://github.com/pingcap/tidb/issues/27937)から外れることがある問題を修正
        -   重複排除により、極端な場合にTiDB Lightning がpanicを引き起こす可能性がある問題を修正します[#34163](https://github.com/pingcap/tidb/issues/34163)
        -   TiDB Lightning がParquet ファイルのスラッシュ、数字、または非 ASCII 文字で始まる列をサポートしない問題を修正します[#36980](https://github.com/pingcap/tidb/issues/36980)
        -   TiDB が IPv6 ホスト[#35880](https://github.com/pingcap/tidb/issues/35880)を使用している場合、 TiDB Lightning がTiDB に接続できない問題を修正します。

    -   TiDB データ移行 (DM)

        -   DB Conn [#3733](https://github.com/pingcap/tiflow/issues/3733)を取得するときに DM Worker がスタックすることがある問題を修正
        -   DM が`Specified key was too long`エラー[#5315](https://github.com/pingcap/tiflow/issues/5315)を報告する問題を修正
        -   レプリケーション[#7028](https://github.com/pingcap/tiflow/issues/7028)中に latin1 データが破損する可能性がある問題を修正
        -   TiDB が IPv6 ホスト[#6249](https://github.com/pingcap/tiflow/issues/6249)を使用している場合に DM が起動できない問題を修正します。
        -   `query-status` [#4811](https://github.com/pingcap/tiflow/issues/4811)で発生する可能性のあるデータ競合の問題を修正
        -   リレーがエラー[#6193](https://github.com/pingcap/tiflow/issues/6193)に遭遇したときの goroutine リークを修正

    -   TiCDC

        -   `enable-old-value = false` [#6198](https://github.com/pingcap/tiflow/issues/6198)を設定した場合の TiCDCpanicの問題を修正

    -   バックアップと復元 (BR)

        -   外部storage[#37469](https://github.com/pingcap/tidb/issues/37469)の認証キーに特殊文字が存在する場合、バックアップと復元が失敗する可能性がある問題を修正します。
        -   復元中の同時実行数の設定が大きすぎるため、リージョンのバランスが取れていない問題を修正します[#37549](https://github.com/pingcap/tidb/issues/37549)

    -   Dumpling

        -   GetDSN が IPv6 をサポートしていない問題を修正[#36112](https://github.com/pingcap/tidb/issues/36112)
