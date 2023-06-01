---
title: TiDB 6.1.1 Release Notes
---

# TiDB 6.1.1 リリースノート {#tidb-6-1-1-release-notes}

発売日：2022年9月1日

TiDB バージョン: 6.1.1

クイックアクセス: [<a href="https://docs.pingcap.com/tidb/v6.1/quick-start-with-tidb">クイックスタート</a>](https://docs.pingcap.com/tidb/v6.1/quick-start-with-tidb) | [<a href="https://docs.pingcap.com/tidb/v6.1/production-deployment-using-tiup">本番展開</a>](https://docs.pingcap.com/tidb/v6.1/production-deployment-using-tiup) | [<a href="https://www.pingcap.com/download/?version=v6.1.1#version-list">インストールパッケージ</a>](https://www.pingcap.com/download/?version=v6.1.1#version-list)

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   `SHOW DATABASES LIKE …`ステートメントの大文字と小文字を区別しないようにします[<a href="https://github.com/pingcap/tidb/issues/34766">#34766</a>](https://github.com/pingcap/tidb/issues/34766) @ [<a href="https://github.com/e1ijah1">e1ijah1</a>](https://github.com/e1ijah1)
    -   デフォルト値[<a href="/system-variables.md#tidb_enable_outer_join_reorder-new-in-v610">`tidb_enable_outer_join_reorder`</a>](/system-variables.md#tidb_enable_outer_join_reorder-new-in-v610) `1`から`0`に変更します。これにより、Join Reorder によるアウター結合のサポートがデフォルトで無効になります。

-   診断

    -   継続的プロファイリング機能をデフォルトで無効にすると、この機能が有効になっているときに発生する可能性のあるTiFlashクラッシュの問題が回避されます。詳細は[<a href="https://github.com/pingcap/tiflash/issues/5687">#5687</a>](https://github.com/pingcap/tiflash/issues/5687) @ [<a href="https://github.com/mornyx">モニクス</a>](https://github.com/mornyx)を参照してください。

## その他の変更点 {#other-changes}

-   `TiDB-community-toolkit`バイナリ パッケージに以下の内容を追加します。詳細は[<a href="/binary-package.md">TiDB インストール パッケージ</a>](/binary-package.md)を参照してください。

    -   `server-{version}-linux-amd64.tar.gz`
    -   `grafana-{version}-linux-amd64.tar.gz`
    -   `alertmanager-{version}-linux-amd64.tar.gz`
    -   `prometheus-{version}-linux-amd64.tar.gz`
    -   `blackbox_exporter-{version}-linux-amd64.tar.gz`
    -   `node_exporter-{version}-linux-amd64.tar.gz`

-   オペレーティング システムと CPU アーキテクチャの組み合わせに関するさまざまな品質基準に対するマルチレベルのサポートを導入します。 [<a href="https://docs.pingcap.com/tidb/v6.1/hardware-and-software-requirements#os-and-platform-requirements">OS とプラットフォームの要件</a>](https://docs.pingcap.com/tidb/v6.1/hardware-and-software-requirements#os-and-platform-requirements)を参照してください。

## 改善点 {#improvements}

-   TiDB

    -   新しいオプティマイザ`SEMI_JOIN_REWRITE`を追加して、 `EXISTS`クエリ[<a href="https://github.com/pingcap/tidb/issues/35323">#35323</a>](https://github.com/pingcap/tidb/issues/35323) @ [<a href="https://github.com/winoros">ウィノロス</a>](https://github.com/winoros)のパフォーマンスを向上させます。

-   TiKV

    -   gzip を使用したメトリクス応答の圧縮をサポートし、HTTP 本文のサイズ[<a href="https://github.com/tikv/tikv/issues/12355">#12355</a>](https://github.com/tikv/tikv/issues/12355) @ [<a href="https://github.com/winoros">ウィノロス</a>](https://github.com/winoros)を削減します。
    -   [<a href="https://docs.pingcap.com/tidb/v6.1/tikv-configuration-file#simplify-metrics-new-in-v611">`server.simplify-metrics`</a>](https://docs.pingcap.com/tidb/v6.1/tikv-configuration-file#simplify-metrics-new-in-v611)構成項目[<a href="https://github.com/tikv/tikv/issues/12355">#12355</a>](https://github.com/tikv/tikv/issues/12355) @ [<a href="https://github.com/glorv">グロルフ</a>](https://github.com/glorv)を使用して一部のメトリクスをフィルタリングすることにより、リクエストごとに返されるデータ量の削減をサポートします。
    -   RocksDB で同時に実行されるサブコンパクション操作の数の動的変更をサポート ( `rocksdb.max-sub-compactions` ) [<a href="https://github.com/tikv/tikv/issues/13145">#13145</a>](https://github.com/tikv/tikv/issues/13145) @ [<a href="https://github.com/ethercflow">エーテルフロー</a>](https://github.com/ethercflow)

-   PD

    -   特定のステージ[<a href="https://github.com/tikv/pd/issues/4990">#4990</a>](https://github.com/tikv/pd/issues/4990) @ [<a href="https://github.com/bufferflies">バッファフライ</a>](https://github.com/bufferflies)におけるバランスリージョンのスケジューリング速度を向上させます。

-   ツール

    -   TiDB Lightning

        -   `stale command`などのエラーに対する再試行メカニズムを追加して、インポート成功率[<a href="https://github.com/pingcap/tidb/issues/36877">#36877</a>](https://github.com/pingcap/tidb/issues/36877) @ [<a href="https://github.com/D3Hunter">D3ハンター</a>](https://github.com/D3Hunter)を向上させます。

    -   TiDB データ移行 (DM)

        -   ユーザーは、Lightning Loader [<a href="https://github.com/pingcap/tiflow/issues/5505">#5505</a>](https://github.com/pingcap/tiflow/issues/5505) @ [<a href="https://github.com/buchuitoudegou">ブチュイトデゴウ</a>](https://github.com/buchuitoudegou)の同時実行量を手動で設定できます。

    -   TiCDC

        -   シンク URI パラメーター`transaction-atomicity`を追加して、変更フィード内の大規模なトランザクションの分割をサポートします。これにより、大規模なトランザクションのレイテンシーとメモリ消費量を大幅に削減できます[<a href="https://github.com/pingcap/tiflow/issues/5231">#5231</a>](https://github.com/pingcap/tiflow/issues/5231) @ [<a href="https://github.com/CharlesCheung96">CharlesCheung96</a>](https://github.com/CharlesCheung96)
        -   マルチリージョン シナリオ[<a href="https://github.com/pingcap/tiflow/issues/5610">#5610</a>](https://github.com/pingcap/tiflow/issues/5610) @ [<a href="https://github.com/hicqu">ひっくり返る</a>](https://github.com/hicqu)でのランタイム コンテキストの切り替えによって生じるパフォーマンスのオーバーヘッドを削減します。
        -   MySQL シンクを強化してセーフ モードを自動的にオフにする[<a href="https://github.com/pingcap/tiflow/issues/5611">#5611</a>](https://github.com/pingcap/tiflow/issues/5611) @ [<a href="https://github.com/overvenus">オーバーヴィーナス</a>](https://github.com/overvenus)

## バグの修正 {#bug-fixes}

-   TiDB

    -   `INL_HASH_JOIN` `LIMIT` [<a href="https://github.com/pingcap/tidb/issues/35638">#35638</a>](https://github.com/pingcap/tidb/issues/35638) @ [<a href="https://github.com/guo-shaoge">グオシャオゲ</a>](https://github.com/guo-shaoge)と一緒に使用するとハングする可能性がある問題を修正
    -   `UPDATE`ステートメント[<a href="https://github.com/pingcap/tidb/issues/32311">#32311</a>](https://github.com/pingcap/tidb/issues/32311) @ [<a href="https://github.com/Yisaer">イーサール</a>](https://github.com/Yisaer)の実行時に TiDB がpanic可能性がある問題を修正
    -   `SHOW COLUMNS`ステートメント[<a href="https://github.com/pingcap/tidb/issues/36496">#36496</a>](https://github.com/pingcap/tidb/issues/36496) @ [<a href="https://github.com/tangenta">タンジェンタ</a>](https://github.com/tangenta)の実行時に TiDB がコプロセッサ リクエストを送信する可能性があるバグを修正
    -   `SHOW WARNINGS`ステートメント[<a href="https://github.com/pingcap/tidb/issues/31569">#31569</a>](https://github.com/pingcap/tidb/issues/31569) @ [<a href="https://github.com/zyguan">ジグアン</a>](https://github.com/zyguan)を実行すると TiDB が`invalid memory address or nil pointer dereference`エラーを返すことがあるバグを修正
    -   静的パーティション プルーン モードにおいて、テーブルが空の場合に集計条件を含む SQL ステートメントが間違った結果を返す可能性があるバグを修正[<a href="https://github.com/pingcap/tidb/issues/35295">#35295</a>](https://github.com/pingcap/tidb/issues/35295) @ [<a href="https://github.com/tiancaiamao">ティエンチャイアマオ</a>](https://github.com/tiancaiamao)
    -   結合したテーブルの再配置操作により誤って外部結合条件[<a href="https://github.com/pingcap/tidb/issues/37238">#37238</a>](https://github.com/pingcap/tidb/issues/37238) @ [<a href="https://github.com/winoros">ウィノロス</a>](https://github.com/winoros)がプッシュダウンされる問題を修正します。
    -   CTE スキーマのハッシュ コードが誤って複製され、CTE が複数回参照されると`Can't find column ... in schema ...`エラーが発生する問題を修正[<a href="https://github.com/pingcap/tidb/issues/35404">#35404</a>](https://github.com/pingcap/tidb/issues/35404) @ [<a href="https://github.com/AilinKid">アイリンキッド</a>](https://github.com/AilinKid)
    -   一部の右外部結合シナリオで結合の再順序が間違っていると、間違ったクエリ結果[<a href="https://github.com/pingcap/tidb/issues/36912">#36912</a>](https://github.com/pingcap/tidb/issues/36912) @ [<a href="https://github.com/winoros">ウィノロス</a>](https://github.com/winoros)が発生する問題を修正します。
    -   EqualAll case [<a href="https://github.com/pingcap/tidb/issues/34584">#34584</a>](https://github.com/pingcap/tidb/issues/34584) @ [<a href="https://github.com/fixdb">修正データベース</a>](https://github.com/fixdb)でのTiFlash `firstrow`集約関数の null フラグが誤って推論される問題を修正
    -   `IGNORE_PLAN_CACHE`ヒント[<a href="https://github.com/pingcap/tidb/issues/34596">#34596</a>](https://github.com/pingcap/tidb/issues/34596) @ [<a href="https://github.com/fzzf678">fzzf678</a>](https://github.com/fzzf678)でバインディングが作成されるとプラン キャッシュが機能しない問題を修正
    -   ハッシュ パーティション ウィンドウと単一パーティション ウィンドウ[<a href="https://github.com/pingcap/tidb/issues/35990">#35990</a>](https://github.com/pingcap/tidb/issues/35990) @ [<a href="https://github.com/LittleFall">リトルフォール</a>](https://github.com/LittleFall)の間に`EXCHANGE`演算子が欠落している問題を修正
    -   場合によっては、パーティション テーブルがインデックスを完全に使用してデータをスキャンできない問題を修正します[<a href="https://github.com/pingcap/tidb/issues/33966">#33966</a>](https://github.com/pingcap/tidb/issues/33966) @ [<a href="https://github.com/mjonss">むじょん</a>](https://github.com/mjonss)
    -   集計がプッシュダウンされた後、部分集計に間違ったデフォルト値が設定されている場合に、間違ったクエリ結果が表示される問題を修正します[<a href="https://github.com/pingcap/tidb/issues/35295">#35295</a>](https://github.com/pingcap/tidb/issues/35295) @ [<a href="https://github.com/tiancaiamao">ティエンチャイアマオ</a>](https://github.com/tiancaiamao)
    -   場合によってはパーティション テーブルのクエリで`index-out-of-range`エラーが発生することがある問題を修正します[<a href="https://github.com/pingcap/tidb/issues/35181">#35181</a>](https://github.com/pingcap/tidb/issues/35181) @ [<a href="https://github.com/mjonss">むじょん</a>](https://github.com/mjonss)
    -   クエリ条件でパーティション キーが使用されており、照合順序がクエリ パーティション テーブル[<a href="https://github.com/pingcap/tidb/issues/32749">#32749</a>](https://github.com/pingcap/tidb/issues/32749) @ [<a href="https://github.com/mjonss">むじょん</a>](https://github.com/mjonss)の照合順序と異なる場合、パーティションが誤ってプルーニングされる問題を修正します。
    -   TiDB Binlogが有効な場合、 `ALTER SEQUENCE`ステートメントを実行するとメタデータのバージョンが間違って、 Drainerが終了する可能性がある問題を修正します[<a href="https://github.com/pingcap/tidb/issues/36276">#36276</a>](https://github.com/pingcap/tidb/issues/36276) @ [<a href="https://github.com/AilinKid">アイリンキッド</a>](https://github.com/AilinKid)
    -   一部の極端なケースで起動時に表示される可能性がある不正な TiDB ステータスの問題を修正します[<a href="https://github.com/pingcap/tidb/issues/36791">#36791</a>](https://github.com/pingcap/tidb/issues/36791) @ [<a href="https://github.com/xhebox">ゼボックス</a>](https://github.com/xhebox)
    -   TiDB ダッシュボード[<a href="https://github.com/pingcap/tidb/issues/35153">#35153</a>](https://github.com/pingcap/tidb/issues/35153) @ [<a href="https://github.com/time-and-fate">時間と運命</a>](https://github.com/time-and-fate)でパーティション化されたテーブルの実行プランをクエリするときに発生する潜在的な問題`UnknownPlanID`修正します。
    -   LOAD DATA ステートメント[<a href="https://github.com/pingcap/tidb/issues/35198">#35198</a>](https://github.com/pingcap/tidb/issues/35198) @ [<a href="https://github.com/SpadeA-Tang">SpadeA-Tang</a>](https://github.com/SpadeA-Tang)で列リストが機能しない問題を修正します。
    -   TiDB Binlogが有効になっている場合に重複した値を挿入するときに発生する`data and columnID count not match`エラーの問題を修正します[<a href="https://github.com/pingcap/tidb/issues/33608">#33608</a>](https://github.com/pingcap/tidb/issues/33608) @ [<a href="https://github.com/zyguan">ジグアン</a>](https://github.com/zyguan)
    -   `tidb_gc_life_time` [<a href="https://github.com/pingcap/tidb/issues/35392">#35392</a>](https://github.com/pingcap/tidb/issues/35392) @ [<a href="https://github.com/TonsnakeLin">トンスネークリン</a>](https://github.com/TonsnakeLin)の制限を削除します
    -   空のフィールドターミネータが使用されている場合の`LOAD DATA`ステートメントのデッドループを修正[<a href="https://github.com/pingcap/tidb/issues/33298">#33298</a>](https://github.com/pingcap/tidb/issues/33298) @ [<a href="https://github.com/zyguan">ジグアン</a>](https://github.com/zyguan)
    -   可用性を向上させるために、異常な TiKV ノードへのリクエストの送信を回避します[<a href="https://github.com/pingcap/tidb/issues/34906">#34906</a>](https://github.com/pingcap/tidb/issues/34906) @ [<a href="https://github.com/sticnarf">スティックナーフ</a>](https://github.com/sticnarf)

-   TiKV

    -   Raftstoreがビジー[<a href="https://github.com/tikv/tikv/issues/13160">#13160</a>](https://github.com/tikv/tikv/issues/13160) @ [<a href="https://github.com/5kbpers">5kbps</a>](https://github.com/5kbpers)の場合リージョンが重なる可能性があるバグを修正
    -   リージョンハートビートが中断された後、PD が TiKV に再接続しない問題を修正[<a href="https://github.com/tikv/tikv/issues/12934">#12934</a>](https://github.com/tikv/tikv/issues/12934) @ [<a href="https://github.com/bufferflies">バッファフライ</a>](https://github.com/bufferflies)
    -   空の文字列[<a href="https://github.com/tikv/tikv/issues/12673">#12673</a>](https://github.com/tikv/tikv/issues/12673) @ [<a href="https://github.com/wshwsh12">wshwsh12</a>](https://github.com/wshwsh12)の型変換を実行すると TiKV がパニックになる問題を修正
    -   TiKV と PD [<a href="https://github.com/tikv/tikv/issues/12518">#12518</a>](https://github.com/tikv/tikv/issues/12518) @ [<a href="https://github.com/5kbpers">5kbps</a>](https://github.com/5kbpers)の間の一貫性のないリージョンサイズ構成の問題を修正
    -   Raft Engineが有効になっている場合に暗号化キーがクリーンアップされない問題を修正[<a href="https://github.com/tikv/tikv/issues/12890">#12890</a>](https://github.com/tikv/tikv/issues/12890) @ [<a href="https://github.com/tabokie">タボキー</a>](https://github.com/tabokie)
    -   ピアの分割と破棄が同時に行われるときに発生する可能性があるpanicの問題を修正[<a href="https://github.com/tikv/tikv/issues/12825">#12825</a>](https://github.com/tikv/tikv/issues/12825) @ [<a href="https://github.com/BusyJay">ビジージェイ</a>](https://github.com/BusyJay)
    -   リージョンマージ プロセス[<a href="https://github.com/tikv/tikv/issues/12663">#12663</a>](https://github.com/tikv/tikv/issues/12663) @ [<a href="https://github.com/BusyJay">ビジージェイ</a>](https://github.com/BusyJay)でソース ピアがスナップショットによってログを追いつくときに発生する可能性があるpanicの問題を修正します。
    -   PD クライアントでエラー[<a href="https://github.com/tikv/tikv/issues/12345">#12345</a>](https://github.com/tikv/tikv/issues/12345) @ [<a href="https://github.com/Connor1996">コナー1996</a>](https://github.com/Connor1996)が発生したときに発生する、PD クライアントの再接続が頻繁に発生する問題を修正します。
    -   Raft Engine [<a href="https://github.com/tikv/tikv/issues/13123">#13123</a>](https://github.com/tikv/tikv/issues/13123) @ [<a href="https://github.com/tabokie">タボキー</a>](https://github.com/tabokie)で並列リカバリが有効になっている場合の潜在的なpanicを修正
    -   新しいリージョンのコミット ログ期間が長すぎるため、QPS が[<a href="https://github.com/tikv/tikv/issues/13077">#13077</a>](https://github.com/tikv/tikv/issues/13077) @ [<a href="https://github.com/Connor1996">コナー1996</a>](https://github.com/Connor1996)低下する問題を修正します。
    -   Raft Engine が有効になっている場合にまれに発生するパニックを修正[<a href="https://github.com/tikv/tikv/issues/12698">#12698</a>](https://github.com/tikv/tikv/issues/12698) @ [<a href="https://github.com/tabokie">タボキー</a>](https://github.com/tabokie)
    -   proc ファイルシステム (procfs) が見つからない場合の冗長なログ警告を回避します[<a href="https://github.com/tikv/tikv/issues/13116">#13116</a>](https://github.com/tikv/tikv/issues/13116) @ [<a href="https://github.com/tabokie">タボキー</a>](https://github.com/tabokie)
    -   ダッシュボード[<a href="https://github.com/tikv/tikv/issues/13086">#13086</a>](https://github.com/tikv/tikv/issues/13086) @ [<a href="https://github.com/glorv">グロルフ</a>](https://github.com/glorv)の`Unified Read Pool CPU`の間違った式を修正
    -   リージョンが大きい場合、デフォルトの[<a href="/tikv-configuration-file.md#region-split-check-diff">`region-split-check-diff`</a>](/tikv-configuration-file.md#region-split-check-diff)バケット サイズ[<a href="https://github.com/tikv/tikv/issues/12598">#12598</a>](https://github.com/tikv/tikv/issues/12598) @ [<a href="https://github.com/tonyxuqqi">トニーシュクキ</a>](https://github.com/tonyxuqqi)より大きくなる可能性がある問題を修正
    -   スナップショットの適用が中止され、 Raft Engineが有効になっている場合に TiKV がpanicになる可能性がある問題を修正[<a href="https://github.com/tikv/tikv/issues/12470">#12470</a>](https://github.com/tikv/tikv/issues/12470) @ [<a href="https://github.com/tabokie">タボキー</a>](https://github.com/tabokie)
    -   PD クライアントがデッドロックを引き起こす可能性がある問題を修正[<a href="https://github.com/tikv/tikv/issues/13191">#13191</a>](https://github.com/tikv/tikv/issues/13191) @ [<a href="https://github.com/bufferflies">バッファフライ</a>](https://github.com/bufferflies) [<a href="https://github.com/tikv/tikv/issues/12933">#12933</a>](https://github.com/tikv/tikv/issues/12933) @ [<a href="https://github.com/BurtonQin">バートン秦</a>](https://github.com/BurtonQin)

-   PD

    -   クラスタノードのラベル設定が無効な場合、オンラインの進行状況が不正確になる問題を修正[<a href="https://github.com/tikv/pd/issues/5234">#5234</a>](https://github.com/tikv/pd/issues/5234) @ [<a href="https://github.com/rleungx">ルルンクス</a>](https://github.com/rleungx)
    -   `enable-forwarding`が有効になっている場合に gRPC がエラーを不適切に処理する問題によって引き起こされる PD パニックを修正[<a href="https://github.com/tikv/pd/issues/5373">#5373</a>](https://github.com/tikv/pd/issues/5373) @ [<a href="https://github.com/bufferflies">バッファフライ</a>](https://github.com/bufferflies)
    -   `/regions/replicated`間違ったステータス[<a href="https://github.com/tikv/pd/issues/5095">#5095</a>](https://github.com/tikv/pd/issues/5095) @ [<a href="https://github.com/rleungx">ルルンクス</a>](https://github.com/rleungx)を返す可能性がある問題を修正

-   TiFlash

    -   一部の状況でクラスター化インデックスを持つテーブルの列を削除した後にTiFlash がクラッシュする問題を修正[<a href="https://github.com/pingcap/tiflash/issues/5154">#5154</a>](https://github.com/pingcap/tiflash/issues/5154) @ [<a href="https://github.com/hongyunyan">ホンユニャン</a>](https://github.com/hongyunyan)
    -   `format`関数が`Data truncated`エラー[<a href="https://github.com/pingcap/tiflash/issues/4891">#4891</a>](https://github.com/pingcap/tiflash/issues/4891) @ [<a href="https://github.com/xzhangxian1008">xzhangxian1008</a>](https://github.com/xzhangxian1008)を返す可能性がある問題を修正します。
    -   一部の古いデータがstorageに残り、削除できない可能性がある問題を修正します[<a href="https://github.com/pingcap/tiflash/issues/5659">#5659</a>](https://github.com/pingcap/tiflash/issues/5659) @ [<a href="https://github.com/lidezhu">リデズ</a>](https://github.com/lidezhu)
    -   一部のエッジケースでの不必要な CPU 使用率を修正[<a href="https://github.com/pingcap/tiflash/issues/5409">#5409</a>](https://github.com/pingcap/tiflash/issues/5409) @ [<a href="https://github.com/breezewish">ブリーズウィッシュ</a>](https://github.com/breezewish)
    -   IPv6 [<a href="https://github.com/pingcap/tiflash/issues/5247">#5247</a>](https://github.com/pingcap/tiflash/issues/5247) @ [<a href="https://github.com/solotzg">ソロッツグ</a>](https://github.com/solotzg)を使用したクラスターでTiFlashが動作できないバグを修正
    -   並列集計[<a href="https://github.com/pingcap/tiflash/issues/5356">#5356</a>](https://github.com/pingcap/tiflash/issues/5356) @ [<a href="https://github.com/gengliqi">ゲンリチ</a>](https://github.com/gengliqi)のエラーによりTiFlash がクラッシュする可能性があるバグを修正
    -   `MinTSOScheduler`クエリエラー[<a href="https://github.com/pingcap/tiflash/issues/5556">#5556</a>](https://github.com/pingcap/tiflash/issues/5556) @ [<a href="https://github.com/windtalker">ウィンドトーカー</a>](https://github.com/windtalker)の場合にスレッドリソースがリークする可能性があるバグを修正

-   ツール

    -   TiDB Lightning

        -   TiDB が IPv6 ホスト[<a href="https://github.com/pingcap/tidb/issues/35880">#35880</a>](https://github.com/pingcap/tidb/issues/35880) @ [<a href="https://github.com/D3Hunter">D3ハンター</a>](https://github.com/D3Hunter)を使用している場合、 TiDB Lightningが TiDB に接続できない問題を修正
        -   再試行メカニズム[<a href="https://github.com/pingcap/tidb/issues/36566">#36566</a>](https://github.com/pingcap/tidb/issues/36566) @ [<a href="https://github.com/D3Hunter">D3ハンター</a>](https://github.com/D3Hunter)を追加して`read index not ready`エラーを修正
        -   ログ内の機密情報がサーバーモード[<a href="https://github.com/pingcap/tidb/issues/36374">#36374</a>](https://github.com/pingcap/tidb/issues/36374) @ [<a href="https://github.com/lichunzhu">リチュンジュ</a>](https://github.com/lichunzhu)で出力される問題を修正
        -   TiDB Lightning がParquet ファイル[<a href="https://github.com/pingcap/tidb/issues/36980">#36980</a>](https://github.com/pingcap/tidb/issues/36980) @ [<a href="https://github.com/D3Hunter">D3ハンター</a>](https://github.com/D3Hunter)でスラッシュ、数字、または非 ASCII 文字で始まる列をサポートしない問題を修正します。
        -   重複排除により、極端な場合にTiDB Lightning がpanicを引き起こす可能性がある問題を修正します[<a href="https://github.com/pingcap/tidb/issues/34163">#34163</a>](https://github.com/pingcap/tidb/issues/34163) @ [<a href="https://github.com/ForwardStar">フォワードスター</a>](https://github.com/ForwardStar)

    -   TiDB データ移行 (DM)

        -   DM [<a href="https://github.com/pingcap/tiflow/issues/6161">#6161</a>](https://github.com/pingcap/tiflow/issues/6161) @ [<a href="https://github.com/ForwardStar">フォワードスター</a>](https://github.com/ForwardStar)で`txn-entry-size-limit`設定項目が有効にならない問題を修正
        -   `check-task`コマンドが特殊文字[<a href="https://github.com/pingcap/tiflow/issues/5895">#5895</a>](https://github.com/pingcap/tiflow/issues/5895) @ [<a href="https://github.com/Ehco1996">Ehco1996</a>](https://github.com/Ehco1996)を処理できない問題を修正
        -   `query-status` [<a href="https://github.com/pingcap/tiflow/issues/4811">#4811</a>](https://github.com/pingcap/tiflow/issues/4811) @ [<a href="https://github.com/lyzx2001">lyzx2001</a>](https://github.com/lyzx2001)で発生する可能性のあるデータ競合の問題を修正
        -   `operate-schema`コマンド[<a href="https://github.com/pingcap/tiflow/issues/5688">#5688</a>](https://github.com/pingcap/tiflow/issues/5688) @ [<a href="https://github.com/ForwardStar">フォワードスター</a>](https://github.com/ForwardStar)の異なる出力形式を修正
        -   リレーがエラー[<a href="https://github.com/pingcap/tiflow/issues/6193">#6193</a>](https://github.com/pingcap/tiflow/issues/6193) @ [<a href="https://github.com/lance6716">ランス6716</a>](https://github.com/lance6716)に遭遇したときの goroutine リークを修正
        -   DB Conn [<a href="https://github.com/pingcap/tiflow/issues/3733">#3733</a>](https://github.com/pingcap/tiflow/issues/3733) @ [<a href="https://github.com/lance6716">ランス6716</a>](https://github.com/lance6716)を取得するときに DM Worker がスタックすることがある問題を修正
        -   TiDB が IPv6 ホスト[<a href="https://github.com/pingcap/tiflow/issues/6249">#6249</a>](https://github.com/pingcap/tiflow/issues/6249) @ [<a href="https://github.com/D3Hunter">D3ハンター</a>](https://github.com/D3Hunter)を使用する場合に DM が起動できない問題を修正

    -   TiCDC

        -   間違った最大互換バージョン番号[<a href="https://github.com/pingcap/tiflow/issues/6039">#6039</a>](https://github.com/pingcap/tiflow/issues/6039) @ [<a href="https://github.com/hi-rustin">こんにちはラスティン</a>](https://github.com/hi-rustin)を修正
        -   cdcサーバーが完全に起動する前に HTTP リクエストを受信するとpanicを引き起こす可能性があるバグを修正[<a href="https://github.com/pingcap/tiflow/issues/5639">#5639</a>](https://github.com/pingcap/tiflow/issues/5639) @ [<a href="https://github.com/asddongmen">東門</a>](https://github.com/asddongmen)
        -   チェンジフィード同期ポイントが有効になっている場合の ddl シンクpanicの問題を修正[<a href="https://github.com/pingcap/tiflow/issues/4934">#4934</a>](https://github.com/pingcap/tiflow/issues/4934) @ [<a href="https://github.com/asddongmen">東門</a>](https://github.com/asddongmen)
        -   同期ポイントが有効になっている場合、一部のシナリオで変更フィードがスタックする問題を修正[<a href="https://github.com/pingcap/tiflow/issues/6827">#6827</a>](https://github.com/pingcap/tiflow/issues/6827) @ [<a href="https://github.com/hicqu">ひっくり返る</a>](https://github.com/hicqu)
        -   CDCサーバーの再起動後にchangefeed APIが正常に動作しないバグを修正[<a href="https://github.com/pingcap/tiflow/issues/5837">#5837</a>](https://github.com/pingcap/tiflow/issues/5837) @ [<a href="https://github.com/asddongmen">東門</a>](https://github.com/asddongmen)
        -   ブラック ホール シンク[<a href="https://github.com/pingcap/tiflow/issues/6206">#6206</a>](https://github.com/pingcap/tiflow/issues/6206) @ [<a href="https://github.com/asddongmen">東門</a>](https://github.com/asddongmen)のデータ競合問題を修正
        -   `enable-old-value = false` [<a href="https://github.com/pingcap/tiflow/issues/6198">#6198</a>](https://github.com/pingcap/tiflow/issues/6198) @ [<a href="https://github.com/hi-rustin">こんにちはラスティン</a>](https://github.com/hi-rustin)を設定した場合の TiCDCpanicの問題を修正
        -   REDO ログ機能が有効になっている場合のデータ整合性の問題を修正[<a href="https://github.com/pingcap/tiflow/issues/6189">#6189</a>](https://github.com/pingcap/tiflow/issues/6189) [<a href="https://github.com/pingcap/tiflow/issues/6368">#6368</a>](https://github.com/pingcap/tiflow/issues/6368) [<a href="https://github.com/pingcap/tiflow/issues/6277">#6277</a>](https://github.com/pingcap/tiflow/issues/6277) [<a href="https://github.com/pingcap/tiflow/issues/6456">#6456</a>](https://github.com/pingcap/tiflow/issues/6456) [<a href="https://github.com/pingcap/tiflow/issues/6695">#6695</a>](https://github.com/pingcap/tiflow/issues/6695) [<a href="https://github.com/pingcap/tiflow/issues/6764">#6764</a>](https://github.com/pingcap/tiflow/issues/6764) [<a href="https://github.com/pingcap/tiflow/issues/6859">#6859</a>](https://github.com/pingcap/tiflow/issues/6859) @ [<a href="https://github.com/asddongmen">東門</a>](https://github.com/asddongmen)
        -   REDO イベントを非同期に書き込むことで、REDO ログのパフォーマンスの低下を修正[<a href="https://github.com/pingcap/tiflow/issues/6011">#6011</a>](https://github.com/pingcap/tiflow/issues/6011) @ [<a href="https://github.com/CharlesCheung96">CharlesCheung96</a>](https://github.com/CharlesCheung96)
        -   MySQL シンクが IPv6 アドレス[<a href="https://github.com/pingcap/tiflow/issues/6135">#6135</a>](https://github.com/pingcap/tiflow/issues/6135) @ [<a href="https://github.com/hi-rustin">こんにちはラスティン</a>](https://github.com/hi-rustin)に接続できない問題を修正

    -   バックアップと復元 (BR)

        -   RawKV モード[<a href="https://github.com/pingcap/tidb/issues/35279">#35279</a>](https://github.com/pingcap/tidb/issues/35279) @ [<a href="https://github.com/3pointer">3ポインター</a>](https://github.com/3pointer)でBR が`ErrRestoreTableIDMismatch`を報告するバグを修正
        -   バックアップ データ ディレクトリ構造を調整して、大規模クラスタ バックアップ[<a href="https://github.com/pingcap/tidb/issues/30087">#30087</a>](https://github.com/pingcap/tidb/issues/30087) @ [<a href="https://github.com/MoCuishle28">モクイシュル28</a>](https://github.com/MoCuishle28)での S3 レート制限によって引き起こされるバックアップの失敗を修正します。
        -   概要ログ[<a href="https://github.com/pingcap/tidb/issues/35553">#35553</a>](https://github.com/pingcap/tidb/issues/35553) @ [<a href="https://github.com/ixuh12">ixuh12</a>](https://github.com/ixuh12)の誤ったバックアップ時間を修正しました。

    -   Dumpling

        -   GetDSN が IPv6 [<a href="https://github.com/pingcap/tidb/issues/36112">#36112</a>](https://github.com/pingcap/tidb/issues/36112) @ [<a href="https://github.com/D3Hunter">D3ハンター</a>](https://github.com/D3Hunter)をサポートしていない問題を修正

    -   TiDBBinlog

        -   `compressor`を`gzip` [<a href="https://github.com/pingcap/tidb-binlog/issues/1152">#1152</a>](https://github.com/pingcap/tidb-binlog/issues/1152) @ [<a href="https://github.com/lichunzhu">リチュンジュ</a>](https://github.com/lichunzhu)に設定すると、 DrainerがPumpにリクエストを正しく送信できないバグを修正
