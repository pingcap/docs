---
title: Troubleshoot Inconsistency Between Data and Indexes
summary: Learn how to deal with errors reported by the consistency check between data and indexes.
---

# データとインデックス間の不整合のトラブルシューティング {#troubleshoot-inconsistency-between-data-and-indexes}

TiDBは、トランザクションまたは[`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md)ステートメントを実行するときに、データとインデックス間の整合性をチェックします。チェックにより、レコードのKey-Valueと対応するインデックスのKey-Valueに一貫性がないことが判明した場合、つまり、行データを格納するKey-Valueペアと、そのインデックスを格納する対応するKey-Valueペアに矛盾がある場合（たとえば、より多くのインデックスまたはインデックスがない場合）、TiDBはデータの不整合エラーを報告し、関連するエラーをエラーログに出力します。

このドキュメントでは、データの不整合エラーの意味を説明し、整合性チェックをバイパスするいくつかの方法を提供します。データ整合性エラーが発生した場合は、トラブルシューティングについてPingCAPテクニカルサポートに連絡してください。

## エラーの説明 {#error-explanation}

データとインデックスの間に不整合が発生した場合は、TiDBエラーメッセージをチェックして、行データとインデックスデータの間に不整合がある項目を確認するか、関連するエラーログを確認してさらに調査することができます。

### トランザクションの実行中に報告されたエラー {#errors-reported-during-transaction-execution}

このセクションでは、TiDBがトランザクションを実行するときに報告されるデータの不整合エラーを一覧表示し、例を使用してこれらのエラーの意味を説明します。

#### エラー8133 {#error-8133}

`ERROR 8133 (HY000): data inconsistency in table: t, index: k2, index-count:1 != record-count:0`

このエラーは、表`t`の`k2`つの索引について、表の索引の数が1であり、行レコードの数が0であることを示しています。数に一貫性がありません。

#### エラー8138 {#error-8138}

`ERROR 8138 (HY000): writing inconsistent data in table: t, expected-values:{KindString green} != record-values:{KindString GREEN}`

このエラーは、トランザクションが誤った行値を書き込もうとしたことを示しています。書き込まれるデータについては、エンコードおよびデコードプロセスの問題により、エンコードされた行データがエンコード前の元のデータと一致しません。

#### エラー8139 {#error-8139}

`ERROR 8139 (HY000): writing inconsistent data in table: t, index: i1, index-handle:4 != record-handle:3, index: tables.mutation{key:kv.Key{0x74, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x49, 0x5f, 0x69, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x1, 0x1, 0x68, 0x65, 0x6c, 0x6c, 0x6f, 0x0, 0x0, 0x0, 0xfc, 0x1, 0x68, 0x65, 0x6c, 0x6c, 0x6f, 0x0, 0x0, 0x0, 0xfc, 0x3, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x4}, flags:0x0, value:[]uint8{0x30}, indexID:1}, record: tables.mutation{key:kv.Key{0x74, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x49, 0x5f, 0x72, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x3}, flags:0xd, value:[]uint8{0x80, 0x0, 0x2, 0x0, 0x0, 0x0, 0x1, 0x2, 0x5, 0x0, 0xa, 0x0, 0x68, 0x65, 0x6c, 0x6c, 0x6f, 0x68, 0x65, 0x6c, 0x6c, 0x6f}, indexID:0}`

このエラーは、書き込まれるデータのハンドル（つまり、行データのキー）に一貫性がないことを示しています。表`t`の索引`i1`の場合、トランザクションによって書き込まれる行のハンドルは、索引のキーと値のペアで4であり、行のレコードのキーと値のペアで3です。この行のデータは書き込まれません。

#### エラー8140 {#error-8140}

`ERROR 8140 (HY000): writing inconsistent data in table: t, index: i2, col: c1, indexed-value:{KindString hellp} != record-value:{KindString hello}`

このエラーは、トランザクションによって書き込まれる行のデータがインデックスのデータと一致しないことを示しています。表`t`のインデックス`i2`の場合、トランザクションによって書き込まれる行には、インデックスのキーと値のペアにデータ`hellp`があり、レコードのキーと値のペアにデータ`hello`があります。この行のデータは書き込まれません。

#### エラー8141 {#error-8141}

`ERROR 8141 (HY000): assertion failed: key: 7480000000000000405f72013300000000000000f8, assertion: NotExist, start_ts: 430590532931813377, existing start ts: 430590532931551233, existing commit ts: 430590532931551234`

このエラーは、トランザクションがコミットされているときにアサーションが失敗したことを示します。データとインデックスに一貫性があると仮定すると、TiDBはキー`7480000000000000405f720133000000000000000000f8`が存在しないと主張しました。トランザクションがコミットされていたとき、TiDBは、 `start ts` `430590532931551233`を使用したトランザクションによって書き込まれた、キーが存在することを検出しました。 TiDBは、このキーのマルチバージョン同時実行制御（MVCC）履歴をログに出力します。

### 管理者チェックで報告されたエラー {#errors-reported-in-admin-check}

このセクションでは、 [`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md)ステートメントを実行したときにTiDBで発生する可能性のあるデータ不整合エラーをリストし、これらのエラーの意味を例を挙げて説明します。

