---
title: TiDB 5.3.2 Release Notes
---

# TiDB 5.3.2 リリースノート {#tidb-5-3-2-release-notes}

リリース日：2022年6月29日

TiDB バージョン: 5.3.2

> **警告：**
>
> このバージョンには既知のバグがあるため、v5.3.2 の使用は推奨されません。詳細は[#12934](https://github.com/tikv/tikv/issues/12934)を参照してください。このバグは v5.3.3 で修正されました。 [v5.3.3](/releases/release-5.3.3.md)を使用することをお勧めします。

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   自動 ID が範囲[#29483](https://github.com/pingcap/tidb/issues/29483)の外にある場合、 `REPLACE`ステートメントが他の行を誤って変更する問題を修正します。

-   PD

    -   Swaggerサーバーのコンパイルをデフォルトで無効にする[#4932](https://github.com/tikv/pd/issues/4932)

## 改善点 {#improvements}

-   TiKV

    -   Raftクライアントによるシステムコールを削減し、CPU 効率を向上させます[#11309](https://github.com/tikv/tikv/issues/11309)
    -   ヘルスチェックを改善して、利用できないRaftstoreを検出し、TiKV クライアントが時間内にリージョンキャッシュを更新できるようにします[#12398](https://github.com/tikv/tikv/issues/12398)
    -   リーダーシップを CDC オブザーバーに移管して、レイテンシージッター[#12111](https://github.com/tikv/tikv/issues/12111)を削減します。
    -   Raftログのガベージコレクションモジュールにメトリクスを追加して、モジュール[#11374](https://github.com/tikv/tikv/issues/11374)のパフォーマンスの問題を特定します。

-   ツール

    -   TiDB データ移行 (DM)

        -   Syncer は内部ファイルの書き込みに`/tmp`ではなく DM ワーカーの作業ディレクトリを使用し、タスクの停止後にディレクトリをクリーニングすることをサポートします[#4107](https://github.com/pingcap/tiflow/issues/4107)

    -   TiDB Lightning

        -   散乱リージョンをバッチ モードに最適化して、散乱リージョンプロセスの安定性を向上させます[#33618](https://github.com/pingcap/tidb/issues/33618)

## バグの修正 {#bug-fixes}

-   TiDB

    -   Amazon S3 が圧縮データのサイズを正しく計算できない問題を修正します[#30534](https://github.com/pingcap/tidb/issues/30534)
    -   楽観的トランザクション モード[#30410](https://github.com/pingcap/tidb/issues/30410)での潜在的なデータ インデックスの不一致の問題を修正します。
    -   JSON 型の列が`CHAR`型の列[#29401](https://github.com/pingcap/tidb/issues/29401)に結合すると SQL 操作がキャンセルされる問題を修正
    -   以前は、ネットワーク接続の問題が発生した場合、TiDB は切断されたセッションによって保持されているリソースを常に正しく解放するとは限りませんでした。この問題は修正され、開いているトランザクションをロールバックして、その他の関連リソースを解放できるようになりました。 [#34722](https://github.com/pingcap/tidb/issues/34722)
    -   TiDB Binlogを有効にして重複した値を挿入すると発生する`data and columnID count not match`エラーの問題を修正します[#33608](https://github.com/pingcap/tidb/issues/33608)
    -   RC 分離レベル[#34447](https://github.com/pingcap/tidb/issues/34447)でプラン キャッシュを開始すると、クエリ結果が間違っていることがある問題を修正
    -   MySQL バイナリ プロトコル[#33509](https://github.com/pingcap/tidb/issues/33509)でテーブル スキーマを変更した後にプリペアドステートメントを実行するときに発生するセッションpanicを修正しました。
    -   新しいパーティションの追加時にテーブル属性のインデックスが作成されない問題と、パーティションの変更時にテーブル範囲情報が更新されない問題を修正します[#33929](https://github.com/pingcap/tidb/issues/33929)
    -   `INFORMATION_SCHEMA.CLUSTER_SLOW_QUERY`テーブルがクエリされるときに TiDBサーバーがメモリ不足になる可能性がある問題を修正します。この問題は、Grafana ダッシュボード[#33893](https://github.com/pingcap/tidb/issues/33893)で遅いクエリをチェックすると発生する可能性があります。
    -   クラスターの PD ノードが交換された後、一部の DDL ステートメントが一定期間スタックすることがある問題を修正します[#33908](https://github.com/pingcap/tidb/issues/33908)
    -   v4.0 [#33588](https://github.com/pingcap/tidb/issues/33588)からアップグレードされたクラスターで`all`権限の付与が失敗する場合がある問題を修正
    -   `left join` [#31321](https://github.com/pingcap/tidb/issues/31321)を使用して複数のテーブルのデータを削除した場合の誤った結果を修正
    -   TiDB が重複したタスクをTiFlash [#32814](https://github.com/pingcap/tidb/issues/32814)にディスパッチする可能性があるバグを修正
    -   TiDB のバックグラウンド HTTP サービスが正常に終了せず、クラスターが異常な状態になる場合がある問題を修正します[#30571](https://github.com/pingcap/tidb/issues/30571)
    -   `fatal error: concurrent map read and map write`エラー[#35340](https://github.com/pingcap/tidb/issues/35340)によって引き起こされるpanicの問題を修正

-   TiKV

    -   PD クライアントでエラー[#12345](https://github.com/tikv/tikv/issues/12345)が発生したときに発生する PD クライアントの再接続が頻繁に発生する問題を修正します。
    -   `DATETIME`値に小数と`Z` [#12739](https://github.com/tikv/tikv/issues/12739)が含まれる場合に発生する時刻解析エラーの問題を修正します。
    -   空の文字列の型変換を実行すると TiKV がパニックになる問題を修正[#12673](https://github.com/tikv/tikv/issues/12673)
    -   非同期コミットが有効になっている場合に、悲観的トランザクションで発生する可能性のある重複コミット レコードを修正します[#12615](https://github.com/tikv/tikv/issues/12615)
    -   Follower Read [#12478](https://github.com/tikv/tikv/issues/12478)使用時にTiKVが`invalid store ID 0`エラーを報告するバグを修正
    -   ピアの破棄とリージョン[#12368](https://github.com/tikv/tikv/issues/12368)のバッチ分割の間の競合によって引き起こされる TiKVpanicの問題を修正します。
    -   ネットワークが貧弱な場合、正常にコミットされた楽観的トランザクションが`Write Conflict`エラーを報告する可能性がある問題を修正します[#34066](https://github.com/pingcap/tidb/issues/34066)
    -   マージ対象のターゲットリージョンが無効な場合、TiKV がパニックを起こして予期せずピアを破棄する問題を修正します[#12232](https://github.com/tikv/tikv/issues/12232)
    -   古いメッセージによって TiKV がpanicになるバグを修正[#12023](https://github.com/tikv/tikv/issues/12023)
    -   メモリメトリクス[#12160](https://github.com/tikv/tikv/issues/12160)のオーバーフローによって引き起こされる断続的なパケット損失とメモリ不足 (OOM) の問題を修正します。
    -   TiKV が Ubuntu 18.04 でプロファイリングを実行するときに発生する潜在的なpanicの問題を修正します[#9765](https://github.com/tikv/tikv/issues/9765)
    -   間違った文字列一致[#12329](https://github.com/tikv/tikv/issues/12329)が原因で tikv-ctl が間違った結果を返す問題を修正
    -   レプリカの読み取りが線形化可能性[#12109](https://github.com/tikv/tikv/issues/12109)に違反する可能性があるバグを修正
    -   リージョン[#12048](https://github.com/tikv/tikv/issues/12048)をマージするときに、ターゲット ピアが初期化されずに破棄されたピアに置き換えられるときに発生する TiKVpanicの問題を修正します。
    -   TiKV が 2 年以上実行されている場合にpanicになる可能性があるバグを修正[#11940](https://github.com/tikv/tikv/issues/11940)

-   PD

    -   ホット リージョンにリーダー[#5005](https://github.com/tikv/pd/issues/5005)がない場合に発生する PDpanicを修正しました。
    -   PDリーダー転送[#4769](https://github.com/tikv/pd/issues/4769)直後にスケジューリングが開始できない問題を修正
    -   PDリーダー移転後、削除された墓石ストアが再び表示される問題を修正[#4941](https://github.com/tikv/pd/issues/4941)
    -   いくつかの特殊なケースにおける TSO フォールバックのバグを修正[#4884](https://github.com/tikv/pd/issues/4884)
    -   大容量のストア（たとえば 2T）が存在する場合、完全に割り当てられた小さなストアを検出できず、バランス演算子が生成されない問題を修正します[#4805](https://github.com/tikv/pd/issues/4805)
    -   `SchedulerMaxWaitingOperator`を`1` [#4946](https://github.com/tikv/pd/issues/4946)に設定するとスケジューラが動作しない問題を修正
    -   ラベル分布のメトリクスに残留ラベルがある問題を修正します[#4825](https://github.com/tikv/pd/issues/4825)

-   TiFlash

    -   無効なstorageディレクトリ構成が予期せぬ動作を引き起こすバグを修正[#4093](https://github.com/pingcap/tiflash/issues/4093)
    -   `NOT NULL`列が追加されたときに報告される`TiFlash_schema_error`修正[#4596](https://github.com/pingcap/tiflash/issues/4596)
    -   `commit state jump backward`エラー[#2576](https://github.com/pingcap/tiflash/issues/2576)によって引き起こされる繰り返しのクラッシュを修正
    -   多数の INSERT および DELETE 操作後の潜在的なデータの不整合を修正[#4956](https://github.com/pingcap/tiflash/issues/4956)
    -   ローカル トンネルが有効になっている場合、MPP クエリをキャンセルするとタスクが永久にハングする可能性があるバグを修正します[#4229](https://github.com/pingcap/tiflash/issues/4229)
    -   TiFlash がリモート読み取り[#3713](https://github.com/pingcap/tiflash/issues/3713)を使用する場合、 TiFlashバージョンが一貫していないという誤ったレポートを修正しました。
    -   ランダムな gRPC キープアライブ タイムアウトにより MPP クエリが失敗する可能性があるバグを修正[#4662](https://github.com/pingcap/tiflash/issues/4662)
    -   交換レシーバー[#3444](https://github.com/pingcap/tiflash/issues/3444)で再試行がある場合、MPP クエリが永久にハングする可能性があるバグを修正
    -   `DATETIME`から`DECIMAL` [#4151](https://github.com/pingcap/tiflash/issues/4151)をキャストするときに発生する間違った結果を修正
    -   `FLOAT` ～ `DECIMAL` [#3998](https://github.com/pingcap/tiflash/issues/3998)キャスト時に発生するオーバーフローを修正
    -   空の文字列[#2705](https://github.com/pingcap/tiflash/issues/2705)で`json_length`を呼び出した場合の潜在的な`index out of bounds`エラーを修正
    -   特殊なケースでの間違った 10 進比較結果を修正[#4512](https://github.com/pingcap/tiflash/issues/4512)
    -   クエリが結合ビルド ステージ[#4195](https://github.com/pingcap/tiflash/issues/4195)で失敗した場合、MPP クエリが永久にハングする可能性があるバグを修正
    -   クエリに`where <string>`句[#3447](https://github.com/pingcap/tiflash/issues/3447)が含まれる場合に発生する可能性のある間違った結果を修正
    -   TiFlashと TiDB または TiKV [#3475](https://github.com/pingcap/tiflash/issues/3475)で`CastStringAsReal`動作が矛盾する問題を修正
    -   文字列を日時[#3556](https://github.com/pingcap/tiflash/issues/3556)にキャストするときの誤った`microsecond`を修正
    -   多くの削除操作を含むテーブルに対してクエリを実行する際の潜在的なエラーを修正します[#4747](https://github.com/pingcap/tiflash/issues/4747)
    -   TiFlashが多数の「Keepalive watchdog fired」エラーをランダムに報告するバグを修正[#4192](https://github.com/pingcap/tiflash/issues/4192)
    -   TiFlashノード[#4414](https://github.com/pingcap/tiflash/issues/4414)にどのリージョン範囲にも一致しないデータが残るバグを修正
    -   MPP タスクがスレッドを永久にリークする可能性があるバグを修正[#4238](https://github.com/pingcap/tiflash/issues/4238)
    -   GC [#4511](https://github.com/pingcap/tiflash/issues/4511)以降に空のセグメントをマージできないバグを修正
    -   TLS が有効になっているときに発生するpanicの問題を修正します[#4196](https://github.com/pingcap/tiflash/issues/4196)
    -   期限切れデータのリサイクルが遅い問題を修正[#4146](https://github.com/pingcap/tiflash/issues/4146)
    -   無効なstorageディレクトリ構成が予期せぬ動作を引き起こすバグを修正[#4093](https://github.com/pingcap/tiflash/issues/4093)
    -   一部の例外が正しく処理されないバグを修正[#4101](https://github.com/pingcap/tiflash/issues/4101)
    -   重い読み取りワークロードで列を追加した後の潜在的なクエリ エラーを修正[#3967](https://github.com/pingcap/tiflash/issues/3967)
    -   `STR_TO_DATE()`関数がマイクロ秒[#3557](https://github.com/pingcap/tiflash/issues/3557)を解析する際に先頭のゼロを誤って処理するバグを修正
    -   TiFlashの再起動後に`EstablishMPPConnection`エラーが返されることがある問題を修正[#3615](https://github.com/pingcap/tiflash/issues/3615)

-   ツール

    -   バックアップと復元 (BR)

        -   増分復元[#33596](https://github.com/pingcap/tidb/issues/33596)後にテーブルにレコードを挿入するときの重複した主キーを修正します。
        -   BRまたはTiDB Lightningが異常終了した後にスケジューラが再開しない問題を修正[#33546](https://github.com/pingcap/tidb/issues/33546)
        -   空のクエリ[#33322](https://github.com/pingcap/tidb/issues/33322)を含む DDL ジョブによりBR増分リストアが誤ってエラーを返すバグを修正
        -   復元中にリージョンに一貫性がない場合、 BR が十分な回数再試行しない問題を修正[#33419](https://github.com/pingcap/tidb/issues/33419)
        -   復元操作で回復不能なエラーが発生した場合にBR がスタックするバグを修正[#33200](https://github.com/pingcap/tidb/issues/33200)
        -   BR がRawKV [#32607](https://github.com/pingcap/tidb/issues/32607)のバックアップに失敗する問題を修正
        -   BR がS3 内部エラーを処理できない問題を修正[#34350](https://github.com/pingcap/tidb/issues/34350)

    -   TiCDC

        -   所有者の変更によって引き起こされた誤ったメトリクスを修正する[#4774](https://github.com/pingcap/tiflow/issues/4774)
        -   REDO ログ マネージャーがログを書き込む前にログをフラッシュするバグを修正[#5486](https://github.com/pingcap/tiflow/issues/5486)
        -   一部のテーブルが REDO ライターによって維持されていない場合、解決された ts の移動が速すぎるバグを修正[#5486](https://github.com/pingcap/tiflow/issues/5486)
        -   UUID サフィックスを REDO ログ ファイル名に追加して、ファイル名の競合によってデータ損失が発生する可能性がある問題を修正します[#5486](https://github.com/pingcap/tiflow/issues/5486)
        -   MySQL シンクが間違ったチェックポイント Ts [#5107](https://github.com/pingcap/tiflow/issues/5107)を保存する可能性があるバグを修正
        -   アップグレード[#5266](https://github.com/pingcap/tiflow/issues/5266)後に TiCDC クラスターがpanicになる可能性がある問題を修正
        -   同じノード[#4464](https://github.com/pingcap/tiflow/issues/4464)でテーブルが繰り返しスケジュールされると、変更フィードがスタックする問題を修正します。
        -   TLS を有効にした後、 `--pd`で設定した最初の PD が利用できない場合に TiCDC の起動に失敗する問題を修正[#4777](https://github.com/pingcap/tiflow/issues/4777)
        -   PDノードが異常[#4778](https://github.com/pingcap/tiflow/issues/4778)の場合、オープンAPIによるステータス問い合わせがブロックされる場合があるバグを修正
        -   Unified Sorter [#4447](https://github.com/pingcap/tiflow/issues/4447)によって使用されるワーカープールの安定性の問題を修正しました。
        -   場合によってはシーケンスが不正に複製されるバグを修正[#4563](https://github.com/pingcap/tiflow/issues/4552)

    -   TiDB データ移行 (DM)

        -   タスクが自動的に再開された後、DM がより多くのディスク領域を占有する問題を修正[#3734](https://github.com/pingcap/tiflow/issues/3734) [#5344](https://github.com/pingcap/tiflow/issues/5344)
        -   `case-sensitive: true`が設定されていない場合、大文字のテーブルが複製できない問題を修正します[#5255](https://github.com/pingcap/tiflow/issues/5255)
        -   場合によっては、フィルタリングされた DDL をダウンストリームで手動で実行すると、タスクの再開が失敗する可能性がある問題を修正します[#5272](https://github.com/pingcap/tiflow/issues/5272)
        -   `SHOW CREATE TABLE`ステートメント[#5159](https://github.com/pingcap/tiflow/issues/5159)によって返されるインデックスの先頭に主キーがない場合に発生する DM ワーカーのpanic問題を修正します。
        -   GTID が有効になっている場合、またはタスクが自動的に再開された場合に、CPU 使用率が増加し、大量のログが出力される場合がある問題を修正します[#5063](https://github.com/pingcap/tiflow/issues/5063)
        -   DM マスターの再起動後にリレー ログが無効になる場合がある問題を修正します[#4803](https://github.com/pingcap/tiflow/issues/4803)

    -   TiDB Lightning

        -   `auto_increment`列[#27937](https://github.com/pingcap/tidb/issues/27937)の範囲外データが原因でローカル バックエンドのインポートが失敗する問題を修正
        -   事前チェックでローカル ディスク リソースとクラスターの可用性がチェックされない問題を修正します[#34213](https://github.com/pingcap/tidb/issues/34213)
        -   チェックサム エラー「GC ライフタイムがトランザクション期間よりも短い」を修正します[#32733](https://github.com/pingcap/tidb/issues/32733)
