---
title: Troubleshoot Inconsistency Between Data and Indexes
summary: データとインデックス間の一貫性チェックによって報告されたエラーを処理する方法を学習します。
---

# データとインデックス間の不整合のトラブルシューティング {#troubleshoot-inconsistency-between-data-and-indexes}

TiDB は、トランザクションまたは[`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md)ステートメントを実行するときに、データとインデックス間の一貫性をチェックします。チェックの結果、レコードのキー値と対応するインデックスのキー値が一致していないことが判明した場合、つまり、行データを格納するキー値のペアと、そのインデックスを格納する対応するキー値のペアが一致していない場合 (たとえば、インデックスが多すぎる、またはインデックスが欠落している)、TiDB はデータ不一致エラーを報告し、関連するエラーをエラー ログに出力。

<CustomContent platform="tidb">

このドキュメントでは、データ不整合エラーの意味について説明し、整合性チェックをバイパスする方法をいくつか紹介します。データ整合性エラーが発生した場合は、PingCAP またはコミュニティから[支持を得ます](/support.md)入手できます。

</CustomContent>

<CustomContent platform="tidb-cloud">

このドキュメントでは、データ不整合エラーの意味について説明し、整合性チェックをバイパスする方法をいくつか紹介します。データ整合性エラーが発生した場合は、 [TiDB Cloudサポートにお問い合わせください](/tidb-cloud/tidb-cloud-support.md)実行できます。

</CustomContent>

## エラーの説明 {#error-explanation}

データとインデックスの不整合が発生した場合は、TiDB エラー メッセージを確認して、行データとインデックス データ間でどの項目が不整合であるかを確認したり、関連するエラー ログを確認してさらに調査したりすることができます。

### トランザクション実行中に報告されたエラー {#errors-reported-during-transaction-execution}

このセクションでは、TiDB がトランザクションを実行するときに報告されるデータ不整合エラーをリストし、例を挙げてこれらのエラーの意味を説明します。

#### エラー 8133 {#error-8133}

`ERROR 8133 (HY000): data inconsistency in table: t, index: k2, index-count:1 != record-count:0`

このエラーは、テーブル`t`の`k2`インデックスについて、テーブル内のインデックスの数が 1 であり、行レコードの数が 0 であることを示しています。数値が不一致です。

#### エラー 8138 {#error-8138}

`ERROR 8138 (HY000): writing inconsistent data in table: t, expected-values:{KindString green} != record-values:{KindString GREEN}`

このエラーは、トランザクションが不正な行値を書き込もうとしたことを示します。書き込まれるデータの場合、エンコードされた行データはエンコード前の元のデータと一致しません。

#### エラー 8139 {#error-8139}

`ERROR 8139 (HY000): writing inconsistent data in table: t, index: i1, index-handle:4 != record-handle:3, index: tables.mutation{key:kv.Key{0x74, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x49, 0x5f, 0x69, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x1, 0x1, 0x68, 0x65, 0x6c, 0x6c, 0x6f, 0x0, 0x0, 0x0, 0xfc, 0x1, 0x68, 0x65, 0x6c, 0x6c, 0x6f, 0x0, 0x0, 0x0, 0xfc, 0x3, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x4}, flags:0x0, value:[]uint8{0x30}, indexID:1}, record: tables.mutation{key:kv.Key{0x74, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x49, 0x5f, 0x72, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x3}, flags:0xd, value:[]uint8{0x80, 0x0, 0x2, 0x0, 0x0, 0x0, 0x1, 0x2, 0x5, 0x0, 0xa, 0x0, 0x68, 0x65, 0x6c, 0x6c, 0x6f, 0x68, 0x65, 0x6c, 0x6c, 0x6f}, indexID:0}`

このエラーは、書き込まれるデータのハンドル (つまり、行データのキー) が矛盾していることを示します。表`t`のインデックス`i1`の場合、トランザクションによって書き込まれる行は、インデックス キーと値のペアのハンドルが 4 で、行レコードのキーと値のペアのハンドルが 3 です。この行のデータは書き込まれません。

#### エラー 8140 {#error-8140}

`ERROR 8140 (HY000): writing inconsistent data in table: t, index: i2, col: c1, indexed-value:{KindString hellp} != record-value:{KindString hello}`

このエラーは、トランザクションによって書き込まれる行のデータがインデックスのデータと一致しないことを示します。表`t`のインデックス`i2`の場合、トランザクションによって書き込まれる行のインデックス キーと値のペアにはデータ`hellp`があり、レコード キーと値のペアにはデータ`hello`あります。この行のデータは書き込まれません。

#### エラー 8141 {#error-8141}

`ERROR 8141 (HY000): assertion failed: key: 7480000000000000405f72013300000000000000f8, assertion: NotExist, start_ts: 430590532931813377, existing start ts: 430590532931551233, existing commit ts: 430590532931551234`

このエラーは、トランザクションのコミット時にアサーションが失敗したことを示します。データとインデックスが一貫していると仮定すると、TiDB はキー`7480000000000000405f720133000000000000000000f8`が存在しないとアサートしました。トランザクションのコミット時に、TiDB は、トランザクションによって`start ts` `430590532931551233`で書き込まれたキーが存在することを検出しました。TiDB は、このキーのマルチバージョン同時実行制御 (MVCC) 履歴をログに出力します。

### 管理者チェックでエラーが報告されました {#errors-reported-in-admin-check}

このセクションでは、 [`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md)ステートメントを実行したときに TiDB で発生する可能性のあるデータ不整合エラーをリストし、例を挙げてこれらのエラーの意味を説明します。

