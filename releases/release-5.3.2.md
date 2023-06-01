---
title: TiDB 5.3.2 Release Notes
---

# TiDB 5.3.2 リリースノート {#tidb-5-3-2-release-notes}

リリース日：2022年6月29日

TiDB バージョン: 5.3.2

> **警告：**
>
> このバージョンには既知のバグがあるため、v5.3.2 の使用は推奨されません。詳細は[<a href="https://github.com/tikv/tikv/issues/12934">#12934</a>](https://github.com/tikv/tikv/issues/12934)を参照してください。このバグは v5.3.3 で修正されました。 [<a href="/releases/release-5.3.3.md">v5.3.3</a>](/releases/release-5.3.3.md)を使用することをお勧めします。

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   自動 ID が範囲[<a href="https://github.com/pingcap/tidb/issues/29483">#29483</a>](https://github.com/pingcap/tidb/issues/29483)の外にある場合、 `REPLACE`ステートメントが他の行を誤って変更する問題を修正します。

-   PD

    -   Swaggerサーバーのコンパイルをデフォルトで無効にする[<a href="https://github.com/tikv/pd/issues/4932">#4932</a>](https://github.com/tikv/pd/issues/4932)

## 改善点 {#improvements}

-   TiKV

    -   Raftクライアントによるシステムコールを削減し、CPU 効率を向上させます[<a href="https://github.com/tikv/tikv/issues/11309">#11309</a>](https://github.com/tikv/tikv/issues/11309)
    -   ヘルスチェックを改善して、利用できないRaftstoreを検出し、TiKV クライアントが時間内にリージョンキャッシュを更新できるようにします[<a href="https://github.com/tikv/tikv/issues/12398">#12398</a>](https://github.com/tikv/tikv/issues/12398)
    -   リーダーシップを CDC オブザーバーに移管して、レイテンシージッター[<a href="https://github.com/tikv/tikv/issues/12111">#12111</a>](https://github.com/tikv/tikv/issues/12111)を削減します。
    -   Raftログのガベージコレクションモジュールにメトリクスを追加して、モジュール[<a href="https://github.com/tikv/tikv/issues/11374">#11374</a>](https://github.com/tikv/tikv/issues/11374)のパフォーマンスの問題を特定します。

-   ツール

    -   TiDB データ移行 (DM)

        -   Syncer は内部ファイルの書き込みに`/tmp`ではなく DM ワーカーの作業ディレクトリを使用し、タスクの停止後にディレクトリをクリーニングすることをサポートします[<a href="https://github.com/pingcap/tiflow/issues/4107">#4107</a>](https://github.com/pingcap/tiflow/issues/4107)

    -   TiDB Lightning

        -   散乱リージョンをバッチ モードに最適化して、散乱リージョンプロセスの安定性を向上させます[<a href="https://github.com/pingcap/tidb/issues/33618">#33618</a>](https://github.com/pingcap/tidb/issues/33618)

## バグの修正 {#bug-fixes}

-   TiDB

    -   Amazon S3 が圧縮データのサイズを正しく計算できない問題を修正します[<a href="https://github.com/pingcap/tidb/issues/30534">#30534</a>](https://github.com/pingcap/tidb/issues/30534)
    -   楽観的トランザクション モード[<a href="https://github.com/pingcap/tidb/issues/30410">#30410</a>](https://github.com/pingcap/tidb/issues/30410)での潜在的なデータ インデックスの不一致の問題を修正します。
    -   JSON 型の列が`CHAR`型の列[<a href="https://github.com/pingcap/tidb/issues/29401">#29401</a>](https://github.com/pingcap/tidb/issues/29401)に結合すると SQL 操作がキャンセルされる問題を修正
    -   以前は、ネットワーク接続の問題が発生した場合、TiDB は切断されたセッションによって保持されているリソースを常に正しく解放するとは限りませんでした。この問題は修正され、開いているトランザクションをロールバックして、その他の関連リソースを解放できるようになりました。 [<a href="https://github.com/pingcap/tidb/issues/34722">#34722</a>](https://github.com/pingcap/tidb/issues/34722)
    -   TiDB Binlogを有効にして重複した値を挿入すると発生する`data and columnID count not match`エラーの問題を修正します[<a href="https://github.com/pingcap/tidb/issues/33608">#33608</a>](https://github.com/pingcap/tidb/issues/33608)
    -   RC 分離レベル[<a href="https://github.com/pingcap/tidb/issues/34447">#34447</a>](https://github.com/pingcap/tidb/issues/34447)でプラン キャッシュを開始すると、クエリ結果が間違っていることがある問題を修正
    -   MySQL バイナリ プロトコル[<a href="https://github.com/pingcap/tidb/issues/33509">#33509</a>](https://github.com/pingcap/tidb/issues/33509)でテーブル スキーマを変更した後にプリペアドステートメントを実行するときに発生するセッションpanicを修正しました。
    -   新しいパーティションの追加時にテーブル属性のインデックスが作成されない問題と、パーティションの変更時にテーブル範囲情報が更新されない問題を修正します[<a href="https://github.com/pingcap/tidb/issues/33929">#33929</a>](https://github.com/pingcap/tidb/issues/33929)
    -   `INFORMATION_SCHEMA.CLUSTER_SLOW_QUERY`テーブルがクエリされるときに TiDBサーバーがメモリ不足になる可能性がある問題を修正します。この問題は、Grafana ダッシュボード[<a href="https://github.com/pingcap/tidb/issues/33893">#33893</a>](https://github.com/pingcap/tidb/issues/33893)で遅いクエリをチェックすると発生する可能性があります。
    -   クラスターの PD ノードが交換された後、一部の DDL ステートメントが一定期間スタックすることがある問題を修正します[<a href="https://github.com/pingcap/tidb/issues/33908">#33908</a>](https://github.com/pingcap/tidb/issues/33908)
    -   v4.0 [<a href="https://github.com/pingcap/tidb/issues/33588">#33588</a>](https://github.com/pingcap/tidb/issues/33588)からアップグレードされたクラスターで`all`権限の付与が失敗する場合がある問題を修正
    -   `left join` [<a href="https://github.com/pingcap/tidb/issues/31321">#31321</a>](https://github.com/pingcap/tidb/issues/31321)を使用して複数のテーブルのデータを削除した場合の誤った結果を修正
    -   TiDB が重複したタスクをTiFlash [<a href="https://github.com/pingcap/tidb/issues/32814">#32814</a>](https://github.com/pingcap/tidb/issues/32814)にディスパッチする可能性があるバグを修正
    -   TiDB のバックグラウンド HTTP サービスが正常に終了せず、クラスターが異常な状態になる場合がある問題を修正します[<a href="https://github.com/pingcap/tidb/issues/30571">#30571</a>](https://github.com/pingcap/tidb/issues/30571)
    -   `fatal error: concurrent map read and map write`エラー[<a href="https://github.com/pingcap/tidb/issues/35340">#35340</a>](https://github.com/pingcap/tidb/issues/35340)によって引き起こされるpanicの問題を修正

-   TiKV

    -   PD クライアントでエラー[<a href="https://github.com/tikv/tikv/issues/12345">#12345</a>](https://github.com/tikv/tikv/issues/12345)が発生したときに発生する PD クライアントの再接続が頻繁に発生する問題を修正します。
    -   `DATETIME`値に小数と`Z` [<a href="https://github.com/tikv/tikv/issues/12739">#12739</a>](https://github.com/tikv/tikv/issues/12739)が含まれる場合に発生する時刻解析エラーの問題を修正します。
    -   空の文字列の型変換を実行すると TiKV がパニックになる問題を修正[<a href="https://github.com/tikv/tikv/issues/12673">#12673</a>](https://github.com/tikv/tikv/issues/12673)
    -   非同期コミットが有効になっている場合に、悲観的トランザクションで発生する可能性のある重複コミット レコードを修正します[<a href="https://github.com/tikv/tikv/issues/12615">#12615</a>](https://github.com/tikv/tikv/issues/12615)
    -   Follower Read [<a href="https://github.com/tikv/tikv/issues/12478">#12478</a>](https://github.com/tikv/tikv/issues/12478)使用時にTiKVが`invalid store ID 0`エラーを報告するバグを修正
    -   ピアの破棄とリージョン[<a href="https://github.com/tikv/tikv/issues/12368">#12368</a>](https://github.com/tikv/tikv/issues/12368)のバッチ分割の間の競合によって引き起こされる TiKVpanicの問題を修正します。
    -   ネットワークが貧弱な場合、正常にコミットされた楽観的トランザクションが`Write Conflict`エラーを報告する可能性がある問題を修正します[<a href="https://github.com/pingcap/tidb/issues/34066">#34066</a>](https://github.com/pingcap/tidb/issues/34066)
    -   マージ対象のターゲットリージョンが無効な場合、TiKV がパニックを起こして予期せずピアを破棄する問題を修正します[<a href="https://github.com/tikv/tikv/issues/12232">#12232</a>](https://github.com/tikv/tikv/issues/12232)
    -   古いメッセージによって TiKV がpanicになるバグを修正[<a href="https://github.com/tikv/tikv/issues/12023">#12023</a>](https://github.com/tikv/tikv/issues/12023)
    -   メモリメトリクス[<a href="https://github.com/tikv/tikv/issues/12160">#12160</a>](https://github.com/tikv/tikv/issues/12160)のオーバーフローによって引き起こされる断続的なパケット損失とメモリ不足 (OOM) の問題を修正します。
    -   TiKV が Ubuntu 18.04 でプロファイリングを実行するときに発生する潜在的なpanicの問題を修正します[<a href="https://github.com/tikv/tikv/issues/9765">#9765</a>](https://github.com/tikv/tikv/issues/9765)
    -   間違った文字列一致[<a href="https://github.com/tikv/tikv/issues/12329">#12329</a>](https://github.com/tikv/tikv/issues/12329)が原因で tikv-ctl が間違った結果を返す問題を修正
    -   レプリカの読み取りが線形化可能性[<a href="https://github.com/tikv/tikv/issues/12109">#12109</a>](https://github.com/tikv/tikv/issues/12109)に違反する可能性があるバグを修正
    -   リージョン[<a href="https://github.com/tikv/tikv/issues/12048">#12048</a>](https://github.com/tikv/tikv/issues/12048)をマージするときに、ターゲット ピアが初期化されずに破棄されたピアに置き換えられるときに発生する TiKVpanicの問題を修正します。
    -   TiKV が 2 年以上実行されている場合にpanicになる可能性があるバグを修正[<a href="https://github.com/tikv/tikv/issues/11940">#11940</a>](https://github.com/tikv/tikv/issues/11940)

-   PD

    -   ホット リージョンにリーダー[<a href="https://github.com/tikv/pd/issues/5005">#5005</a>](https://github.com/tikv/pd/issues/5005)がない場合に発生する PDpanicを修正しました。
    -   PDリーダー転送[<a href="https://github.com/tikv/pd/issues/4769">#4769</a>](https://github.com/tikv/pd/issues/4769)直後にスケジューリングが開始できない問題を修正
    -   PDリーダー移転後、削除された墓石ストアが再び表示される問題を修正[<a href="https://github.com/tikv/pd/issues/4941">#4941</a>](https://github.com/tikv/pd/issues/4941)
    -   いくつかの特殊なケースにおける TSO フォールバックのバグを修正[<a href="https://github.com/tikv/pd/issues/4884">#4884</a>](https://github.com/tikv/pd/issues/4884)
    -   大容量のストア（たとえば 2T）が存在する場合、完全に割り当てられた小さなストアが検出できず、バランス演算子が生成されない問題を修正します[<a href="https://github.com/tikv/pd/issues/4805">#4805</a>](https://github.com/tikv/pd/issues/4805)
    -   `SchedulerMaxWaitingOperator`を`1` [<a href="https://github.com/tikv/pd/issues/4946">#4946</a>](https://github.com/tikv/pd/issues/4946)に設定するとスケジューラが動作しない問題を修正
    -   ラベル分布のメトリクスに残留ラベルがある問題を修正します[<a href="https://github.com/tikv/pd/issues/4825">#4825</a>](https://github.com/tikv/pd/issues/4825)

-   TiFlash

    -   無効なstorageディレクトリ構成が予期せぬ動作を引き起こすバグを修正[<a href="https://github.com/pingcap/tiflash/issues/4093">#4093</a>](https://github.com/pingcap/tiflash/issues/4093)
    -   `NOT NULL`列が追加されたときに報告される`TiFlash_schema_error`修正[<a href="https://github.com/pingcap/tiflash/issues/4596">#4596</a>](https://github.com/pingcap/tiflash/issues/4596)
    -   `commit state jump backward`エラー[<a href="https://github.com/pingcap/tiflash/issues/2576">#2576</a>](https://github.com/pingcap/tiflash/issues/2576)によって引き起こされる繰り返しのクラッシュを修正
    -   多数の INSERT および DELETE 操作後の潜在的なデータの不整合を修正[<a href="https://github.com/pingcap/tiflash/issues/4956">#4956</a>](https://github.com/pingcap/tiflash/issues/4956)
    -   ローカル トンネルが有効になっている場合、MPP クエリをキャンセルするとタスクが永久にハングする可能性があるバグを修正します[<a href="https://github.com/pingcap/tiflash/issues/4229">#4229</a>](https://github.com/pingcap/tiflash/issues/4229)
    -   TiFlash がリモート読み取り[<a href="https://github.com/pingcap/tiflash/issues/3713">#3713</a>](https://github.com/pingcap/tiflash/issues/3713)を使用する場合、 TiFlashバージョンが一貫していないという誤ったレポートを修正しました。
    -   ランダムな gRPC キープアライブ タイムアウトにより MPP クエリが失敗する可能性があるバグを修正[<a href="https://github.com/pingcap/tiflash/issues/4662">#4662</a>](https://github.com/pingcap/tiflash/issues/4662)
    -   交換レシーバー[<a href="https://github.com/pingcap/tiflash/issues/3444">#3444</a>](https://github.com/pingcap/tiflash/issues/3444)で再試行がある場合、MPP クエリが永久にハングする可能性があるバグを修正
    -   `DATETIME`から`DECIMAL` [<a href="https://github.com/pingcap/tiflash/issues/4151">#4151</a>](https://github.com/pingcap/tiflash/issues/4151)をキャストするときに発生する間違った結果を修正
    -   `FLOAT` ～ `DECIMAL` [<a href="https://github.com/pingcap/tiflash/issues/3998">#3998</a>](https://github.com/pingcap/tiflash/issues/3998)キャスト時に発生するオーバーフローを修正
    -   空の文字列[<a href="https://github.com/pingcap/tiflash/issues/2705">#2705</a>](https://github.com/pingcap/tiflash/issues/2705)で`json_length`を呼び出した場合の潜在的な`index out of bounds`エラーを修正
    -   特殊なケースでの間違った 10 進比較結果を修正[<a href="https://github.com/pingcap/tiflash/issues/4512">#4512</a>](https://github.com/pingcap/tiflash/issues/4512)
    -   クエリが結合ビルド ステージ[<a href="https://github.com/pingcap/tiflash/issues/4195">#4195</a>](https://github.com/pingcap/tiflash/issues/4195)で失敗した場合、MPP クエリが永久にハングする可能性があるバグを修正
    -   クエリに`where <string>`句[<a href="https://github.com/pingcap/tiflash/issues/3447">#3447</a>](https://github.com/pingcap/tiflash/issues/3447)が含まれる場合に発生する可能性のある間違った結果を修正
    -   TiFlashと TiDB または TiKV [<a href="https://github.com/pingcap/tiflash/issues/3475">#3475</a>](https://github.com/pingcap/tiflash/issues/3475)で`CastStringAsReal`動作が矛盾する問題を修正
    -   文字列を日時[<a href="https://github.com/pingcap/tiflash/issues/3556">#3556</a>](https://github.com/pingcap/tiflash/issues/3556)にキャストするときの誤った`microsecond`を修正
    -   多くの削除操作を含むテーブルに対してクエリを実行する際の潜在的なエラーを修正します[<a href="https://github.com/pingcap/tiflash/issues/4747">#4747</a>](https://github.com/pingcap/tiflash/issues/4747)
    -   TiFlashが多数の「Keepalive watchdog fired」エラーをランダムに報告するバグを修正[<a href="https://github.com/pingcap/tiflash/issues/4192">#4192</a>](https://github.com/pingcap/tiflash/issues/4192)
    -   TiFlashノード[<a href="https://github.com/pingcap/tiflash/issues/4414">#4414</a>](https://github.com/pingcap/tiflash/issues/4414)にどのリージョン範囲にも一致しないデータが残るバグを修正
    -   MPP タスクがスレッドを永久にリークする可能性があるバグを修正[<a href="https://github.com/pingcap/tiflash/issues/4238">#4238</a>](https://github.com/pingcap/tiflash/issues/4238)
    -   GC [<a href="https://github.com/pingcap/tiflash/issues/4511">#4511</a>](https://github.com/pingcap/tiflash/issues/4511)以降に空のセグメントをマージできないバグを修正
    -   TLS が有効になっているときに発生するpanicの問題を修正します[<a href="https://github.com/pingcap/tiflash/issues/4196">#4196</a>](https://github.com/pingcap/tiflash/issues/4196)
    -   期限切れデータのリサイクルが遅い問題を修正[<a href="https://github.com/pingcap/tiflash/issues/4146">#4146</a>](https://github.com/pingcap/tiflash/issues/4146)
    -   無効なstorageディレクトリ構成が予期せぬ動作を引き起こすバグを修正[<a href="https://github.com/pingcap/tiflash/issues/4093">#4093</a>](https://github.com/pingcap/tiflash/issues/4093)
    -   一部の例外が正しく処理されないバグを修正[<a href="https://github.com/pingcap/tiflash/issues/4101">#4101</a>](https://github.com/pingcap/tiflash/issues/4101)
    -   重い読み取りワークロードで列を追加した後の潜在的なクエリ エラーを修正[<a href="https://github.com/pingcap/tiflash/issues/3967">#3967</a>](https://github.com/pingcap/tiflash/issues/3967)
    -   `STR_TO_DATE()`関数がマイクロ秒[<a href="https://github.com/pingcap/tiflash/issues/3557">#3557</a>](https://github.com/pingcap/tiflash/issues/3557)を解析する際に先頭のゼロを誤って処理するバグを修正
    -   TiFlashの再起動後に`EstablishMPPConnection`エラーが返されることがある問題を修正[<a href="https://github.com/pingcap/tiflash/issues/3615">#3615</a>](https://github.com/pingcap/tiflash/issues/3615)

-   ツール

    -   バックアップと復元 (BR)

        -   増分復元[<a href="https://github.com/pingcap/tidb/issues/33596">#33596</a>](https://github.com/pingcap/tidb/issues/33596)後にテーブルにレコードを挿入するときの重複した主キーを修正します。
        -   BRまたはTiDB Lightningが異常終了した後にスケジューラが再開しない問題を修正[<a href="https://github.com/pingcap/tidb/issues/33546">#33546</a>](https://github.com/pingcap/tidb/issues/33546)
        -   空のクエリ[<a href="https://github.com/pingcap/tidb/issues/33322">#33322</a>](https://github.com/pingcap/tidb/issues/33322)を含む DDL ジョブによりBR増分リストアが誤ってエラーを返すバグを修正
        -   復元中にリージョンに一貫性がない場合、 BR が十分な回数再試行しない問題を修正[<a href="https://github.com/pingcap/tidb/issues/33419">#33419</a>](https://github.com/pingcap/tidb/issues/33419)
        -   復元操作で回復不能なエラーが発生した場合にBR がスタックするバグを修正[<a href="https://github.com/pingcap/tidb/issues/33200">#33200</a>](https://github.com/pingcap/tidb/issues/33200)
        -   BR がRawKV [<a href="https://github.com/pingcap/tidb/issues/32607">#32607</a>](https://github.com/pingcap/tidb/issues/32607)のバックアップに失敗する問題を修正
        -   BR がS3 内部エラーを処理できない問題を修正[<a href="https://github.com/pingcap/tidb/issues/34350">#34350</a>](https://github.com/pingcap/tidb/issues/34350)

    -   TiCDC

        -   所有者の変更によって引き起こされた誤ったメトリクスを修正する[<a href="https://github.com/pingcap/tiflow/issues/4774">#4774</a>](https://github.com/pingcap/tiflow/issues/4774)
        -   REDO ログ マネージャーがログを書き込む前にログをフラッシュするバグを修正[<a href="https://github.com/pingcap/tiflow/issues/5486">#5486</a>](https://github.com/pingcap/tiflow/issues/5486)
        -   一部のテーブルが REDO ライターによって維持されていない場合、解決された ts の移動が速すぎるバグを修正[<a href="https://github.com/pingcap/tiflow/issues/5486">#5486</a>](https://github.com/pingcap/tiflow/issues/5486)
        -   UUID サフィックスを REDO ログ ファイル名に追加して、ファイル名の競合によってデータ損失が発生する可能性がある問題を修正します[<a href="https://github.com/pingcap/tiflow/issues/5486">#5486</a>](https://github.com/pingcap/tiflow/issues/5486)
        -   MySQL シンクが間違ったチェックポイント Ts [<a href="https://github.com/pingcap/tiflow/issues/5107">#5107</a>](https://github.com/pingcap/tiflow/issues/5107)を保存する可能性があるバグを修正
        -   アップグレード[<a href="https://github.com/pingcap/tiflow/issues/5266">#5266</a>](https://github.com/pingcap/tiflow/issues/5266)後に TiCDC クラスターがpanicになる可能性がある問題を修正
        -   同じノード[<a href="https://github.com/pingcap/tiflow/issues/4464">#4464</a>](https://github.com/pingcap/tiflow/issues/4464)でテーブルが繰り返しスケジュールされると、変更フィードがスタックする問題を修正します。
        -   TLS を有効にした後、 `--pd`で設定した最初の PD が利用できない場合に TiCDC が起動できない問題を修正[<a href="https://github.com/pingcap/tiflow/issues/4777">#4777</a>](https://github.com/pingcap/tiflow/issues/4777)
        -   PDノードが異常[<a href="https://github.com/pingcap/tiflow/issues/4778">#4778</a>](https://github.com/pingcap/tiflow/issues/4778)の場合、オープンAPIによるステータス問い合わせがブロックされる場合があるバグを修正
        -   Unified Sorter [<a href="https://github.com/pingcap/tiflow/issues/4447">#4447</a>](https://github.com/pingcap/tiflow/issues/4447)によって使用されるワーカープールの安定性の問題を修正しました。
        -   場合によってはシーケンスが不正に複製されるバグを修正[<a href="https://github.com/pingcap/tiflow/issues/4552">#4563</a>](https://github.com/pingcap/tiflow/issues/4552)

    -   TiDB データ移行 (DM)

        -   タスクが自動的に再開された後、DM がより多くのディスク領域を占有する問題を修正[<a href="https://github.com/pingcap/tiflow/issues/3734">#3734</a>](https://github.com/pingcap/tiflow/issues/3734) [<a href="https://github.com/pingcap/tiflow/issues/5344">#5344</a>](https://github.com/pingcap/tiflow/issues/5344)
        -   `case-sensitive: true`が設定されていない場合、大文字のテーブルが複製できない問題を修正します[<a href="https://github.com/pingcap/tiflow/issues/5255">#5255</a>](https://github.com/pingcap/tiflow/issues/5255)
        -   場合によっては、フィルタリングされた DDL をダウンストリームで手動で実行すると、タスクの再開が失敗する可能性がある問題を修正します[<a href="https://github.com/pingcap/tiflow/issues/5272">#5272</a>](https://github.com/pingcap/tiflow/issues/5272)
        -   `SHOW CREATE TABLE`ステートメント[<a href="https://github.com/pingcap/tiflow/issues/5159">#5159</a>](https://github.com/pingcap/tiflow/issues/5159)によって返されるインデックスの先頭に主キーがない場合に発生する DM ワーカーのpanic問題を修正します。
        -   GTID が有効になっている場合、またはタスクが自動的に再開された場合に、CPU 使用率が増加し、大量のログが出力される場合がある問題を修正します[<a href="https://github.com/pingcap/tiflow/issues/5063">#5063</a>](https://github.com/pingcap/tiflow/issues/5063)
        -   DM マスターの再起動後にリレー ログが無効になる場合がある問題を修正します[<a href="https://github.com/pingcap/tiflow/issues/4803">#4803</a>](https://github.com/pingcap/tiflow/issues/4803)

    -   TiDB Lightning

        -   `auto_increment`列[<a href="https://github.com/pingcap/tidb/issues/27937">#27937</a>](https://github.com/pingcap/tidb/issues/27937)の範囲外データが原因でローカル バックエンドのインポートが失敗する問題を修正
        -   事前チェックでローカル ディスク リソースとクラスターの可用性がチェックされない問題を修正します[<a href="https://github.com/pingcap/tidb/issues/34213">#34213</a>](https://github.com/pingcap/tidb/issues/34213)
        -   チェックサム エラー「GC ライフタイムがトランザクション期間よりも短い」を修正します[<a href="https://github.com/pingcap/tidb/issues/32733">#32733</a>](https://github.com/pingcap/tidb/issues/32733)
