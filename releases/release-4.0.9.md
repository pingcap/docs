---
title: TiDB 4.0.9 Release Notes
---

# TiDB 4.0.9 リリースノート {#tidb-4-0-9-release-notes}

発売日：2020年12月21日

TiDB バージョン: 4.0.9

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   `enable-streaming`構成アイテム[#21055](https://github.com/pingcap/tidb/pull/21055)を非推奨にします

-   TiKV

    -   保存時の暗号化が有効になっている場合、I/O とミューテックスの競合を減らします。この変更は下位互換性がありません。ユーザーがクラスターを v4.0.9 より前のバージョンにダウングレードする必要がある場合は、ダウングレードの前に`security.encryption.enable-file-dictionary-log`を無効にし、TiKV を再起動する必要があります。 [#9195](https://github.com/tikv/tikv/pull/9195)

## 新機能 {#new-features}

-   TiFlash

    -   複数のディスクへのstorageエンジンの最新データの保存をサポート (実験的)

-   TiDB ダッシュボード

    -   **SQL ステートメント**ページ[#749](https://github.com/pingcap/tidb-dashboard/pull/749)のすべてのフィールドによる表示と並べ替えをサポートします。
    -   トポロジ グラフのズームとパンをサポート[#772](https://github.com/pingcap/tidb-dashboard/pull/772)
    -   **[SQL ステートメント]**ページと<strong>[スロー クエリ]</strong>ページでのディスク使用情報の表示のサポート[#777](https://github.com/pingcap/tidb-dashboard/pull/777)
    -   **SQL ステートメント**および<strong>スロー クエリ</strong>ページでのリスト データのエクスポートのサポート[#778](https://github.com/pingcap/tidb-dashboard/pull/778)
    -   Prometheus アドレスのカスタマイズをサポート[#808](https://github.com/pingcap/tidb-dashboard/pull/808)
    -   クラスター統計のページを追加する[#815](https://github.com/pingcap/tidb-dashboard/pull/815)
    -   **スロー クエリ**の詳細に時間関連のフィールドを追加します[#810](https://github.com/pingcap/tidb-dashboard/pull/810)

## 改良点 {#improvements}

-   TiDB

    -   等しい条件を他の条件に変換するときは、ヒューリスティックな方法で (インデックス) マージ結合を回避します[#21146](https://github.com/pingcap/tidb/pull/21146)
    -   ユーザー変数の種類を区別する[#21107](https://github.com/pingcap/tidb/pull/21107)
    -   構成ファイルで`GOGC`変数の設定をサポート[#20922](https://github.com/pingcap/tidb/pull/20922)
    -   ダンプされたバイナリ時間 ( `Timestamp`と`Datetime` ) を MySQL [#21135](https://github.com/pingcap/tidb/pull/21135)との互換性を高める
    -   `LOCK IN SHARE MODE`構文[#21005](https://github.com/pingcap/tidb/pull/21005)を使用するステートメントのエラー メッセージを提供する
    -   ショートカット可能な式で定数を折りたたむときに不要な警告やエラーを出力しないようにする[#21040](https://github.com/pingcap/tidb/pull/21040)
    -   `LOAD DATA`ステートメントの準備時にエラーを発生させる[#21199](https://github.com/pingcap/tidb/pull/21199)
    -   整数列タイプを変更する場合、整数のゼロ フィル サイズの属性を無視する[#20986](https://github.com/pingcap/tidb/pull/20986)
    -   `EXPLAIN ANALYZE` [#21066](https://github.com/pingcap/tidb/pull/21066)の結果に DML ステートメントのエグゼキュータ関連の実行時情報を追加します
    -   単一の SQL ステートメントで主キーの複数の更新を許可しない[#21113](https://github.com/pingcap/tidb/pull/21113)
    -   接続アイドル時間のモニタリング メトリックを追加します[#21301](https://github.com/pingcap/tidb/pull/21301)
    -   `runtime/trace`ツールの実行中にスローログを一時的に有効にする[#20578](https://github.com/pingcap/tidb/pull/20578)

-   TiKV

    -   `split`コマンドのソースをトレースするタグを追加します[#8936](https://github.com/tikv/tikv/pull/8936)
    -   `pessimistic-txn.pipelined`構成の動的変更のサポート[#9100](https://github.com/tikv/tikv/pull/9100)
    -   バックアップと復元およびTiDB Lightning [#9098](https://github.com/tikv/tikv/pull/9098)を実行するときのパフォーマンスへの影響を軽減します
    -   取り込み SST エラーのモニタリング メトリックを追加します[#9096](https://github.com/tikv/tikv/pull/9096)
    -   一部のピアがまだログをレプリケートする必要がある場合に、リーダーが休止状態にならないようにする[#9093](https://github.com/tikv/tikv/pull/9093)
    -   パイプライン化された悲観的ロックの成功率を高める[#9086](https://github.com/tikv/tikv/pull/9086)
    -   `apply-max-batch-size`と`store-max-batch-size`のデフォルト値を`1024` [#9020](https://github.com/tikv/tikv/pull/9020)に変更します
    -   `max-background-flushes`構成アイテム[#8947](https://github.com/tikv/tikv/pull/8947)を追加
    -   パフォーマンスを向上させるためにデフォルトで`force-consistency-checks`無効にします[#9029](https://github.com/tikv/tikv/pull/9029)
    -   リージョンサイズのクエリを`pd heartbeat worker`から`split check worker` [#9185](https://github.com/tikv/tikv/pull/9185)にオフロードします

-   PD

    -   TiKV ストアが`Tombstone`になったときに TiKV クラスターのバージョンを確認します。これにより、ユーザーはダウングレードまたはアップグレードのプロセス中に互換性のない機能を有効にすることができなくなります[#3213](https://github.com/pingcap/pd/pull/3213)
    -   下位バージョンの TiKV ストアが`Tombstone`から`Up`に戻ることを許可しない[#3206](https://github.com/pingcap/pd/pull/3206)

-   TiDB ダッシュボード

    -   SQL文[#775](https://github.com/pingcap/tidb-dashboard/pull/775)の「展開」をクリックすると展開し続ける
    -   **SQL ステートメント**と<strong>スロー クエリ</strong>の詳細ページを新しいウィンドウで開く[#816](https://github.com/pingcap/tidb-dashboard/pull/816)
    -   **スロー クエリの**詳細の時間関連フィールドの説明を改善する[#817](https://github.com/pingcap/tidb-dashboard/pull/817)
    -   詳細なエラー メッセージを表示する[#794](https://github.com/pingcap/tidb-dashboard/pull/794)

-   TiFlash

    -   レプリカ読み取りのレイテンシーを短縮する
    -   TiFlash のエラー メッセージを改善する
    -   データ量が膨大な場合にキャッシュ データのメモリ使用量を制限する
    -   処理中のコプロセッサー・タスク数のモニター・メトリックを追加します

-   ツール

    -   バックアップと復元 (BR)

        -   コマンド ラインであいまいな`--checksum false`引数を許可しないようにします。これにより、チェックサムが正しく無効になりません。 `--checksum=false`だけ受け付けます。 [#588](https://github.com/pingcap/br/pull/588)
        -   BR が誤って存在した後に PD が元の構成を回復できるように、 [#596](https://github.com/pingcap/br/pull/596)的に PD 構成を変更することをサポートします。
        -   復元後のテーブル分析のサポート[#622](https://github.com/pingcap/br/pull/622)
        -   `read index not ready`と`proposal in merging mode`エラーの再試行[#626](https://github.com/pingcap/br/pull/626)

    -   TiCDC

        -   TiKV の Hibernate リージョン機能を有効にするためのアラートを追加します[#1120](https://github.com/pingcap/tiflow/pull/1120)
        -   スキーマstorageのメモリ使用量を減らす[#1127](https://github.com/pingcap/tiflow/pull/1127)
        -   インクリメンタルスキャンのデータサイズが大きい場合にレプリケーションを高速化するユニファイドソーターの機能を追加 (実験的) [#1122](https://github.com/pingcap/tiflow/pull/1122)
        -   TiCDC Open Protocol メッセージでの最大メッセージ サイズと最大メッセージ バッチの設定をサポート (Kafka シンクのみ) [#1079](https://github.com/pingcap/tiflow/pull/1079)

    -   Dumpling

        -   失敗したチャンクでデータのダンプを再試行します[#182](https://github.com/pingcap/dumpling/pull/182)
        -   `-F`と`-r`の両方の引数の同時設定をサポート[#177](https://github.com/pingcap/dumpling/pull/177)
        -   デフォルトで`--filter`のシステム データベースを除外する[#194](https://github.com/pingcap/dumpling/pull/194)
        -   `--transactional-consistency`パラメーターをサポートし、再試行中の MySQL 接続の再構築をサポートします[#199](https://github.com/pingcap/dumpling/pull/199)
        -   Dumplingで使用される圧縮アルゴリズムを指定する`-c,--compress`パラメーターの使用をサポートします。空の文字列は、圧縮がないことを意味します。 [#202](https://github.com/pingcap/dumpling/pull/202)

    -   TiDB Lightning

        -   デフォルトですべてのシステム スキーマを除外する[#459](https://github.com/pingcap/tidb-lightning/pull/459)
        -   Local-backend または Importer-backend [#457](https://github.com/pingcap/tidb-lightning/pull/457)の自動ランダム主キーのデフォルト値の設定をサポート
        -   範囲プロパティを使用して、ローカル バックエンド[#422](https://github.com/pingcap/tidb-lightning/pull/422)で範囲分割をより正確にします
        -   `tikv-importer.region-split-size` 、 `mydumper.read-block-size` 、 `mydumper.batch-size` 、および`mydumper.max-region-size` [#471](https://github.com/pingcap/tidb-lightning/pull/471)で人間が読める形式 (「2.5 GiB」など) をサポートする

    -   TiDBBinlog

        -   アップストリーム PD がダウンしている場合、またはダウンストリームへの DDL または DML ステートメントの適用が失敗した場合は、 [#1012](https://github.com/pingcap/tidb-binlog/pull/1012)以外のコードでDrainerプロセスを終了します。

## バグの修正 {#bug-fixes}

-   TiDB

    -   `OR`条件[#21287](https://github.com/pingcap/tidb/pull/21287)でプレフィックス インデックスを使用すると、誤った結果が得られる問題を修正します。
    -   自動再試行が有効になっているときにpanicを引き起こす可能性があるバグを修正します[#21285](https://github.com/pingcap/tidb/pull/21285)
    -   列タイプ[#21273](https://github.com/pingcap/tidb/pull/21273)によるパーティション定義のチェック時に発生するバグを修正
    -   パーティション式の値の型がパーティション列の型[#21136](https://github.com/pingcap/tidb/pull/21136)と一致しない不具合を修正
    -   ハッシュ型パーティションがパーティション名が一意かどうかをチェックしないバグを修正[#21257](https://github.com/pingcap/tidb/pull/21257)
    -   非`INT`型の値をハッシュパーティションテーブルに挿入した後に返される間違った結果を修正します[#21238](https://github.com/pingcap/tidb/pull/21238)
    -   場合によっては`INSERT`ステートメントでインデックス結合を使用すると予期しないエラーが発生する問題を修正[#21249](https://github.com/pingcap/tidb/pull/21249)
    -   `CASE WHEN`演算子の`BigInt`符号なし列値が`BigInt`付き値[#21236](https://github.com/pingcap/tidb/pull/21236)に誤って変換される問題を修正します
    -   インデックス ハッシュ結合とインデックス マージ結合が照合順序[#21219](https://github.com/pingcap/tidb/pull/21219)を考慮しないバグを修正
    -   パーティションテーブルが`CREATE TABLE`と`SELECT`構文で照合順序を考慮しないバグを修正[#21181](https://github.com/pingcap/tidb/pull/21181)
    -   `slow_query`のクエリ結果が一部の行を欠落する可能性がある問題を修正します[#21211](https://github.com/pingcap/tidb/pull/21211)
    -   データベース名が純粋な下位表現でない場合、データが正しく削除されない可能性が`DELETE`問題を修正[#21206](https://github.com/pingcap/tidb/pull/21206)
    -   DML 操作後にスキーマの変更を引き起こすバグを修正します[#21050](https://github.com/pingcap/tidb/pull/21050)
    -   結合[#21021](https://github.com/pingcap/tidb/pull/21021)を使用すると、結合された列をクエリできないというバグを修正します。
    -   一部の準結合クエリの誤った結果を修正する[#21019](https://github.com/pingcap/tidb/pull/21019)
    -   `UPDATE`文[#21002](https://github.com/pingcap/tidb/pull/21002)でテーブルロックが効かない問題を修正
    -   再帰ビュー[#21001](https://github.com/pingcap/tidb/pull/21001)のビルド時に発生するスタック オーバーフローの問題を修正します。
    -   外部結合[#20954](https://github.com/pingcap/tidb/pull/20954)でインデックス マージ結合操作を実行したときに返される予期しない結果を修正します。
    -   結果が未定のトランザクションが失敗として扱われる場合がある問題を修正します[#20925](https://github.com/pingcap/tidb/pull/20925)
    -   `EXPLAIN FOR CONNECTION`最後のクエリ プランを表示できない問題を修正します[#21315](https://github.com/pingcap/tidb/pull/21315)
    -   Read Committed 分離レベルのトランザクションで Index Merge を使用すると、結果が正しくない可能性がある問題を修正します[#21253](https://github.com/pingcap/tidb/pull/21253)
    -   書き込み競合後のトランザクションの再試行によって引き起こされる自動 ID 割り当ての失敗を修正します[#21079](https://github.com/pingcap/tidb/pull/21079)
    -   `LOAD DATA` [#21074](https://github.com/pingcap/tidb/pull/21074)を使用して JSON データを TiDB に正しくインポートできない問題を修正
    -   新しく追加された`Enum`型の列のデフォルト値が正しくない問題を修正します[#20998](https://github.com/pingcap/tidb/pull/20998)
    -   `adddate`関数が無効な文字を挿入する問題を修正[#21176](https://github.com/pingcap/tidb/pull/21176)
    -   一部の状況で間違った`PointGet`プランが生成され、間違った結果が生じる問題を修正[#21244](https://github.com/pingcap/tidb/pull/21244)
    -   MySQL [#20888](https://github.com/pingcap/tidb/pull/20888)と互換性を持たせるために、 `ADD_DATE`関数で夏時間の変換を無視します。
    -   `varchar`または`char`の長さ制限[#21282](https://github.com/pingcap/tidb/pull/21282)を超える末尾にスペースがある文字列を挿入できないバグを修正します。
    -   `int`と`year` [#21283](https://github.com/pingcap/tidb/pull/21283)を比較するとき、整数を`[1, 69]`から`[2001, 2069]`または`[70, 99]`から`[1970, 1999]`に変換しないバグを修正します
    -   `Double`型フィールド[#21272](https://github.com/pingcap/tidb/pull/21272)の計算時に`sum()`関数の結果がオーバーフローしてパニックが発生するpanicを修正
    -   `DELETE`ユニークキーのロック追加に失敗するバグを修正[#20705](https://github.com/pingcap/tidb/pull/20705)
    -   スナップショットの読み込みがロックキャッシュにヒットするバグを修正[#21539](https://github.com/pingcap/tidb/pull/21539)
    -   存続期間の長いトランザクションで大量のデータを読み取った後の潜在的なメモリリークの問題を修正します[#21129](https://github.com/pingcap/tidb/pull/21129)
    -   サブクエリでテーブル エイリアスを省略すると、構文エラー[#20367](https://github.com/pingcap/tidb/pull/20367)が返される問題を修正します。
    -   クエリの`IN`関数の引数が時間型の場合、クエリが間違った結果を返すことがある問題を修正します[#21290](https://github.com/pingcap/tidb/issues/21290)

-   TiKV

    -   列数が 255 を超えると、 コプロセッサー が間違った結果を返すことがある問題を修正します[#9131](https://github.com/tikv/tikv/pull/9131)
    -   リージョンマージがネットワーク パーティション[#9108](https://github.com/tikv/tikv/pull/9108)中にデータ損失を引き起こす可能性がある問題を修正します
    -   `latin1`文字セット[#9082](https://github.com/tikv/tikv/pull/9082)を使用すると、 `ANALYZE`ステートメントでpanicが発生する可能性がある問題を修正します。
    -   数値型を時間型に変換するときに返される間違った結果を修正します[#9031](https://github.com/tikv/tikv/pull/9031)
    -   透過的データ暗号化 (TDE) が有効になっている場合、 TiDB Lightning がImporter-backend または Local-backend を使用して SST ファイルを TiKV に取り込めないというバグを修正します[#8995](https://github.com/tikv/tikv/pull/8995)
    -   無効な`advertise-status-addr`値を修正 ( `0.0.0.0` ) [#9036](https://github.com/tikv/tikv/pull/9036)
    -   コミットされたトランザクションでキーがロックされ、削除されている場合、キーが存在することを示すエラーが返される問題を修正します[#8930](https://github.com/tikv/tikv/pull/8930)
    -   RocksDB キャッシュ マッピング エラーが原因でデータが破損する問題を修正します[#9029](https://github.com/tikv/tikv/pull/9029)
    -   リーダーが転送された後、 Follower Read が古いデータを返す可能性があるバグを修正します[#9240](https://github.com/tikv/tikv/pull/9240)
    -   悲観的ロック[#9282](https://github.com/tikv/tikv/pull/9282)で古い値が読み取られる可能性がある問題を修正します。
    -   リーダーの転送後にレプリカの読み取りで古いデータが取得される可能性があるバグを修正します[#9240](https://github.com/tikv/tikv/pull/9240)
    -   プロファイリング[#9229](https://github.com/tikv/tikv/pull/9229)後に`SIGPROF`受信すると TiKV がクラッシュする問題を修正

-   PD

    -   配置ルールで指定したリーダーの役割が有効にならない場合がある問題を修正[#3208](https://github.com/pingcap/pd/pull/3208)
    -   `trace-region-flow`の値が予期せず`false` [#3120](https://github.com/pingcap/pd/pull/3120)に設定される問題を修正
    -   Time To Live (TTL) が無限のサービスセーフポイントが機能しないバグを修正[#3143](https://github.com/pingcap/pd/pull/3143)

-   TiDB ダッシュボード

    -   中国語の時間表示の問題を修正[#755](https://github.com/pingcap/tidb-dashboard/pull/755)
    -   ブラウザの互換性通知が機能しない不具合を修正[#776](https://github.com/pingcap/tidb-dashboard/pull/776)
    -   トランザクション`start_ts`が一部のシナリオで正しく表示されない問題を修正[#793](https://github.com/pingcap/tidb-dashboard/pull/793)
    -   一部の SQL テキストの形式が正しくない問題を修正します[#805](https://github.com/pingcap/tidb-dashboard/pull/805)

-   TiFlash

    -   `INFORMATION_SCHEMA.CLUSTER_HARDWARE`に使用されていないディスクの情報が含まれる可能性がある問題を修正
    -   Delta Cache のメモリ使用量の見積もりが実際の使用量よりも少ない問題を修正
    -   スレッド情報の統計によって引き起こされるメモリリークを修正します。

-   ツール

    -   バックアップと復元 (BR)

        -   S3 シークレット アクセス キー[#617](https://github.com/pingcap/br/pull/617)の特殊文字による障害を修正します。

    -   TiCDC

        -   所有者のキャンペーン キーを削除すると複数の所有者が存在する可能性がある問題を修正します[#1104](https://github.com/pingcap/tiflow/pull/1104)
        -   TiKV ノードがクラッシュまたはクラッシュから回復したときに、TiCDC がデータの複製を続行できない可能性があるというバグを修正します。このバグは v4.0.8 にのみ存在します。 [#1198](https://github.com/pingcap/tiflow/pull/1198)
        -   テーブルが初期化される前に、メタデータが etcd に繰り返しフラッシュされる問題を修正します[#1191](https://github.com/pingcap/tiflow/pull/1191)
        -   スキーマstorageがTiDB テーブルをキャッシュしている場合に、初期の GC または更新のレイテンシー`TableInfo`によって引き起こされるレプリケーションの中断の問題を修正します[#1114](https://github.com/pingcap/tiflow/pull/1114)
        -   DDL 操作が頻繁に行われると、スキーマstorageがメモリを消費しすぎる問題を修正します[#1127](https://github.com/pingcap/tiflow/pull/1127)
        -   変更フィードが一時停止または停止されたときのゴルーチン リークを修正します[#1075](https://github.com/pingcap/tiflow/pull/1075)
        -   Kafka プロデューサーで最大再試行タイムアウトを 600 秒に増やして、ダウンストリーム Kafka [#1118](https://github.com/pingcap/tiflow/pull/1118)でのサービスまたはネットワーク ジッターによって引き起こされるレプリケーションの中断を防ぎます。
        -   Kafkaのバッチサイズが反映されないバグを修正[#1112](https://github.com/pingcap/tiflow/pull/1112)
        -   TiCDC と PD 間のネットワークにジッターがあり、 [#1213](https://github.com/pingcap/tiflow/pull/1213)停止中の変更フィードが同時に再開されると、一部のテーブルの行の変更が失われる可能性があるというバグを修正します。
        -   TiCDC と PD 間のネットワークが安定していない場合、TiCDC プロセスが終了する可能性があるバグを修正します[#1218](https://github.com/pingcap/tiflow/pull/1218)
        -   TiCDC でシングルトン PD クライアントを使用し、TiCDC が誤って PD クライアントを閉じてレプリケーション ブロック[#1217](https://github.com/pingcap/tiflow/pull/1217)が発生するバグを修正します。
        -   TiCDC 所有者が etcd ウォッチ クライアントでメモリを消費しすぎる可能性があるバグを修正します[#1224](https://github.com/pingcap/tiflow/pull/1224)

    -   Dumpling

        -   MySQL データベースサーバーへの接続が閉じられたときにDumpling がブロックされる可能性がある問題を修正します[#190](https://github.com/pingcap/dumpling/pull/190)

    -   TiDB Lightning

        -   間違ったフィールド情報を使用してキーがエンコードされる問題を修正します[#437](https://github.com/pingcap/tidb-lightning/pull/437)
        -   GC ライフタイム TTL が有効にならない問題を修正[#448](https://github.com/pingcap/tidb-lightning/pull/448)
        -   ローカル バックエンド モード[#484](https://github.com/pingcap/tidb-lightning/pull/484)で実行中のTiDB Lightning を手動で停止すると、panicが発生する問題を修正します。
