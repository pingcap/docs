---
title: TiDB 5.4.3 Release Notes
summary: TiDB 5.4.3は2022年10月13日にリリースされました。このリリースには、TiKV、ツール、TiCDC、 TiFlash、PD、その他のツールに対するさまざまな改善とバグ修正が含まれています。改善点には、RocksDBの書き込みストール設定のサポート、Scatter リージョンのバッチモードへの最適化、マルチリージョンシナリオにおけるパフォーマンスオーバーヘッドの削減が含まれます。バグ修正では、「SHOW CREATE PLACEMENT POLICY」の出力が正しくない、PDノードの置き換え後にDDL文がスタックする、TiDB、TiKV、PD、 TiFlash、その他のツールで誤った結果やエラーを引き起こすさまざまな問題が修正されています。また、このリリースでは、特定の問題に対する回避策と影響を受けるバージョンも提供されています。
---

# TiDB 5.4.3 リリースノート {#tidb-5-4-3-release-notes}

発売日：2022年10月13日

TiDB バージョン: 5.4.3

## 改善点 {#improvements}

-   TiKV

    -   RocksDB 書き込みストール設定をフロー制御しきい値[＃13467](https://github.com/tikv/tikv/issues/13467)より小さい値に設定できるようになりました。
    -   1つのピアが到達不能になった後にRaftstoreが過剰なメッセージをブロードキャストするのを避けるために`unreachable_backoff`項目の設定をサポートします[＃13054](https://github.com/tikv/tikv/issues/13054)

-   ツール

    -   TiDB Lightning

        -   散布リージョンをバッチモードに最適化して、散布リージョンプロセスの安定性を向上させます[＃33618](https://github.com/pingcap/tidb/issues/33618)

    -   TiCDC

        -   マルチリージョンシナリオにおける実行時コンテキスト切り替えによるパフォーマンスオーバーヘッドを削減[＃5610](https://github.com/pingcap/tiflow/issues/5610)

## バグ修正 {#bug-fixes}

-   TiDB

    -   `SHOW CREATE PLACEMENT POLICY` [＃37526](https://github.com/pingcap/tidb/issues/37526)の誤った出力を修正
    -   クラスターのPDノードが交換された後、一部のDDL文が一定期間スタックする可能性がある問題を修正しました[＃33908](https://github.com/pingcap/tidb/issues/33908)
    -   `KILL TIDB`アイドル接続時にすぐに効果を発揮できない問題を修正[＃24031](https://github.com/pingcap/tidb/issues/24031)
    -   `INFORMSTION_SCHEMA.COLUMNS`システムテーブル[＃36496](https://github.com/pingcap/tidb/issues/36496)をクエリするときに`DATA_TYPE`と`COLUMN_TYPE`列に誤った結果が返される問題を修正しました
    -   TiDB Binlogが有効な場合、 `ALTER SEQUENCE`文を実行するとメタデータ バージョンが間違って発生し、 Drainerが終了する可能性がある問題を修正しました[＃36276](https://github.com/pingcap/tidb/issues/36276)
    -   `UNION`演算子が予期しない空の結果[＃36903](https://github.com/pingcap/tidb/issues/36903)を返す可能性がある問題を修正しました
    -   TiFlash [＃37254](https://github.com/pingcap/tidb/issues/37254)のパーティションテーブルでダイナミックモードを有効にしたときに発生する誤った結果を修正しました
    -   `LIMIT` [＃35638](https://github.com/pingcap/tidb/issues/35638)と併用すると`INL_HASH_JOIN`ハングアップする可能性がある問題を修正
    -   TiDBが`SHOW WARNINGS`ステートメント[＃31569](https://github.com/pingcap/tidb/issues/31569)を実行するときに`invalid memory address or nil pointer dereference`エラーを返す可能性がある問題を修正しました
    -   RC分離レベル[＃30872](https://github.com/pingcap/tidb/issues/30872)でステイル読み取りを実行するときに発生する`invalid transaction`エラーを修正
    -   DMLエグゼキュータを使用した`EXPLAIN ANALYZE`文がトランザクションコミットが完了する前に結果を返す可能性がある問題を修正しました[＃37373](https://github.com/pingcap/tidb/issues/37373)
    -   TiDB Binlogを有効にして重複した値を挿入すると発生する`data and columnID count not match`エラーの問題を修正しました[＃33608](https://github.com/pingcap/tidb/issues/33608)
    -   静的パーティションプルーニングモードで、テーブルが空の場合に集計条件を含むSQL文が間違った結果を返す可能性がある問題を修正しました[＃35295](https://github.com/pingcap/tidb/issues/35295)
    -   `UPDATE`文[＃32311](https://github.com/pingcap/tidb/issues/32311)を実行するときに TiDB がpanic可能性がある問題を修正しました
    -   `UnionScan`演算子が順序を維持できないために間違ったクエリ結果が発生する問題を修正[＃33175](https://github.com/pingcap/tidb/issues/33175)
    -   UPDATE文が場合によっては投影を誤って削除し、 `Can't find column`エラー[＃37568](https://github.com/pingcap/tidb/issues/37568)が発生する問題を修正しました。
    -   パーティションテーブルがインデックスを完全に使用してデータをスキャンできない場合がある問題を修正[＃33966](https://github.com/pingcap/tidb/issues/33966)
    -   特定のシナリオ[＃37187](https://github.com/pingcap/tidb/issues/37187)予期しないエラーが発生する可能性がある問題を修正しました`EXECUTE`
    -   準備済みプランキャッシュが有効になっている`BIT`タイプのインデックスを使用すると、TiDBが間違った結果を返す可能性がある問題を修正しました[＃33067](https://github.com/pingcap/tidb/issues/33067)

-   TiKV

    -   PDリーダーの切り替え後またはPDの再起動後にクラスタ内でSQL実行エラーが継続する問題を修正[＃12934](https://github.com/tikv/tikv/issues/12934)
        -   原因：この問題は、TiKVのバグが原因で発生します。このバグにより、ハートビート要求が失敗した後、TiKVはPDクライアントに再接続するまで、PDクライアントへのハートビート情報の送信を再試行しません。その結果、障害が発生したTiKVノードのリージョン情報が古くなり、TiDBは最新のリージョン情報を取得できず、SQL実行エラーが発生します。
        -   影響を受けるバージョン: v5.3.2 および v5.4.2。この問題は v5.3.3 および v5.4.3 で修正されています。v5.4.2 をご利用の場合は、クラスターを v5.4.3 にアップグレードできます。
        -   回避策: アップグレードに加えて、送信するリージョンハートビートがなくなるまで、リージョンハートビートを PD に送信できない TiKV ノードを再起動することもできます。
    -   TiKV が Web ID プロバイダーからエラーを取得し、デフォルトのプロバイダー[＃13122](https://github.com/tikv/tikv/issues/13122)にフェイルバックしたときに、権限拒否エラーが発生する問題を修正しました。
    -   PDクライアントがデッドロックを引き起こす可能性がある問題を修正[＃13191](https://github.com/tikv/tikv/issues/13191)
    -   Raftstoreがビジー状態の場合にリージョンが重複する可能性がある問題を修正[＃13160](https://github.com/tikv/tikv/issues/13160)

-   PD

    -   PDがダッシュボードプロキシリクエストを正しく処理できない問題を修正[＃5321](https://github.com/tikv/pd/issues/5321)
    -   PDリーダー移転後に削除した墓石ストアが再び表示される問題を修正[＃4941](https://github.com/tikv/pd/issues/4941)
    -   TiFlash学習者レプリカが作成されない可能性がある問題を修正[＃5401](https://github.com/tikv/pd/issues/5401)

-   TiFlash

    -   `format`関数が`Data truncated`エラー[＃4891](https://github.com/pingcap/tiflash/issues/4891)を返す可能性がある問題を修正しました
    -   並列集約[＃5356](https://github.com/pingcap/tiflash/issues/5356)エラーによりTiFlashがクラッシュする可能性がある問題を修正
    -   `NULL`値[＃5859](https://github.com/pingcap/tiflash/issues/5859)を含む列を持つプライマリインデックスを作成した後に発生するpanicを修正しました

-   ツール

    -   TiDB Lightning

        -   `BIGINT`型の自動増分列が範囲外になる可能性がある問題を修正[＃27937](https://github.com/pingcap/tidb/issues/27937)
        -   重複排除により極端な場合にTiDB Lightning がpanicを起こす可能性がある問題を修正[＃34163](https://github.com/pingcap/tidb/issues/34163)
        -   TiDB Lightning がParquet ファイル内のスラッシュ、数字、または非 ASCII 文字で始まる列をサポートしない問題を修正しました[＃36980](https://github.com/pingcap/tidb/issues/36980)
        -   TiDBがIPv6ホスト[＃35880](https://github.com/pingcap/tidb/issues/35880)を使用しているときにTiDB LightningがTiDBに接続できない問題を修正しました

    -   TiDB データ移行 (DM)

        -   DB Conn [＃3733](https://github.com/pingcap/tiflow/issues/3733)取得する際に DM ワーカーがスタックする可能性がある問題を修正しました
        -   DMが`Specified key was too long`エラーを報告する問題を修正しました[＃5315](https://github.com/pingcap/tiflow/issues/5315)
        -   レプリケーション[＃7028](https://github.com/pingcap/tiflow/issues/7028)中にlatin1データが破損する可能性がある問題を修正
        -   TiDBがIPv6ホスト[＃6249](https://github.com/pingcap/tiflow/issues/6249)を使用しているときにDMが起動に失敗する問題を修正
        -   `query-status` [＃4811](https://github.com/pingcap/tiflow/issues/4811)で起こりうるデータ競合の問題を修正
        -   リレーがエラー[＃6193](https://github.com/pingcap/tiflow/issues/6193)に遭遇したときの goroutine リークを修正

    -   TiCDC

        -   `enable-old-value = false` [＃6198](https://github.com/pingcap/tiflow/issues/6198)を設定すると TiCDCpanicする問題を修正

    -   バックアップと復元 (BR)

        -   外部storage[＃37469](https://github.com/pingcap/tidb/issues/37469)の認証キーに特殊文字が含まれている場合にバックアップと復元が失敗する可能性がある問題を修正しました
        -   復元中に同時実行が大きすぎる設定になっているために領域のバランスが取れていない問題を修正[＃37549](https://github.com/pingcap/tidb/issues/37549)

    -   Dumpling

        -   GetDSNがIPv6 [＃36112](https://github.com/pingcap/tidb/issues/36112)をサポートしていない問題を修正
