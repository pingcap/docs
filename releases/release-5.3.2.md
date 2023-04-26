---
title: TiDB 5.3.2 Release Notes
---

# TiDB 5.3.2 リリースノート {#tidb-5-3-2-release-notes}

リリース日：2022年6月29日

TiDB バージョン: 5.3.2

> **警告：**
>
> このバージョンには既知のバグがあるため、v5.3.2 の使用はお勧めしません。詳細については、 [#12934](https://github.com/tikv/tikv/issues/12934)を参照してください。このバグは v5.3.3 で修正されています。 [v5.3.3](/releases/release-5.3.3.md)を使用することをお勧めします。

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   自動 ID が範囲外の場合に`REPLACE`ステートメントが他の行を誤って変更する問題を修正します[#29483](https://github.com/pingcap/tidb/issues/29483)

-   PD

    -   デフォルトでswaggerサーバーのコンパイルを無効にする[#4932](https://github.com/tikv/pd/issues/4932)

## 改良点 {#improvements}

-   TiKV

    -   Raftクライアントによるシステム コールを減らし、CPU 効率を高める[#11309](https://github.com/tikv/tikv/issues/11309)
    -   TiKV クライアントがリージョンキャッシュを時間[#12398](https://github.com/tikv/tikv/issues/12398)に更新できるように、ヘルス チェックを改善して利用できないRaftstoreを検出します。
    -   リーダーシップを CDC オブザーバーに移管し、レイテンシーのジッターを減らします[#12111](https://github.com/tikv/tikv/issues/12111)
    -   Raftログのガベージコレクションモジュールにメトリックを追加して、モジュール[#11374](https://github.com/tikv/tikv/issues/11374)のパフォーマンスの問題を特定します。

-   ツール

    -   TiDB データ移行 (DM)

        -   内部ファイルの書き込みに`/tmp`ではなく DM-worker の作業ディレクトリを使用し、タスクの停止後にディレクトリをクリーニングする Syncer をサポートします[#4107](https://github.com/pingcap/tiflow/issues/4107)

    -   TiDB Lightning

        -   分散リージョンをバッチ モードに最適化して、分散リージョンプロセスの安定性を向上させます[#33618](https://github.com/pingcap/tidb/issues/33618)

## バグの修正 {#bug-fixes}

-   TiDB

    -   Amazon S3 が圧縮データのサイズを正しく計算できない問題を修正[#30534](https://github.com/pingcap/tidb/issues/30534)
    -   楽観的トランザクション モード[#30410](https://github.com/pingcap/tidb/issues/30410)での潜在的なデータ インデックスの不整合の問題を修正します。
    -   JSON 型の列が`CHAR`型の列を結合すると SQL 操作がキャンセルされる問題を修正します[#29401](https://github.com/pingcap/tidb/issues/29401)
    -   以前は、ネットワーク接続の問題が発生した場合、TiDB は切断されたセッションによって保持されていたリソースを常に正しく解放するとは限りませんでした。この問題は修正され、開いているトランザクションをロールバックし、関連する他のリソースを解放できるようになりました。 [#34722](https://github.com/pingcap/tidb/issues/34722)
    -   TiDB Binlogを有効にして重複した値を挿入すると`data and columnID count not match`エラーが発生する問題を修正[#33608](https://github.com/pingcap/tidb/issues/33608)
    -   Plan Cache を RC 分離レベル[#34447](https://github.com/pingcap/tidb/issues/34447)で開始すると、クエリの結果が正しくない場合がある問題を修正します。
    -   MySQL バイナリ プロトコル[#33509](https://github.com/pingcap/tidb/issues/33509)でテーブル スキーマ変更後にプリペアドステートメントを実行するとセッション パニックが発生するpanicを修正
    -   新しいパーティションが追加されたときにテーブルの属性がインデックス化されない問題と、パーティションが変更されたときにテーブルの範囲情報が更新されない問題を修正します[#33929](https://github.com/pingcap/tidb/issues/33929)
    -   `INFORMATION_SCHEMA.CLUSTER_SLOW_QUERY`テーブルをクエリすると、TiDBサーバーがメモリ不足になることがある問題を修正します。この問題は、Grafana ダッシュボードでスロー クエリを確認すると発生する可能性があります[#33893](https://github.com/pingcap/tidb/issues/33893)
    -   クラスターの PD ノードが交換された後、一部の DDL ステートメントが一定期間停止する可能性がある問題を修正します[#33908](https://github.com/pingcap/tidb/issues/33908)
    -   [#33588](https://github.com/pingcap/tidb/issues/33588)からアップグレードされたクラスターで`all`特権の付与が失敗する可能性がある問題を修正します。
    -   `left join` [#31321](https://github.com/pingcap/tidb/issues/31321)を使用して複数のテーブルのデータを削除したときの誤った結果を修正
    -   TiDB が重複したタスクをTiFlash [#32814](https://github.com/pingcap/tidb/issues/32814)にディスパッチする可能性があるバグを修正
    -   TiDB のバックグラウンド HTTP サービスが正常に終了せず、クラスターが異常な状態になることがある問題を修正します[#30571](https://github.com/pingcap/tidb/issues/30571)
    -   `fatal error: concurrent map read and map write`エラー[#35340](https://github.com/pingcap/tidb/issues/35340)によって引き起こされるpanicの問題を修正します。

-   TiKV

    -   PD クライアントがエラー[#12345](https://github.com/tikv/tikv/issues/12345)に遭遇したときに発生する PD クライアントの再接続が頻繁に発生する問題を修正します。
    -   `DATETIME`値に分数と`Z` [#12739](https://github.com/tikv/tikv/issues/12739)が含まれている場合に発生する時間解析エラーの問題を修正します。
    -   空の文字列の型変換を実行すると TiKV がパニックになる問題を修正します[#12673](https://github.com/tikv/tikv/issues/12673)
    -   悲観的トランザクションでコミット レコードが重複する可能性がある問題を修正します[#12615](https://github.com/tikv/tikv/issues/12615)
    -   Follower Read [#12478](https://github.com/tikv/tikv/issues/12478)使用時に TiKV が`invalid store ID 0`エラーを報告するバグを修正
    -   ピアの破棄とリージョン[#12368](https://github.com/tikv/tikv/issues/12368)のバッチ分割の間の競合によって引き起こされる TiKVpanicの問題を修正します。
    -   ネットワークが貧弱な場合、楽観的トランザクションを正常にコミットしても`Write Conflict`エラーが報告される可能性がある問題を修正します[#34066](https://github.com/pingcap/tidb/issues/34066)
    -   マージする対象のリージョンが無効な場合、TiKV が予期せずパニックを起こし、ピアを破棄する問題を修正します[#12232](https://github.com/tikv/tikv/issues/12232)
    -   古いメッセージが原因で TiKV がpanicになるバグを修正[#12023](https://github.com/tikv/tikv/issues/12023)
    -   メモリメトリック[#12160](https://github.com/tikv/tikv/issues/12160)のオーバーフローが原因で発生する断続的なパケット損失とメモリ不足 (OOM) の問題を修正します。
    -   TiKV が Ubuntu [#9765](https://github.com/tikv/tikv/issues/9765)でプロファイリングを実行するときに発生する潜在的なpanicの問題を修正します。
    -   間違った文字列の一致が原因で tikv-ctl が間違った結果を返す問題を修正します[#12329](https://github.com/tikv/tikv/issues/12329)
    -   レプリカの読み取りが線形化可能性に違反する可能性があるバグを修正します[#12109](https://github.com/tikv/tikv/issues/12109)
    -   リージョン[#12048](https://github.com/tikv/tikv/issues/12048)のマージ時にターゲット ピアが初期化されずに破棄されたピアに置き換えられると発生する TiKVpanicの問題を修正します。
    -   TiKVが2年以上稼働しているとpanicになることがあるバグを修正[#11940](https://github.com/tikv/tikv/issues/11940)

-   PD

    -   ホット リージョンにリーダーがない場合に発生する PDpanicを修正します[#5005](https://github.com/tikv/pd/issues/5005)
    -   PD リーダーの転送[#4769](https://github.com/tikv/pd/issues/4769)の直後にスケジュールを開始できない問題を修正します。
    -   PDリーダーの転送後、削除されたトゥームストーンストアが再び表示される問題を修正[#4941](https://github.com/tikv/pd/issues/4941)
    -   一部のまれなケースでの TSO フォールバックのバグを修正します[#4884](https://github.com/tikv/pd/issues/4884)
    -   大容量(例えば2T)のストアが存在する場合、満杯に割り当てられた小さなストアが検出されず、バランス演算子が生成されない問題を修正します[#4805](https://github.com/tikv/pd/issues/4805)
    -   `SchedulerMaxWaitingOperator`を`1` [#4946](https://github.com/tikv/pd/issues/4946)に設定するとスケジューラーが動作しない問題を修正
    -   ラベル分布がメトリクス[#4825](https://github.com/tikv/pd/issues/4825)に残留ラベルを持つ問題を修正します。

-   TiFlash

    -   無効なstorageディレクトリ構成が予期しない動作を引き起こすバグを修正します[#4093](https://github.com/pingcap/tiflash/issues/4093)
    -   `NOT NULL`列が追加されたときに報告された修正`TiFlash_schema_error` [#4596](https://github.com/pingcap/tiflash/issues/4596)
    -   `commit state jump backward`エラーが原因で繰り返されるクラッシュを修正[#2576](https://github.com/pingcap/tiflash/issues/2576)
    -   多数の INSERT 操作と DELETE 操作の後に発生する可能性のあるデータの不整合を修正します[#4956](https://github.com/pingcap/tiflash/issues/4956)
    -   ローカル トンネルが有効になっている場合、MPP クエリをキャンセルすると、タスクが[#4229](https://github.com/pingcap/tiflash/issues/4229)にハングする可能性があるというバグを修正します。
    -   TiFlash がリモート読み取り[#3713](https://github.com/pingcap/tiflash/issues/3713)を使用する場合に、一貫性のないTiFlashバージョンの誤ったレポートを修正します。
    -   ランダムな gRPC キープアライブ タイムアウト[#4662](https://github.com/pingcap/tiflash/issues/4662)が原因で MPP クエリが失敗する可能性があるバグを修正します
    -   交換レシーバーで再試行がある場合、MPP クエリが永久にハングする可能性があるというバグを修正します[#3444](https://github.com/pingcap/tiflash/issues/3444)
    -   `DATETIME`から`DECIMAL` [#4151](https://github.com/pingcap/tiflash/issues/4151)をキャストしたときに発生する誤った結果を修正します
    -   `FLOAT`から`DECIMAL` [#3998](https://github.com/pingcap/tiflash/issues/3998)へのキャスト時に発生するオーバーフローを修正
    -   空の文字列[#2705](https://github.com/pingcap/tiflash/issues/2705)で`json_length`を呼び出すと発生する可能性のある`index out of bounds`エラーを修正
    -   コーナーケースで間違った小数比較結果を修正する[#4512](https://github.com/pingcap/tiflash/issues/4512)
    -   結合ビルド ステージ[#4195](https://github.com/pingcap/tiflash/issues/4195)でクエリが失敗した場合、MPP クエリが永久にハングする可能性があるバグを修正
    -   クエリに`where <string>`句[#3447](https://github.com/pingcap/tiflash/issues/3447)が含まれている場合に発生する可能性のある間違った結果を修正します
    -   `CastStringAsReal`動作がTiFlashと TiDB または TiKV [#3475](https://github.com/pingcap/tiflash/issues/3475)で一貫していない問題を修正
    -   文字列を日時[#3556](https://github.com/pingcap/tiflash/issues/3556)にキャストするときの誤った`microsecond`を修正
    -   削除操作が多いテーブルに対してクエリを実行するときに発生する可能性のあるエラーを修正します[#4747](https://github.com/pingcap/tiflash/issues/4747)
    -   TiFlashが多数の &quot;Keepalive watchdog の起動&quot; エラーをランダムに報告するバグを修正[#4192](https://github.com/pingcap/tiflash/issues/4192)
    -   どのリージョン範囲とも一致しないデータがTiFlashノード[#4414](https://github.com/pingcap/tiflash/issues/4414)に残るバグを修正
    -   MPP タスクがスレッドを永久にリークする可能性があるバグを修正します[#4238](https://github.com/pingcap/tiflash/issues/4238)
    -   GC [#4511](https://github.com/pingcap/tiflash/issues/4511)の後で空のセグメントをマージできないバグを修正
    -   TLS が有効になっているときに発生するpanicの問題を修正します[#4196](https://github.com/pingcap/tiflash/issues/4196)
    -   期限切れのデータがゆっくりとリサイクルされる問題を修正します[#4146](https://github.com/pingcap/tiflash/issues/4146)
    -   無効なstorageディレクトリ構成が予期しない動作を引き起こすバグを修正します[#4093](https://github.com/pingcap/tiflash/issues/4093)
    -   一部の例外が適切に処理されないバグを修正[#4101](https://github.com/pingcap/tiflash/issues/4101)
    -   重い読み取りワークロードの下で列を追加した後の潜在的なクエリ エラーを修正します[#3967](https://github.com/pingcap/tiflash/issues/3967)
    -   `STR_TO_DATE()`関数がマイクロ秒の解析時に先頭のゼロを正しく処理しないというバグを修正します[#3557](https://github.com/pingcap/tiflash/issues/3557)
    -   TiFlash が再起動後に`EstablishMPPConnection`エラーを返す場合がある問題を修正[#3615](https://github.com/pingcap/tiflash/issues/3615)

-   ツール

    -   バックアップと復元 (BR)

        -   増分復元後にテーブルにレコードを挿入するときに重複する主キーを修正する[#33596](https://github.com/pingcap/tidb/issues/33596)
        -   BRまたはTiDB Lightning が異常終了した後、スケジューラが再開されない問題を修正します[#33546](https://github.com/pingcap/tidb/issues/33546)
        -   空のクエリを持つ DDL ジョブが原因で、 BR増分復元が誤ってエラーを返すバグを修正します[#33322](https://github.com/pingcap/tidb/issues/33322)
        -   復元中にリージョンが一致しない場合、 BR が十分な回数再試行しないという問題を修正します[#33419](https://github.com/pingcap/tidb/issues/33419)
        -   復元操作がいくつかの回復不能なエラーに遭遇したときにBR がスタックするバグを修正します[#33200](https://github.com/pingcap/tidb/issues/33200)
        -   BR がRawKV [#32607](https://github.com/pingcap/tidb/issues/32607)のバックアップに失敗する問題を修正
        -   BR がS3 内部エラーを処理できない問題を修正します[#34350](https://github.com/pingcap/tidb/issues/34350)

    -   TiCDC

        -   所有者の変更による不正確な指標の修正[#4774](https://github.com/pingcap/tiflow/issues/4774)
        -   REDO ログマネージャがログを書き込む前にログをフラッシュするバグを修正[#5486](https://github.com/pingcap/tiflow/issues/5486)
        -   一部のテーブルが REDO ライターによって維持されていない場合、解決された ts の移動が速すぎるというバグを修正します[#5486](https://github.com/pingcap/tiflow/issues/5486)
        -   UUID サフィックスを REDO ログ ファイル名に追加して、ファイル名の競合によってデータが失われる可能性があるという問題を修正します[#5486](https://github.com/pingcap/tiflow/issues/5486)
        -   MySQL Sink が誤ったチェックポイントを保存する可能性があるバグを修正Ts [#5107](https://github.com/pingcap/tiflow/issues/5107)
        -   アップグレード後に TiCDC クラスターがpanicになる可能性がある問題を修正します[#5266](https://github.com/pingcap/tiflow/issues/5266)
        -   テーブルが同じノード[#4464](https://github.com/pingcap/tiflow/issues/4464)で繰り返しスケジュールされると、changefeed が停止する問題を修正します。
        -   TLS が有効になった後、 `--pd`で設定された最初の PD が使用できない場合、TiCDC が開始に失敗する問題を修正します[#4777](https://github.com/pingcap/tiflow/issues/4777)
        -   PD ノードが異常な場合、オープン API を介したステータスのクエリがブロックされる可能性があるバグを修正します[#4778](https://github.com/pingcap/tiflow/issues/4778)
        -   Unified Sorter [#4447](https://github.com/pingcap/tiflow/issues/4447)が使用するワーカープールの安定性の問題を修正
        -   場合によってはシーケンスが正しく複製されないというバグを修正[#4563](https://github.com/pingcap/tiflow/issues/4552)

    -   TiDB データ移行 (DM)

        -   タスクが自動的に再開された後、DM がより多くのディスク領域を占有する問題を修正します[#3734](https://github.com/pingcap/tiflow/issues/3734) [#5344](https://github.com/pingcap/tiflow/issues/5344)
        -   `case-sensitive: true`が設定されていない場合に大文字のテーブルが複製されない問題を修正します[#5255](https://github.com/pingcap/tiflow/issues/5255)
        -   フィルタリングされた DDL をダウンストリームで手動で実行すると、タスクの再開に失敗する場合があるという問題を修正します[#5272](https://github.com/pingcap/tiflow/issues/5272)
        -   主キーが`SHOW CREATE TABLE`ステートメントによって返されるインデックスの先頭にない場合に発生する DM ワーカーpanicの問題を修正します[#5159](https://github.com/pingcap/tiflow/issues/5159)
        -   GTID有効時やタスク自動再開時にCPU使用率が上昇し、大量のログが出力されることがある問題を修正[#5063](https://github.com/pingcap/tiflow/issues/5063)
        -   DM マスターの再起動後にリレー ログが無効になる可能性がある問題を修正します[#4803](https://github.com/pingcap/tiflow/issues/4803)

    -   TiDB Lightning

        -   `auto_increment`列[#27937](https://github.com/pingcap/tidb/issues/27937)の範囲外のデータが原因でローカル バックエンドのインポートが失敗する問題を修正します。
        -   事前チェックでローカル ディスク リソースとクラスタの可用性がチェックされない問題を修正します[#34213](https://github.com/pingcap/tidb/issues/34213)
        -   チェックサム エラー「GC ライフ タイムがトランザクション期間よりも短い」を修正します[#32733](https://github.com/pingcap/tidb/issues/32733)
