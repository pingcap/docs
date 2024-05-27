---
title: TiDB 4.0.9 Release Notes
summary: TiDB 4.0.9 は 2020 年 12 月 21 日にリリースされました。このリリースには、互換性の変更、新機能、改善、バグ修正、および TiKV、TiDB Dashboard、PD、 TiFlash 、およびさまざまなツールの更新が含まれています。注目すべき変更点としては、TiDB での `enable-streaming` 構成項目の非推奨、 TiFlashでのstorageエンジンの最新データを複数のディスクに保存するためのサポート、および TiDB と TiKV でのさまざまなバグ修正が挙げられます。
---

# TiDB 4.0.9 リリースノート {#tidb-4-0-9-release-notes}

発売日: 2020年12月21日

TiDB バージョン: 4.0.9

## 互換性の変更 {#compatibility-changes}

-   ティビ

    -   `enable-streaming`構成項目[＃21055](https://github.com/pingcap/tidb/pull/21055)を廃止する

-   ティクヴ

    -   保存時の暗号化が有効になっている場合、I/O とミューテックスの競合が軽減されます。この変更は下位互換性がありません。ユーザーがクラスターを v4.0.9 より前のバージョンにダウングレードする必要がある場合は、 `security.encryption.enable-file-dictionary-log`無効にし、ダウングレード前に TiKV を再起動する必要があります[＃9195](https://github.com/tikv/tikv/pull/9195)

## 新機能 {#new-features}

-   TiFlash

    -   storageエンジンの最新データを複数のディスクに保存する機能をサポート (実験的)

-   TiDBダッシュボード

    -   **SQLステートメント**ページ[＃749](https://github.com/pingcap/tidb-dashboard/pull/749)のすべてのフィールドによる表示と並べ替えをサポート
    -   トポロジーグラフのズームとパンをサポート[＃772](https://github.com/pingcap/tidb-dashboard/pull/772)
    -   **SQL ステートメント**と**スロークエリの**ページでディスク使用量情報を表示する機能をサポート[＃777](https://github.com/pingcap/tidb-dashboard/pull/777)
    -   **SQL ステートメント**と**スロークエリ**ページでリストデータのエクスポートをサポート[＃778](https://github.com/pingcap/tidb-dashboard/pull/778)
    -   Prometheusアドレス[＃808](https://github.com/pingcap/tidb-dashboard/pull/808)カスタマイズをサポート
    -   クラスター統計[＃815](https://github.com/pingcap/tidb-dashboard/pull/815)のページを追加
    -   **スロークエリ**の詳細に時間関連のフィールドを追加する[＃810](https://github.com/pingcap/tidb-dashboard/pull/810)

## 改善点 {#improvements}

-   ティビ

    -   等条件を他の条件に変換するときに、（インデックス）マージ結合をヒューリスティックな方法で回避する[＃21146](https://github.com/pingcap/tidb/pull/21146)
    -   ユーザー変数の種類を区別する[＃21107](https://github.com/pingcap/tidb/pull/21107)
    -   設定ファイル[＃20922](https://github.com/pingcap/tidb/pull/20922)の`GOGC`変数の設定をサポート
    -   ダンプされたバイナリタイム（ `Timestamp`と`Datetime` ）をMySQL [＃21135](https://github.com/pingcap/tidb/pull/21135)とより互換性のあるものにする
    -   `LOCK IN SHARE MODE`構文[＃21005](https://github.com/pingcap/tidb/pull/21005)を使用する文にエラーメッセージを表示する
    -   ショートカット可能な式で定数を折りたたむときに不要な警告やエラーを出力しないようにする[＃21040](https://github.com/pingcap/tidb/pull/21040)
    -   `LOAD DATA`文[＃21199](https://github.com/pingcap/tidb/pull/21199)を準備するときにエラーが発生する
    -   整数列タイプを変更するときに整数ゼロフィルサイズの属性を無視する[＃20986](https://github.com/pingcap/tidb/pull/20986)
    -   `EXPLAIN ANALYZE` [＃21066](https://github.com/pingcap/tidb/pull/21066)の結果にDML文の実行関連実行情報を追加する
    -   単一のSQL文で主キーの複数の更新を許可しない[＃21113](https://github.com/pingcap/tidb/pull/21113)
    -   接続アイドル時間の監視メトリックを追加する[＃21301](https://github.com/pingcap/tidb/pull/21301)
    -   `runtime/trace`ツールの実行中にスローログを一時的に有効にする[＃20578](https://github.com/pingcap/tidb/pull/20578)

-   ティクヴ

    -   `split`コマンド[＃8936](https://github.com/tikv/tikv/pull/8936)のソースをトレースするためのタグを追加します
    -   `pessimistic-txn.pipelined`構成[＃9100](https://github.com/tikv/tikv/pull/9100)の動的変更をサポート
    -   バックアップと復元およびTiDB Lightning [＃9098](https://github.com/tikv/tikv/pull/9098)を実行する際のパフォーマンスへの影響を軽減
    -   取り込み中のSSTエラーの監視メトリックを追加する[＃9096](https://github.com/tikv/tikv/pull/9096)
    -   一部のピアがログを複製する必要がある場合にリーダーが休止状態にならないようにします[＃9093](https://github.com/tikv/tikv/pull/9093)
    -   パイプライン化され悲観的ロックの成功率を向上させる[＃9086](https://github.com/tikv/tikv/pull/9086)
    -   デフォルト値`apply-max-batch-size`と`store-max-batch-size`を`1024` [＃9020](https://github.com/tikv/tikv/pull/9020)に変更
    -   `max-background-flushes`構成項目[＃8947](https://github.com/tikv/tikv/pull/8947)を追加する
    -   パフォーマンスを向上させるためにデフォルトで`force-consistency-checks`無効にする[＃9029](https://github.com/tikv/tikv/pull/9029)
    -   リージョンサイズを`pd heartbeat worker`から`split check worker` [＃9185](https://github.com/tikv/tikv/pull/9185)にオフロードする

-   PD

    -   TiKVストアが`Tombstone`になったときにTiKVクラスターのバージョンをチェックします。これにより、ダウングレードまたはアップグレード[＃3213](https://github.com/pingcap/pd/pull/3213)のプロセス中にユーザーが互換性のない機能を有効にすることを防ぎます。
    -   下位バージョンの TiKV ストアを`Tombstone`から`Up` [＃3206](https://github.com/pingcap/pd/pull/3206)に戻すことを禁止します。

-   TiDBダッシュボード

    -   SQL ステートメント[＃775](https://github.com/pingcap/tidb-dashboard/pull/775)の [展開] をクリックすると展開が継続されます。
    -   **SQL ステートメント**と**スロークエリ**[＃816](https://github.com/pingcap/tidb-dashboard/pull/816)詳細ページを新しいウィンドウで開く
    -   **スロークエリの**詳細[＃817](https://github.com/pingcap/tidb-dashboard/pull/817)における時間関連フィールドの説明の改善
    -   詳細なエラーメッセージを表示する[＃794](https://github.com/pingcap/tidb-dashboard/pull/794)

-   TiFlash

    -   レプリカ読み取りのレイテンシーを削減
    -   TiFlashのエラーメッセージを改善する
    -   データ量が大きい場合、キャッシュデータのメモリ使用量を制限する
    -   処理されているコプロセッサタスクの数を監視するメトリックを追加します。

-   ツール

    -   バックアップと復元 (BR)

        -   コマンドラインであいまいな`--checksum false`引数を許可しません。チェックサムを正しく無効にしません。3 `--checksum=false`が受け入れられます[＃588](https://github.com/pingcap/br/pull/588)
        -   BRが誤って存在した後にPDが元の構成を回復できるように、PD構成を一時的に変更することをサポートします[＃596](https://github.com/pingcap/br/pull/596)
        -   復元後のテーブル分析をサポート[＃622](https://github.com/pingcap/br/pull/622)
        -   `read index not ready`と`proposal in merging mode`エラーを再試行してください[＃626](https://github.com/pingcap/br/pull/626)

    -   ティCDC

        -   TiKV の Hibernate リージョン機能を有効にするアラートを追加する[＃1120](https://github.com/pingcap/tiflow/pull/1120)
        -   スキーマstorage[＃1127](https://github.com/pingcap/tiflow/pull/1127)メモリ使用量を削減する
        -   増分スキャンのデータサイズが大きい場合にレプリケーションを高速化する統合ソーター機能を追加（実験的） [＃1122](https://github.com/pingcap/tiflow/pull/1122)
        -   TiCDC オープン プロトコル メッセージの最大メッセージ サイズと最大メッセージ バッチの構成をサポート (Kafka シンクのみ) [＃1079](https://github.com/pingcap/tiflow/pull/1079)

    -   Dumpling

        -   失敗したチャンク[＃182](https://github.com/pingcap/dumpling/pull/182)のデータのダンプを再試行します
        -   `-F`と`-r`引数を同時に設定するサポート[＃177](https://github.com/pingcap/dumpling/pull/177)
        -   デフォルトで`--filter`のシステムデータベースを除外[＃194](https://github.com/pingcap/dumpling/pull/194)
        -   `--transactional-consistency`パラメータをサポートし、再試行[＃199](https://github.com/pingcap/dumpling/pull/199)中に MySQL 接続を再構築することをサポートします。
        -   Dumplingで使用される圧縮アルゴリズムを指定するために`-c,--compress`パラメータの使用をサポートします。空の文字列は圧縮なしを意味します[＃202](https://github.com/pingcap/dumpling/pull/202)

    -   TiDB Lightning

        -   デフォルトですべてのシステムスキーマを除外する[＃459](https://github.com/pingcap/tidb-lightning/pull/459)
        -   ローカルバックエンドまたはインポーターバックエンド[＃457](https://github.com/pingcap/tidb-lightning/pull/457)の自動ランダムプライマリキーのデフォルト値の設定をサポート
        -   範囲プロパティを使用して、Local-backend [＃422](https://github.com/pingcap/tidb-lightning/pull/422)で範囲分割をより正確にします。
        -   `tikv-importer.region-split-size` `mydumper.read-block-size`人間が読める形式（「 `mydumper.batch-size` GiB」など） [＃471](https://github.com/pingcap/tidb-lightning/pull/471)サポートする`mydumper.max-region-size`

    -   TiDBBinlog

        -   上流PDがダウンしているか、下流へのDDLまたはDMLステートメントの適用に失敗した場合は、ゼロ以外のコードでDrainerプロセスを終了します[＃1012](https://github.com/pingcap/tidb-binlog/pull/1012)

## バグの修正 {#bug-fixes}

-   ティビ

    -   プレフィックスインデックスを条件`OR`と条件[＃21287](https://github.com/pingcap/tidb/pull/21287)で使用した場合に誤った結果が出る問題を修正
    -   自動再試行が有効になっている場合にpanicを引き起こす可能性があるバグを修正[＃21285](https://github.com/pingcap/tidb/pull/21285)
    -   列タイプ[＃21273](https://github.com/pingcap/tidb/pull/21273)に従ってパーティション定義をチェックするときに発生するバグを修正
    -   パーティション式の値の型がパーティション列の型と一致しないバグを修正[＃21136](https://github.com/pingcap/tidb/pull/21136)
    -   ハッシュ型パーティションがパーティション名が一意かどうかをチェックしないバグを修正[＃21257](https://github.com/pingcap/tidb/pull/21257)
    -   ハッシュパーティションテーブル[＃21238](https://github.com/pingcap/tidb/pull/21238)に`INT`以外の型の値を挿入した後に返される誤った結果を修正
    -   `INSERT`ステートメントでインデックス結合を使用すると予期しないエラーが発生する場合がある問題を修正[＃21249](https://github.com/pingcap/tidb/pull/21249)
    -   `CASE WHEN`演算子の`BigInt`符号なし列値が`BigInt`符号付き値[＃21236](https://github.com/pingcap/tidb/pull/21236)に誤って変換される問題を修正
    -   インデックスハッシュ結合とインデックスマージ結合が照合順序[＃21219](https://github.com/pingcap/tidb/pull/21219)を考慮しないバグを修正
    -   パーティションテーブルが構文`CREATE TABLE`と`SELECT`照合順序を考慮しないバグを修正[＃21181](https://github.com/pingcap/tidb/pull/21181)
    -   `slow_query`のクエリ結果で一部の行が欠落する可能性がある問題を修正[＃21211](https://github.com/pingcap/tidb/pull/21211)
    -   データベース名が純粋な下位表現ではない場合にデータを正しく削除でき`DELETE`可能性がある問題を修正しました[＃21206](https://github.com/pingcap/tidb/pull/21206)
    -   DML操作後にスキーマ変更を引き起こすバグを修正[＃21050](https://github.com/pingcap/tidb/pull/21050)
    -   結合[＃21021](https://github.com/pingcap/tidb/pull/21021)を使用するときに結合された列をクエリできないバグを修正
    -   一部のセミ結合クエリの誤った結果を修正[＃21019](https://github.com/pingcap/tidb/pull/21019)
    -   テーブルロックが`UPDATE`文[＃21002](https://github.com/pingcap/tidb/pull/21002)で有効にならない問題を修正
    -   再帰ビュー[＃21001](https://github.com/pingcap/tidb/pull/21001)構築時に発生するスタックオーバーフローの問題を修正
    -   外部結合[＃20954](https://github.com/pingcap/tidb/pull/20954)でインデックス マージ結合操作を実行したときに返される予期しない結果を修正しました。
    -   結果が未確定のトランザクションが失敗として扱われることがある問題を修正[＃20925](https://github.com/pingcap/tidb/pull/20925)
    -   `EXPLAIN FOR CONNECTION`最後のクエリプランを表示できない問題を修正[＃21315](https://github.com/pingcap/tidb/pull/21315)
    -   インデックスマージが Read Committed 分離レベルのトランザクションで使用されると、結果が不正確になる可能性がある問題を修正しました[＃21253](https://github.com/pingcap/tidb/pull/21253)
    -   書き込み競合後のトランザクション再試行によって発生する自動ID割り当ての失敗を修正[＃21079](https://github.com/pingcap/tidb/pull/21079)
    -   `LOAD DATA` [＃21074](https://github.com/pingcap/tidb/pull/21074)を使用してJSONデータをTiDBに正しくインポートできない問題を修正
    -   新しく追加された`Enum`型列のデフォルト値が正しくない問題を修正しました[＃20998](https://github.com/pingcap/tidb/pull/20998)
    -   `adddate`関数が無効な文字を挿入する問題を修正[＃21176](https://github.com/pingcap/tidb/pull/21176)
    -   状況によっては間違った`PointGet`プランが生成され、間違った結果[＃21244](https://github.com/pingcap/tidb/pull/21244)が発生する問題を修正しました
    -   MySQL [＃20888](https://github.com/pingcap/tidb/pull/20888)との互換性を保つため、 `ADD_DATE`関数の夏時間の変換を無視する
    -   `varchar`または`char`の長さ制約を超える末尾のスペースを含む文字列を挿入できないバグを修正[＃21282](https://github.com/pingcap/tidb/pull/21282)
    -   `int`と`year` [＃21283](https://github.com/pingcap/tidb/pull/21283)比較するときに、整数が`[1, 69]`から`[2001, 2069]`または`[70, 99]`から`[1970, 1999]`に変換されないバグを修正しました。
    -   `Double`型フィールド[＃21272](https://github.com/pingcap/tidb/pull/21272)を計算するときに`sum()`関数の結果がオーバーフローして発生するpanicを修正
    -   `DELETE`ユニークキー[＃20705](https://github.com/pingcap/tidb/pull/20705)にロックを追加できないバグを修正
    -   スナップショットの読み取りがロックキャッシュ[＃21539](https://github.com/pingcap/tidb/pull/21539)にヒットするバグを修正
    -   長時間トランザクションで大量のデータを読み込んだ後に発生する可能性のあるメモリリークの問題を修正[＃21129](https://github.com/pingcap/tidb/pull/21129)
    -   サブクエリでテーブルエイリアスを省略すると構文エラーが返される問題を修正しました[＃20367](https://github.com/pingcap/tidb/pull/20367)
    -   クエリ内の`IN`番目の関数の引数が時間型の場合、クエリが誤った結果を返す可能性がある問題を修正しました[＃21290](https://github.com/pingcap/tidb/issues/21290)

-   ティクヴ

    -   列数が255を超える場合にコプロセッサーが誤った結果を返す可能性がある問題を修正[＃9131](https://github.com/tikv/tikv/pull/9131)
    -   リージョンマージによりネットワークパーティション[＃9108](https://github.com/tikv/tikv/pull/9108)中にデータが失われる可能性がある問題を修正
    -   `latin1`文字セット[＃9082](https://github.com/tikv/tikv/pull/9082)を使用すると`ANALYZE`文でpanicが発生する可能性がある問題を修正
    -   数値型を時間型に変換するときに返される誤った結果を修正[＃9031](https://github.com/tikv/tikv/pull/9031)
    -   透過的データ暗号化 (TDE) が有効になっている場合、 TiDB Lightning がインポーター バックエンドまたはローカル バックエンドを使用して SST ファイルを TiKV に取り込むことができないバグを修正しました[＃8995](https://github.com/tikv/tikv/pull/8995)
    -   無効な値`advertise-status-addr`を修正する（ `0.0.0.0` ） [＃9036](https://github.com/tikv/tikv/pull/9036)
    -   コミットされたトランザクション[＃8930](https://github.com/tikv/tikv/pull/8930)でキーがロックされ削除されたときに、キーが存在することを示すエラーが返される問題を修正しました。
    -   RocksDB キャッシュ マッピング エラーによりデータ破損が発生する問題を修正[＃9029](https://github.com/tikv/tikv/pull/9029)
    -   リーダーが転送された後にFollower Readが古いデータを返す可能性があるバグを修正[＃9240](https://github.com/tikv/tikv/pull/9240)
    -   悲観的ロック[＃9282](https://github.com/tikv/tikv/pull/9282)で古い値が読み取られる可能性がある問題を修正
    -   リーダー転送後にレプリカ読み取りで古いデータが取得される可能性があるバグを修正[＃9240](https://github.com/tikv/tikv/pull/9240)
    -   プロファイリング[＃9229](https://github.com/tikv/tikv/pull/9229)後に`SIGPROF`受信すると発生するTiKVクラッシュの問題を修正

-   PD

    -   配置ルールを使用して指定されたリーダーロールが、場合によっては有効にならない問題を修正[＃3208](https://github.com/pingcap/pd/pull/3208)
    -   `trace-region-flow`値が予期せず`false` [＃3120](https://github.com/pingcap/pd/pull/3120)に設定される問題を修正
    -   無制限の Time To Live (TTL) を持つサービスセーフポイントが機能しないバグを修正[＃3143](https://github.com/pingcap/pd/pull/3143)

-   TiDBダッシュボード

    -   中国語の時間表示の問題を修正[＃755](https://github.com/pingcap/tidb-dashboard/pull/755)
    -   ブラウザ互換性通知が機能しないバグを修正[＃776](https://github.com/pingcap/tidb-dashboard/pull/776)
    -   一部のシナリオでトランザクション`start_ts`が誤って表示される問題を修正[＃793](https://github.com/pingcap/tidb-dashboard/pull/793)
    -   一部のSQLテキストのフォーマットが間違っている問題を修正[＃805](https://github.com/pingcap/tidb-dashboard/pull/805)

-   TiFlash

    -   `INFORMATION_SCHEMA.CLUSTER_HARDWARE`に使用されていないディスクの情報が含まれる可能性がある問題を修正
    -   デルタキャッシュのメモリ使用量の推定値が実際の使用量よりも小さい問題を修正しました
    -   スレッド情報統計によるメモリリークを修正

-   ツール

    -   バックアップと復元 (BR)

        -   S3 シークレット アクセス キー[＃617](https://github.com/pingcap/br/pull/617)の特殊文字によって発生する障害を修正

    -   ティCDC

        -   所有者キャンペーンキーが削除されたときに複数の所有者が存在する可能性がある問題を修正[＃1104](https://github.com/pingcap/tiflow/pull/1104)
        -   TiKV ノードがクラッシュしたり、クラッシュから回復したりしたときに、TiCDC がデータのレプリケーションを続行できなくなる可能性があるバグを修正しました。このバグは[＃1198](https://github.com/pingcap/tiflow/pull/1198)にのみ存在します。1
        -   テーブルが初期化される前にメタデータが繰り返しetcdにフラッシュされる問題を修正[＃1191](https://github.com/pingcap/tiflow/pull/1191)
        -   スキーマstorageが TiDB テーブル[＃1114](https://github.com/pingcap/tiflow/pull/1114)をキャッシュするときに、早期 GC または更新`TableInfo`のレイテンシーによってレプリケーションが中断される問題を修正しました。
        -   DDL操作が頻繁に行われる場合にスキーマstorageのメモリ消費量が多すぎる問題を修正[＃1127](https://github.com/pingcap/tiflow/pull/1127)
        -   チェンジフィードが一時停止または停止されたときの goroutine リークを修正[＃1075](https://github.com/pingcap/tiflow/pull/1075)
        -   下流の Kafka [＃1118](https://github.com/pingcap/tiflow/pull/1118)サービスまたはネットワークのジッターによるレプリケーションの中断を防ぐために、Kafka プロデューサーの最大再試行タイムアウトを 600 秒に増やします。
        -   Kafka バッチサイズが有効にならないバグを修正[＃1112](https://github.com/pingcap/tiflow/pull/1112)
        -   TiCDC と PD 間のネットワークにジッターがあり、一時停止された変更フィードが同時に再開されると、一部のテーブルの行の変更が失われる可能性があるバグを修正しました[＃1213](https://github.com/pingcap/tiflow/pull/1213)
        -   TiCDCとPD間のネットワークが安定していない場合にTiCDCプロセスが終了する可能性があるバグを修正[＃1218](https://github.com/pingcap/tiflow/pull/1218)
        -   TiCDC でシングルトン PD クライアントを使用し、TiCDC が誤って PD クライアントを閉じてレプリケーション ブロック[＃1217](https://github.com/pingcap/tiflow/pull/1217)が発生するバグを修正しました。
        -   TiCDC 所有者が etcd ウォッチ クライアント[＃1224](https://github.com/pingcap/tiflow/pull/1224)でメモリを過剰に消費する可能性があるバグを修正しました。

    -   Dumpling

        -   MySQLデータベースサーバーへの接続が閉じられたときにDumplingがブロックされる可能性がある問題を修正しました[＃190](https://github.com/pingcap/dumpling/pull/190)

    -   TiDB Lightning

        -   キーが間違ったフィールド情報を使用してエンコードされる問題を修正[＃437](https://github.com/pingcap/tidb-lightning/pull/437)
        -   GCライフタイムTTLが有効にならない問題を修正[＃448](https://github.com/pingcap/tidb-lightning/pull/448)
        -   ローカルバックエンドモードで実行中のTiDB Lightning を手動で停止するとpanicが発生する問題を修正[＃484](https://github.com/pingcap/tidb-lightning/pull/484)
