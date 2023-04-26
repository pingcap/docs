---
title: Troubleshoot Inconsistency Between Data and Indexes
summary: Learn how to deal with errors reported by the consistency check between data and indexes.
---

# データとインデックス間の不一致のトラブルシューティング {#troubleshoot-inconsistency-between-data-and-indexes}

TiDB は、トランザクションまたは[`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md)ステートメントを実行するときに、データとインデックスの間の整合性をチェックします。チェックにより、レコードのキー値と対応するインデックスのキー値が矛盾していることが判明した場合、つまり、行データを格納するキーと値のペアとそのインデックスを格納する対応するキーと値のペアが矛盾している場合 (たとえば、より多くのインデックスまたはインデックスが見つからない)、TiDB はデータの不整合エラーを報告し、関連するエラーをエラー ログに出力。

<CustomContent platform="tidb">

このドキュメントでは、データ不整合エラーの意味について説明し、整合性チェックをバイパスするいくつかの方法を提供します。データ整合性エラーが発生した場合は、PingCAP またはコミュニティから[支持を得ます](/support.md)を入手できます。

</CustomContent>

<CustomContent platform="tidb-cloud">

このドキュメントでは、データ不整合エラーの意味について説明し、整合性チェックをバイパスするいくつかの方法を提供します。データ整合性エラーが発生した場合は、次のことができます[TiDB Cloudサポートに連絡する](/tidb-cloud/tidb-cloud-support.md) 。

</CustomContent>

## エラーの説明 {#error-explanation}

データとインデックスの間で不整合が発生した場合、TiDB エラー メッセージをチェックして、行データとインデックス データの間でどの項目が不整合であるかを確認したり、関連するエラー ログをチェックしてさらに調査したりできます。

### トランザクション実行中に報告されたエラー {#errors-reported-during-transaction-execution}

このセクションでは、TiDB がトランザクションを実行するときに報告されるデータ不整合エラーをリストし、これらのエラーの意味を例を挙げて説明します。

#### エラー 8133 {#error-8133}

`ERROR 8133 (HY000): data inconsistency in table: t, index: k2, index-count:1 != record-count:0`

このエラーは、テーブル`t`の`k2`インデックスについて、テーブル内のインデックスの数が 1 で、行レコードの数が 0 であることを示しています。数が矛盾しています。

#### エラー 8138 {#error-8138}

`ERROR 8138 (HY000): writing inconsistent data in table: t, expected-values:{KindString green} != record-values:{KindString GREEN}`

このエラーは、トランザクションが誤った行の値を書き込もうとしたことを示しています。書き込まれるデータは、エンコードされた行データがエンコード前の元のデータと一致しません。

#### エラー 8139 {#error-8139}

`ERROR 8139 (HY000): writing inconsistent data in table: t, index: i1, index-handle:4 != record-handle:3, index: tables.mutation{key:kv.Key{0x74, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x49, 0x5f, 0x69, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x1, 0x1, 0x68, 0x65, 0x6c, 0x6c, 0x6f, 0x0, 0x0, 0x0, 0xfc, 0x1, 0x68, 0x65, 0x6c, 0x6c, 0x6f, 0x0, 0x0, 0x0, 0xfc, 0x3, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x4}, flags:0x0, value:[]uint8{0x30}, indexID:1}, record: tables.mutation{key:kv.Key{0x74, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x49, 0x5f, 0x72, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x3}, flags:0xd, value:[]uint8{0x80, 0x0, 0x2, 0x0, 0x0, 0x0, 0x1, 0x2, 0x5, 0x0, 0xa, 0x0, 0x68, 0x65, 0x6c, 0x6c, 0x6f, 0x68, 0x65, 0x6c, 0x6c, 0x6f}, indexID:0}`

このエラーは、書き込むデータのハンドル (つまり、行データのキー) が一致していないことを示しています。テーブル`t`のインデックス`i1`の場合、トランザクションによって書き込まれる行には、インデックスのキーと値のペアに 4 のハンドルがあり、行レコードのキーと値のペアに 3 のハンドルがあります。この行のデータは書き込まれません。

#### エラー 8140 {#error-8140}

`ERROR 8140 (HY000): writing inconsistent data in table: t, index: i2, col: c1, indexed-value:{KindString hellp} != record-value:{KindString hello}`

このエラーは、トランザクションによって書き込まれる行のデータがインデックスのデータと一致しないことを示しています。テーブル`t`のインデックス`i2`の場合、トランザクションによって書き込まれる行には、インデックスのキーと値のペアにデータ`hellp`があり、レコードのキーと値のペアにデータ`hello`あります。この行のデータは書き込まれません。

#### エラー 8141 {#error-8141}

`ERROR 8141 (HY000): assertion failed: key: 7480000000000000405f72013300000000000000f8, assertion: NotExist, start_ts: 430590532931813377, existing start ts: 430590532931551233, existing commit ts: 430590532931551234`

このエラーは、トランザクションのコミット中にアサーションが失敗したことを示しています。データとインデックスが一致していると仮定すると、TiDB はキー`7480000000000000405f720133000000000000000000f8`が存在しないと主張しました。トランザクションがコミットされたとき、TiDB は`start ts` `430590532931551233`のトランザクションによって書き込まれたキーが存在することを発見しました。 TiDB は、このキーの Multi-Version Concurrency Control (MVCC) 履歴をログに出力します。

### 管理チェックで報告されたエラー {#errors-reported-in-admin-check}

このセクションでは、 [`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md)ステートメントを実行したときに TiDB で発生する可能性のあるデータ不整合エラーをリストし、これらのエラーの意味を例を挙げて説明します。

