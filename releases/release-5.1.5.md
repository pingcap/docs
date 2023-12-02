---
title: TiDB 5.1.5 Release Notes
---

# TiDB 5.1.5 リリースノート {#tidb-5-1-5-release-notes}

発売日：2022年12月28日

TiDB バージョン: 5.1.5

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v5.1/quick-start-with-tidb) | [本番展開](https://docs.pingcap.com/tidb/v5.1/production-deployment-using-tiup) | [インストールパッケージ](https://www.pingcap.com/download/?version=v5.1.5#version-list)

## 互換性の変更 {#compatibility-changes}

-   PD

    -   Swaggerサーバーのコンパイルをデフォルトで無効にする[#4932](https://github.com/tikv/pd/issues/4932)

## バグの修正 {#bug-fixes}

-   TiDB

    -   ウィンドウ関数により TiDB がエラーを報告する代わりにpanicを引き起こす問題を修正します[#30326](https://github.com/pingcap/tidb/issues/30326)
    -   TiFlash [#37254](https://github.com/pingcap/tidb/issues/37254)のパーティション化されたテーブルで動的モードを有効にしたときに発生する間違った結果を修正しました。
    -   符号なし`BIGINT`引数[#30101](https://github.com/pingcap/tidb/issues/30101)を渡すときの`GREATEST`と`LEAST`の間違った結果を修正
    -   `left join` [#31321](https://github.com/pingcap/tidb/issues/31321)を使用して複数のテーブルのデータを削除した場合の誤った結果を修正
    -   TiDB の`concat(ifnull(time(3)))`の結果が MySQL [#29498](https://github.com/pingcap/tidb/issues/29498)の結果と異なる問題を修正
    -   `cast(integer as char) union string`を含む SQL ステートメントが間違った結果を返す問題を修正します[#29513](https://github.com/pingcap/tidb/issues/29513)
    -   `LIMIT` [#35638](https://github.com/pingcap/tidb/issues/35638)と一緒に使用すると`INL_HASH_JOIN`ハングする可能性がある問題を修正
    -   リージョンが空のデータを返したときに発生する間違った結果`ANY_VALUE`修正しました[#30923](https://github.com/pingcap/tidb/issues/30923)
    -   innerWorkerpanic[#31494](https://github.com/pingcap/tidb/issues/31494)によって引き起こされるインデックス結合の間違った結果を修正します。
    -   JSON 型の列が`CHAR`型の列[#29401](https://github.com/pingcap/tidb/issues/29401)に結合すると SQL 操作がキャンセルされる問題を修正
    -   TiDB のバックグラウンド HTTP サービスが正常に終了せず、クラスターが異常な状態になる場合がある問題を修正します[#30571](https://github.com/pingcap/tidb/issues/30571)
    -   同時に列の型を変更すると、スキーマとデータの間で不整合が発生する問題を修正します[#31048](https://github.com/pingcap/tidb/issues/31048)
    -   アイドル状態の接続で`KILL TIDB`がすぐに有効にならない問題を修正[#24031](https://github.com/pingcap/tidb/issues/24031)
    -   セッション変数を設定すると`tidb_snapshot`が機能しなくなるバグを修正[#35515](https://github.com/pingcap/tidb/issues/35515)
    -   リージョンがマージされるときにリージョンキャッシュが時間内にクリーンアップされない問題を修正します[#37141](https://github.com/pingcap/tidb/issues/37141)
    -   KV クライアント[#33773](https://github.com/pingcap/tidb/issues/33773)での接続アレイの競合によって引き起こされるpanicの問題を修正します。
    -   TiDB Binlogが有効な場合、 `ALTER SEQUENCE`ステートメントを実行するとメタデータ バージョンが間違ってDrainerが終了する可能性がある問題を修正します[#36276](https://github.com/pingcap/tidb/issues/36276)
    -   ステートメント概要テーブル[#35340](https://github.com/pingcap/tidb/issues/35340)をクエリするときに TiDB がpanicになる可能性があるバグを修正
    -   TiFlash は空の範囲を持つテーブルの読み取りをサポートしていませんが、 TiFlashを使用して空の範囲を持つテーブルをスキャンすると、 TiFlashが間違った結果を取得する問題を修正します[#33083](https://github.com/pingcap/tidb/issues/33083)
    -   TiFlash [#29952](https://github.com/pingcap/tidb/issues/29952)からクエリすると`avg()`関数が`ERROR 1105 (HY000): other error for mpp stream: Could not convert to the target type - -value is out of range.`を返す問題を修正
    -   `HashJoinExec` [#30289](https://github.com/pingcap/tidb/issues/30289)を使用すると`ERROR 1105 (HY000): close of nil channel`が返される問題を修正
    -   論理演算のクエリ時に TiKV とTiFlashが異なる結果を返す問題を修正[#37258](https://github.com/pingcap/tidb/issues/37258)
    -   特定のシナリオで`EXECUTE`ステートメントが予期しないエラーをスローする可能性がある問題を修正します[#37187](https://github.com/pingcap/tidb/issues/37187)
    -   `tidb_opt_agg_push_down`と`tidb_enforce_mpp`が有効になっている場合に発生するプランナーの誤った動作を修正します[#34465](https://github.com/pingcap/tidb/issues/34465)
    -   `SHOW COLUMNS`ステートメント[#36496](https://github.com/pingcap/tidb/issues/36496)の実行時に TiDB がコプロセッサ リクエストを送信する可能性があるバグを修正
    -   `enable-table-lock`フラグが有効になっていない場合の`lock tables`と`unlock tables`の警告を追加[#28967](https://github.com/pingcap/tidb/issues/28967)
    -   範囲パーティションで複数の`MAXVALUE`パーティションが許可される問題を修正します[#36329](https://github.com/pingcap/tidb/issues/36329)

-   TiKV

    -   `DATETIME`値に小数と`Z` [#12739](https://github.com/tikv/tikv/issues/12739)が含まれる場合に発生する時刻解析エラーの問題を修正します。
    -   レプリカの読み取りが線形化可能性[#12109](https://github.com/tikv/tikv/issues/12109)に違反する可能性があるバグを修正
    -   Raftstoreがビジー状態の場合にリージョンが重なる可能性があるバグを修正[#13160](https://github.com/tikv/tikv/issues/13160)
    -   スナップショットの適用が中止されるときに発生する TiKVpanicの問題を修正します[#11618](https://github.com/tikv/tikv/issues/11618)
    -   TiKV が 2 年以上実行されている場合にpanicになる可能性があるバグを修正[#11940](https://github.com/tikv/tikv/issues/11940)
    -   リージョンマージ プロセス[#12663](https://github.com/tikv/tikv/issues/12663)でソース ピアがスナップショットによってログを追いつくときに発生する可能性があるpanicの問題を修正します。
    -   空の文字列の型変換を実行すると TiKV がパニックになる問題を修正[#12673](https://github.com/tikv/tikv/issues/12673)
    -   古いメッセージによって TiKV がpanicになるバグを修正[#12023](https://github.com/tikv/tikv/issues/12023)
    -   ピアの分割と破棄が同時に行われるときに発生する可能性があるpanicの問題を修正します[#12825](https://github.com/tikv/tikv/issues/12825)
    -   リージョン[#12048](https://github.com/tikv/tikv/issues/12048)をマージするときに、ターゲット ピアが初期化されずに破棄されたピアに置き換えられるときに発生する TiKVpanicの問題を修正します。
    -   Follower Read [#12478](https://github.com/tikv/tikv/issues/12478)を使用すると TiKV が`invalid store ID 0`エラーを報告する問題を修正
    -   非同期コミットが有効になっている場合に、悲観的トランザクションで発生する可能性のある重複コミット レコードを修正します[#12615](https://github.com/tikv/tikv/issues/12615)
    -   1 つのピアが到達不能になった後にRaftstore が大量のメッセージをブロードキャストすることを避けるための`unreachable_backoff`項目の設定をサポートします[#13054](https://github.com/tikv/tikv/issues/13054)
    -   ネットワークが貧弱な場合、正常にコミットされた楽観的トランザクションが`Write Conflict`エラーを報告する可能性がある問題を修正します[#34066](https://github.com/pingcap/tidb/issues/34066)
    -   ダッシュボード[#13086](https://github.com/tikv/tikv/issues/13086)の`Unified Read Pool CPU`の誤った表現を修正

-   PD

    -   PDリーダー移転後、削除された墓石ストアが再び表示される問題を修正[#4941](https://github.com/tikv/pd/issues/4941)
    -   PDリーダー転送[#4769](https://github.com/tikv/pd/issues/4769)直後にスケジューリングが開始できない問題を修正
    -   `not leader` [#4797](https://github.com/tikv/pd/issues/4797)の間違ったステータス コードを修正
    -   PD がダッシュボード プロキシ リクエストを正しく処理できない問題を修正します[#5321](https://github.com/tikv/pd/issues/5321)
    -   いくつかの特殊なケースにおける TSO フォールバックのバグを修正[#4884](https://github.com/tikv/pd/issues/4884)
    -   特定のシナリオ[#5401](https://github.com/tikv/pd/issues/5401)でTiFlash学習者レプリカが作成されないことがある問題を修正します。
    -   ラベル分布のメトリクスに残留ラベルがある問題を修正します[#4825](https://github.com/tikv/pd/issues/4825)
    -   大容量のストア（たとえば 2T）が存在する場合、完全に割り当てられた小さなストアを検出できず、バランス演算子が生成されない問題を修正します[#4805](https://github.com/tikv/pd/issues/4805)
    -   `SchedulerMaxWaitingOperator`を`1` [#4946](https://github.com/tikv/pd/issues/4946)に設定するとスケジューラが動作しない問題を修正

-   TiFlash

    -   文字列を日時[#3556](https://github.com/pingcap/tiflash/issues/3556)にキャストするときの誤った`microsecond`を修正
    -   TLS が有効になっているときに発生するpanicの問題を修正します[#4196](https://github.com/pingcap/tiflash/issues/4196)
    -   並列集計[#5356](https://github.com/pingcap/tiflash/issues/5356)のエラーによりTiFlashがクラッシュする場合があるバグを修正
    -   `JOIN`を含むクエリでエラーが発生した場合にハングする可能性がある問題を修正します[#4195](https://github.com/pingcap/tiflash/issues/4195)
    -   関数`OR`が間違った結果[#5849](https://github.com/pingcap/tiflash/issues/5849)を返す問題を修正します。
    -   無効なstorageディレクトリ構成が予期せぬ動作を引き起こすバグを修正[#4093](https://github.com/pingcap/tiflash/issues/4093)
    -   多数の INSERT および DELETE 操作後の潜在的なデータの不整合を修正[#4956](https://github.com/pingcap/tiflash/issues/4956)
    -   TiFlashノード[#4414](https://github.com/pingcap/tiflash/issues/4414)にどのリージョン範囲にも一致しないデータが残るバグを修正
    -   重い読み取りワークロードで列を追加した後の潜在的なクエリ エラーを修正[#3967](https://github.com/pingcap/tiflash/issues/3967)
    -   `commit state jump backward`エラー[#2576](https://github.com/pingcap/tiflash/issues/2576)によって引き起こされる繰り返しのクラッシュを修正
    -   多くの削除操作を含むテーブルに対してクエリを実行する際の潜在的なエラーを修正します[#4747](https://github.com/pingcap/tiflash/issues/4747)
    -   日付形式で`''`無効な区切り文字[#4036](https://github.com/pingcap/tiflash/issues/4036)として識別される問題を修正します。
    -   `DATETIME`から`DECIMAL` [#4151](https://github.com/pingcap/tiflash/issues/4151)をキャストするときに発生する間違った結果を修正
    -   一部の例外が正しく処理されないバグを修正[#4101](https://github.com/pingcap/tiflash/issues/4101)
    -   `Prepare Merge` raft ストアのメタデータが破損し、 TiFlashが再起動する可能性がある問題を修正します[#3435](https://github.com/pingcap/tiflash/issues/3435)
    -   ランダムな gRPC キープアライブ タイムアウトにより MPP クエリが失敗する可能性があるバグを修正[#4662](https://github.com/pingcap/tiflash/issues/4662)
    -   複数値式[#4016](https://github.com/pingcap/tiflash/issues/4016)で`IN`の結果が正しくない問題を修正
    -   MPP タスクがスレッドを永久にリークする可能性があるバグを修正[#4238](https://github.com/pingcap/tiflash/issues/4238)
    -   期限切れデータのリサイクルが遅い問題を修正[#4146](https://github.com/pingcap/tiflash/issues/4146)
    -   `FLOAT` ～ `DECIMAL` [#3998](https://github.com/pingcap/tiflash/issues/3998)キャスト時に発生するオーバーフローを修正
    -   引数の型が UInt8 [#6127](https://github.com/pingcap/tiflash/issues/6127)の場合、論理演算子が間違った結果を返す問題を修正
    -   空の文字列[#2705](https://github.com/pingcap/tiflash/issues/2705)で`json_length`を呼び出した場合の潜在的な`index out of bounds`エラーを修正
    -   特殊なケースでの間違った 10 進比較結果を修正[#4512](https://github.com/pingcap/tiflash/issues/4512)
    -   `NOT NULL`列が追加されたときに報告される`TiFlash_schema_error`修正[#4596](https://github.com/pingcap/tiflash/issues/4596)
    -   整数のデフォルト値として`0.0`が使用されている場合 (例: `` `i` int(11) NOT NULL DEFAULT '0.0'`` [#3157](https://github.com/pingcap/tiflash/issues/3157) 、 TiFlashブートストラップが失敗する問題を修正します。

-   ツール

    -   TiDBBinlog

        -   `compressor`が`zip` [#1152](https://github.com/pingcap/tidb-binlog/issues/1152)に設定されている場合、 Drainer がPumpにリクエストを正しく送信できない問題を修正

    -   バックアップと復元 (BR)

        -   システム テーブルを同時にバックアップするとテーブル名の更新に失敗するため、システム テーブルを復元できない問題を修正します[#29710](https://github.com/pingcap/tidb/issues/29710)

    -   TiCDC

        -   特別な増分スキャン シナリオ[#5468](https://github.com/pingcap/tiflow/issues/5468)で発生するデータ損失を修正します。
        -   ソーターメトリクスが存在しない問題を修正[#5690](https://github.com/pingcap/tiflow/issues/5690)
        -   DDL スキーマのバッファリング方法を最適化することで過剰なメモリ使用量を修正します[#1386](https://github.com/pingcap/tiflow/issues/1386)
