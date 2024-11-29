---
title: TiDB 5.4.3 Release Notes
summary: TiDB 5.4.3 は 2022 年 10 月 13 日にリリースされました。このリリースには、TiKV、ツール、TiCDC、 TiFlash、PD、およびその他のツールのさまざまな改善とバグ修正が含まれています。改善には、RocksDB 書き込みストール設定の構成のサポート、Scatter リージョン のバッチ モードへの最適化、およびマルチリージョン シナリオでのパフォーマンス オーバーヘッドの削減が含まれます。バグ修正では、SHOW CREATE PLACEMENT POLICY` の誤った出力、PD ノードの置き換え後に DDL ステートメントがスタックする問題、TiDB、TiKV、PD、 TiFlash、およびその他のツールで誤った結果やエラーを引き起こすさまざまな問題に対処しています。このリリースでは、特定の問題に対する回避策と影響を受けるバージョンも提供されています。
---

# TiDB 5.4.3 リリースノート {#tidb-5-4-3-release-notes}

発売日: 2022年10月13日

TiDB バージョン: 5.4.3

## 改善点 {#improvements}

-   ティクヴ

    -   RocksDB 書き込みストール設定をフロー制御しきい値[＃13467](https://github.com/tikv/tikv/issues/13467)より小さい値に設定できるようになりました。
    -   1 つのピアが到達不能になった後にRaftstore がメッセージを大量にブロードキャストするのを回避するための`unreachable_backoff`項目の設定をサポートします[＃13054](https://github.com/tikv/tikv/issues/13054)

-   ツール

    -   TiDB Lightning

        -   散布リージョンをバッチモードに最適化して、散布リージョンプロセスの安定性を向上させる[＃33618](https://github.com/pingcap/tidb/issues/33618)

    -   ティCDC

        -   マルチリージョンシナリオでのランタイムコンテキスト切り替えによるパフォーマンスオーバーヘッドを削減[＃5610](https://github.com/pingcap/tiflow/issues/5610)

## バグ修正 {#bug-fixes}

-   ティビ

    -   `SHOW CREATE PLACEMENT POLICY` [＃37526](https://github.com/pingcap/tidb/issues/37526)の誤った出力を修正
    -   クラスターの PD ノードが置き換えられた後、一部の DDL ステートメントが一定期間停止する可能性がある問題を修正しました[＃33908](https://github.com/pingcap/tidb/issues/33908)
    -   `KILL TIDB`アイドル接続ですぐに効果を発揮できない問題を修正[＃24031](https://github.com/pingcap/tidb/issues/24031)
    -   `INFORMSTION_SCHEMA.COLUMNS`システム テーブル[＃36496](https://github.com/pingcap/tidb/issues/36496)クエリするときに`DATA_TYPE`列と`COLUMN_TYPE`列に誤った結果が返される問題を修正しました。
    -   TiDB Binlogが有効な場合、 `ALTER SEQUENCE`ステートメントを実行するとメタデータ バージョンが間違って生成され、 Drainer が終了する可能性がある問題を修正しました[＃36276](https://github.com/pingcap/tidb/issues/36276)
    -   `UNION`演算子が予期しない空の結果[＃36903](https://github.com/pingcap/tidb/issues/36903)を返す可能性がある問題を修正しました
    -   TiFlash [＃37254](https://github.com/pingcap/tidb/issues/37254)のパーティション テーブルで動的モードを有効にしたときに発生する誤った結果を修正しました。
    -   `INL_HASH_JOIN` `LIMIT` [＃35638](https://github.com/pingcap/tidb/issues/35638)と併用するとハングアップする可能性がある問題を修正
    -   `SHOW WARNINGS`ステートメント[＃31569](https://github.com/pingcap/tidb/issues/31569)実行するときに TiDB が`invalid memory address or nil pointer dereference`エラーを返す可能性がある問題を修正しました。
    -   RC分離レベル[＃30872](https://github.com/pingcap/tidb/issues/30872)でステイル読み取りを実行するときに発生する`invalid transaction`エラーを修正
    -   DMLエグゼキュータを使用した`EXPLAIN ANALYZE`文がトランザクションコミットが完了する前に結果を返す可能性がある問題を修正しました[＃37373](https://github.com/pingcap/tidb/issues/37373)
    -   TiDB Binlog を有効にして重複した値を挿入すると発生する`data and columnID count not match`エラーの問題を修正[＃33608](https://github.com/pingcap/tidb/issues/33608)
    -   静的パーティションプルーニングモードで、テーブルが空の場合に集計条件を含む SQL ステートメントが間違った結果を返す可能性がある問題を修正しました[＃35295](https://github.com/pingcap/tidb/issues/35295)
    -   `UPDATE`文[＃32311](https://github.com/pingcap/tidb/issues/32311)を実行するときに TiDB がpanic可能性がある問題を修正しました
    -   `UnionScan`演算子が順序を維持できないために間違ったクエリ結果が発生する問題を修正[＃33175](https://github.com/pingcap/tidb/issues/33175)
    -   UPDATE文が場合によっては投影を誤って削除し、 `Can't find column`エラー[＃37568](https://github.com/pingcap/tidb/issues/37568)が発生する問題を修正しました。
    -   パーティションテーブルがインデックスを完全に使用してデータをスキャンできない場合がある問題を修正[＃33966](https://github.com/pingcap/tidb/issues/33966)
    -   特定のシナリオで予期しない`EXECUTE`が発生する可能性がある問題を修正しました[＃37187](https://github.com/pingcap/tidb/issues/37187)
    -   準備済みプランキャッシュを有効にした`BIT`タイプのインデックスを使用すると、TiDBが間違った結果を返す可能性がある問題を修正しました[＃33067](https://github.com/pingcap/tidb/issues/33067)

-   ティクヴ

    -   PDリーダーの切り替え後またはPDの再起動後にクラスター内でSQL実行エラーが継続する問題を修正[＃12934](https://github.com/tikv/tikv/issues/12934)
        -   原因: この問題は、TiKV のバグによって発生します。TiKV は、ハートビート要求が失敗した後、PD クライアントに再接続するまで、PD クライアントへのハートビート情報の送信を再試行しません。その結果、障害が発生した TiKV ノードのリージョン情報が古くなり、TiDB は最新のリージョン情報を取得できず、SQL 実行エラーが発生します。
        -   影響を受けるバージョン: v5.3.2 および v5.4.2。この問題は v5.3.3 および v5.4.3 で修正されています。v5.4.2 を使用している場合は、クラスターを v5.4.3 にアップグレードできます。
        -   回避策: アップグレードに加えて、送信するリージョンハートビートがなくなるまで、リージョンハートビートをPD に送信できない TiKV ノードを再起動することもできます。
    -   TiKV が Web ID プロバイダーからエラーを受け取り、デフォルトのプロバイダー[＃13122](https://github.com/tikv/tikv/issues/13122)にフェールバックしたときに、権限拒否エラーが発生する問題を修正しました。
    -   PDクライアントがデッドロックを引き起こす可能性がある問題を修正[＃13191](https://github.com/tikv/tikv/issues/13191)
    -   Raftstoreがビジー状態の場合にリージョンが重複する可能性がある問題を修正[＃13160](https://github.com/tikv/tikv/issues/13160)

-   PD

    -   PDがダッシュボードプロキシリクエストを正しく処理できない問題を修正[＃5321](https://github.com/tikv/pd/issues/5321)
    -   PDリーダーの移転後に削除された墓石ストアが再び表示される問題を修正[＃4941](https://github.com/tikv/pd/issues/4941)
    -   TiFlash学習レプリカが作成されない可能性がある問題を修正[＃5401](https://github.com/tikv/pd/issues/5401)

-   TiFlash

    -   `format`関数が`Data truncated`エラー[＃4891](https://github.com/pingcap/tiflash/issues/4891)を返す可能性がある問題を修正
    -   並列集約[＃5356](https://github.com/pingcap/tiflash/issues/5356)のエラーによりTiFlashがクラッシュする可能性がある問題を修正
    -   `NULL`値[＃5859](https://github.com/pingcap/tiflash/issues/5859)を含む列でプライマリインデックスを作成した後に発生するpanicを修正

-   ツール

    -   TiDB Lightning

        -   `BIGINT`タイプの自動増分列が範囲外になる可能性がある問題を修正[＃27937](https://github.com/pingcap/tidb/issues/27937)
        -   重複排除により極端な場合にTiDB Lightning がpanicを起こす可能性がある問題を修正[＃34163](https://github.com/pingcap/tidb/issues/34163)
        -   TiDB Lightning がParquet ファイル内のスラッシュ、数字、または非 ASCII 文字で始まる列をサポートしない問題を修正しました[＃36980](https://github.com/pingcap/tidb/issues/36980)
        -   TiDB が IPv6 ホスト[＃35880](https://github.com/pingcap/tidb/issues/35880)を使用している場合にTiDB Lightning がTiDB に接続できない問題を修正しました。

    -   TiDB データ移行 (DM)

        -   DB Conn [＃3733](https://github.com/pingcap/tiflow/issues/3733)取得する際に DM Worker がスタックする可能性がある問題を修正しました。
        -   DMが`Specified key was too long`エラー[＃5315](https://github.com/pingcap/tiflow/issues/5315)報告する問題を修正
        -   レプリケーション中にlatin1データが破損する可能性がある問題を修正[＃7028](https://github.com/pingcap/tiflow/issues/7028)
        -   TiDBがIPv6ホスト[＃6249](https://github.com/pingcap/tiflow/issues/6249)を使用するとDMが起動に失敗する問題を修正
        -   `query-status` [＃4811](https://github.com/pingcap/tiflow/issues/4811)で起こりうるデータ競合の問題を修正
        -   リレーがエラーに遭遇したときの goroutine リークを修正[＃6193](https://github.com/pingcap/tiflow/issues/6193)

    -   ティCDC

        -   `enable-old-value = false` [＃6198](https://github.com/pingcap/tiflow/issues/6198)を設定すると TiCDCpanic問題を修正

    -   バックアップと復元 (BR)

        -   外部storage[＃37469](https://github.com/pingcap/tidb/issues/37469)の認証キーに特殊文字が含まれている場合にバックアップと復元が失敗する可能性がある問題を修正
        -   復元中に同時実行数が大きすぎるために領域のバランスが取れない問題を修正[＃37549](https://github.com/pingcap/tidb/issues/37549)

    -   Dumpling

        -   GetDSNがIPv6をサポートしていない問題を修正[＃36112](https://github.com/pingcap/tidb/issues/36112)
