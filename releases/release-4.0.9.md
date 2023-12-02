---
title: TiDB 4.0.9 Release Notes
---

# TiDB 4.0.9 リリースノート {#tidb-4-0-9-release-notes}

発売日：2020年12月21日

TiDB バージョン: 4.0.9

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   `enable-streaming`構成アイテム[#21055](https://github.com/pingcap/tidb/pull/21055)を非推奨にする

-   TiKV

    -   保存時の暗号化が有効になっている場合、I/O とミューテックスの競合を軽減します。この変更には下位互換性がありません。ユーザーがクラスターを v4.0.9 より前のバージョンにダウングレードする必要がある場合は、ダウングレード前に`security.encryption.enable-file-dictionary-log`を無効にし、TiKV を再起動する必要があります。 [#9195](https://github.com/tikv/tikv/pull/9195)

## 新機能 {#new-features}

-   TiFlash

    -   storageエンジンの最新データを複数のディスクに保存するサポート (実験的)

-   TiDB ダッシュボード

    -   **SQL ステートメント**ページ[#749](https://github.com/pingcap/tidb-dashboard/pull/749)のすべてのフィールドによる表示と並べ替えのサポート
    -   トポロジ グラフのズームとパンのサポート[#772](https://github.com/pingcap/tidb-dashboard/pull/772)
    -   **SQL ステートメント**および**スロー クエリ**ページでのディスク使用量情報の表示のサポート[#777](https://github.com/pingcap/tidb-dashboard/pull/777)
    -   **SQL ステートメント**と**スロー クエリ**ページでのリスト データのエクスポートのサポート[#778](https://github.com/pingcap/tidb-dashboard/pull/778)
    -   Prometheus アドレスのカスタマイズのサポート[#808](https://github.com/pingcap/tidb-dashboard/pull/808)
    -   クラスター統計[#815](https://github.com/pingcap/tidb-dashboard/pull/815)のページを追加します。
    -   **スロークエリ**の詳細に時間関連フィールドを追加[#810](https://github.com/pingcap/tidb-dashboard/pull/810)

## 改善点 {#improvements}

-   TiDB

    -   等しい条件を他の条件に変換する場合、ヒューリスティックな方法で (インデックス) マージ結合を回避します[#21146](https://github.com/pingcap/tidb/pull/21146)
    -   ユーザー変数の種類を区別する[#21107](https://github.com/pingcap/tidb/pull/21107)
    -   構成ファイル[#20922](https://github.com/pingcap/tidb/pull/20922)での`GOGC`変数の設定のサポート
    -   ダンプされたバイナリ時刻 ( `Timestamp`および`Datetime` ) を MySQL [#21135](https://github.com/pingcap/tidb/pull/21135)との互換性を高める
    -   `LOCK IN SHARE MODE`構文[#21005](https://github.com/pingcap/tidb/pull/21005)を使用するステートメントにはエラー メッセージを提供します。
    -   ショートカット可能な式[#21040](https://github.com/pingcap/tidb/pull/21040)で定数を折りたたむときに、不要な警告やエラーが出力されるのを回避します。
    -   `LOAD DATA`ステートメント[#21199](https://github.com/pingcap/tidb/pull/21199)の準備時にエラーが発生します。
    -   整数列の型を変更する場合、整数のゼロ埋めサイズの属性を無視します[#20986](https://github.com/pingcap/tidb/pull/20986)
    -   `EXPLAIN ANALYZE` [#21066](https://github.com/pingcap/tidb/pull/21066)の結果に DML ステートメントのエグゼキューター関連の実行時情報を追加します。
    -   単一の SQL ステートメントで主キーに対する複数の更新を禁止する[#21113](https://github.com/pingcap/tidb/pull/21113)
    -   接続アイドル時間の監視メトリックを追加します[#21301](https://github.com/pingcap/tidb/pull/21301)
    -   `runtime/trace`ツールの実行中にスローログを一時的に有効にする[#20578](https://github.com/pingcap/tidb/pull/20578)

-   TiKV

    -   `split`コマンドのソースをトレースするタグを追加します[#8936](https://github.com/tikv/tikv/pull/8936)
    -   `pessimistic-txn.pipelined`構成の動的変更をサポート[#9100](https://github.com/tikv/tikv/pull/9100)
    -   バックアップと復元およびTiDB Lightning [#9098](https://github.com/tikv/tikv/pull/9098)の実行時のパフォーマンスへの影響を軽減します。
    -   取り込み SST エラーの監視メトリクスを追加[#9096](https://github.com/tikv/tikv/pull/9096)
    -   一部のピアがログを複製する必要がある場合にリーダーが休止状態にならないようにする[#9093](https://github.com/tikv/tikv/pull/9093)
    -   パイプライン化された悲観的ロックの成功率を向上させる[#9086](https://github.com/tikv/tikv/pull/9086)
    -   デフォルト値の`apply-max-batch-size`と`store-max-batch-size` `1024` [#9020](https://github.com/tikv/tikv/pull/9020)に変更します。
    -   `max-background-flushes`設定項目[#8947](https://github.com/tikv/tikv/pull/8947)を追加します
    -   パフォーマンスを向上させるには、デフォルトで`force-consistency-checks`を無効にします[#9029](https://github.com/tikv/tikv/pull/9029)
    -   リージョンサイズ`pd heartbeat worker` ～ `split check worker` [#9185](https://github.com/tikv/tikv/pull/9185)に関するクエリをオフロードします。

-   PD

    -   TiKV ストアが`Tombstone`になったときに TiKV クラスターのバージョンを確認します。これにより、ユーザーはダウングレードまたはアップグレードのプロセス中に互換性のない機能を有効にできなくなります[#3213](https://github.com/pingcap/pd/pull/3213)
    -   下位バージョンの TiKV ストアを`Tombstone`から`Up`に戻すことを禁止します[#3206](https://github.com/pingcap/pd/pull/3206)

-   TiDB ダッシュボード

    -   SQL文[#775](https://github.com/pingcap/tidb-dashboard/pull/775)の「展開」をクリックすると展開し続けます
    -   **SQL ステートメント**と**スロー クエリ**の詳細ページを新しいウィンドウで開く[#816](https://github.com/pingcap/tidb-dashboard/pull/816)
    -   **スロークエリの**詳細[#817](https://github.com/pingcap/tidb-dashboard/pull/817)の時間関連フィールドの説明を改善
    -   詳細なエラーメッセージを表示[#794](https://github.com/pingcap/tidb-dashboard/pull/794)

-   TiFlash

    -   レプリカ読み取りのレイテンシーを短縮する
    -   TiFlash のエラー メッセージを修正する
    -   データ量が大きい場合にキャッシュデータのメモリ使用量を制限する
    -   処理されるコプロセッサ タスクの数の監視メトリックを追加します。

-   ツール

    -   バックアップと復元 (BR)

        -   コマンド ラインで曖昧な`--checksum false`引数を使用しないでください。チェックサムは正しく無効になりません。 `--checksum=false`のみ受け付けます。 [#588](https://github.com/pingcap/br/pull/588)
        -   BR が誤って存在した後に PD が元の設定を回復できるように、PD 設定の一時的な変更をサポートします[#596](https://github.com/pingcap/br/pull/596)
        -   復元後のテーブル分析のサポート[#622](https://github.com/pingcap/br/pull/622)
        -   `read index not ready`と`proposal in merging mode`エラーについては再試行[#626](https://github.com/pingcap/br/pull/626)

    -   TiCDC

        -   TiKV の休止リージョン機能を有効にするためのアラートを追加します[#1120](https://github.com/pingcap/tiflow/pull/1120)
        -   スキーマstorage[#1127](https://github.com/pingcap/tiflow/pull/1127)のメモリ使用量を削減します。
        -   インクリメンタルスキャンのデータサイズが大きい場合にレプリケーションを高速化するユニファイドソーター機能を追加（実験的） [#1122](https://github.com/pingcap/tiflow/pull/1122)
        -   TiCDC オープン プロトコル メッセージでの最大メッセージ サイズと最大メッセージ バッチの構成をサポート (Kafka シンクのみ) [#1079](https://github.com/pingcap/tiflow/pull/1079)

    -   Dumpling

        -   失敗したチャンクのデータのダンプを再試行します[#182](https://github.com/pingcap/dumpling/pull/182)
        -   `-F`引数と`-r`引数の両方の同時構成をサポート[#177](https://github.com/pingcap/dumpling/pull/177)
        -   デフォルトで`--filter`のシステムデータベースを除外[#194](https://github.com/pingcap/dumpling/pull/194)
        -   `--transactional-consistency`パラメータをサポートし、再試行[#199](https://github.com/pingcap/dumpling/pull/199)中の MySQL 接続の再構築をサポートします。
        -   Dumplingで使用される圧縮アルゴリズムを指定するための`-c,--compress`パラメーターの使用をサポートします。空の文字列は圧縮がないことを意味します。 [#202](https://github.com/pingcap/dumpling/pull/202)

    -   TiDB Lightning

        -   デフォルトですべてのシステム スキーマを除外する[#459](https://github.com/pingcap/tidb-lightning/pull/459)
        -   Local-backend または Importer-backend [#457](https://github.com/pingcap/tidb-lightning/pull/457)の自動ランダム主キーのデフォルト値の設定のサポート
        -   範囲プロパティを使用して、ローカル バックエンド[#422](https://github.com/pingcap/tidb-lightning/pull/422)での範囲分割をより正確にします。
        -   `tikv-importer.region-split-size` 、 `mydumper.read-block-size` 、 `mydumper.batch-size` 、および`mydumper.max-region-size`で人間が判読できる形式 (「2.5 GiB」など) をサポートします[#471](https://github.com/pingcap/tidb-lightning/pull/471)

    -   TiDBBinlog

        -   上流の PD がダウンしている場合、または下流への DDL または DML ステートメントの適用が失敗した場合は、ゼロ以外のコードでDrainerプロセスを終了します[#1012](https://github.com/pingcap/tidb-binlog/pull/1012)

## バグの修正 {#bug-fixes}

-   TiDB

    -   `OR`条件[#21287](https://github.com/pingcap/tidb/pull/21287)でプレフィックス インデックスを使用するときに誤った結果が表示される問題を修正しました。
    -   自動再試行が有効になっている場合にpanicを引き起こす可能性があるバグを修正[#21285](https://github.com/pingcap/tidb/pull/21285)
    -   カラムタイプ[#21273](https://github.com/pingcap/tidb/pull/21273)に応じてパーティション定義をチェックするときに発生するバグを修正
    -   パーティション式の値の型がパーティション列の型[#21136](https://github.com/pingcap/tidb/pull/21136)と一致しないバグを修正
    -   ハッシュ型パーティションがパーティション名が一意であるかどうかをチェックしないバグを修正[#21257](https://github.com/pingcap/tidb/pull/21257)
    -   ハッシュパーティションテーブル[#21238](https://github.com/pingcap/tidb/pull/21238)に`INT`以外のタイプの値を挿入した後に返される間違った結果を修正しました。
    -   `INSERT`ステートメントでインデックス結合を使用すると、場合によっては予期しないエラーが発生する問題を修正[#21249](https://github.com/pingcap/tidb/pull/21249)
    -   `CASE WHEN`演算子の`BigInt`符号なし列の値が、 `BigInt`符号付き値[#21236](https://github.com/pingcap/tidb/pull/21236)に誤って変換される問題を修正します。
    -   インデックスハッシュジョインとインデックスマージジョインが照合照合順序[#21219](https://github.com/pingcap/tidb/pull/21219)を考慮しないバグを修正
    -   パーティションテーブルが`CREATE TABLE`と`SELECT`構文での照合順序を考慮しないバグを修正[#21181](https://github.com/pingcap/tidb/pull/21181)
    -   `slow_query`のクエリ結果で一部の行が欠落する可能性がある問題を修正します[#21211](https://github.com/pingcap/tidb/pull/21211)
    -   データベース名が純粋な下位表現ではない場合、データが正しく削除されない場合が`DELETE`問題を修正します[#21206](https://github.com/pingcap/tidb/pull/21206)
    -   DML 操作後にスキーマ変更を引き起こすバグを修正[#21050](https://github.com/pingcap/tidb/pull/21050)
    -   結合[#21021](https://github.com/pingcap/tidb/pull/21021)を使用すると結合された列をクエリできないバグを修正
    -   一部の準結合クエリの誤った結果を修正[#21019](https://github.com/pingcap/tidb/pull/21019)
    -   `UPDATE`ステートメント[#21002](https://github.com/pingcap/tidb/pull/21002)でテーブル ロックが有効にならない問題を修正します。
    -   再帰的ビュー[#21001](https://github.com/pingcap/tidb/pull/21001)の構築時に発生するスタック オーバーフローの問題を修正します。
    -   外部結合[#20954](https://github.com/pingcap/tidb/pull/20954)でインデックス マージ ジョイン操作を実行すると返される予期しない結果を修正しました。
    -   結果が不定のトランザクションが失敗として扱われる場合がある問題を修正[#20925](https://github.com/pingcap/tidb/pull/20925)
    -   `EXPLAIN FOR CONNECTION`最後のクエリプランを表示できない問題を修正[#21315](https://github.com/pingcap/tidb/pull/21315)
    -   Read Committed 分離レベルのトランザクションで Index Merge が使用されると、結果が正しくない場合がある問題を修正します[#21253](https://github.com/pingcap/tidb/pull/21253)
    -   書き込み競合後のトランザクション再試行によって引き起こされる自動 ID 割り当ての失敗を修正[#21079](https://github.com/pingcap/tidb/pull/21079)
    -   `LOAD DATA` [#21074](https://github.com/pingcap/tidb/pull/21074)を使用して JSON データを TiDB に正しくインポートできない問題を修正
    -   新規追加した`Enum`型カラムのデフォルト値が正しくない問題を修正[#20998](https://github.com/pingcap/tidb/pull/20998)
    -   `adddate`関数で無効な文字が挿入される問題を修正[#21176](https://github.com/pingcap/tidb/pull/21176)
    -   状況によっては間違った`PointGet`プランが生成されると間違った結果が生じる問題を修正[#21244](https://github.com/pingcap/tidb/pull/21244)
    -   MySQL [#20888](https://github.com/pingcap/tidb/pull/20888)と互換性を持たせるために、 `ADD_DATE`関数での夏時間の変換を無視します。
    -   `varchar`または`char`の長さの制約を超える末尾のスペースを含む文字列を挿入できないバグを修正します[#21282](https://github.com/pingcap/tidb/pull/21282)
    -   `int`と`year` [#21283](https://github.com/pingcap/tidb/pull/21283)を比較するときに、整数が`[1, 69]`から`[2001, 2069]`または`[70, 99]`から`[1970, 1999]`に変換されないバグを修正
    -   `Double`型フィールド[#21272](https://github.com/pingcap/tidb/pull/21272)を計算するときに`sum()`関数の結果がオーバーフローすることによって引き起こされるpanicを修正しました。
    -   `DELETE`ユニークキー[#20705](https://github.com/pingcap/tidb/pull/20705)へのロックの追加に失敗するバグを修正
    -   スナップショットの読み取りがロック キャッシュにヒットするバグを修正[#21539](https://github.com/pingcap/tidb/pull/21539)
    -   存続期間の長いトランザクションで大量のデータを読み取った後の潜在的なメモリリークの問題を修正します[#21129](https://github.com/pingcap/tidb/pull/21129)
    -   サブクエリでテーブル エイリアスを省略すると構文エラー[#20367](https://github.com/pingcap/tidb/pull/20367)が返される問題を修正します。
    -   クエリ内の`IN`関数の引数が時刻型の場合、クエリが不正な結果を返すことがある問題を修正します[#21290](https://github.com/pingcap/tidb/issues/21290)

-   TiKV

    -   255 を超える列がある場合にコプロセッサーが間違った結果を返す可能性がある問題を修正します[#9131](https://github.com/tikv/tikv/pull/9131)
    -   ネットワーク パーティション[#9108](https://github.com/tikv/tikv/pull/9108)でリージョンマージによりデータ損失が発生する可能性がある問題を修正
    -   `latin1`文字セット[#9082](https://github.com/tikv/tikv/pull/9082)を使用する場合、 `ANALYZE`ステートメントでpanicが発生する可能性がある問題を修正します。
    -   数値型を時間型[#9031](https://github.com/tikv/tikv/pull/9031)に変換するときに返される間違った結果を修正しました。
    -   透過的データ暗号化 (TDE) が有効になっている場合、 TiDB Lightning がインポーター バックエンドまたはローカル バックエンドを使用して TiKV に SST ファイルを取り込むことができないバグを修正します[#8995](https://github.com/tikv/tikv/pull/8995)
    -   無効な`advertise-status-addr`値を修正 ( `0.0.0.0` ) [#9036](https://github.com/tikv/tikv/pull/9036)
    -   コミットされたトランザクションでこのキーがロックされ削除された場合、キーが存在することを示すエラーが返される問題を修正します[#8930](https://github.com/tikv/tikv/pull/8930)
    -   RocksDB キャッシュ マッピング エラーによりデータ破損が発生する問題を修正[#9029](https://github.com/tikv/tikv/pull/9029)
    -   リーダーが転送された後、Follower Readが古いデータを返す場合があるバグを修正[#9240](https://github.com/tikv/tikv/pull/9240)
    -   悲観的ロック[#9282](https://github.com/tikv/tikv/pull/9282)で古い値が読み込まれる可能性がある問題を修正
    -   リーダー転送[#9240](https://github.com/tikv/tikv/pull/9240)後にレプリカの読み取りが古いデータを取得する可能性があるバグを修正
    -   プロファイリング[#9229](https://github.com/tikv/tikv/pull/9229)後に`SIGPROF`受信すると TiKV がクラッシュする問題を修正

-   PD

    -   配置ルールで指定したリーダーの役割が有効にならない場合がある問題を修正[#3208](https://github.com/pingcap/pd/pull/3208)
    -   `trace-region-flow`の値が予期せず`false` [#3120](https://github.com/pingcap/pd/pull/3120)に設定される問題を修正
    -   無限の Time To Live (TTL) を持つサービス セーフポイントが機能しないバグを修正[#3143](https://github.com/pingcap/pd/pull/3143)

-   TiDB ダッシュボード

    -   中国語での時間の表示の問題を修正[#755](https://github.com/pingcap/tidb-dashboard/pull/755)
    -   ブラウザ互換性通知が機能しないバグを修正[#776](https://github.com/pingcap/tidb-dashboard/pull/776)
    -   一部のシナリオ[#793](https://github.com/pingcap/tidb-dashboard/pull/793)でトランザクション`start_ts`が正しく表示されない問題を修正
    -   一部の SQL テキストの形式が正しくない問題を修正[#805](https://github.com/pingcap/tidb-dashboard/pull/805)

-   TiFlash

    -   `INFORMATION_SCHEMA.CLUSTER_HARDWARE`に使用されていないディスクの情報が含まれる可能性がある問題を修正
    -   デルタキャッシュのメモリ使用量の見積もりが実際の使用量よりも小さい問題を修正
    -   スレッド情報統計によるメモリリークを修正

-   ツール

    -   バックアップと復元 (BR)

        -   S3 シークレット アクセス キーの特殊文字によって引き起こされる障害を修正[#617](https://github.com/pingcap/br/pull/617)

    -   TiCDC

        -   所有者のキャンペーン キーを削除すると複数の所有者が存在する可能性がある問題を修正[#1104](https://github.com/pingcap/tiflow/pull/1104)
        -   TiKV ノードがクラッシュしたとき、またはクラッシュから回復したときに、TiCDC がデータのレプリケーションを続行できない可能性があるバグを修正しました。このバグは v4.0.8 にのみ存在します。 [#1198](https://github.com/pingcap/tiflow/pull/1198)
        -   テーブルが初期化される前にメタデータが繰り返し etcd にフラッシュされる問題を修正します[#1191](https://github.com/pingcap/tiflow/pull/1191)
        -   スキーマstorageがTiDB テーブル[#1114](https://github.com/pingcap/tiflow/pull/1114)をキャッシュするときに、初期の GC または更新`TableInfo`のレイテンシーによって引き起こされるレプリケーションの中断の問題を修正します。
        -   DDL 操作が頻繁に行われる場合、スキーマstorageのメモリ消費量が多すぎる問題を修正します[#1127](https://github.com/pingcap/tiflow/pull/1127)
        -   チェンジフィードが一時停止または停止したときの goroutine リークを修正[#1075](https://github.com/pingcap/tiflow/pull/1075)
        -   Kafka プロデューサーの最大再試行タイムアウトを 600 秒に増やし、ダウンストリーム Kafka [#1118](https://github.com/pingcap/tiflow/pull/1118)のサービスまたはネットワーク ジッターによって引き起こされるレプリケーションの中断を防ぎます。
        -   Kafkaのバッチサイズが反映されないバグを修正[#1112](https://github.com/pingcap/tiflow/pull/1112)
        -   TiCDC と PD の間のネットワークにジッターがあり、一時停止された変更フィードが同時に再開されている場合、一部のテーブルの行変更が失われる可能性があるバグを修正します[#1213](https://github.com/pingcap/tiflow/pull/1213)
        -   TiCDC と PD 間のネットワークが安定していない場合、TiCDC プロセスが終了する可能性があるバグを修正[#1218](https://github.com/pingcap/tiflow/pull/1218)
        -   TiCDC でシングルトン PD クライアントを使用し、TiCDC が誤って PD クライアントを閉じてレプリケーション ブロック[#1217](https://github.com/pingcap/tiflow/pull/1217)を引き起こすバグを修正しました。
        -   TiCDC 所有者が etcd 監視クライアント[#1224](https://github.com/pingcap/tiflow/pull/1224)でメモリを過剰に消費する可能性があるバグを修正

    -   Dumpling

        -   MySQL データベースサーバーへの接続が閉じられたときにDumpling がブロックされる可能性がある問題を修正します[#190](https://github.com/pingcap/dumpling/pull/190)

    -   TiDB Lightning

        -   キーが間違ったフィールド情報を使用してエンコードされる問題を修正[#437](https://github.com/pingcap/tidb-lightning/pull/437)
        -   GC ライフタイム TTL が有効にならない問題を修正[#448](https://github.com/pingcap/tidb-lightning/pull/448)
        -   ローカル バックエンド モード[#484](https://github.com/pingcap/tidb-lightning/pull/484)で実行中のTiDB Lightning を手動で停止するとpanicが発生する問題を修正します。
