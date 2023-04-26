---
title: TiDB 5.1.5 Release Notes
---

# TiDB 5.1.5 リリースノート {#tidb-5-1-5-release-notes}

発売日：2022年12月28日

TiDB バージョン: 5.1.5

クイック アクセス: [クイックスタート](https://docs.pingcap.com/tidb/v5.1/quick-start-with-tidb) | [本番展開](https://docs.pingcap.com/tidb/v5.1/production-deployment-using-tiup) | [インストール パッケージ](https://www.pingcap.com/download/?version=v5.1.5#version-list)

## 互換性の変更 {#compatibility-changes}

-   PD

    -   デフォルトでswaggerサーバーのコンパイルを無効にする[#4932](https://github.com/tikv/pd/issues/4932)

## バグの修正 {#bug-fixes}

-   TiDB

    -   ウィンドウ関数が原因で TiDB がエラーを報告する代わりにpanicになる問題を修正します[#30326](https://github.com/pingcap/tidb/issues/30326)
    -   TiFlash [#37254](https://github.com/pingcap/tidb/issues/37254)のパーティション テーブルで動的モードを有効にしたときに発生する誤った結果を修正します。
    -   符号なし`BIGINT`引数を渡すときの`GREATEST`と`LEAST`の間違った結果を修正[#30101](https://github.com/pingcap/tidb/issues/30101)
    -   `left join` [#31321](https://github.com/pingcap/tidb/issues/31321)を使用して複数のテーブルのデータを削除したときの誤った結果を修正
    -   TiDB の`concat(ifnull(time(3)))`の結果が MySQL [#29498](https://github.com/pingcap/tidb/issues/29498)の結果と異なる問題を修正
    -   `cast(integer as char) union string`を含む SQL ステートメントが間違った結果を返す問題を修正します[#29513](https://github.com/pingcap/tidb/issues/29513)
    -   `LIMIT` [#35638](https://github.com/pingcap/tidb/issues/35638)で使用すると`INL_HASH_JOIN`がハングする問題を修正
    -   リージョン が空のデータを返すときに発生する間違った結果`ANY_VALUE`修正します[#30923](https://github.com/pingcap/tidb/issues/30923)
    -   innerWorkerpanic[#31494](https://github.com/pingcap/tidb/issues/31494)によって引き起こされたインデックス結合の誤った結果を修正
    -   JSON 型の列が`CHAR`型の列を結合すると SQL 操作がキャンセルされる問題を修正します[#29401](https://github.com/pingcap/tidb/issues/29401)
    -   TiDB のバックグラウンド HTTP サービスが正常に終了せず、クラスターが異常な状態になることがある問題を修正します[#30571](https://github.com/pingcap/tidb/issues/30571)
    -   列の型を同時に変更すると、スキーマとデータの間で不整合が発生する問題を修正します[#31048](https://github.com/pingcap/tidb/issues/31048)
    -   `KILL TIDB`がアイドル状態の接続ですぐに有効にならない問題を修正します[#24031](https://github.com/pingcap/tidb/issues/24031)
    -   セッション変数を設定すると`tidb_snapshot`が動作しなくなるバグを修正[#35515](https://github.com/pingcap/tidb/issues/35515)
    -   リージョンのマージ時にリージョンのキャッシュが時間内にクリーンアップされない問題を修正します[#37141](https://github.com/pingcap/tidb/issues/37141)
    -   KV クライアント[#33773](https://github.com/pingcap/tidb/issues/33773)での接続配列の競合によって引き起こされるpanicの問題を修正します。
    -   TiDB Binlog が有効な場合に`ALTER SEQUENCE`ステートメントを実行すると、間違ったメタデータ バージョンが発生し、 Drainerが[#36276](https://github.com/pingcap/tidb/issues/36276)終了する可能性があるという問題を修正します。
    -   ステートメントの要約テーブルをクエリすると TiDB がpanicになる可能性があるバグを修正します[#35340](https://github.com/pingcap/tidb/issues/35340)
    -   TiFlashを使用して空の範囲を持つテーブルをスキャンすると、TiDB が間違った結果を取得する問題を修正しますが、 TiFlash はまだ空の範囲を持つテーブルの読み取りをサポートしていません[#33083](https://github.com/pingcap/tidb/issues/33083)
    -   TiFlash [#29952](https://github.com/pingcap/tidb/issues/29952)からクエリを実行すると`avg()`関数が`ERROR 1105 (HY000): other error for mpp stream: Could not convert to the target type - -value is out of range.`を返す問題を修正
    -   `HashJoinExec` [#30289](https://github.com/pingcap/tidb/issues/30289)を使用すると`ERROR 1105 (HY000): close of nil channel`が返される問題を修正
    -   論理演算のクエリ時に TiKV とTiFlashが異なる結果を返す問題を修正します[#37258](https://github.com/pingcap/tidb/issues/37258)
    -   特定のシナリオで`EXECUTE`ステートメントが予期しないエラーをスローする可能性がある問題を修正します[#37187](https://github.com/pingcap/tidb/issues/37187)
    -   `tidb_opt_agg_push_down`と`tidb_enforce_mpp`が有効な場合に発生する Planner の誤った動作を修正します[#34465](https://github.com/pingcap/tidb/issues/34465)
    -   `SHOW COLUMNS`ステートメント[#36496](https://github.com/pingcap/tidb/issues/36496)の実行時に TiDB がコプロセッサー要求を送信する可能性があるバグを修正します。
    -   `enable-table-lock`フラグが有効になっていない場合、 `lock tables`と`unlock tables`の警告を追加します[#28967](https://github.com/pingcap/tidb/issues/28967)
    -   範囲パーティションが複数の`MAXVALUE`パーティションを許可する問題を修正します[#36329](https://github.com/pingcap/tidb/issues/36329)

-   TiKV

    -   `DATETIME`値に分数と`Z` [#12739](https://github.com/tikv/tikv/issues/12739)が含まれている場合に発生する時間解析エラーの問題を修正します。
    -   レプリカの読み取りが線形化可能性に違反する可能性があるバグを修正します[#12109](https://github.com/tikv/tikv/issues/12109)
    -   Raftstore が混雑しているとリージョンが重複する可能性があるバグを修正[#13160](https://github.com/tikv/tikv/issues/13160)
    -   スナップショットの適用が中止されたときに発生する TiKVpanicの問題を修正します[#11618](https://github.com/tikv/tikv/issues/11618)
    -   TiKVが2年以上稼働しているとpanicになることがあるバグを修正[#11940](https://github.com/tikv/tikv/issues/11940)
    -   ソース ピアがリージョンマージ プロセスでスナップショットによってログをキャッチするときに発生する可能性があるpanicの問題を修正します[#12663](https://github.com/tikv/tikv/issues/12663)
    -   空の文字列の型変換を実行すると TiKV がパニックになる問題を修正します[#12673](https://github.com/tikv/tikv/issues/12673)
    -   古いメッセージが原因で TiKV がpanicになるバグを修正[#12023](https://github.com/tikv/tikv/issues/12023)
    -   ピアの分割と破棄が同時に行われると発生する可能性があるpanicの問題を修正します[#12825](https://github.com/tikv/tikv/issues/12825)
    -   リージョン[#12048](https://github.com/tikv/tikv/issues/12048)のマージ時にターゲット ピアが初期化されずに破棄されたピアに置き換えられると発生する TiKVpanicの問題を修正します。
    -   Follower Read [#12478](https://github.com/tikv/tikv/issues/12478)の使用時に TiKV が`invalid store ID 0`エラーを報告する問題を修正
    -   悲観的トランザクションでコミット レコードが重複する可能性がある問題を修正します[#12615](https://github.com/tikv/tikv/issues/12615)
    -   1 つのピアが到達不能になった後にRaftstore があまりにも多くのメッセージをブロードキャストするのを避けるために、 `unreachable_backoff`項目の構成をサポートします[#13054](https://github.com/tikv/tikv/issues/13054)
    -   ネットワークが貧弱な場合、楽観的トランザクションを正常にコミットしても`Write Conflict`エラーが報告される可能性がある問題を修正します[#34066](https://github.com/pingcap/tidb/issues/34066)
    -   ダッシュボード[#13086](https://github.com/tikv/tikv/issues/13086)の`Unified Read Pool CPU`の間違った表現を修正

-   PD

    -   PDリーダーの転送後、削除されたトゥームストーンストアが再び表示される問題を修正[#4941](https://github.com/tikv/pd/issues/4941)
    -   PD リーダーの転送[#4769](https://github.com/tikv/pd/issues/4769)の直後にスケジュールを開始できない問題を修正します。
    -   `not leader` [#4797](https://github.com/tikv/pd/issues/4797)の間違ったステータス コードを修正
    -   PD がダッシュボード プロキシ リクエストを正しく処理できない問題を修正します[#5321](https://github.com/tikv/pd/issues/5321)
    -   一部のまれなケースでの TSO フォールバックのバグを修正します[#4884](https://github.com/tikv/pd/issues/4884)
    -   特定のシナリオでTiFlash学習者のレプリカが作成されない場合がある問題を修正します[#5401](https://github.com/tikv/pd/issues/5401)
    -   ラベル分布がメトリクス[#4825](https://github.com/tikv/pd/issues/4825)に残留ラベルを持つ問題を修正します。
    -   大容量(例えば2T)のストアが存在する場合、満杯に割り当てられた小さなストアが検出されず、バランス演算子が生成されない問題を修正します[#4805](https://github.com/tikv/pd/issues/4805)
    -   `SchedulerMaxWaitingOperator`を`1` [#4946](https://github.com/tikv/pd/issues/4946)に設定するとスケジューラーが動作しない問題を修正

-   TiFlash

    -   文字列を日時[#3556](https://github.com/pingcap/tiflash/issues/3556)にキャストするときの誤った`microsecond`を修正
    -   TLS が有効になっているときに発生するpanicの問題を修正します[#4196](https://github.com/pingcap/tiflash/issues/4196)
    -   並列集計[#5356](https://github.com/pingcap/tiflash/issues/5356)でエラーによりTiFlashがクラッシュすることがある不具合を修正
    -   エラーが発生した場合に`JOIN`含むクエリがハングする可能性がある問題を修正します[#4195](https://github.com/pingcap/tiflash/issues/4195)
    -   関数`OR`が間違った結果を返す問題を修正[#5849](https://github.com/pingcap/tiflash/issues/5849)
    -   無効なstorageディレクトリ構成が予期しない動作を引き起こすバグを修正します[#4093](https://github.com/pingcap/tiflash/issues/4093)
    -   多数の INSERT 操作と DELETE 操作の後に発生する可能性のあるデータの不整合を修正します[#4956](https://github.com/pingcap/tiflash/issues/4956)
    -   どのリージョン範囲とも一致しないデータがTiFlashノード[#4414](https://github.com/pingcap/tiflash/issues/4414)に残るバグを修正
    -   重い読み取りワークロードの下で列を追加した後の潜在的なクエリ エラーを修正します[#3967](https://github.com/pingcap/tiflash/issues/3967)
    -   `commit state jump backward`エラーが原因で繰り返されるクラッシュを修正[#2576](https://github.com/pingcap/tiflash/issues/2576)
    -   削除操作が多いテーブルに対してクエリを実行するときに発生する可能性のあるエラーを修正します[#4747](https://github.com/pingcap/tiflash/issues/4747)
    -   日付形式が`''`を無効な区切り文字として識別する問題を修正します[#4036](https://github.com/pingcap/tiflash/issues/4036)
    -   `DATETIME`から`DECIMAL` [#4151](https://github.com/pingcap/tiflash/issues/4151)をキャストしたときに発生する誤った結果を修正します
    -   一部の例外が適切に処理されないバグを修正[#4101](https://github.com/pingcap/tiflash/issues/4101)
    -   `Prepare Merge`ラフト ストアのメタデータが破損し、 TiFlashが再起動する可能性がある問題を修正[#3435](https://github.com/pingcap/tiflash/issues/3435)
    -   ランダムな gRPC キープアライブ タイムアウト[#4662](https://github.com/pingcap/tiflash/issues/4662)が原因で MPP クエリが失敗する可能性があるバグを修正します
    -   多値式で`IN`の結果が正しくない問題を修正[#4016](https://github.com/pingcap/tiflash/issues/4016)
    -   MPP タスクがスレッドを永久にリークする可能性があるバグを修正します[#4238](https://github.com/pingcap/tiflash/issues/4238)
    -   期限切れのデータがゆっくりとリサイクルされる問題を修正します[#4146](https://github.com/pingcap/tiflash/issues/4146)
    -   `FLOAT`から`DECIMAL` [#3998](https://github.com/pingcap/tiflash/issues/3998)へのキャスト時に発生するオーバーフローを修正
    -   引数の型が UInt8 [#6127](https://github.com/pingcap/tiflash/issues/6127)の場合、論理演算子が間違った結果を返す問題を修正
    -   空の文字列[#2705](https://github.com/pingcap/tiflash/issues/2705)で`json_length`を呼び出すと発生する可能性のある`index out of bounds`エラーを修正
    -   コーナーケースで間違った小数比較結果を修正する[#4512](https://github.com/pingcap/tiflash/issues/4512)
    -   `NOT NULL`列が追加されたときに報告された修正`TiFlash_schema_error` [#4596](https://github.com/pingcap/tiflash/issues/4596)
    -   整数のデフォルト値として`0.0`を使用すると、 TiFlashブートストラップが失敗する問題を修正します (例: `` `i` int(11) NOT NULL DEFAULT '0.0'`` [#3157](https://github.com/pingcap/tiflash/issues/3157) 。

-   ツール

    -   TiDBBinlog

        -   `compressor`が`zip` [#1152](https://github.com/pingcap/tidb-binlog/issues/1152)に設定されている場合、 Drainer がPumpに正しくリクエストを送信できない問題を修正します。

    -   バックアップと復元 (BR)

        -   システム テーブルを同時にバックアップすると、テーブル名が更新されないため、システム テーブルを復元できない問題を修正します[#29710](https://github.com/pingcap/tidb/issues/29710)

    -   TiCDC

        -   特別な増分スキャン シナリオで発生するデータ損失を修正します[#5468](https://github.com/pingcap/tiflow/issues/5468)
        -   ソーター メトリックがない問題を修正します[#5690](https://github.com/pingcap/tiflow/issues/5690)
        -   DDL スキーマがバッファリングされる方法を最適化することにより、過剰なメモリ使用量を修正します[#1386](https://github.com/pingcap/tiflow/issues/1386)
