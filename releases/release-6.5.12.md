---
title: TiDB 6.5.12 Release Notes
summary: TiDB 6.5.12 の改善点とバグ修正について説明します。
---

# TiDB 6.5.12 リリースノート {#tidb-6-5-12-release-notes}

発売日: 2025年2月27日

TiDB バージョン: 6.5.12

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [実稼働環境への導入](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   openEuler 22.03 LTS SP3/SP4 オペレーティング システムをサポートします。詳細については、 [OSおよびプラットフォームの要件](https://docs.pingcap.com/tidb/v6.5/hardware-and-software-requirements#os-and-platform-requirements)参照してください。
-   [TiDB HTTP API](https://github.com/pingcap/tidb/blob/release-6.5/docs/tidb_http_api.md)から取得される DDL 履歴タスクのデフォルトの制限を 2048 に設定して、履歴タスク[＃55711](https://github.com/pingcap/tidb/issues/55711) @ [ジョッカウ](https://github.com/joccau)の過剰による OOM の問題を防止します。
-   インデックス[＃57156](https://github.com/pingcap/tidb/issues/57156) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)を追加する際の取り込みフェーズの最大速度を制限する新しいシステム変数[`tidb_ddl_reorg_max_write_speed`](https://docs.pingcap.com/tidb/v6.5/system-variables#tidb_ddl_reorg_max_write_speed-new-in-v6512)を追加します。

## 改善点 {#improvements}

-   ティビ

    -   読み取りタイムスタンプ[＃57786](https://github.com/pingcap/tidb/issues/57786) @ [ミョンケミンタ](https://github.com/MyonKeminta)の有効性チェックを強化する

-   ティクヴ

    -   無効な`max_ts`更新[＃17916](https://github.com/tikv/tikv/issues/17916) @ [エキシウム](https://github.com/ekexium)の検出メカニズムを追加します

-   TiFlash

    -   クラスター化インデックス[＃9529](https://github.com/pingcap/tiflash/issues/9529) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)を持つテーブルで、バックグラウンドでの古いデータのガベージコレクションの速度が向上します。

-   ツール

    -   バックアップと復元 (BR)

        -   完全復元のためにターゲット クラスターが空のクラスターであるかどうかを確認するチェックを追加します[＃35744](https://github.com/pingcap/tidb/issues/35744) @ [3ポインター](https://github.com/3pointer)
        -   非完全復元の場合、ターゲット クラスターに同じ名前のテーブルが含まれているかどうかを確認するチェックを追加します[＃55087](https://github.com/pingcap/tidb/issues/55087) @ [リドリス](https://github.com/RidRisR)
        -   `br log restore`サブコマンドを除き、他の`br log`サブコマンドはすべて、メモリ消費量を削減するために TiDB `domain`データ構造のロードをスキップすることをサポートしています[＃52088](https://github.com/pingcap/tidb/issues/52088) @ [リーヴルス](https://github.com/Leavrth)
        -   バックアップパフォーマンスを向上させるために、フルバックアップ中のテーブルレベルのチェックサム計算をデフォルトで無効にする（ `--checksum=false` ） [＃56373](https://github.com/pingcap/tidb/issues/56373) @ [トリスタン1900](https://github.com/Tristan1900)

    -   TiDB Lightning

        -   OOM の問題を防ぐために、CSV ファイルを解析するときに行幅チェックを追加します[＃58590](https://github.com/pingcap/tidb/issues/58590) @ [D3ハンター](https://github.com/D3Hunter)

## バグ修正 {#bug-fixes}

-   ティビ

    -   `NATURAL JOIN`または`USING`節の後にサブクエリを使用するとエラー[＃53766](https://github.com/pingcap/tidb/issues/53766) @ [ダッシュ12653](https://github.com/dash12653)が発生する可能性がある問題を修正しました
    -   `CAST`関数が文字セット[＃55677](https://github.com/pingcap/tidb/issues/55677) @ [定義2014](https://github.com/Defined2014)の明示的な設定をサポートしていない問題を修正
    -   `LOAD DATA ... REPLACE INTO`操作でデータの不整合が発生する問題を修正[＃56408](https://github.com/pingcap/tidb/issues/56408) @ [ふーふー](https://github.com/fzzf678)
    -   `ADD INDEX` [＃56930](https://github.com/pingcap/tidb/issues/56930) @ [ふーふー](https://github.com/fzzf678)を実行するときに TiDB がインデックスの長さ制限をチェックしない問題を修正しました
    -   共通テーブル式 (CTE) に複数のデータ コンシューマーがあり、1 つのコンシューマーがデータを読み取らずに終了した場合に発生する可能性のある不正なメモリアクセスの問題を修正しました[＃55881](https://github.com/pingcap/tidb/issues/55881) @ [風の話し手](https://github.com/windtalker)
    -   `IndexMerge` [＃58476](https://github.com/pingcap/tidb/issues/58476) @ [ホーキングレイ](https://github.com/hawkingrei)を構築するときに一部の述語が失われる可能性がある問題を修正しました
    -   `BIT`型から`CHAR`型にデータを変換すると TiKV パニック[＃56494](https://github.com/pingcap/tidb/issues/56494) @ [lcwangchao](https://github.com/lcwangchao)が発生する可能性がある問題を修正しました
    -   `CREATE VIEW`ステートメントで変数またはパラメータを使用してもエラーが報告されない問題を修正[＃53176](https://github.com/pingcap/tidb/issues/53176) @ [ミョンス](https://github.com/mjonss)
    -   解放されていないセッションリソースがメモリリークを引き起こす可能性がある問題を修正[＃56271](https://github.com/pingcap/tidb/issues/56271) @ [ランス6716](https://github.com/lance6716)
    -   分散実行フレームワーク[＃48680](https://github.com/pingcap/tidb/issues/48680) @ [ランス6716](https://github.com/lance6716)で PD メンバーを変更した後に`ADD INDEX`実行が失敗する可能性がある問題を修正
    -   `cluster_slow_query table`クエリするときに`ORDER BY`使用すると、順序付けられていない結果[＃51723](https://github.com/pingcap/tidb/issues/51723) @ [定義2014](https://github.com/Defined2014)が生成される可能性がある問題を修正しました。
    -   古い読み取りが読み取り操作のタイムスタンプを厳密に検証しない問題を修正しました。その結果、TSO と実際の物理時間[＃56809](https://github.com/pingcap/tidb/issues/56809) @ [ミョンケミンタ](https://github.com/MyonKeminta)の間にオフセットが存在する場合に、トランザクションの一貫性にわずかながら影響が出る可能性があります。
    -   クエリ`INFORMATION_SCHEMA.columns`のパフォーマンスが[＃58184](https://github.com/pingcap/tidb/issues/58184) @ [ランス6716](https://github.com/lance6716)で低下する問題を修正
    -   `INSERT ... ON DUPLICATE KEY`ステートメントが`mysql_insert_id` [＃55965](https://github.com/pingcap/tidb/issues/55965) @ [天菜まお](https://github.com/tiancaiamao)と互換性がない問題を修正
    -   クエリ条件`column IS NULL` [＃56116](https://github.com/pingcap/tidb/issues/56116) @ [ホーキングレイ](https://github.com/hawkingrei)で一意のインデックスにアクセスするときに、オプティマイザが行数を誤って 1 と見積もる問題を修正しました。
    -   `IndexLookUp`演算子のメモリの一部が[＃56440](https://github.com/pingcap/tidb/issues/56440) @ [うわー](https://github.com/wshwsh12)で追跡されない問題を修正
    -   TiDBの内部コルーチンで発生する可能性のあるデータ競合の問題を修正[＃57798](https://github.com/pingcap/tidb/issues/57798) [＃56053](https://github.com/pingcap/tidb/issues/56053) @ [フィシュウ](https://github.com/fishiu) @ [天菜まお](https://github.com/tiancaiamao)
    -   クエリに利用可能なインデックスマージ実行プラン[＃56217](https://github.com/pingcap/tidb/issues/56217) @ [アイリンキッド](https://github.com/AilinKid)がある場合に`read_from_storage`ヒントが有効にならない可能性がある問題を修正しました。
    -   エイリアス[＃56726](https://github.com/pingcap/tidb/issues/56726) @ [ホーキングレイ](https://github.com/hawkingrei)を持つマルチテーブル`DELETE`ステートメントに対して実行プラン バインディングを作成できない問題を修正しました。
    -   異常終了時に`INDEX_HASH_JOIN`アップする可能性がある問題を修正[＃54055](https://github.com/pingcap/tidb/issues/54055) @ [うわー](https://github.com/wshwsh12)
    -   2 人の DDL 所有者が同時に存在する可能性がある問題を修正[＃54689](https://github.com/pingcap/tidb/issues/54689) @ [ジョッカウ](https://github.com/joccau)
    -   `information_schema.cluster_slow_query`テーブルをクエリするときに、時間フィルターが追加されていない場合、最新のスロー ログ ファイルのみがクエリされる問題を修正しました[＃56100](https://github.com/pingcap/tidb/issues/56100) @ [クレイジーcs520](https://github.com/crazycs520)
    -   ユニークインデックス[＃56161](https://github.com/pingcap/tidb/issues/56161) @ [タンジェンタ](https://github.com/tangenta)を追加するときに`duplicate entry`発生する可能性がある問題を修正
    -   特定の型変換エラーでエラーメッセージが正しく表示されない問題を修正[＃41730](https://github.com/pingcap/tidb/issues/41730) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   `VIEW`で定義されたCTEが誤ってインライン化される問題を修正[＃56582](https://github.com/pingcap/tidb/issues/56582) @ [エルサ0520](https://github.com/elsa0520)
    -   `UPDATE`文が`ENUM`型[＃56832](https://github.com/pingcap/tidb/issues/56832) @ [xhebox](https://github.com/xhebox)の値を誤って更新する問題を修正しました。
    -   `DATE`列を追加した後に`UPDATE`ステートメントを実行すると、場合によっては[＃59047](https://github.com/pingcap/tidb/issues/59047) @ [ミョンス](https://github.com/mjonss)エラー`Incorrect date value: '0000-00-00'`発生する問題を修正しました。
    -   Prepareプロトコルで、クライアントがUTF8以外の文字セット[＃58870](https://github.com/pingcap/tidb/issues/58870) @ [xhebox](https://github.com/xhebox)を使用するとエラーが発生する問題を修正
    -   一時テーブルをクエリすると、場合によっては予期しない TiKV 要求がトリガーされる可能性がある問題を修正[＃58875](https://github.com/pingcap/tidb/issues/58875) @ [天菜まお](https://github.com/tiancaiamao)
    -   ビュー[＃53175](https://github.com/pingcap/tidb/issues/53175) @ [ミョンス](https://github.com/mjonss)のステートメントに`ONLY_FULL_GROUP_BY`設定が適用されない問題を修正しました
    -   不一致な値タイプとタイプ変換エラーを含む`IN`条件を使用してパーティション テーブルをクエリすると、誤ったクエリ結果[＃54746](https://github.com/pingcap/tidb/issues/54746) @ [ミョンス](https://github.com/mjonss)が発生する問題を修正しました。
    -   特定のフィールドに空の値が含まれている場合にスローログのクエリが失敗する可能性がある問題を修正[＃58147](https://github.com/pingcap/tidb/issues/58147) @ [いいえ](https://github.com/yibin87)
    -   `RADIANS()`関数が誤った順序で値を計算する問題を修正[＃57671](https://github.com/pingcap/tidb/issues/57671) @ [ゲンリキ](https://github.com/gengliqi)
    -   `BIT`列目のデフォルト値が正しくない問題を修正[＃57301](https://github.com/pingcap/tidb/issues/57301) @ [ヤンケオ](https://github.com/YangKeao)
    -   CTE に`ORDER BY` 、 `LIMIT` 、または`SELECT DISTINCT`個の節が含まれ、別の CTE [＃56603](https://github.com/pingcap/tidb/issues/56603) @ [エルサ0520](https://github.com/elsa0520)の再帰部分によって参照されている場合にインライン エラーが発生する可能性がある問題を修正しました。
    -   統計情報を同期的にロードする際に発生するタイムアウトが正しく処理されない可能性がある問題を修正[＃57710](https://github.com/pingcap/tidb/issues/57710) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   CTE [＃54582](https://github.com/pingcap/tidb/issues/54582) @ [ホーキングレイ](https://github.com/hawkingrei)でデータベース名を解析するときに誤ったデータベース名が返される可能性がある問題を修正しました。
    -   無効なデータバインディング[＃58016](https://github.com/pingcap/tidb/issues/58016) @ [qw4990](https://github.com/qw4990)が原因で起動時に TiDB がpanicになる可能性がある問題を修正しました
    -   特定の極端なケースでコスト見積もりによって無効な INF/NaN 値が生成される可能性があり、その結果、結合したテーブルの再配置の結果が不正確になる可能性がある問題を修正しました[＃56704](https://github.com/pingcap/tidb/issues/56704) @ [ウィノロス](https://github.com/winoros)
    -   統計ファイルに null 値[＃53966](https://github.com/pingcap/tidb/issues/53966) @ [キング・ディラン](https://github.com/King-Dylan)が含まれている場合に統計を手動でロードすると失敗する可能性がある問題を修正しました。
    -   同じ名前のビューを 2 つ作成してもエラーが報告されない問題を修正[＃58769](https://github.com/pingcap/tidb/issues/58769) @ [天菜まお](https://github.com/tiancaiamao)
    -   仮想生成列の依存関係に`ON UPDATE`属性の列が含まれている場合、更新された行のデータとそのインデックス データが不整合になる可能性がある問題を修正しました[＃56829](https://github.com/pingcap/tidb/issues/56829) @ [ジョーチェン](https://github.com/joechenrh)
    -   `INFORMATION_SCHEMA.TABLES`システム テーブルが誤った結果を返す問題を修正[＃57345](https://github.com/pingcap/tidb/issues/57345) @ [タンジェンタ](https://github.com/tangenta)

-   ティクヴ

    -   Follower Readが古いデータ[＃17018](https://github.com/tikv/tikv/issues/17018) @ [栄光](https://github.com/glorv)を読み取る可能性がある問題を修正
    -   ピア[＃18005](https://github.com/tikv/tikv/issues/18005) @ [栄光](https://github.com/glorv)を破棄するときに TiKV がpanic可能性がある問題を修正しました
    -   タイムロールバックにより異常な RocksDB フロー制御が発生し、パフォーマンスジッター[＃17995](https://github.com/tikv/tikv/issues/17995) @ [リクササシネーター](https://github.com/LykxSassinator)が発生する可能性がある問題を修正しました
    -   ディスクの停止によりリーダーの移行が妨げられ、パフォーマンスのジッターが発生する可能性がある問題を修正[＃17363](https://github.com/tikv/tikv/issues/17363) @ [いいえ](https://github.com/hhwyt)
    -   1 フェーズ コミット (1PC) のみが有効で、非同期コミットが有効になっていない場合に、最新の書き込みデータが読み取れない可能性がある問題を修正[＃18117](https://github.com/tikv/tikv/issues/18117) @ [ジグアン](https://github.com/zyguan)
    -   GCワーカーに高負荷がかかったときにデッドロックが発生する可能性がある問題を修正[＃18214](https://github.com/tikv/tikv/issues/18214) @ [ジグアン](https://github.com/zyguan)
    -   Grafana の TiKV パネルの**ストレージ非同期書き込み期間**監視メトリックが不正確であるという問題を修正[＃17579](https://github.com/tikv/tikv/issues/17579) @ [金星の上](https://github.com/overvenus)
    -   `RADIANS()`または`DEGREES()`関数を含むクエリを実行するときに TiKV がpanicになる可能性がある問題を修正[＃17852](https://github.com/tikv/tikv/issues/17852) @ [ゲンリキ](https://github.com/gengliqi)
    -   リージョンをマージすると稀に TiKV がpanic可能性がある問題を修正[＃17840](https://github.com/tikv/tikv/issues/17840) @ [栄光](https://github.com/glorv)
    -   リージョンを[＃17602](https://github.com/tikv/tikv/issues/17602)対[リクササシネーター](https://github.com/LykxSassinator)に分割した後、リーダーをすぐに選出できない問題を修正しました。
    -   GBK/GB18030 エンコードされたデータ[＃17618](https://github.com/tikv/tikv/issues/17618) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)を処理するときにエンコードが失敗する可能性がある問題を修正しました。

-   PD

    -   TSO [＃9004](https://github.com/tikv/pd/issues/9004) @ [rleungx](https://github.com/rleungx)を割り当てるときにメモリリークが発生する可能性がある問題を修正しました
    -   `tidb_enable_tso_follower_proxy`システム変数が[＃8947](https://github.com/tikv/pd/issues/8947) @ [じゃがいも](https://github.com/JmPotato)で有効にならない可能性がある問題を修正
    -   PD がpanicを起こす可能性のある潜在的な問題を修正[＃8915](https://github.com/tikv/pd/issues/8915) @ [バッファフライ](https://github.com/bufferflies)
    -   長時間実行クラスタでメモリリークが発生する可能性がある問題を修正[＃9047](https://github.com/tikv/pd/issues/9047) @ [バッファフライ](https://github.com/bufferflies)
    -   PDノードがLeader[＃9051](https://github.com/tikv/pd/issues/9051) @ [rleungx](https://github.com/rleungx)でない場合でもTSOを生成する可能性がある問題を修正しました。
    -   PDLeader[＃9017](https://github.com/tikv/pd/issues/9017)対[rleungx](https://github.com/rleungx)切り替え時にリージョンシンカーが時間内に終了しない可能性がある問題を修正しました
    -   `evict-leader-scheduler`または`grant-leader-scheduler`作成時にエラーが発生しても、エラーメッセージが pd-ctl [＃8759](https://github.com/tikv/pd/issues/8759) @ [ok江](https://github.com/okJiang)に返されない問題を修正しました。
    -   ホットスポット キャッシュ[＃8698](https://github.com/tikv/pd/issues/8698) @ [翻訳者](https://github.com/lhy1024)のメモリリーク問題を修正
    -   多数のリージョンが存在する場合にPDのリージョンAPIをリクエストできない問題を修正[＃55872](https://github.com/pingcap/tidb/issues/55872) @ [rleungx](https://github.com/rleungx)
    -   同じストアID [＃8756](https://github.com/tikv/pd/issues/8756) @ [ok江](https://github.com/okJiang)で繰り返し作成された場合に`evict-leader-scheduler`正常に動作しない問題を修正
    -   潜在的なセキュリティ脆弱性を修正するため、Gin Web Framework のバージョンを v1.9.1 から v1.10.0 にアップグレードします[＃8643](https://github.com/tikv/pd/issues/8643) @ [じゃがいも](https://github.com/JmPotato)
    -   `evict-leader-scheduler`で間違ったパラメータを使用すると、PD がエラーを正しく報告せず、一部のスケジューラが使用できなくなる問題を修正しました[＃8619](https://github.com/tikv/pd/issues/8619) @ [rleungx](https://github.com/rleungx)
    -   ラベル統計[＃8700](https://github.com/tikv/pd/issues/8700) @ [翻訳者](https://github.com/lhy1024)のメモリリーク問題を修正
    -   TiDBダッシュボードがPD `trace`データを正しく読み取れない問題を修正[＃7253](https://github.com/tikv/pd/issues/7253) @ [ノルーシュ](https://github.com/nolouch)
    -   リージョン統計[＃8710](https://github.com/tikv/pd/issues/8710) @ [rleungx](https://github.com/rleungx)のメモリリーク問題を修正
    -   etcd リーダー遷移[＃8823](https://github.com/tikv/pd/issues/8823) @ [rleungx](https://github.com/rleungx)中に PD がリーダーを迅速に再選出できない問題を修正

-   TiFlash

    -   `SUBSTRING()`関数が特定の整数型の`pos`と`len`引数をサポートせず、クエリ エラー[＃9473](https://github.com/pingcap/tiflash/issues/9473) @ [ゲンリキ](https://github.com/gengliqi)が発生する問題を修正しました。
    -   TiFlashでサポートされていない一部の JSON関数がTiFlash [＃9444](https://github.com/pingcap/tiflash/issues/9444) @ [風の話し手](https://github.com/windtalker)にプッシュダウンされる問題を修正しました
    -   2 番目のパラメータが負の[＃9604](https://github.com/pingcap/tiflash/issues/9604) @ [グオシャオゲ](https://github.com/guo-shaoge)場合に`SUBSTRING()`関数が誤った結果を返す問題を修正しました
    -   `LPAD()`と`RPAD()`関数が場合によっては誤った結果を返す問題を修正[＃9465](https://github.com/pingcap/tiflash/issues/9465) @ [グオシャオゲ](https://github.com/guo-shaoge)
    -   大きなテーブルで`DROP TABLE`実行するとTiFlash OOM [＃9437](https://github.com/pingcap/tiflash/issues/9437) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)が発生する可能性がある問題を修正
    -   CPU コア数[＃9212](https://github.com/pingcap/tiflash/issues/9212) @ [翻訳者](https://github.com/xzhangxian1008)を取得するときにゼロ除算エラーが発生し、 TiFlash が起動に失敗する問題を修正しました。
    -   大量のデータをインポートした後にTiFlash のメモリ使用量が高くなる可能性がある問題を修正[＃9812](https://github.com/pingcap/tiflash/issues/9812) @ [カルビンネオ](https://github.com/CalvinNeo)

-   ツール

    -   バックアップと復元 (BR)

        -   TiKV [＃58845](https://github.com/pingcap/tidb/issues/58845) @ [トリスタン1900](https://github.com/Tristan1900)にリクエストを送信するときに`rpcClient is idle`エラーが発生し、 BRが復元に失敗する問題を修正しました。
        -   `br log status --json` [＃57959](https://github.com/pingcap/tidb/issues/57959) @ [リーヴルス](https://github.com/Leavrth)を使用してログ バックアップ タスクをクエリすると、結果に`status`フィールドが表示されない問題を修正しました。
        -   ログバックアップ中のPDLeaderI/Oレイテンシーによりチェックポイントレイテンシー[＃58574](https://github.com/pingcap/tidb/issues/58574) @ [ユジュンセン](https://github.com/YuJuncen)が増加する可能性がある問題を修正しました。
        -   `tiup br restore`コマンドがデータベースまたはテーブルの復元中にターゲット クラスター テーブルが既に存在するかどうかのチェックを省略し、既存のテーブル[＃58168](https://github.com/pingcap/tidb/issues/58168) @ [リドリス](https://github.com/RidRisR)を上書きする可能性がある問題を修正しました。
        -   アドバンサー所有者が[＃58031](https://github.com/pingcap/tidb/issues/58031) @ [3ポインター](https://github.com/3pointer)に切り替わったときに、ログ バックアップが予期せず一時停止状態になる可能性がある問題を修正しました。
        -   ログバックアップが残留ロックをすぐに解決できず、チェックポイントが[＃57134](https://github.com/pingcap/tidb/issues/57134) @ [3ポインター](https://github.com/3pointer)に進まない問題を修正しました。
        -   BR統合テスト ケースが不安定になる問題を修正し、スナップショットまたはログ バックアップ ファイルの破損をシミュレートする新しいテスト ケースを追加します[＃53835](https://github.com/pingcap/tidb/issues/53835) @ [リーヴルス](https://github.com/Leavrth)
        -   ログに暗号化された情報が出力される問題を修正[＃57585](https://github.com/pingcap/tidb/issues/57585) @ [ケニー](https://github.com/kennytm)
        -   クラスター内に多数のテーブルがあるが、実際のデータ サイズが小さい場合に PITR タスクが`Information schema is out of date`エラーを返す可能性がある問題を修正しました[＃57743](https://github.com/pingcap/tidb/issues/57743) @ [トリスタン1900](https://github.com/Tristan1900)

    -   ティCDC

        -   TiCDC が`RENAME TABLE`操作[＃11946](https://github.com/pingcap/tiflow/issues/11946) @ [989898 円](https://github.com/wk989898)中にフィルタリングに誤ったテーブル名を使用する問題を修正
        -   Avroプロトコル[＃11994](https://github.com/pingcap/tiflow/issues/11994) @ [989898 円](https://github.com/wk989898)経由で`default NULL`文を複製するときにTiCDCがエラーを報告する問題を修正
        -   PDスケールイン[＃12004](https://github.com/pingcap/tiflow/issues/12004) @ [リデズ](https://github.com/lidezhu)後にTiCDCがPDに正しく接続できない問題を修正
        -   変更フィードが停止または削除された後に初期スキャンがキャンセルされない問題を修正[＃11638](https://github.com/pingcap/tiflow/issues/11638) @ [3エースショーハンド](https://github.com/3AceShowHand)
        -   アップストリームで新しく追加された列のデフォルト値を`NOT NULL`から`NULL`に変更すると、ダウンストリームのその列のデフォルト値が正しくなくなる問題を修正しました[＃12037](https://github.com/pingcap/tiflow/issues/12037) @ [989898 円](https://github.com/wk989898)
        -   `changefeed pause`コマンドで`--overwrite-checkpoint-ts`パラメータを使用すると、changefeed が[＃12055](https://github.com/pingcap/tiflow/issues/12055) @ [ホンユンヤン](https://github.com/hongyunyan)で停止する可能性がある問題を修正しました。
        -   `CREATE TABLE IF NOT EXISTS`または`CREATE DATABASE IF NOT EXISTS`ステートメント[＃11839](https://github.com/pingcap/tiflow/issues/11839) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)を複製するときに TiCDC がpanicになる可能性がある問題を修正しました。
        -   有効なインデックス[＃11765](https://github.com/pingcap/tiflow/issues/11765) @ [アズドンメン](https://github.com/asddongmen)のないテーブルで`TRUNCATE TABLE` DDL を複製するときに TiCDC がエラーを報告する可能性がある問題を修正しました。
        -   TiDB DDL 所有者の変更中に DDL タスクのスキーマ バージョンが非増分になったときに、TiCDC が誤って DDL タスクを破棄する問題を修正[＃11714](https://github.com/pingcap/tiflow/issues/11714) @ [ウィリアム](https://github.com/wlwilliamx)
        -   新しい TiKV ノードがクラスター[＃11766](https://github.com/pingcap/tiflow/issues/11766) @ [リデズ](https://github.com/lidezhu)に追加された後に、変更フィードが停止する可能性がある問題を修正しました。
        -   Sarama クライアントによって順序が乱れたメッセージが再送信されると Kafka メッセージの順序が不正確になる問題を修正[＃11935](https://github.com/pingcap/tiflow/issues/11935) @ [3エースショーハンド](https://github.com/3AceShowHand)
        -   Puller モジュールの解決済み TSレイテンシーモニタリングで誤った値[＃11561](https://github.com/pingcap/tiflow/issues/11561) @ [ウィリアム](https://github.com/wlwilliamx)が表示される問題を修正しました。
        -   やり直しモジュールがエラー[＃11744](https://github.com/pingcap/tiflow/issues/11744) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)を適切に報告できない問題を修正

    -   TiDB データ移行 (DM)

        -   複数の DM マスター ノードが同時にリーダーになり、データの不整合が発生する可能性がある問題を修正しました[＃11602](https://github.com/pingcap/tiflow/issues/11602) @ [GMHDBJD](https://github.com/GMHDBJD)
        -   パスワードの長さが19文字を超えるとMySQL 8.0への接続に失敗する問題を修正[＃11603](https://github.com/pingcap/tiflow/issues/11603) @ [フィシュウ](https://github.com/fishiu)
        -   TLSと`shard-mode`両方が構成されている場合に`start-task`の事前チェックが失敗する問題を修正[＃11842](https://github.com/pingcap/tiflow/issues/11842) @ [孫暁光](https://github.com/sunxiaoguang)

    -   TiDB Lightning

        -   ログが適切に感度低下されない問題を修正[＃59086](https://github.com/pingcap/tidb/issues/59086) @ [GMHDBJD](https://github.com/GMHDBJD)
        -   エンコード段階でのキャッシュ不足によりパフォーマンスが低下する問題を修正[＃56705](https://github.com/pingcap/tidb/issues/56705) @ [オリバーS929](https://github.com/OliverS929)
        -   高同時実行シナリオでクラウドstorageからデータをインポートするときにパフォーマンスが低下する問題を修正[＃57413](https://github.com/pingcap/tidb/issues/57413) @ [翻訳者](https://github.com/xuanyu66)
        -   メタデータ更新中に`Lock wait timeout`エラーが発生した場合にTiDB Lightning が自動的に再試行しない問題を修正[＃53042](https://github.com/pingcap/tidb/issues/53042) @ [グオショウヤン](https://github.com/guoshouyan)
        -   TiDB Lightning がTiKV [＃56114](https://github.com/pingcap/tidb/issues/56114) @ [フィシュウ](https://github.com/fishiu)から送信されたサイズ超過のメッセージを受信できない問題を修正しました
        -   TiDB Lightning [＃58085](https://github.com/pingcap/tidb/issues/58085) @ [ランス6716](https://github.com/lance6716)を使用してデータをインポートするときにエラー レポート出力が切り捨てられる問題を修正しました

    -   Dumpling

        -   Google Cloud Storage (GCS) [＃56127](https://github.com/pingcap/tidb/issues/56127) @ [オリバーS929](https://github.com/OliverS929)から 503 エラーを受信したときにDumpling が適切に再試行できない問題を修正しました
