---
title: TiDB 4.0.9 Release Notes
---

# TiDB4.0.9リリースノート {#tidb-4-0-9-release-notes}

発売日：2020年12月21日

TiDBバージョン：4.0.9

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   `enable-streaming`構成アイテム[＃21055](https://github.com/pingcap/tidb/pull/21055)を廃止します

-   TiKV

    -   静止時の暗号化が有効になっている場合のI/Oとミューテックスの競合を減らします。変更は後方互換性がありません。ユーザーがクラスタをv4.0.9より前のバージョンにダウングレードする必要がある場合は、ダウングレードの前に`security.encryption.enable-file-dictionary-log`を無効にし、TiKVを再起動する必要があります。 [＃9195](https://github.com/tikv/tikv/pull/9195)

## 新機能 {#new-features}

-   TiFlash

    -   ストレージエンジンの最新データを複数のディスクに保存することをサポートします（実験的）

-   TiDBダッシュボード

    -   **SQLステートメント**ページ[＃749](https://github.com/pingcap/tidb-dashboard/pull/749)のすべてのフィールドによる表示と並べ替えをサポート
    -   トポロジグラフのズームとパンのサポート[＃772](https://github.com/pingcap/tidb-dashboard/pull/772)
    -   **SQLステートメント**および<strong>低速クエリ</strong>ページ[＃777](https://github.com/pingcap/tidb-dashboard/pull/777)でのディスク使用量情報の表示のサポート
    -   **SQLステートメント**および<strong>低速クエリ</strong>ページ[＃778](https://github.com/pingcap/tidb-dashboard/pull/778)でのリストデータのエクスポートのサポート
    -   Prometheusアドレスのカスタマイズのサポート[＃808](https://github.com/pingcap/tidb-dashboard/pull/808)
    -   クラスタ統計のページを追加する[＃815](https://github.com/pingcap/tidb-dashboard/pull/815)
    -   **低速クエリ**の詳細に時間関連のフィールドを追加する[＃810](https://github.com/pingcap/tidb-dashboard/pull/810)

## 改善 {#improvements}

-   TiDB

    -   等しい条件を他の条件に変換するときに、ヒューリスティックな方法で（インデックス）マージ結合を回避します[＃21146](https://github.com/pingcap/tidb/pull/21146)
    -   ユーザー変数のタイプを区別する[＃21107](https://github.com/pingcap/tidb/pull/21107)
    -   構成ファイル[＃20922](https://github.com/pingcap/tidb/pull/20922)での`GOGC`変数の設定のサポート
    -   ダンプされたバイナリ時間（ `Timestamp`および`Datetime` ）を[＃21135](https://github.com/pingcap/tidb/pull/21135)との互換性を高めます
    -   `LOCK IN SHARE MODE`構文[＃21005](https://github.com/pingcap/tidb/pull/21005)を使用するステートメントにエラーメッセージを提供します
    -   ショートカット可能な式で定数を折りたたむときに、不要な警告やエラーを出力しないようにする[＃21040](https://github.com/pingcap/tidb/pull/21040)
    -   `LOAD DATA`ステートメント[＃21199](https://github.com/pingcap/tidb/pull/21199)を準備するときにエラーを発生させます
    -   整数列タイプを変更するときは、整数のゼロフィルサイズの属性を無視します[＃20986](https://github.com/pingcap/tidb/pull/20986)
    -   `EXPLAIN ANALYZE` [＃21066](https://github.com/pingcap/tidb/pull/21066)の結果に、DMLステートメントのエグゼキュータ関連のランタイム情報を追加します。
    -   単一のSQLステートメントの主キーに対する複数の更新を禁止する[＃21113](https://github.com/pingcap/tidb/pull/21113)
    -   接続アイドル時間の監視メトリックを追加します[＃21301](https://github.com/pingcap/tidb/pull/21301)
    -   `runtime/trace`のツールが実行されているときに一時的にスローログを有効にします[＃20578](https://github.com/pingcap/tidb/pull/20578)

-   TiKV

    -   タグを追加して、 `split`コマンドのソースをトレースします[＃8936](https://github.com/tikv/tikv/pull/8936)
    -   `pessimistic-txn.pipelined`構成の動的変更をサポート[＃9100](https://github.com/tikv/tikv/pull/9100)
    -   Backup＆ [＃9098](https://github.com/tikv/tikv/pull/9098)とTiDB Lightningを実行する際のパフォーマンスへの影響を減らす
    -   取り込み中のSSTエラーの監視メトリックを追加する[＃9096](https://github.com/tikv/tikv/pull/9096)
    -   一部のピアがまだログを複製する必要があるときにリーダーが休止状態になるのを防ぐ[＃9093](https://github.com/tikv/tikv/pull/9093)
    -   パイプライン化された悲観的ロックの成功率を上げる[＃9086](https://github.com/tikv/tikv/pull/9086)
    -   デフォルト値の`apply-max-batch-size`と`store-max-batch-size`を[＃9020](https://github.com/tikv/tikv/pull/9020)に変更し`1024` 。
    -   `max-background-flushes`の構成アイテム[＃8947](https://github.com/tikv/tikv/pull/8947)を追加します
    -   パフォーマンスを向上させるために、デフォルトで`force-consistency-checks`を無効にします[＃9029](https://github.com/tikv/tikv/pull/9029)
    -   リージョンサイズのクエリを`pd heartbeat worker`から[＃9185](https://github.com/tikv/tikv/pull/9185)までオフロードし`split check worker`

-   PD

    -   TiKVストアが`Tombstone`になったときにTiKVクラスタのバージョンを確認します。これにより、ユーザーはダウングレードまたはアップグレードのプロセス中に互換性のない機能を有効にできなくなります[＃3213](https://github.com/pingcap/pd/pull/3213)
    -   下位バージョンの[＃3206](https://github.com/pingcap/pd/pull/3206)ストアを`Tombstone`から35に変更することを禁止し`Up`

-   TiDBダッシュボード

    -   SQLステートメント[＃775](https://github.com/pingcap/tidb-dashboard/pull/775)で[展開]をクリックしても展開を続ける
    -   **SQLステートメント**と<strong>低速クエリ</strong>の詳細ページを新しいウィンドウで開きます[＃816](https://github.com/pingcap/tidb-dashboard/pull/816)
    -   **SlowQueries**の詳細[＃817](https://github.com/pingcap/tidb-dashboard/pull/817)の時間関連フィールドの説明を改善する
    -   詳細なエラーメッセージを表示する[＃794](https://github.com/pingcap/tidb-dashboard/pull/794)

-   TiFlash

    -   レプリカ読み取りの待ち時間を短縮する
    -   TiFlashのエラーメッセージを調整する
    -   データ量が膨大な場合は、キャッシュデータのメモリ使用量を制限してください
    -   処理されているコプロセッサー・タスクの数のモニター・メトリックを追加します

-   ツール

    -   バックアップと復元（BR）

        -   チェックサムを正しく無効にしない、コマンドラインのあいまいな`--checksum false`引数を禁止します。 `--checksum=false`だけ受け入れられます。 [＃588](https://github.com/pingcap/br/pull/588)
        -   BRが誤って存在した後にPDが元の構成を復元できるように、PD構成を一時的に変更することをサポートします[＃596](https://github.com/pingcap/br/pull/596)
        -   復元後のテーブルの分析をサポート[＃622](https://github.com/pingcap/br/pull/622)
        -   `read index not ready`と`proposal in merging mode`のエラーを再試行します[＃626](https://github.com/pingcap/br/pull/626)

    -   TiCDC

        -   TiKVの休止状態機能を有効にするためのアラートを追加する[＃1120](https://github.com/pingcap/tiflow/pull/1120)
        -   スキーマストレージのメモリ使用量を削減する[＃1127](https://github.com/pingcap/tiflow/pull/1127)
        -   インクリメンタルスキャンのデータサイズが大きい場合にレプリケーションを高速化する統合ソーターの機能を追加します（実験的） [＃1122](https://github.com/pingcap/tiflow/pull/1122)
        -   TiCDC Open Protocolメッセージでの最大メッセージサイズと最大メッセージバッチの構成のサポート（Kafkaシンクの場合のみ） [＃1079](https://github.com/pingcap/tiflow/pull/1079)

    -   Dumpling

        -   失敗したチャンクでデータのダンプを再試行します[＃182](https://github.com/pingcap/dumpling/pull/182)
        -   `-F`つと`-r`の引数の両方を同時に構成することをサポートします[＃177](https://github.com/pingcap/dumpling/pull/177)
        -   デフォルトで`--filter`のシステムデータベースを除外します[＃194](https://github.com/pingcap/dumpling/pull/194)
        -   `--transactional-consistency`パラメータをサポートし、再試行[＃199](https://github.com/pingcap/dumpling/pull/199)中のMySQL接続の再構築をサポートします
        -   Dumplingで使用される圧縮アルゴリズムを指定するための`-c,--compress`パラメーターの使用をサポートします。空の文字列は、圧縮されていないことを意味します。 [＃202](https://github.com/pingcap/dumpling/pull/202)

    -   TiDB Lightning

        -   デフォルトですべてのシステムスキーマを除外する[＃459](https://github.com/pingcap/tidb-lightning/pull/459)
        -   ローカルバックエンドまたはインポーターバックエンド[＃457](https://github.com/pingcap/tidb-lightning/pull/457)の自動ランダム主キーのデフォルト値の設定をサポート
        -   範囲プロパティを使用して、ローカルバックエンド[＃422](https://github.com/pingcap/tidb-lightning/pull/422)で範囲分割をより正確にします
        -   `tikv-importer.region-split-size` 、および`mydumper.batch-size` `mydumper.read-block-size`で人間が読める形式（「 `mydumper.max-region-size` 」など）を[＃471](https://github.com/pingcap/tidb-lightning/pull/471)する

    -   TiDB Binlog

        -   アップストリームPDがダウンしている場合、またはダウンストリームへのDDLまたはDMLステートメントの適用が失敗した場合は、ゼロ以外のコードでDrainerプロセスを終了します[＃1012](https://github.com/pingcap/tidb-binlog/pull/1012)

## バグの修正 {#bug-fixes}

-   TiDB

    -   `OR`条件[＃21287](https://github.com/pingcap/tidb/pull/21287)でプレフィックスインデックスを使用した場合の誤った結果の問題を修正します。
    -   自動再試行が有効になっているときにpanicを引き起こす可能性のあるバグを修正します[＃21285](https://github.com/pingcap/tidb/pull/21285)
    -   列タイプ[＃21273](https://github.com/pingcap/tidb/pull/21273)に従ってパーティション定義をチェックするときに発生するバグを修正します
    -   パーティション式の値タイプがパーティション列タイプ[＃21136](https://github.com/pingcap/tidb/pull/21136)と一致しないバグを修正します
    -   ハッシュタイプのパーティションがパーティション名が一意であるかどうかをチェックしないバグを修正します[＃21257](https://github.com/pingcap/tidb/pull/21257)
    -   非`INT`タイプの値をハッシュパーティションテーブル[＃21238](https://github.com/pingcap/tidb/pull/21238)に挿入した後に返される誤った結果を修正します
    -   場合によっては`INSERT`ステートメントでインデックス結合を使用するときの予期しないエラーを修正します[＃21249](https://github.com/pingcap/tidb/pull/21249)
    -   `CASE WHEN`演算子の`BigInt`の符号なし列の値が`BigInt`の符号付きの値に誤って変換される問題を修正します[＃21236](https://github.com/pingcap/tidb/pull/21236)
    -   インデックスハッシュ結合とインデックスマージ結合が照合順序を考慮しないバグを修正します[＃21219](https://github.com/pingcap/tidb/pull/21219)
    -   パーティション化されたテーブルが`CREATE TABLE`および`SELECT`構文の照合順序を考慮しないバグを修正します[＃21181](https://github.com/pingcap/tidb/pull/21181)
    -   `slow_query`のクエリ結果が一部の行[＃21211](https://github.com/pingcap/tidb/pull/21211)を見逃す可能性がある問題を修正します
    -   データベース名が純粋な下位表現でない場合に`DELETE`がデータを正しく削除しない可能性があるという問題を修正します[＃21206](https://github.com/pingcap/tidb/pull/21206)
    -   DML操作後にスキーマ変更を引き起こすバグを修正します[＃21050](https://github.com/pingcap/tidb/pull/21050)
    -   結合[＃21021](https://github.com/pingcap/tidb/pull/21021)を使用すると合体した列を照会できないバグを修正します
    -   一部の半結合クエリの誤った結果を修正する[＃21019](https://github.com/pingcap/tidb/pull/21019)
    -   テーブルロックが`UPDATE`ステートメント[＃21002](https://github.com/pingcap/tidb/pull/21002)で有効にならない問題を修正します。
    -   再帰ビューを構築するときに発生するスタックオーバーフローの問題を修正します[＃21001](https://github.com/pingcap/tidb/pull/21001)
    -   外部結合[＃20954](https://github.com/pingcap/tidb/pull/20954)でインデックスマージ結合操作を実行したときに返される予期しない結果を修正しました
    -   結果が不明なトランザクションが失敗したものとして扱われることがあるという問題を修正します[＃20925](https://github.com/pingcap/tidb/pull/20925)
    -   `EXPLAIN FOR CONNECTION`が最後のクエリプラン[＃21315](https://github.com/pingcap/tidb/pull/21315)を表示できない問題を修正します
    -   読み取りコミット分離レベルのトランザクションでインデックスマージを使用すると、結果が正しくない可能性があるという問題を修正します[＃21253](https://github.com/pingcap/tidb/pull/21253)
    -   書き込みの競合後のトランザクションの再試行によって引き起こされる自動ID割り当ての失敗を修正します[＃21079](https://github.com/pingcap/tidb/pull/21079)
    -   13を使用してJSONデータを[＃21074](https://github.com/pingcap/tidb/pull/21074)に正しくインポートできない問題を修正し`LOAD DATA`
    -   新しく追加された`Enum`型列のデフォルト値が正しくない問題を修正します[＃20998](https://github.com/pingcap/tidb/pull/20998)
    -   `adddate`関数が無効な文字を挿入する問題を修正します[＃21176](https://github.com/pingcap/tidb/pull/21176)
    -   いくつかの状況で生成された間違った`PointGet`プランが間違った結果を引き起こすという問題を修正します[＃21244](https://github.com/pingcap/tidb/pull/21244)
    -   MySQL [＃20888](https://github.com/pingcap/tidb/pull/20888)と互換性があるように、 `ADD_DATE`関数の夏時間の変換を無視します
    -   末尾のスペースが`varchar`または`char`の長さの制約を超える文字列を挿入できないバグを修正します[＃21282](https://github.com/pingcap/tidb/pull/21282)
    -   `int`と`year`を比較するときに、整数を`[1, 69]`から`[2001, 2069]`または`[70, 99]`から`[1970, 1999]`に変換しない[＃21283](https://github.com/pingcap/tidb/pull/21283)を修正します。
    -   `Double`タイプのフィールド[＃21272](https://github.com/pingcap/tidb/pull/21272)を計算するときに、 `sum()`関数のオーバーフロー結果によって引き起こされるpanicを修正します。
    -   `DELETE`が一意キー[＃20705](https://github.com/pingcap/tidb/pull/20705)にロックを追加できないバグを修正します
    -   スナップショットの読み取りがロックキャッシュにヒットするバグを修正[＃21539](https://github.com/pingcap/tidb/pull/21539)
    -   長期間のトランザクションで大量のデータを読み取った後の潜在的なメモリリークの問題を修正します[＃21129](https://github.com/pingcap/tidb/pull/21129)
    -   サブクエリでテーブルエイリアスを省略すると、構文エラーが返される問題を修正します[＃20367](https://github.com/pingcap/tidb/pull/20367)
    -   クエリの`IN`関数の引数が時間型の場合、クエリが誤った結果を返す可能性がある問題を修正します[＃21290](https://github.com/pingcap/tidb/issues/21290)

-   TiKV

    -   列が255を超える場合、コプロセッサーが誤った結果を返す可能性がある問題を修正します[＃9131](https://github.com/tikv/tikv/pull/9131)
    -   リージョンマージがネットワークパーティション[＃9108](https://github.com/tikv/tikv/pull/9108)の間にデータ損失を引き起こす可能性がある問題を修正します
    -   `latin1`文字セット[＃9082](https://github.com/tikv/tikv/pull/9082)を使用すると、 `ANALYZE`ステートメントがpanicを引き起こす可能性がある問題を修正します。
    -   数値タイプを時間タイプ[＃9031](https://github.com/tikv/tikv/pull/9031)に変換したときに返される誤った結果を修正します
    -   透過的データ暗号化（TDE）が有効になっている場合、TiDBLightningがインポーターバックエンドまたはローカルバックエンドを使用してSSTファイルをTiDB Lightningに取り込めないバグを修正します[＃8995](https://github.com/tikv/tikv/pull/8995)
    -   無効な`advertise-status-addr`の値を修正します（ `0.0.0.0` ） [＃9036](https://github.com/tikv/tikv/pull/9036)
    -   コミットされたトランザクションでこのキーがロックされて削除されたときにキーが存在することを示すエラーが返される問題を修正します[＃8930](https://github.com/tikv/tikv/pull/8930)
    -   RocksDBキャッシュマッピングエラーがデータ破損を引き起こす問題を修正します[＃9029](https://github.com/tikv/tikv/pull/9029)
    -   リーダーが転送された後、フォロワー読み取りが古いデータを返す可能性があるバグを修正します[＃9240](https://github.com/tikv/tikv/pull/9240)
    -   古い値が悲観的なロックで読み取られる可能性がある問題を修正します[＃9282](https://github.com/tikv/tikv/pull/9282)
    -   リーダーの転送後にレプリカの読み取りで古いデータが取得される可能性があるバグを修正します[＃9240](https://github.com/tikv/tikv/pull/9240)
    -   プロファイリング[＃9229](https://github.com/tikv/tikv/pull/9229)の後に`SIGPROF`を受信したときに発生するTiKVクラッシュの問題を修正します

-   PD

    -   配置ルールを使用して指定されたリーダーの役割が有効にならない場合がある問題を修正します[＃3208](https://github.com/pingcap/pd/pull/3208)
    -   `trace-region-flow`の値が予期せず[＃3120](https://github.com/pingcap/pd/pull/3120)に設定される問題を修正し`false`
    -   存続時間（TTL）が無限のサービスセーフポイントが機能しないバグを修正します[＃3143](https://github.com/pingcap/pd/pull/3143)

-   TiDBダッシュボード

    -   中国語での時間の表示の問題を修正[＃755](https://github.com/pingcap/tidb-dashboard/pull/755)
    -   ブラウザの互換性に関する通知が機能しないバグを修正します[＃776](https://github.com/pingcap/tidb-dashboard/pull/776)
    -   一部のシナリオでトランザクション`start_ts`が正しく表示されない問題を修正します[＃793](https://github.com/pingcap/tidb-dashboard/pull/793)
    -   一部のSQLテキストが正しくフォーマットされていない問題を修正します[＃805](https://github.com/pingcap/tidb-dashboard/pull/805)

-   TiFlash

    -   `INFORMATION_SCHEMA.CLUSTER_HARDWARE`に使用されていないディスクの情報が含まれている可能性があるという問題を修正します
    -   DeltaCacheのメモリ使用量の見積もりが実際の使用量よりも小さいという問題を修正します
    -   スレッド情報の統計によって引き起こされるメモリリークを修正します

-   ツール

    -   バックアップと復元（BR）

        -   S3シークレットアクセスキー[＃617](https://github.com/pingcap/br/pull/617)の特殊文字によって引き起こされる障害を修正します

    -   TiCDC

        -   所有者キャンペーンキーが削除されたときに複数の所有者が存在する可能性がある問題を修正します[＃1104](https://github.com/pingcap/tiflow/pull/1104)
        -   TiKVノードがクラッシュしたとき、またはクラッシュから回復したときに、TiCDCがデータの複製を続行できない可能性があるバグを修正します。このバグはv4.0.8にのみ存在します。 [＃1198](https://github.com/pingcap/tiflow/pull/1198)
        -   テーブルが初期化される前にメタデータがetcdに繰り返しフラッシュされる問題を修正します[＃1191](https://github.com/pingcap/tiflow/pull/1191)
        -   初期のGCまたはスキーマストレージがTiDBテーブルをキャッシュするときの更新`TableInfo`の遅延によって引き起こされるレプリケーションの中断の問題を修正します[＃1114](https://github.com/pingcap/tiflow/pull/1114)
        -   DDL操作が頻繁に行われる場合にスキーマストレージのメモリコストが高くなる問題を修正します[＃1127](https://github.com/pingcap/tiflow/pull/1127)
        -   チェンジフィードが一時停止または停止したときのゴルーチンリークを修正する[＃1075](https://github.com/pingcap/tiflow/pull/1075)
        -   ダウンストリームKafka1のサービスまたはネットワークジッターによって引き起こされるレプリケーションの中断を防ぐために、Kafkaプロデューサーの最大再試行タイムアウトを600秒に増やし[＃1118](https://github.com/pingcap/tiflow/pull/1118) 。
        -   Kafkaバッチサイズが有効にならないバグを修正します[＃1112](https://github.com/pingcap/tiflow/pull/1112)
        -   TiCDCとPDの間のネットワークにジッターがあり、同時に再開される一時停止された変更フィードがある場合に、一部のテーブルの行変更が失われる可能性があるバグを修正します[＃1213](https://github.com/pingcap/tiflow/pull/1213)
        -   TiCDCとPDの間のネットワークが安定していない場合にTiCDCプロセスが終了する可能性があるバグを修正します[＃1218](https://github.com/pingcap/tiflow/pull/1218)
        -   TiCDCでシングルトンPDクライアントを使用し、TiCDCが誤ってPDクライアントを閉じてレプリケーションブロック[＃1217](https://github.com/pingcap/tiflow/pull/1217)を引き起こすバグを修正します。
        -   TiCDC所有者がetcdウォッチクライアントで大量のメモリを消費する可能性があるバグを修正します[＃1224](https://github.com/pingcap/tiflow/pull/1224)

    -   Dumpling

        -   MySQLデータベースサーバーへの接続が閉じられたときにDumplingがブロックされる可能性がある問題を修正します[＃190](https://github.com/pingcap/dumpling/pull/190)

    -   TiDB Lightning

        -   キーが間違ったフィールド情報を使用してエンコードされる問題を修正します[＃437](https://github.com/pingcap/tidb-lightning/pull/437)
        -   GC存続時間TTLが有効にならない問題を修正します[＃448](https://github.com/pingcap/tidb-lightning/pull/448)
        -   ローカルバックエンドモードで実行中のTiDB Lightningを手動で停止するとpanicが発生する問題を修正します[＃484](https://github.com/pingcap/tidb-lightning/pull/484)
