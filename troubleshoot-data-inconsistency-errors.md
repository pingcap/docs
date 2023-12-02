---
title: Troubleshoot Inconsistency Between Data and Indexes
summary: Learn how to deal with errors reported by the consistency check between data and indexes.
---

# データとインデックス間の不一致のトラブルシューティング {#troubleshoot-inconsistency-between-data-and-indexes}

TiDB は、トランザクション[`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md)ステートメントを実行するときに、データとインデックス間の一貫性をチェックします。チェックで、レコードのキーと値、および対応するインデックスのキーと値が矛盾していることが判明した場合、つまり、行データを格納するキーと値のペアと、そのインデックスを格納する対応するキーと値のペアが一致しない場合 (たとえば、インデックスを増やすか、インデックスが欠落している場合)、TiDB はデータ不整合エラーを報告し、関連するエラーをエラー ログに出力。

<CustomContent platform="tidb">

このドキュメントでは、データ不整合エラーの意味について説明し、整合性チェックをバイパスするいくつかの方法を提供します。データ整合性エラーが発生した場合は、PingCAP またはコミュニティから[支持を得ます](/support.md)できます。

</CustomContent>

<CustomContent platform="tidb-cloud">

このドキュメントでは、データ不整合エラーの意味について説明し、整合性チェックをバイパスするいくつかの方法を提供します。データ整合性エラーが発生した場合は、 [TiDB Cloudサポートにお問い合わせください](/tidb-cloud/tidb-cloud-support.md)を行うことができます。

</CustomContent>

## エラーの説明 {#error-explanation}

データとインデックスの間で不一致が発生した場合、TiDB エラー メッセージをチェックして行データとインデックス データの間でどの項目が不一致であるかを確認したり、関連するエラー ログをチェックして詳細な調査を行ったりすることができます。

### トランザクション実行中に報告されるエラー {#errors-reported-during-transaction-execution}

このセクションでは、TiDB がトランザクションを実行するときに報告されるデータ不整合エラーをリストし、これらのエラーの意味を例とともに説明します。

#### エラー8133 {#error-8133}

`ERROR 8133 (HY000): data inconsistency in table: t, index: k2, index-count:1 != record-count:0`

このエラーは、 table `t`の`k2`インデックスについて、テーブル内のインデックスの数が 1 で、行レコードの数が 0 であることを示します。この数は矛盾しています。

#### エラー8138 {#error-8138}

`ERROR 8138 (HY000): writing inconsistent data in table: t, expected-values:{KindString green} != record-values:{KindString GREEN}`

このエラーは、トランザクションが不正な行値を書き込もうとしたことを示します。書き込まれるデータは、エンコードされた行データがエンコード前の元のデータと一致しません。

#### エラー 8139 {#error-8139}

`ERROR 8139 (HY000): writing inconsistent data in table: t, index: i1, index-handle:4 != record-handle:3, index: tables.mutation{key:kv.Key{0x74, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x49, 0x5f, 0x69, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x1, 0x1, 0x68, 0x65, 0x6c, 0x6c, 0x6f, 0x0, 0x0, 0x0, 0xfc, 0x1, 0x68, 0x65, 0x6c, 0x6c, 0x6f, 0x0, 0x0, 0x0, 0xfc, 0x3, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x4}, flags:0x0, value:[]uint8{0x30}, indexID:1}, record: tables.mutation{key:kv.Key{0x74, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x49, 0x5f, 0x72, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x3}, flags:0xd, value:[]uint8{0x80, 0x0, 0x2, 0x0, 0x0, 0x0, 0x1, 0x2, 0x5, 0x0, 0xa, 0x0, 0x68, 0x65, 0x6c, 0x6c, 0x6f, 0x68, 0x65, 0x6c, 0x6c, 0x6f}, indexID:0}`

このエラーは、書き込むデータのハンドル（つまりロウデータのキー）が不一致であることを示します。 table `t`のインデックス`i1`の場合、トランザクションによって書き込まれる行には、インデックスのキーと値のペアのハンドル 4 と、行レコードのキーと値のペアのハンドル 3 があります。この行のデータは書き込まれません。

#### エラー 8140 {#error-8140}

`ERROR 8140 (HY000): writing inconsistent data in table: t, index: i2, col: c1, indexed-value:{KindString hellp} != record-value:{KindString hello}`

このエラーは、トランザクションによって書き込まれる行のデータがインデックス内のデータと一致しないことを示します。テーブル`t`のインデックス`i2`の場合、トランザクションによって書き込まれる行には、インデックスのキーと値のペアにデータ`hellp`があり、レコードのキーと値のペアにデータ`hello`あります。この行のデータは書き込まれません。

#### エラー8141 {#error-8141}

`ERROR 8141 (HY000): assertion failed: key: 7480000000000000405f72013300000000000000f8, assertion: NotExist, start_ts: 430590532931813377, existing start ts: 430590532931551233, existing commit ts: 430590532931551234`

このエラーは、トランザクションのコミット中にアサーションが失敗したことを示します。データとインデックスが一貫していると仮定すると、TiDB はキー`7480000000000000405f720133000000000000000000f8`が存在しないと主張しました。トランザクションがコミットされているときに、TiDB は、 `start ts` `430590532931551233`を使用してトランザクションによって書き込まれたキーが存在することを検出しました。 TiDB は、このキーのマルチバージョン同時実行制御 (MVCC) 履歴をログに出力します。

### 管理者チェックで報告されたエラー {#errors-reported-in-admin-check}

このセクションでは、 [`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md)ステートメントの実行時に TiDB で発生する可能性のあるデータ不整合エラーをリストし、これらのエラーの意味を例を示して説明します。

