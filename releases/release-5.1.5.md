---
title: TiDB 5.1.5 Release Notes
summary: TiDB 5.1.5は2022年12月28日にリリースされました。このリリースには、TiDB、TiKV、PD、 TiFlash、および各種ツールの互換性の変更と多数のバグ修正が含まれています。バグ修正では、パニック、誤った結果、不適切な動作などの問題に対処しています。また、データ損失、メモリ使用量、および不正確なメトリックに関連する問題も修正されています。
---

# TiDB 5.1.5 リリースノート {#tidb-5-1-5-release-notes}

発売日：2022年12月28日

TiDBバージョン：5.1.5

クイックアクセス: [クイックスタート](https://docs-archive.pingcap.com/tidb/v5.1/quick-start-with-tidb)| [本番環境への展開](https://docs-archive.pingcap.com/tidb/v5.1/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   PD

    -   Swaggerサーバーのコンパイルをデフォルトで無効にする [#4932](https://github.com/tikv/pd/issues/4932)

## バグ修正 {#bug-fixes}

-   TiDB

    -   ウィンドウ関数がエラーを報告する代わりにTiDBをpanicにする問題を修正しました [#30326](https://github.com/pingcap/tidb/issues/30326)
    -   TiFlashのパーティションテーブルで動的モードを有効にした際に発生する誤った結果を修正します [#37254](https://github.com/pingcap/tidb/issues/37254)
    -   符号なしの`GREATEST`引数を渡した場合の`LEAST`と`BIGINT`の誤った結果を修正 [#30101](https://github.com/pingcap/tidb/issues/30101)
    -   `left join`を使用して複数のテーブルのデータを削除する際の誤った結果を修正 [#31321](https://github.com/pingcap/tidb/issues/31321)
    -   TiDB における`concat(ifnull(time(3)))`の結果が MySQL における結果と異なる問題を修正しました [#29498](https://github.com/pingcap/tidb/issues/29498)
    -   `cast(integer as char) union string`を含むSQL文が誤った結果を返す問題を修正しました [#29513](https://github.com/pingcap/tidb/issues/29513)
    -   `INL_HASH_JOIN` `LIMIT`と一緒に使用した場合にハングアップする可能性がある問題を修正しました [#35638](https://github.com/pingcap/tidb/issues/35638)
    -   リージョンが空のデータを返した場合に発生する誤った`ANY_VALUE`の結果を修正する [#30923](https://github.com/pingcap/tidb/issues/30923)
    -   innerWorkerのpanicによって発生したインデックス結合の誤った結果を修正 [#31494](https://github.com/pingcap/tidb/issues/31494)
    -   SQL操作がJSON型の列と`CHAR`型の列を結合する際にキャンセルされる問題を修正しました [#29401](https://github.com/pingcap/tidb/issues/29401)
    -   TiDBのバックグラウンドHTTPサービスが正常に終了せず、クラスタが異常な状態になる問題を修正しました [#30571](https://github.com/pingcap/tidb/issues/30571)
    -   同時実行される列型変更によってスキーマとデータの間に不整合が生じる問題を修正します [#31048](https://github.com/pingcap/tidb/issues/31048)
    -   `KILL TIDB`がアイドル状態の接続で即座に有効にならない問題を修正します [#24031](https://github.com/pingcap/tidb/issues/24031)
    -   セッション変数を設定すると`tidb_snapshot`が機能しなくなるバグを修正しました [#35515](https://github.com/pingcap/tidb/issues/35515)
    -   リージョンがマージされた際にリージョンキャッシュが時間内にクリーンアップされない問題を修正します [#37141](https://github.com/pingcap/tidb/issues/37141)
    -   KVクライアントの接続配列競合によって発生するpanic問題を修正 [#33773](https://github.com/pingcap/tidb/issues/33773)
    -   TiDB Binlogが有効になっている場合、 `ALTER SEQUENCE`ステートメントを実行すると、メタデータのバージョンが間違っていて、 Drainerが終了する可能性がある問題を修正しました。 [#36276](https://github.com/pingcap/tidb/issues/36276)
    -   TiDBがステートメントサマリーテーブルをクエリする際にpanic可能性があるバグを修正しました [#35340](https://github.com/pingcap/tidb/issues/35340)
    -   TiFlashがまだ空の範囲のテーブル読み取りをサポートしていないにもかかわらず、TiDBが空の範囲のテーブルをスキャンする際に誤った結果を取得する問題を修正します。 [#33083](https://github.com/pingcap/tidb/issues/33083)
    -   TiFlashからクエリを実行した際に`avg()`関数が`ERROR 1105 (HY000): other error for mpp stream: Could not convert to the target type - -value is out of range.`を返す問題を修正しました。 [#29952](https://github.com/pingcap/tidb/issues/29952)
    -   `ERROR 1105 (HY000): close of nil channel`を使用した場合に`HashJoinExec`が返される問題を修正しました [#30289](https://github.com/pingcap/tidb/issues/30289)
    -   TiKVとTiFlashが論理演算を照会した際に異なる結果を返す問題を修正しました [#37258](https://github.com/pingcap/tidb/issues/37258)
    -   `EXECUTE`ステートメントが特定のシナリオで予期しないエラーを発生させる可能性がある問題を修正しました [#37187](https://github.com/pingcap/tidb/issues/37187)
    -   `tidb_opt_agg_push_down`と`tidb_enforce_mpp`が有効になっている場合に発生するプランナーの誤った動作を修正します [#34465](https://github.com/pingcap/tidb/issues/34465)
    -   TiDBが`SHOW COLUMNS`ステートメントを実行する際にコプロセッサ要求を送信する可能性があるバグを修正しました [#36496](https://github.com/pingcap/tidb/issues/36496)
    -   `lock tables`フラグが有効になっていない場合に、 `unlock tables`と`enable-table-lock`に対する警告を追加する [#28967](https://github.com/pingcap/tidb/issues/28967)
    -   範囲パーティションで複数の`MAXVALUE`パーティションが許可される問題を修正 [#36329](https://github.com/pingcap/tidb/issues/36329)

-   TiKV

    -   `DATETIME`値に小数点が含まれる場合と`Z`値が含まれる場合に発生する時間解析エラーの問題を修正します。 [#12739](https://github.com/tikv/tikv/issues/12739)
    -   レプリカ読み取りが線形化可能性に違反する可能性があるバグを修正 [#12109](https://github.com/tikv/tikv/issues/12109)
    -   Raftstoreがビジー状態の場合にリージョンが重複する可能性があるバグを修正しました [#13160](https://github.com/tikv/tikv/issues/13160)
    -   スナップショットの適用が中止された際に発生する TiKVpanicの問題を修正 [#11618](https://github.com/tikv/tikv/issues/11618)
    -   TiKVが2年以上実行されている場合にpanic可能性があるバグを修正しました [#11940](https://github.com/tikv/tikv/issues/11940)
    -   リージョンマージプロセスでソースピアがスナップショットによってログを追いついた際に発生する可能性のpanic問題を修正します [#12663](https://github.com/tikv/tikv/issues/12663)
    -   TiKVが空文字列の型変換を実行する際にパニックを起こす問題を修正しました [#12673](https://github.com/tikv/tikv/issues/12673)
    -   古いメッセージが原因で TiKV がpanicを起こすバグを修正しました [#12023](https://github.com/tikv/tikv/issues/12023)
    -   ピアが分割され、同時に破棄される際に発生する可能性のあるpanic問題を修正します [#12825](https://github.com/tikv/tikv/issues/12825)
    -   リージョンをマージする際に、初期化されずに破棄されたピアでターゲットピアが置き換えられた場合に発生する TiKVpanicの問題を修正します [#12048](https://github.com/tikv/tikv/issues/12048)
    -   Follower Readを使用する際に TiKV が`invalid store ID 0`エラーを報告する問題を修正しました [#12478](https://github.com/tikv/tikv/issues/12478)
    -   非同期コミットが有効になっている場合に、悲観的トランザクションで発生する可能性のある重複コミットレコードを修正する [#12615](https://github.com/tikv/tikv/issues/12615)
    -   ピアの1つが到達不能になった後にRaftstoreがメッセージを過剰にブロードキャストするのを回避するために`unreachable_backoff`アイテムの設定をサポートします [#13054](https://github.com/tikv/tikv/issues/13054)
    -   ネットワークの状態が悪い場合、正常にコミットされた楽観的トランザクションが`Write Conflict`エラーを報告する可能性がある問題を修正します [#34066](https://github.com/pingcap/tidb/issues/34066)
    -   ダッシュボード内の`Unified Read Pool CPU`の誤った表現を修正 [#13086](https://github.com/tikv/tikv/issues/13086)

-   PD

    -   PDリーダーの移籍後に削除されたtombstoneストアが再び表示される問題を修正しました[#4941](https://github.com/tikv/pd/issues/4941)
    -   PDリーダーの転送後すぐにスケジューリングを開始できない問題を修正します [#4769](https://github.com/tikv/pd/issues/4769)
    -   `not leader` の誤ったステータスコードを修正します。 [#4797](https://github.com/tikv/pd/issues/4797)
    -   PDがダッシュボードプロキシ要求を正しく処理できない問題を修正 [#5321](https://github.com/tikv/pd/issues/5321)
    -   TSOフォールバックの特定の特殊ケースにおけるバグを修正 [#4884](https://github.com/tikv/pd/issues/4884)
    -   特定のシナリオでTiFlashラーナーレプリカが作成されない可能性がある問題を修正しました [#5401](https://github.com/tikv/pd/issues/5401)
    -   ラベル分布にメトリクスに残余ラベルが含まれる問題を修正 [#4825](https://github.com/tikv/pd/issues/4825)
    -   大容量（例えば2T）のストアが存在する場合、完全に割り当てられた小型ストアを検出できず、結果としてバランス演算子が生成されない問題を修正します [#4805](https://github.com/tikv/pd/issues/4805)
    -   `SchedulerMaxWaitingOperator`が`1`に設定されている場合、スケジューラが機能しない問題を修正します。 [#4946](https://github.com/tikv/pd/issues/4946)

-   TiFlash

    -   文字列をdatetimeにキャストした際に`microsecond`正しく表示されない問題を修正 [#3556](https://github.com/pingcap/tiflash/issues/3556)
    -   TLSが有効になっているときに発生するpanic問題を修正 [#4196](https://github.com/pingcap/tiflash/issues/4196)
    -   並列集計のエラーによりTiFlashがクラッシュする可能性があるバグを修正しました [#5356](https://github.com/pingcap/tiflash/issues/5356)
    -   `JOIN`を含むクエリでエラーが発生した場合にハングアップする可能性がある問題を修正しました [#4195](https://github.com/pingcap/tiflash/issues/4195)
    -   関数`OR`が誤った結果を返す問題を修正しました [#5849](https://github.com/pingcap/tiflash/issues/5849)
    -   無効なストレージディレクトリ構成が予期しない動作を引き起こすバグを修正 [#4093](https://github.com/pingcap/tiflash/issues/4093)
    -   多数のINSERTおよびDELETE操作後に発生する可能性のあるデータ不整合を修正する [#4956](https://github.com/pingcap/tiflash/issues/4956)
    -   リージョン範囲に一致しないデータがTiFlashノード上に残ってしまうバグを修正しました [#4414](https://github.com/pingcap/tiflash/issues/4414)
    -   読み取り負荷の高い環境で列を追加した後に発生する可能性のあるクエリエラーを修正する [#3967](https://github.com/pingcap/tiflash/issues/3967)
    -   `commit state jump backward`エラーによる繰り返し発生するクラッシュを修正 [#2576](https://github.com/pingcap/tiflash/issues/2576)
    -   削除操作が多数含まれるテーブルをクエリする際に発生する可能性のあるエラーを修正 [#4747](https://github.com/pingcap/tiflash/issues/4747)
    -   日付フォーマットが`''`無効な区切り文字として認識する問題を修正 [#4036](https://github.com/pingcap/tiflash/issues/4036)
    -   `DATETIME`を`DECIMAL`にキャストした際に発生する誤った結果を修正します [#4151](https://github.com/pingcap/tiflash/issues/4151)
    -   一部の例外が正しく処理されないバグを修正 [#4101](https://github.com/pingcap/tiflash/issues/4101)
    -   `Prepare Merge`ラフトストアのメタデータを破損させ、 TiFlashが再起動する可能性がある問題を修正しました [#3435](https://github.com/pingcap/tiflash/issues/3435)
    -   ランダムなgRPCキープアライブタイムアウトによりMPPクエリが失敗する可能性があるバグを修正しました [#4662](https://github.com/pingcap/tiflash/issues/4662)
    -   `IN`の結果が複数値式で正しくない問題を修正 [#4016](https://github.com/pingcap/tiflash/issues/4016)
    -   MPPタスクがスレッドを永久にリークする可能性があるバグを修正 [#4238](https://github.com/pingcap/tiflash/issues/4238)
    -   期限切れデータの再利用が遅い問題を修正 [#4146](https://github.com/pingcap/tiflash/issues/4146)
    -   `FLOAT`を`DECIMAL`にキャストする際に発生するオーバーフローを修正します [#3998](https://github.com/pingcap/tiflash/issues/3998)
    -   論理演算子が引数の型がUInt8の場合に誤った結果を返す問題を修正しました [#6127](https://github.com/pingcap/tiflash/issues/6127)
    -   `index out of bounds`を空の文字列で呼び出した場合に発生する可能性のある`json_length`エラーを修正 [#2705](https://github.com/pingcap/tiflash/issues/2705)
    -   コーナーケースにおける誤った小数点比較結果を修正 [#4512](https://github.com/pingcap/tiflash/issues/4512)
    -   `TiFlash_schema_error`列を追加した際に`NOT NULL`が報告される問題を修正 [#4596](https://github.com/pingcap/tiflash/issues/4596)
    -   整数のデフォルト値として`0.0`を使用した場合にTiFlashブートストラップが失敗する問題を修正します (例: `` `i` int(11) NOT NULL DEFAULT '0.0'`` [#3157](https://github.com/pingcap/tiflash/issues/3157)

-   ツール

    -   TiDB Binlog

        -   `compressor`が`zip`に設定されている場合、 Drainer がPumpにリクエストを正しく送信できない問題を修正します。 [#1152](https://github.com/pingcap/tidb-binlog/issues/1152)

    -   Backup & Restore (BR)

        -   システムテーブルの同時バックアップによってテーブル名の更新が失敗し、システムテーブルを復元できない問題を修正しました [#29710](https://github.com/pingcap/tidb/issues/29710)

    -   TiCDC

        -   特殊な増分スキャンシナリオで発生するデータ損失を修正 [#5468](https://github.com/pingcap/tiflow/issues/5468)
        -   ソーターのメトリクスがない問題を修正 [#5690](https://github.com/pingcap/tiflow/issues/5690)
        -   DDLスキーマのバッファリング方法を最適化することで、過剰なメモリ使用量を修正します [#1386](https://github.com/pingcap/tiflow/issues/1386)
