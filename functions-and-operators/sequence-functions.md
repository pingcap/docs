---
title: Sequence Functions
summary: このドキュメントでは、TiDB でサポートされているシーケンス関数について説明します。
---

# シーケンス関数 {#sequence-functions}

TiDB のシーケンス関数は、 [`CREATE SEQUENCE`](/sql-statements/sql-statement-create-sequence.md)ステートメントを使用して作成されたシーケンス オブジェクトの値を返すか設定するために使用されます。

| 関数名                            | 機能の説明                |
| :----------------------------- | :------------------- |
| `NEXTVAL()`または`NEXT VALUE FOR` | シーケンスの次の値を返します       |
| `SETVAL()`                     | シーケンスの現在の値を設定します     |
| `LASTVAL()`                    | シーケンスの最後に使用された値を返します |

## MySQL 互換性 {#mysql-compatibility}

MySQL は、 [ISO/IEC 9075-2](https://www.iso.org/standard/76584.html)で定義されているシーケンスを作成および操作するための関数とステートメントをサポートしていません。