#### エラー8003 {#error-8003}

`ERROR 8003 (HY000): table count 3 != index(idx) count 2`

このエラーは、 [`ADMIN CHECK`](/sql-statements/sql-statement-admin-check-table-index.md)ステートメントが実行されるテーブルには 3 つの行キーと値のペアがあるが、インデックス キーと値のペアは 2 つしかないことを示します。

#### エラー8134 {#error-8134}

`ERROR 8134 (HY000): data inconsistency in table: t, index: c2, col: c2, handle: "2", index-values:"KindInt64 13" != record-values:"KindInt64 12", compare err:<nil>`

このエラーは、テーブル`t`のインデックス`c2`について、列`c2`の値に次の矛盾があることを示します。

-   ハンドルが`2`である行のインデックスのキーと値のペアでは、列`c2`の値は`13`です。
-   行レコードのキーと値のペアでは、列`c2`の値は`12`です。

#### エラー8223 {#error-8223}

`ERROR 8223 (HY000): data inconsistency in table: t2, index: i1, handle: {hello, hello}, index-values:"" != record-values:"handle: {hello, hello}, values: [KindString hello KindString hello]"`

このエラーは、 `index-values`が null で、 `record-values` null ではないことを示します。これは、行に対応するインデックスが存在しないことを意味します。

## ソリューション {#solutions}

<CustomContent platform="tidb">

データの不整合エラーが発生した場合は、自分でエラーに対処するのではなく、すぐにトラブルシューティングのために PingCAP から[支持を得ます](/support.md)を受け取ります。アプリケーションでこのようなエラーを緊急にスキップする必要がある場合は、次の方法を使用してチェックをバイパスできます。

</CustomContent>

<CustomContent platform="tidb-cloud">

データの不整合エラーが発生した場合は、自分でエラーに対処するのではなく[TiDB Cloudサポートにお問い合わせください](/tidb-cloud/tidb-cloud-support.md)すぐにトラブルシューティングを行ってください。アプリケーションでこのようなエラーを緊急にスキップする必要がある場合は、次の方法を使用してチェックをバイパスできます。

</CustomContent>

### SQLを書き換える {#rewrite-sql}

データ不整合エラーが特定の SQL ステートメントでのみ発生する場合は、別の実行演算子を使用して SQL ステートメントを別の同等の形式に書き直すことで、このエラーを回避できます。

### エラーチェックを無効にする {#disable-error-checks}

トランザクションの実行時に報告される次のエラーについては、対応するチェックをバイパスできます。

-   エラー 8138、8139、および 8140 のチェックをバイパスするには、 `set @@tidb_enable_mutation_checker=0`を設定します。
-   エラー 8141 のチェックをバイパスするには、 `set @@tidb_txn_assertion_level=OFF`を構成します。

> **注記：**
>
> `tidb_enable_mutation_checker`と`tidb_txn_assertion_level`を無効にすると、すべての SQL ステートメントの対応するチェックがバイパスされます。

トランザクションの実行で報告される他のエラーと、 [`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md)ステートメントの実行中に報告されるすべてのエラーについては、データがすでに不整合であるため、対応するチェックをバイパスできません。