#### エラー8003 {#error-8003}

`ERROR 8003 (HY000): table count 3 != index(idx) count 2`

このエラーは、 `ADMIN CHECK`ステートメントが実行されるテーブルに3つの行のキーと値のペアがありますが、2つのインデックスのキーと値のペアしかないことを示しています。

#### エラー8134 {#error-8134}

`ERROR 8134 (HY000): data inconsistency in table: t, index: c2, col: c2, handle: "2", index-values:"KindInt64 13" != record-values:"KindInt64 12", compare err:<nil>`

このエラーは、表`t`の索引`c2`の場合、行のハンドルが索引キーと値のペアでは13であるが、行レコードのキーと値のペアでは12であり、一貫性がないことを示しています。

#### エラー8223 {#error-8223}

`ERROR 8223 (HY000): data inconsistency in table: t2, index: i1, handle: {hello, hello}, index-values:"" != record-values:"handle: {hello, hello}, values: [KindString hello KindString hello]"`

このエラーは、 `index-values`がヌルで`record-values`がヌルではないことを示します。これは、行に対応するインデックスがないことを意味します。

## 理由と解決策 {#reasons-and-solutions}

データ整合性エラーが発生した場合、その理由は次のとおりです。

-   既存のデータのデータとインデックスは一貫しており、現在のバージョンのTiDBにはバグがあります。進行中のトランザクションが一貫性のないデータを書き込もうとしている場合、TiDBはトランザクションを中止します。
-   既存のデータのデータとインデックスに一貫性がありません。一貫性のないデータは、過去に誤って実行された危険な操作、またはTiDBのバグが原因である可能性があります。
-   データとインデックスは一貫していますが、検出アルゴリズムには誤ってエラーを引き起こすバグがあります。

データの不整合エラーが発生した場合は、自分でエラーに対処するのではなく、すぐにPingCAPテクニカルサポートに連絡してトラブルシューティングを行ってください。 PingCAPテクニカルサポートがエラーが誤って報告されたことを確認した場合、またはアプリケーションがそのようなエラーを緊急にスキップする必要がある場合は、次の方法を使用してチェックをバイパスできます。

### エラーチェックを無効にする {#disable-error-check}

トランザクションの実行で報告された次のエラーについては、対応するチェックをバイパスできます。

-   エラー8138、8139、および8140のチェックをバイパスするには、 `set @@tidb_enable_mutation_checker=0`を構成します。
-   エラー8141のチェックをバイパスするには、 `set @@tidb_txn_assertion_level=OFF`を構成します。

トランザクションの実行で報告されたその他のエラーおよび`ADMIN CHECK [TABLE|INDEX]`ステートメントの実行中に報告されたすべてのエラーについては、データの不整合がすでに発生しているため、対応するチェックをバイパスすることはできません。

### SQLを書き直す {#rewrite-sql}

前のセクションで説明した`tidb_enable_mutation_checker`と`tidb_txn_assertion_level`を無効にすると、すべてのSQLステートメントの対応するチェックがバイパスされます。特定のSQLステートメントについて不整合エラーが誤って報告された場合は、別の実行演算子を使用してSQLステートメントを別の同等の形式に書き換えることにより、エラーを回避してみてください。
