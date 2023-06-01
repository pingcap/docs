---
title: TiDB 5.1.5 Release Notes
---

# TiDB 5.1.5 リリースノート {#tidb-5-1-5-release-notes}

発売日：2022年12月28日

TiDB バージョン: 5.1.5

クイックアクセス: [<a href="https://docs.pingcap.com/tidb/v5.1/quick-start-with-tidb">クイックスタート</a>](https://docs.pingcap.com/tidb/v5.1/quick-start-with-tidb) | [<a href="https://docs.pingcap.com/tidb/v5.1/production-deployment-using-tiup">本番展開</a>](https://docs.pingcap.com/tidb/v5.1/production-deployment-using-tiup) | [<a href="https://www.pingcap.com/download/?version=v5.1.5#version-list">インストールパッケージ</a>](https://www.pingcap.com/download/?version=v5.1.5#version-list)

## 互換性の変更 {#compatibility-changes}

-   PD

    -   Swaggerサーバーのコンパイルをデフォルトで無効にする[<a href="https://github.com/tikv/pd/issues/4932">#4932</a>](https://github.com/tikv/pd/issues/4932)

## バグの修正 {#bug-fixes}

-   TiDB

    -   ウィンドウ関数により TiDB がエラーを報告する代わりにpanicを引き起こす問題を修正します[<a href="https://github.com/pingcap/tidb/issues/30326">#30326</a>](https://github.com/pingcap/tidb/issues/30326)
    -   TiFlash [<a href="https://github.com/pingcap/tidb/issues/37254">#37254</a>](https://github.com/pingcap/tidb/issues/37254)のパーティション化されたテーブルで動的モードを有効にしたときに発生する間違った結果を修正しました。
    -   符号なし`BIGINT`引数[<a href="https://github.com/pingcap/tidb/issues/30101">#30101</a>](https://github.com/pingcap/tidb/issues/30101)を渡すときの`GREATEST`と`LEAST`の間違った結果を修正
    -   `left join` [<a href="https://github.com/pingcap/tidb/issues/31321">#31321</a>](https://github.com/pingcap/tidb/issues/31321)を使用して複数のテーブルのデータを削除した場合の誤った結果を修正
    -   TiDB の`concat(ifnull(time(3)))`の結果が MySQL [<a href="https://github.com/pingcap/tidb/issues/29498">#29498</a>](https://github.com/pingcap/tidb/issues/29498)の結果と異なる問題を修正
    -   `cast(integer as char) union string`を含む SQL ステートメントが間違った結果を返す問題を修正します[<a href="https://github.com/pingcap/tidb/issues/29513">#29513</a>](https://github.com/pingcap/tidb/issues/29513)
    -   `LIMIT` [<a href="https://github.com/pingcap/tidb/issues/35638">#35638</a>](https://github.com/pingcap/tidb/issues/35638)と一緒に使用すると`INL_HASH_JOIN`ハングする可能性がある問題を修正
    -   リージョンが空のデータを返したときに発生する間違った結果`ANY_VALUE`修正しました[<a href="https://github.com/pingcap/tidb/issues/30923">#30923</a>](https://github.com/pingcap/tidb/issues/30923)
    -   innerWorkerpanic[<a href="https://github.com/pingcap/tidb/issues/31494">#31494</a>](https://github.com/pingcap/tidb/issues/31494)によって引き起こされるインデックス結合の間違った結果を修正します。
    -   JSON 型の列が`CHAR`型の列[<a href="https://github.com/pingcap/tidb/issues/29401">#29401</a>](https://github.com/pingcap/tidb/issues/29401)に結合すると SQL 操作がキャンセルされる問題を修正
    -   TiDB のバックグラウンド HTTP サービスが正常に終了せず、クラスターが異常な状態になる場合がある問題を修正します[<a href="https://github.com/pingcap/tidb/issues/30571">#30571</a>](https://github.com/pingcap/tidb/issues/30571)
    -   同時に列の型を変更すると、スキーマとデータの間で不整合が発生する問題を修正します[<a href="https://github.com/pingcap/tidb/issues/31048">#31048</a>](https://github.com/pingcap/tidb/issues/31048)
    -   アイドル状態の接続で`KILL TIDB`がすぐに有効にならない問題を修正[<a href="https://github.com/pingcap/tidb/issues/24031">#24031</a>](https://github.com/pingcap/tidb/issues/24031)
    -   セッション変数を設定すると`tidb_snapshot`が機能しなくなるバグを修正[<a href="https://github.com/pingcap/tidb/issues/35515">#35515</a>](https://github.com/pingcap/tidb/issues/35515)
    -   リージョンがマージされるときにリージョンキャッシュが時間内にクリーンアップされない問題を修正します[<a href="https://github.com/pingcap/tidb/issues/37141">#37141</a>](https://github.com/pingcap/tidb/issues/37141)
    -   KV クライアント[<a href="https://github.com/pingcap/tidb/issues/33773">#33773</a>](https://github.com/pingcap/tidb/issues/33773)での接続アレイの競合によって引き起こされるpanicの問題を修正します。
    -   TiDB Binlogが有効な場合、 `ALTER SEQUENCE`ステートメントを実行するとメタデータ バージョンが間違ってDrainerが終了する可能性がある問題を修正します[<a href="https://github.com/pingcap/tidb/issues/36276">#36276</a>](https://github.com/pingcap/tidb/issues/36276)
    -   ステートメント概要テーブル[<a href="https://github.com/pingcap/tidb/issues/35340">#35340</a>](https://github.com/pingcap/tidb/issues/35340)をクエリするときに TiDB がpanicになる可能性があるバグを修正
    -   TiFlash は空の範囲を持つテーブルの読み取りをまだサポートしていませんが、 TiFlashを使用して空の範囲を持つテーブルをスキャンすると、TiDB が間違った結果を取得する問題を修正します[<a href="https://github.com/pingcap/tidb/issues/33083">#33083</a>](https://github.com/pingcap/tidb/issues/33083)
    -   TiFlash [<a href="https://github.com/pingcap/tidb/issues/29952">#29952</a>](https://github.com/pingcap/tidb/issues/29952)からクエリすると`avg()`関数が`ERROR 1105 (HY000): other error for mpp stream: Could not convert to the target type - -value is out of range.`を返す問題を修正
    -   `HashJoinExec` [<a href="https://github.com/pingcap/tidb/issues/30289">#30289</a>](https://github.com/pingcap/tidb/issues/30289)を使用すると`ERROR 1105 (HY000): close of nil channel`が返される問題を修正
    -   論理演算のクエリ時に TiKV とTiFlashが異なる結果を返す問題を修正[<a href="https://github.com/pingcap/tidb/issues/37258">#37258</a>](https://github.com/pingcap/tidb/issues/37258)
    -   特定のシナリオで`EXECUTE`ステートメントが予期しないエラーをスローする可能性がある問題を修正します[<a href="https://github.com/pingcap/tidb/issues/37187">#37187</a>](https://github.com/pingcap/tidb/issues/37187)
    -   `tidb_opt_agg_push_down`と`tidb_enforce_mpp`が有効になっている場合に発生するプランナーの誤った動作を修正します[<a href="https://github.com/pingcap/tidb/issues/34465">#34465</a>](https://github.com/pingcap/tidb/issues/34465)
    -   `SHOW COLUMNS`ステートメント[<a href="https://github.com/pingcap/tidb/issues/36496">#36496</a>](https://github.com/pingcap/tidb/issues/36496)の実行時に TiDB がコプロセッサ リクエストを送信する可能性があるバグを修正
    -   `enable-table-lock`フラグが有効になっていない場合の`lock tables`と`unlock tables`の警告を追加[<a href="https://github.com/pingcap/tidb/issues/28967">#28967</a>](https://github.com/pingcap/tidb/issues/28967)
    -   範囲パーティションで複数の`MAXVALUE`パーティションが許可される問題を修正します[<a href="https://github.com/pingcap/tidb/issues/36329">#36329</a>](https://github.com/pingcap/tidb/issues/36329)

-   TiKV

    -   `DATETIME`値に小数と`Z` [<a href="https://github.com/tikv/tikv/issues/12739">#12739</a>](https://github.com/tikv/tikv/issues/12739)が含まれる場合に発生する時刻解析エラーの問題を修正します。
    -   レプリカの読み取りが線形化可能性[<a href="https://github.com/tikv/tikv/issues/12109">#12109</a>](https://github.com/tikv/tikv/issues/12109)に違反する可能性があるバグを修正
    -   Raftstoreがビジー状態の場合にリージョンが重なる可能性があるバグを修正[<a href="https://github.com/tikv/tikv/issues/13160">#13160</a>](https://github.com/tikv/tikv/issues/13160)
    -   スナップショットの適用が中止されたときに発生する TiKVpanicの問題を修正します[<a href="https://github.com/tikv/tikv/issues/11618">#11618</a>](https://github.com/tikv/tikv/issues/11618)
    -   TiKV が 2 年以上実行されている場合にpanicになる可能性があるバグを修正[<a href="https://github.com/tikv/tikv/issues/11940">#11940</a>](https://github.com/tikv/tikv/issues/11940)
    -   リージョンマージ プロセス[<a href="https://github.com/tikv/tikv/issues/12663">#12663</a>](https://github.com/tikv/tikv/issues/12663)でソース ピアがスナップショットによってログを追いつくときに発生する可能性があるpanicの問題を修正します。
    -   空の文字列の型変換を実行すると TiKV がパニックになる問題を修正[<a href="https://github.com/tikv/tikv/issues/12673">#12673</a>](https://github.com/tikv/tikv/issues/12673)
    -   古いメッセージによって TiKV がpanicになるバグを修正[<a href="https://github.com/tikv/tikv/issues/12023">#12023</a>](https://github.com/tikv/tikv/issues/12023)
    -   ピアの分割と破棄が同時に行われるときに発生する可能性があるpanicの問題を修正します[<a href="https://github.com/tikv/tikv/issues/12825">#12825</a>](https://github.com/tikv/tikv/issues/12825)
    -   リージョン[<a href="https://github.com/tikv/tikv/issues/12048">#12048</a>](https://github.com/tikv/tikv/issues/12048)をマージするときに、ターゲット ピアが初期化されずに破棄されたピアに置き換えられるときに発生する TiKVpanicの問題を修正します。
    -   Follower Read [<a href="https://github.com/tikv/tikv/issues/12478">#12478</a>](https://github.com/tikv/tikv/issues/12478)を使用すると TiKV が`invalid store ID 0`エラーを報告する問題を修正
    -   非同期コミットが有効になっている場合に、悲観的トランザクションで発生する可能性のある重複コミット レコードを修正します[<a href="https://github.com/tikv/tikv/issues/12615">#12615</a>](https://github.com/tikv/tikv/issues/12615)
    -   1 つのピアが到達不能になった後にRaftstore が大量のメッセージをブロードキャストすることを避けるための`unreachable_backoff`項目の設定をサポートします[<a href="https://github.com/tikv/tikv/issues/13054">#13054</a>](https://github.com/tikv/tikv/issues/13054)
    -   ネットワークが貧弱な場合、正常にコミットされた楽観的トランザクションが`Write Conflict`エラーを報告する可能性がある問題を修正します[<a href="https://github.com/pingcap/tidb/issues/34066">#34066</a>](https://github.com/pingcap/tidb/issues/34066)
    -   ダッシュボード[<a href="https://github.com/tikv/tikv/issues/13086">#13086</a>](https://github.com/tikv/tikv/issues/13086)の`Unified Read Pool CPU`の誤った表現を修正

-   PD

    -   PDリーダー移転後、削除された墓石ストアが再び表示される問題を修正[<a href="https://github.com/tikv/pd/issues/4941">#4941</a>](https://github.com/tikv/pd/issues/4941)
    -   PDリーダー転送[<a href="https://github.com/tikv/pd/issues/4769">#4769</a>](https://github.com/tikv/pd/issues/4769)直後にスケジューリングが開始できない問題を修正
    -   `not leader` [<a href="https://github.com/tikv/pd/issues/4797">#4797</a>](https://github.com/tikv/pd/issues/4797)の間違ったステータス コードを修正
    -   PD がダッシュボード プロキシ リクエストを正しく処理できない問題を修正します[<a href="https://github.com/tikv/pd/issues/5321">#5321</a>](https://github.com/tikv/pd/issues/5321)
    -   いくつかの特殊なケースにおける TSO フォールバックのバグを修正[<a href="https://github.com/tikv/pd/issues/4884">#4884</a>](https://github.com/tikv/pd/issues/4884)
    -   特定のシナリオ[<a href="https://github.com/tikv/pd/issues/5401">#5401</a>](https://github.com/tikv/pd/issues/5401)でTiFlash学習者レプリカが作成されないことがある問題を修正します。
    -   ラベル分布のメトリクスに残留ラベルがある問題を修正します[<a href="https://github.com/tikv/pd/issues/4825">#4825</a>](https://github.com/tikv/pd/issues/4825)
    -   大容量のストア（たとえば 2T）が存在する場合、完全に割り当てられた小さなストアが検出できず、バランス演算子が生成されない問題を修正します[<a href="https://github.com/tikv/pd/issues/4805">#4805</a>](https://github.com/tikv/pd/issues/4805)
    -   `SchedulerMaxWaitingOperator`を`1` [<a href="https://github.com/tikv/pd/issues/4946">#4946</a>](https://github.com/tikv/pd/issues/4946)に設定するとスケジューラが動作しない問題を修正

-   TiFlash

    -   文字列を日時[<a href="https://github.com/pingcap/tiflash/issues/3556">#3556</a>](https://github.com/pingcap/tiflash/issues/3556)にキャストするときの誤った`microsecond`を修正
    -   TLS が有効になっているときに発生するpanicの問題を修正します[<a href="https://github.com/pingcap/tiflash/issues/4196">#4196</a>](https://github.com/pingcap/tiflash/issues/4196)
    -   並列集計[<a href="https://github.com/pingcap/tiflash/issues/5356">#5356</a>](https://github.com/pingcap/tiflash/issues/5356)のエラーによりTiFlashがクラッシュする場合があるバグを修正
    -   `JOIN`を含むクエリでエラーが発生した場合にハングする可能性がある問題を修正[<a href="https://github.com/pingcap/tiflash/issues/4195">#4195</a>](https://github.com/pingcap/tiflash/issues/4195)
    -   関数`OR`が間違った結果[<a href="https://github.com/pingcap/tiflash/issues/5849">#5849</a>](https://github.com/pingcap/tiflash/issues/5849)を返す問題を修正します。
    -   無効なstorageディレクトリ構成が予期せぬ動作を引き起こすバグを修正[<a href="https://github.com/pingcap/tiflash/issues/4093">#4093</a>](https://github.com/pingcap/tiflash/issues/4093)
    -   多数の INSERT および DELETE 操作後の潜在的なデータの不整合を修正[<a href="https://github.com/pingcap/tiflash/issues/4956">#4956</a>](https://github.com/pingcap/tiflash/issues/4956)
    -   TiFlashノード[<a href="https://github.com/pingcap/tiflash/issues/4414">#4414</a>](https://github.com/pingcap/tiflash/issues/4414)にどのリージョン範囲にも一致しないデータが残るバグを修正
    -   重い読み取りワークロードで列を追加した後の潜在的なクエリ エラーを修正[<a href="https://github.com/pingcap/tiflash/issues/3967">#3967</a>](https://github.com/pingcap/tiflash/issues/3967)
    -   `commit state jump backward`エラー[<a href="https://github.com/pingcap/tiflash/issues/2576">#2576</a>](https://github.com/pingcap/tiflash/issues/2576)によって引き起こされる繰り返しのクラッシュを修正
    -   多くの削除操作を含むテーブルに対してクエリを実行する際の潜在的なエラーを修正します[<a href="https://github.com/pingcap/tiflash/issues/4747">#4747</a>](https://github.com/pingcap/tiflash/issues/4747)
    -   日付形式で`''`無効な区切り文字[<a href="https://github.com/pingcap/tiflash/issues/4036">#4036</a>](https://github.com/pingcap/tiflash/issues/4036)として識別される問題を修正します。
    -   `DATETIME`から`DECIMAL` [<a href="https://github.com/pingcap/tiflash/issues/4151">#4151</a>](https://github.com/pingcap/tiflash/issues/4151)をキャストするときに発生する間違った結果を修正
    -   一部の例外が正しく処理されないバグを修正[<a href="https://github.com/pingcap/tiflash/issues/4101">#4101</a>](https://github.com/pingcap/tiflash/issues/4101)
    -   `Prepare Merge` raft ストアのメタデータが破損し、 TiFlashが再起動する可能性がある問題を修正します[<a href="https://github.com/pingcap/tiflash/issues/3435">#3435</a>](https://github.com/pingcap/tiflash/issues/3435)
    -   ランダムな gRPC キープアライブ タイムアウトにより MPP クエリが失敗する可能性があるバグを修正[<a href="https://github.com/pingcap/tiflash/issues/4662">#4662</a>](https://github.com/pingcap/tiflash/issues/4662)
    -   複数値式[<a href="https://github.com/pingcap/tiflash/issues/4016">#4016</a>](https://github.com/pingcap/tiflash/issues/4016)で`IN`の結果が正しくない問題を修正
    -   MPP タスクがスレッドを永久にリークする可能性があるバグを修正[<a href="https://github.com/pingcap/tiflash/issues/4238">#4238</a>](https://github.com/pingcap/tiflash/issues/4238)
    -   期限切れデータのリサイクルが遅い問題を修正[<a href="https://github.com/pingcap/tiflash/issues/4146">#4146</a>](https://github.com/pingcap/tiflash/issues/4146)
    -   `FLOAT` ～ `DECIMAL` [<a href="https://github.com/pingcap/tiflash/issues/3998">#3998</a>](https://github.com/pingcap/tiflash/issues/3998)キャスト時に発生するオーバーフローを修正
    -   引数の型が UInt8 [<a href="https://github.com/pingcap/tiflash/issues/6127">#6127</a>](https://github.com/pingcap/tiflash/issues/6127)の場合、論理演算子が間違った結果を返す問題を修正
    -   空の文字列[<a href="https://github.com/pingcap/tiflash/issues/2705">#2705</a>](https://github.com/pingcap/tiflash/issues/2705)で`json_length`を呼び出した場合の潜在的な`index out of bounds`エラーを修正
    -   特殊なケースでの間違った 10 進比較結果を修正[<a href="https://github.com/pingcap/tiflash/issues/4512">#4512</a>](https://github.com/pingcap/tiflash/issues/4512)
    -   `NOT NULL`列が追加されたときに報告される`TiFlash_schema_error`修正[<a href="https://github.com/pingcap/tiflash/issues/4596">#4596</a>](https://github.com/pingcap/tiflash/issues/4596)
    -   整数のデフォルト値として`0.0`が使用されている場合 (例: `` `i` int(11) NOT NULL DEFAULT '0.0'`` [<a href="https://github.com/pingcap/tiflash/issues/3157">#3157</a>](https://github.com/pingcap/tiflash/issues/3157) 、 TiFlashブートストラップが失敗する問題を修正します。

-   ツール

    -   TiDBBinlog

        -   `compressor`が`zip` [<a href="https://github.com/pingcap/tidb-binlog/issues/1152">#1152</a>](https://github.com/pingcap/tidb-binlog/issues/1152)に設定されている場合、 Drainer がPumpにリクエストを正しく送信できない問題を修正

    -   バックアップと復元 (BR)

        -   システム テーブルを同時にバックアップするとテーブル名の更新に失敗するため、システム テーブルを復元できない問題を修正します[<a href="https://github.com/pingcap/tidb/issues/29710">#29710</a>](https://github.com/pingcap/tidb/issues/29710)

    -   TiCDC

        -   特別な増分スキャン シナリオ[<a href="https://github.com/pingcap/tiflow/issues/5468">#5468</a>](https://github.com/pingcap/tiflow/issues/5468)で発生するデータ損失を修正します。
        -   ソーターメトリクスが存在しない問題を修正[<a href="https://github.com/pingcap/tiflow/issues/5690">#5690</a>](https://github.com/pingcap/tiflow/issues/5690)
        -   DDL スキーマのバッファリング方法を最適化することで過剰なメモリ使用量を修正します[<a href="https://github.com/pingcap/tiflow/issues/1386">#1386</a>](https://github.com/pingcap/tiflow/issues/1386)
