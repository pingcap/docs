---
title: TiDB 5.4.3 Release Notes
---

# TiDB 5.4.3 リリースノート {#tidb-5-4-3-release-notes}

発売日：2022年10月13日

TiDB バージョン: 5.4.3

## 改良点 {#improvements}

-   TiKV

    -   フロー制御しきい値[#13467](https://github.com/tikv/tikv/issues/13467)より小さい値への RocksDB 書き込みストール設定の構成のサポート
    -   1 つのピアが到達不能になった後にRaftstore があまりにも多くのメッセージをブロードキャストするのを避けるために、 `unreachable_backoff`項目の構成をサポートします[#13054](https://github.com/tikv/tikv/issues/13054)

-   ツール

    -   TiDB Lightning

        -   分散リージョンをバッチ モードに最適化して、分散リージョンプロセスの安定性を向上させます[#33618](https://github.com/pingcap/tidb/issues/33618)

    -   TiCDC

        -   マルチリージョン シナリオでのランタイム コンテキストの切り替えによって発生するパフォーマンス オーバーヘッドを削減する[#5610](https://github.com/pingcap/tiflow/issues/5610)

## バグの修正 {#bug-fixes}

-   TiDB

    -   `SHOW CREATE PLACEMENT POLICY` [#37526](https://github.com/pingcap/tidb/issues/37526)の誤った出力を修正
    -   クラスターの PD ノードが交換された後、一部の DDL ステートメントが一定期間停止する可能性がある問題を修正します[#33908](https://github.com/pingcap/tidb/issues/33908)
    -   `KILL TIDB`がアイドル状態の接続ですぐに有効にならない問題を修正します[#24031](https://github.com/pingcap/tidb/issues/24031)
    -   `INFORMSTION_SCHEMA.COLUMNS`システム テーブル[#36496](https://github.com/pingcap/tidb/issues/36496)をクエリすると、 `DATA_TYPE`と`COLUMN_TYPE`列で誤った結果が返される問題を修正します。
    -   TiDB Binlog が有効な場合に`ALTER SEQUENCE`ステートメントを実行すると、間違ったメタデータ バージョンが発生し、 Drainerが[#36276](https://github.com/pingcap/tidb/issues/36276)終了する可能性があるという問題を修正します。
    -   `UNION`演算子が予期しない空の結果[#36903](https://github.com/pingcap/tidb/issues/36903)を返す可能性がある問題を修正します
    -   TiFlash [#37254](https://github.com/pingcap/tidb/issues/37254)のパーティション テーブルで動的モードを有効にしたときに発生する誤った結果を修正します。
    -   `LIMIT` [#35638](https://github.com/pingcap/tidb/issues/35638)で使用すると`INL_HASH_JOIN`がハングする問題を修正
    -   `SHOW WARNINGS`ステートメント[#31569](https://github.com/pingcap/tidb/issues/31569)を実行すると、TiDB が`invalid memory address or nil pointer dereference`エラーを返す場合がある問題を修正します。
    -   RC 分離レベル[#30872](https://github.com/pingcap/tidb/issues/30872)でステイル読み取り を実行すると発生する`invalid transaction`エラーを修正します。
    -   トランザクションのコミットが完了する前に、DML executor を含む`EXPLAIN ANALYZE`ステートメントが結果を返す可能性があるという問題を修正します[#37373](https://github.com/pingcap/tidb/issues/37373)
    -   TiDB Binlogを有効にして重複した値を挿入すると`data and columnID count not match`エラーが発生する問題を修正[#33608](https://github.com/pingcap/tidb/issues/33608)
    -   静的パーティションのプルーニング モードで、テーブルが空の場合に集計条件を含む SQL ステートメントが間違った結果を返す可能性があるという問題を修正します[#35295](https://github.com/pingcap/tidb/issues/35295)
    -   `UPDATE`ステートメントの実行時に TiDB がpanicになる可能性がある問題を修正します[#32311](https://github.com/pingcap/tidb/issues/32311)
    -   `UnionScan`演算子が順序[#33175](https://github.com/pingcap/tidb/issues/33175)を維持できないため、間違ったクエリ結果が返される問題を修正します。
    -   UPDATE ステートメントが誤ってプロジェクションを除外する場合があり、 `Can't find column`エラー[#37568](https://github.com/pingcap/tidb/issues/37568)が発生する問題を修正します。
    -   場合によっては、分割されたテーブルがインデックスを完全に使用してデータをスキャンできないという問題を修正します[#33966](https://github.com/pingcap/tidb/issues/33966)
    -   特定のシナリオで`EXECUTE`予期しないエラーをスローする可能性がある問題を修正します[#37187](https://github.com/pingcap/tidb/issues/37187)
    -   準備済みプラン キャッシュを有効にして`BIT`タイプのインデックスを使用すると、TiDB が間違った結果を返すことがある問題を修正します[#33067](https://github.com/pingcap/tidb/issues/33067)

-   TiKV

    -   PD リーダーの切り替え後または PD の再起動後にクラスターで SQL 実行エラーが継続して発生する問題を修正します[#12934](https://github.com/tikv/tikv/issues/12934)
        -   原因: この問題は、TiKV が PD クライアントに再接続するまで、ハートビート要求が失敗した後、TiKV が PD クライアントにハートビート情報を送信することを再試行しないという TiKV のバグによって引き起こされます。その結果、障害が発生した TiKV ノードのリージョン情報が古くなり、TiDB が最新のリージョン情報を取得できなくなり、SQL 実行エラーが発生します。
        -   影響を受けるバージョン: v5.3.2 および v5.4.2。この問題は、v5.3.3 および v5.4.3 で修正されています。 v5.4.2 を使用している場合は、クラスターを v5.4.3 にアップグレードできます。
        -   回避策: アップグレードに加えて、送信するリージョンハートビートがなくなるまで、リージョンハートビートを PD に送信できない TiKV ノードを再起動することもできます。
    -   TiKV が Web ID プロバイダーからエラーを受け取り、デフォルト プロバイダー[#13122](https://github.com/tikv/tikv/issues/13122)にフェールバックしたときに、アクセス許可が拒否されたというエラーが発生する問題を修正します。
    -   PD クライアントがデッドロックを引き起こす可能性がある問題を修正します[#13191](https://github.com/tikv/tikv/issues/13191)
    -   Raftstore がビジー状態の場合、リージョンが重複する可能性がある問題を修正します[#13160](https://github.com/tikv/tikv/issues/13160)

-   PD

    -   PD がダッシュボード プロキシ リクエストを正しく処理できない問題を修正します[#5321](https://github.com/tikv/pd/issues/5321)
    -   PDリーダーの転送後、削除されたトゥームストーンストアが再び表示される問題を修正[#4941](https://github.com/tikv/pd/issues/4941)
    -   TiFlash学習者のレプリカが作成されない場合がある問題を修正します[#5401](https://github.com/tikv/pd/issues/5401)

-   TiFlash

    -   `format`関数が`Data truncated`エラー[#4891](https://github.com/pingcap/tiflash/issues/4891)を返す場合がある問題を修正します。
    -   並列集計[#5356](https://github.com/pingcap/tiflash/issues/5356)でエラーが発生してTiFlash がクラッシュすることがある問題を修正
    -   `NULL`値[#5859](https://github.com/pingcap/tiflash/issues/5859)を含む列でプライマリ インデックスを作成した後に発生するpanicを修正します。

-   ツール

    -   TiDB Lightning

        -   タイプ`BIGINT`の自動インクリメント列が範囲外になる可能性がある問題を修正します[#27397](https://github.com/pingcap/tidb/issues/27937)
        -   重複除外が極端な場合にTiDB Lightning でpanicを引き起こす可能性がある問題を修正します[#34163](https://github.com/pingcap/tidb/issues/34163)
        -   TiDB Lightning がParquet ファイルのスラッシュ、数字、または非 ASCII 文字で始まる列をサポートしていない問題を修正します[#36980](https://github.com/pingcap/tidb/issues/36980)
        -   TiDB が IPv6 ホストを使用している場合、 TiDB Lightning がTiDB に接続できない問題を修正します[#35880](https://github.com/pingcap/tidb/issues/35880)

    -   TiDB データ移行 (DM)

        -   DB Conn [#3733](https://github.com/pingcap/tiflow/issues/3733)の取得時に DM Worker がスタックする問題を修正
        -   DM が`Specified key was too long`エラー[#5315](https://github.com/pingcap/tiflow/issues/5315)を報告する問題を修正
        -   レプリケーション中に latin1 データが破損する可能性がある問題を修正します[#7028](https://github.com/pingcap/tiflow/issues/7028)
        -   TiDB が IPv6 ホストを使用する場合に DM の開始に失敗する問題を修正します[#6249](https://github.com/pingcap/tiflow/issues/6249)
        -   `query-status` [#4811](https://github.com/pingcap/tiflow/issues/4811)でデータ競合が発生する可能性がある問題を修正
        -   リレーがエラーに遭遇したときのゴルーチン リークを修正します[#6193](https://github.com/pingcap/tiflow/issues/6193)

    -   TiCDC

        -   `enable-old-value = false` [#6198](https://github.com/pingcap/tiflow/issues/6198)を設定したときの TiCDCpanicの問題を修正します。

    -   バックアップと復元 (BR)

        -   外部storage[#37469](https://github.com/pingcap/tidb/issues/37469)の認証キーに特殊文字が含まれていると、バックアップと復元に失敗する可能性がある問題を修正
        -   復元時に同時実行数が大きすぎるため、リージョンのバランスが取れていない問題を修正します[#37549](https://github.com/pingcap/tidb/issues/37549)

    -   Dumpling

        -   GetDSN が IPv6 をサポートしていない問題を修正[#36112](https://github.com/pingcap/tidb/issues/36112)