#### エラー 8003 {#error-8003}

`ERROR 8003 (HY000): table count 3 != index(idx) count 2`

このエラーは、 [`ADMIN CHECK`](/sql-statements/sql-statement-admin-check-table-index.md)ステートメントが実行されたテーブルに 3 つの行のキーと値のペアがあり、インデックスのキーと値のペアが 2 つしかないことを示しています。

#### エラー 8134 {#error-8134}

`ERROR 8134 (HY000): data inconsistency in table: t, index: c2, col: c2, handle: "2", index-values:"KindInt64 13" != record-values:"KindInt64 12", compare err:<nil>`

このエラーは、テーブル`t`のインデックス`c2`で、列`c2`の値に次の矛盾があることを示しています。

-   ハンドルが`2`である行のインデックス キーと値のペアでは、列`c2`の値は`13`です。
-   行レコードのキーと値のペアでは、列`c2`の値は`12`です。

#### エラー 8223 {#error-8223}

`ERROR 8223 (HY000): data inconsistency in table: t2, index: i1, handle: {hello, hello}, index-values:"" != record-values:"handle: {hello, hello}, values: [KindString hello KindString hello]"`

このエラーは、 `index-values`が null で`record-values` null ではないことを示します。つまり、行に対応するインデックスがないことを意味します。

## ソリューション {#solutions}

<CustomContent platform="tidb">

データ不整合エラーが発生し[支持を得ます](/support.md)場合は、自分でエラーに対処するのではなく、すぐに PingCAP からトラブルシューティングを依頼してください。アプリケーションでこのようなエラーを緊急にスキップする必要がある場合は、次の方法を使用してチェックをバイパスできます。

</CustomContent>

<CustomContent platform="tidb-cloud">

データの不整合エラーが発生した場合は、自分でエラーに対処[TiDB Cloudサポートに連絡する](/tidb-cloud/tidb-cloud-support.md)のではなく、すぐにトラブルシューティングを行います。アプリケーションでこのようなエラーを緊急にスキップする必要がある場合は、次の方法を使用してチェックをバイパスできます。

</CustomContent>

### SQLを書き換える {#rewrite-sql}

データ不整合エラーが特定の SQL ステートメントでのみ発生する場合は、別の実行演算子を使用して SQL ステートメントを別の同等の形式に書き換えることで、このエラーを回避できます。

### エラーチェックを無効にする {#disable-error-checks}

トランザクションの実行で報告された次のエラーについては、対応するチェックをバイパスできます。

-   エラー 8138、8139、および 8140 のチェックをバイパスするには、 `set @@tidb_enable_mutation_checker=0`を構成します。
-   エラー 8141 のチェックをバイパスするには、 `set @@tidb_txn_assertion_level=OFF`を構成します。

> **ノート：**
>
> `tidb_enable_mutation_checker`と`tidb_txn_assertion_level`を無効にすると、すべての SQL ステートメントの対応するチェックがバイパスされます。

トランザクションの実行で報告されたその他のエラー、および[`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md)ステートメントの実行中に報告されたすべてのエラーについては、データがすでに矛盾しているため、対応するチェックをバイパスすることはできません。
