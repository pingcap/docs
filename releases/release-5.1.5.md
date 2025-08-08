---
title: TiDB 5.1.5 Release Notes
summary: TiDB 5.1.5は2022年12月28日にリリースされました。このリリースには、TiDB、TiKV、PD、 TiFlash、および各種ツールの互換性に関する変更と多数のバグ修正が含まれています。バグ修正では、パニック、誤った結果、不適切な動作などの問題が修正されています。また、データ損失、メモリ使用量、メトリクスの誤りに関する問題も修正されています。
---

# TiDB 5.1.5 リリースノート {#tidb-5-1-5-release-notes}

発売日：2022年12月28日

TiDB バージョン: 5.1.5

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v5.1/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v5.1/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   PD

    -   デフォルトでSwaggerサーバーのコンパイルを無効にする[＃4932](https://github.com/tikv/pd/issues/4932)

## バグ修正 {#bug-fixes}

-   TiDB

    -   ウィンドウ関数がエラーを報告する代わりに TiDB をpanic問題を修正[＃30326](https://github.com/pingcap/tidb/issues/30326)
    -   TiFlash [＃37254](https://github.com/pingcap/tidb/issues/37254)のパーティションテーブルでダイナミックモードを有効にしたときに発生する誤った結果を修正しました
    -   符号なし`BIGINT`引数[＃30101](https://github.com/pingcap/tidb/issues/30101)を渡したときに`GREATEST`と`LEAST`間違った結果が返される問題を修正
    -   `left join` [＃31321](https://github.com/pingcap/tidb/issues/31321)を使用して複数のテーブルのデータを削除した場合の誤った結果を修正
    -   TiDBの`concat(ifnull(time(3)))`の結果がMySQL [＃29498](https://github.com/pingcap/tidb/issues/29498)の結果と異なる問題を修正
    -   `cast(integer as char) union string`を含む SQL 文が間違った結果を返す問題を修正[＃29513](https://github.com/pingcap/tidb/issues/29513)
    -   `LIMIT` [＃35638](https://github.com/pingcap/tidb/issues/35638)と併用すると`INL_HASH_JOIN`ハングアップする可能性がある問題を修正
    -   リージョンが空のデータ[＃30923](https://github.com/pingcap/tidb/issues/30923)を返すときに発生する間違った結果`ANY_VALUE`修正します
    -   innerWorkerpanic[＃31494](https://github.com/pingcap/tidb/issues/31494)によって発生するインデックス結合の誤った結果を修正しました
    -   JSON型の列が`CHAR`型の列[＃29401](https://github.com/pingcap/tidb/issues/29401)に結合するとSQL操作がキャンセルされる問題を修正
    -   TiDBのバックグラウンドHTTPサービスが正常に終了せず、クラスターが異常な状態になる可能性がある問題を修正しました[＃30571](https://github.com/pingcap/tidb/issues/30571)
    -   同時列型変更によりスキーマとデータの間に不整合が発生する問題を修正[＃31048](https://github.com/pingcap/tidb/issues/31048)
    -   `KILL TIDB`アイドル接続時にすぐに効果を発揮できない問題を修正[＃24031](https://github.com/pingcap/tidb/issues/24031)
    -   セッション変数を設定すると`tidb_snapshot`が動作しなくなるバグを修正[＃35515](https://github.com/pingcap/tidb/issues/35515)
    -   リージョンがマージされたときにリージョンキャッシュが時間内にクリーンアップされない問題を修正[＃37141](https://github.com/pingcap/tidb/issues/37141)
    -   KVクライアント[＃33773](https://github.com/pingcap/tidb/issues/33773)の接続配列競合によって発生するpanic問題を修正
    -   TiDB Binlogが有効な場合、 `ALTER SEQUENCE`文を実行するとメタデータ バージョンが間違って発生し、 Drainerが終了する可能性がある問題を修正しました[＃36276](https://github.com/pingcap/tidb/issues/36276)
    -   ステートメントサマリーテーブルをクエリするときに TiDB がpanic可能性があるバグを修正[＃35340](https://github.com/pingcap/tidb/issues/35340)
    -   TiFlash が空の範囲を持つテーブルの読み取りをまだサポートしていないにもかかわらず、 TiFlashを使用して空の範囲を持つテーブルをスキャンすると TiDB が間違った結果を取得する問題を修正しました[＃33083](https://github.com/pingcap/tidb/issues/33083)
    -   TiFlash [＃29952](https://github.com/pingcap/tidb/issues/29952)からクエリされたときに`avg()`関数が`ERROR 1105 (HY000): other error for mpp stream: Could not convert to the target type - -value is out of range.`返す問題を修正しました
    -   `HashJoinExec` [＃30289](https://github.com/pingcap/tidb/issues/30289)を使用すると`ERROR 1105 (HY000): close of nil channel`が返される問題を修正
    -   論理演算をクエリするときに TiKV とTiFlash が異なる結果を返す問題を修正[＃37258](https://github.com/pingcap/tidb/issues/37258)
    -   特定のシナリオで`EXECUTE`文が予期しないエラーをスローする可能性がある問題を修正しました[＃37187](https://github.com/pingcap/tidb/issues/37187)
    -   `tidb_opt_agg_push_down`と`tidb_enforce_mpp`有効になっているときに発生するプランナーの誤った動作を修正[＃34465](https://github.com/pingcap/tidb/issues/34465)
    -   `SHOW COLUMNS`文[＃36496](https://github.com/pingcap/tidb/issues/36496)を実行するときに TiDB がコプロセッサ要求を送信する可能性があるバグを修正しました。
    -   `enable-table-lock`フラグが有効になっていない場合に`lock tables`と`unlock tables`警告を追加する[＃28967](https://github.com/pingcap/tidb/issues/28967)
    -   範囲パーティションが複数の`MAXVALUE`のパーティション[＃36329](https://github.com/pingcap/tidb/issues/36329)許可する問題を修正

-   TiKV

    -   `DATETIME`値に小数点と`Z` [＃12739](https://github.com/tikv/tikv/issues/12739)が含まれている場合に発生する時間解析エラーの問題を修正しました
    -   レプリカ読み取りが線形化可能性[＃12109](https://github.com/tikv/tikv/issues/12109)に違反する可能性があるバグを修正しました
    -   Raftstoreがビジー状態の場合にリージョンが重複する可能性があるバグを修正[＃13160](https://github.com/tikv/tikv/issues/13160)
    -   スナップショットの適用が中止されたときに発生する TiKVpanic問題を修正しました[＃11618](https://github.com/tikv/tikv/issues/11618)
    -   TiKV が 2 年以上実行されている場合にpanic可能性があるバグを修正[＃11940](https://github.com/tikv/tikv/issues/11940)
    -   リージョンマージプロセス[＃12663](https://github.com/tikv/tikv/issues/12663)でソースピアがスナップショットによってログをキャッチアップするときに発生する可能性のpanic問題を修正しました。
    -   空の文字列の型変換を実行するときに TiKV がパニックになる問題を修正[＃12673](https://github.com/tikv/tikv/issues/12673)
    -   古いメッセージによって TiKV がpanicを起こすバグを修正[＃12023](https://github.com/tikv/tikv/issues/12023)
    -   ピアが同時に分割され、破棄されたときに発生する可能性のあるpanic問題を修正しました[＃12825](https://github.com/tikv/tikv/issues/12825)
    -   リージョン[＃12048](https://github.com/tikv/tikv/issues/12048)をマージする際に、ターゲットピアが初期化されずに破棄されたピアに置き換えられたときに発生するTiKVpanic問題を修正しました。
    -   Follower Read [＃12478](https://github.com/tikv/tikv/issues/12478)使用時に TiKV が`invalid store ID 0`エラーを報告する問題を修正しました
    -   非同期コミットが有効な場合の悲観的トランザクションにおけるコミットレコードの重複の可能性を修正[＃12615](https://github.com/tikv/tikv/issues/12615)
    -   1つのピアが到達不能になった後にRaftstoreが過剰なメッセージをブロードキャストするのを避けるために`unreachable_backoff`項目の設定をサポートします[＃13054](https://github.com/tikv/tikv/issues/13054)
    -   ネットワークが貧弱な場合、正常にコミットされた楽観的トランザクションが`Write Conflict`エラーを報告する可能性がある問題を修正しました[＃34066](https://github.com/pingcap/tidb/issues/34066)
    -   ダッシュボード[＃13086](https://github.com/tikv/tikv/issues/13086)の`Unified Read Pool CPU`の間違った表現を修正

-   PD

    -   PDリーダー移転後に削除した墓石ストアが再び表示される問題を修正[＃4941](https://github.com/tikv/pd/issues/4941)
    -   PDリーダー移行後すぐにスケジュールを開始できない問題を修正[＃4769](https://github.com/tikv/pd/issues/4769)
    -   `not leader` [＃4797](https://github.com/tikv/pd/issues/4797)の間違ったステータスコードを修正
    -   PDがダッシュボードプロキシリクエストを正しく処理できない問題を修正[＃5321](https://github.com/tikv/pd/issues/5321)
    -   いくつかのコーナーケースにおけるTSOフォールバックのバグを修正[＃4884](https://github.com/tikv/pd/issues/4884)
    -   特定のシナリオでTiFlash学習者レプリカが作成されない可能性がある問題を修正[＃5401](https://github.com/tikv/pd/issues/5401)
    -   ラベル分布にメトリクス[＃4825](https://github.com/tikv/pd/issues/4825)の残余ラベルがある問題を修正
    -   大容量（例えば2T）のストアが存在する場合、完全に割り当てられた小さなストアを検出できず、バランス演算子が生成されない問題を修正しました[＃4805](https://github.com/tikv/pd/issues/4805)
    -   `SchedulerMaxWaitingOperator` `1` [＃4946](https://github.com/tikv/pd/issues/4946)に設定するとスケジューラが動作しない問題を修正しました

-   TiFlash

    -   文字列を日付時刻[＃3556](https://github.com/pingcap/tiflash/issues/3556)にキャストする際の誤った`microsecond`修正
    -   TLS が有効になっているときに発生するpanic問題を修正[＃4196](https://github.com/pingcap/tiflash/issues/4196)
    -   並列集約[＃5356](https://github.com/pingcap/tiflash/issues/5356)エラーによりTiFlashがクラッシュする可能性があるバグを修正
    -   エラーが発生した場合に`JOIN`を含むクエリがハングする可能性がある問題を修正しました[＃4195](https://github.com/pingcap/tiflash/issues/4195)
    -   関数`OR`間違った結果を返す問題を修正[＃5849](https://github.com/pingcap/tiflash/issues/5849)
    -   無効なstorageディレクトリ設定が予期しない動作を引き起こすバグを修正[＃4093](https://github.com/pingcap/tiflash/issues/4093)
    -   多数のINSERTおよびDELETE操作後に発生する可能性のあるデータの不整合を修正[＃4956](https://github.com/pingcap/tiflash/issues/4956)
    -   どの領域範囲にも一致しないデータがTiFlashノード[＃4414](https://github.com/pingcap/tiflash/issues/4414)に残るバグを修正しました
    -   読み取り負荷が高い状態で列を追加した後に発生する可能性のあるクエリエラーを修正[＃3967](https://github.com/pingcap/tiflash/issues/3967)
    -   `commit state jump backward`エラー[＃2576](https://github.com/pingcap/tiflash/issues/2576)による繰り返しのクラッシュを修正
    -   削除操作を多数含むテーブルをクエリするときに発生する可能性のあるエラーを修正[＃4747](https://github.com/pingcap/tiflash/issues/4747)
    -   日付形式が`''`無効な区切り文字として認識する問題を修正[＃4036](https://github.com/pingcap/tiflash/issues/4036)
    -   `DATETIME`を`DECIMAL` [＃4151](https://github.com/pingcap/tiflash/issues/4151)にキャストするときに発生する誤った結果を修正
    -   一部の例外が適切に処理されないバグを修正[＃4101](https://github.com/pingcap/tiflash/issues/4101)
    -   `Prepare Merge`ラフトストアのメタデータが破損し、 TiFlashが再起動する可能性がある問題を修正[＃3435](https://github.com/pingcap/tiflash/issues/3435)
    -   ランダムな gRPC キープアライブタイムアウトにより MPP クエリが失敗する可能性があるバグを修正[＃4662](https://github.com/pingcap/tiflash/issues/4662)
    -   複数値式[＃4016](https://github.com/pingcap/tiflash/issues/4016)で`IN`の結果が正しくない問題を修正
    -   MPP タスクがスレッドを永久にリークする可能性があるバグを修正[＃4238](https://github.com/pingcap/tiflash/issues/4238)
    -   期限切れのデータがゆっくりとリサイクルされる問題を修正[＃4146](https://github.com/pingcap/tiflash/issues/4146)
    -   `FLOAT`を`DECIMAL` [＃3998](https://github.com/pingcap/tiflash/issues/3998)にキャストするときに発生するオーバーフローを修正
    -   引数の型がUInt8 [＃6127](https://github.com/pingcap/tiflash/issues/6127)場合に論理演算子が間違った結果を返す問題を修正しました
    -   空の文字列[＃2705](https://github.com/pingcap/tiflash/issues/2705)で`json_length`呼び出す場合に発生する可能性のある`index out of bounds`エラーを修正
    -   コーナーケース[＃4512](https://github.com/pingcap/tiflash/issues/4512)での誤った小数比較結果を修正
    -   `NOT NULL`列を追加したときに報告された修正`TiFlash_schema_error` [＃4596](https://github.com/pingcap/tiflash/issues/4596)
    -   整数のデフォルト値として`0.0`使用されている場合 (例: `` `i` int(11) NOT NULL DEFAULT '0.0'`` [＃3157](https://github.com/pingcap/tiflash/issues/3157) 、 TiFlashブートストラップが失敗する問題を修正しました。

-   ツール

    -   TiDBBinlog

        -   `compressor` `zip` [＃1152](https://github.com/pingcap/tidb-binlog/issues/1152)に設定されている場合に、 Drainer がPumpにリクエストを正しく送信できない問題を修正しました。

    -   バックアップと復元 (BR)

        -   システムテーブルを同時にバックアップするとテーブル名の更新に失敗するため、システムテーブルを復元できない問題を修正しました[＃29710](https://github.com/pingcap/tidb/issues/29710)

    -   TiCDC

        -   特別な増分スキャンシナリオで発生するデータ損失を修正[＃5468](https://github.com/pingcap/tiflow/issues/5468)
        -   ソーターメトリック[＃5690](https://github.com/pingcap/tiflow/issues/5690)がない問題を修正
        -   DDLスキーマのバッファリング方法を最適化することで過剰なメモリ使用量を修正[＃1386](https://github.com/pingcap/tiflow/issues/1386)