#### エラー 8003 {#error-8003}

`ERROR 8003 (HY000): table count 3 != index(idx) count 2`

このエラーは、 [`ADMIN CHECK`](/sql-statements/sql-statement-admin-check-table-index.md)のステートメントが実行されるテーブルに行のキーと値のペアが 3 つあるが、インデックスのキーと値のペアが 2 つしかないことを示します。

#### エラー 8134 {#error-8134}

`ERROR 8134 (HY000): data inconsistency in table: t, index: c2, col: c2, handle: "2", index-values:"KindInt64 13" != record-values:"KindInt64 12", compare err:<nil>`

このエラーは、表`t`のインデックス`c2`について、列`c2`の値に次の不一致があることを示しています。

-   ハンドルが`2`である行のインデックスキーと値のペアでは、列`c2`の値は`13`です。
-   行レコードのキーと値のペアでは、列`c2`の値は`12`です。

#### エラー 8223 {#error-8223}

`ERROR 8223 (HY000): data inconsistency in table: t2, index: i1, handle: {hello, hello}, index-values:"" != record-values:"handle: {hello, hello}, values: [KindString hello KindString hello]"`

このエラーは、 `index-values`が null で、 `record-values`が null でないことを示します。つまり、行に対応するインデックスがないことを意味します。

## ソリューション {#solutions}

<CustomContent platform="tidb">

データの不整合エラーが発生した場合は、自分でエラーに対処するのではなく、PingCAP から[支持を得ます](/support.md)取得してすぐにトラブルシューティングを行ってください。アプリケーションでこのようなエラーを緊急にスキップする必要がある場合は、次の方法を使用してチェックをバイパスできます。

</CustomContent>

<CustomContent platform="tidb-cloud">

データの不整合エラーが発生した場合は、自分でエラーに対処するのでは[TiDB Cloudサポートにお問い合わせください](/tidb-cloud/tidb-cloud-support.md) 、すぐにトラブルシューティングを行ってください。アプリケーションでこのようなエラーを緊急にスキップする必要がある場合は、次の方法を使用してチェックをバイパスできます。

</CustomContent>

### SQLの書き換え {#rewrite-sql}

特定の SQL ステートメントでのみデータ不整合エラーが発生する場合は、異なる実行演算子を使用して SQL ステートメントを別の同等の形式に書き換えることで、このエラーを回避できます。

### エラーチェックを無効にする {#disable-error-checks}

トランザクション実行時に報告される次のエラーについては、対応するチェックをバイパスできます。

-   エラー 8138、8139、および 8140 のチェックをバイパスするには、 `set @@tidb_enable_mutation_checker=0`設定します。
-   エラー 8141 のチェックをバイパスするには、 `set @@tidb_txn_assertion_level=OFF`設定します。

> **注記：**
>
> `tidb_enable_mutation_checker`と`tidb_txn_assertion_level`を無効にすると、すべての SQL ステートメントの対応するチェックがバイパスされます。

トランザクション実行で報告されたその他のエラー、および[`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md)ステートメントの実行中に報告されたすべてのエラーについては、データがすでに不整合であるため、対応するチェックをバイパスすることはできません。
