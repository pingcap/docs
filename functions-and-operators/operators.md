---
title: Operators
summary: 演算子の優先順位、比較関数と演算子、論理演算子、代入演算子について学習します。
---

# オペレーター {#operators}

このドキュメントでは、演算子の優先順位、比較関数と演算子、論理演算子、および代入演算子について説明します。

-   [演算子の優先順位](#operator-precedence)
-   [比較関数と演算子](#comparison-functions-and-operators)
-   [論理演算子](#logical-operators)
-   [代入演算子](#assignment-operators)

| 名前                                                                                                        | 説明                                                                                                                                                                   |
| --------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [そして、 ＆＆](https://dev.mysql.com/doc/refman/8.0/en/logical-operators.html#operator_and)                    | 論理積                                                                                                                                                                  |
| [=](https://dev.mysql.com/doc/refman/8.0/en/assignment-operators.html#operator_assign-equal)              | 値を割り当てる（ [`SET`](https://dev.mysql.com/doc/refman/8.0/en/set-variable.html)文の一部として、または[`UPDATE`](https://dev.mysql.com/doc/refman/8.0/en/update.html)文の`SET`節の一部として） |
| [:=](https://dev.mysql.com/doc/refman/8.0/en/assignment-operators.html#operator_assign-value)             | 値を割り当てる                                                                                                                                                              |
| [...と...の間](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_between)           | 値が範囲内にあるかどうかを確認します                                                                                                                                                   |
| [バイナリ](https://dev.mysql.com/doc/refman/8.0/en/cast-functions.html#operator_binary)                       | 文字列をバイナリ文字列に変換する                                                                                                                                                     |
| [＆](https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html#operator_bitwise-and)                      | ビットAND                                                                                                                                                               |
| [〜](https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html#operator_bitwise-invert)                   | ビット反転                                                                                                                                                                |
| [|](https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html#operator_bitwise-or)                       | ビットOR                                                                                                                                                                |
| [^](https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html#operator_bitwise-xor)                      | ビット単位の排他的論理和                                                                                                                                                         |
| [場合](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html#operator_case)                   | ケース演算子                                                                                                                                                               |
| [部門](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_div)                      | 整数除算                                                                                                                                                                 |
| [/](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_divide)                    | 除算演算子                                                                                                                                                                |
| [=](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_equal)                     | 等号演算子                                                                                                                                                                |
| [`&#x3C;=>`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_equal-to)         | NULL セーフな等号演算子                                                                                                                                                       |
| [&gt;](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_greater-than)           | より大きい演算子                                                                                                                                                             |
| [&gt;=](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_greater-than-or-equal) | より大きいか等しい演算子                                                                                                                                                         |
| [は](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_is)                        | 値をブール値でテストする                                                                                                                                                         |
| [ではありません](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_is-not)              | 値をブール値でテストする                                                                                                                                                         |
| [NULLではない](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_is-not-null)        | NOT NULL値テスト                                                                                                                                                         |
| [無効である](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_is-null)               | NULL値テスト                                                                                                                                                             |
| [-&gt;](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#operator_json-column-path)     | パスを評価した後、JSON列から値を返します。1 `JSON_EXTRACT()`相当します。                                                                                                                      |
| [-&gt;&gt;](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#operator_json-inline-path) | パスを評価し、結果を引用符で囲んだ後のJSON列からの値を返します。1に相当します`JSON_UNQUOTE(JSON_EXTRACT())`                                                                                              |
| [&lt;&lt;](https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html#operator_left-shift)                | 左方移動                                                                                                                                                                 |
| [&lt;](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_less-than)              | より小さい演算子                                                                                                                                                             |
| [&lt;=](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_less-than-or-equal)    | 以下演算子                                                                                                                                                                |
| [のように](https://dev.mysql.com/doc/refman/8.0/en/string-comparison-functions.html#operator_like)            | シンプルなパターンマッチング                                                                                                                                                       |
| [好き](https://www.postgresql.org/docs/current/functions-matching.html)                                     | 大文字と小文字を区別しない単純なパターン マッチング (TiDB ではサポートされていますが、MySQL ではサポートされていません)                                                                                                  |
| [-](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_minus)                     | マイナス演算子                                                                                                                                                              |
| [％、 モッド](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_mod)                  | モジュロ演算子                                                                                                                                                              |
| [ない、 ！](https://dev.mysql.com/doc/refman/8.0/en/logical-operators.html#operator_not)                      | 価値を否定する                                                                                                                                                              |
| [...と...の間ではない](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_not-between)   | 値が範囲内にないか確認する                                                                                                                                                        |
| [!=, `&lt;&gt;`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_not-equal)    | 等しくない演算子                                                                                                                                                             |
| [みたいではなく](https://dev.mysql.com/doc/refman/8.0/en/string-comparison-functions.html#operator_not-like)     | 単純なパターンマッチングの否定                                                                                                                                                      |
| [正規表現ではない](https://dev.mysql.com/doc/refman/8.0/en/regexp.html#operator_not-regexp)                       | REGEXPの否定                                                                                                                                                            |
| [||、または](https://dev.mysql.com/doc/refman/8.0/en/logical-operators.html#operator_or)                      | 論理和                                                                                                                                                                  |
| [+](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_plus)                      | 加算演算子                                                                                                                                                                |
| [正規表現](https://dev.mysql.com/doc/refman/8.0/en/regexp.html#operator_regexp)                               | 正規表現を使用したパターンマッチング                                                                                                                                                   |
| [&gt;&gt;](https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html#operator_right-shift)               | 右シフト                                                                                                                                                                 |
| [RLIKE](https://dev.mysql.com/doc/refman/8.0/en/regexp.html#operator_regexp)                              | REGEXPの同義語                                                                                                                                                           |
| [*](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_times)                     | 乗算演算子                                                                                                                                                                |
| [-](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_unary-minus)               | 引数の符号を変更する                                                                                                                                                           |
| [排他的論理和](https://dev.mysql.com/doc/refman/8.0/en/logical-operators.html#operator_xor)                     | 論理排他的論理和                                                                                                                                                             |

## サポートされていない演算子 {#unsupported-operators}

-   [`SOUNDS LIKE`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#operator_sounds-like)

## 演算子の優先順位 {#operator-precedence}

演算子の優先順位は、次のリストに、優先順位の高いものから低いものの順に示されています。 1 行に一緒に表示されている演算子の優先順位は同じです。

```sql
INTERVAL
BINARY, COLLATE
!
- (unary minus), ~ (unary bit inversion)
^
*, /, DIV, %, MOD
-, +
<<, >>
&
|
= (comparison), <=>, >=, >, <=, <, <>, !=, IS, LIKE, REGEXP, IN
BETWEEN, CASE, WHEN, THEN, ELSE
NOT
AND, &&
XOR
OR, ||
= (assignment), :=
```

詳細は[演算子の優先順位](https://dev.mysql.com/doc/refman/8.0/en/operator-precedence.html)参照。

## 比較関数と演算子 {#comparison-functions-and-operators}

| 名前                                                                                                        | 説明                                                                  |
| --------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| [...と...の間](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_between)           | 値が範囲内にあるかどうかを確認します                                                  |
| [合体()](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#function_coalesce)               | 最初のNULL以外の引数を返す                                                     |
| [=](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_equal)                     | 等号演算子                                                               |
| [`&#x3C;=>`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_equal-to)         | NULL セーフな等号演算子                                                      |
| [&gt;](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_greater-than)           | より大きい演算子                                                            |
| [&gt;=](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_greater-than-or-equal) | より大きいか等しい演算子                                                        |
| [最高の（）](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#function_greatest)              | 最大の引数を返す                                                            |
| [で（）](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_in)                      | 値が値セット内にあるかどうかを確認する                                                 |
| [間隔（）](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#function_interval)               | 最初の引数より小さい引数のインデックスを返します                                            |
| [は](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_is)                        | 値をブール値でテストする                                                        |
| [ではありません](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_is-not)              | 値をブール値でテストする                                                        |
| [NULLではない](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_is-not-null)        | NOT NULL値テスト                                                        |
| [無効である](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_is-null)               | NULL値テスト                                                            |
| [無効である（）](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#function_isnull)              | 引数がNULLかどうかをテストする                                                   |
| [少しでも（）](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#function_least)                | 最小の引数を返す                                                            |
| [&lt;](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_less-than)              | より小さい演算子                                                            |
| [&lt;=](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_less-than-or-equal)    | 以下演算子                                                               |
| [のように](https://dev.mysql.com/doc/refman/8.0/en/string-comparison-functions.html#operator_like)            | シンプルなパターンマッチング                                                      |
| [好き](https://www.postgresql.org/docs/current/functions-matching.html)                                     | 大文字と小文字を区別しない単純なパターン マッチング (TiDB ではサポートされていますが、MySQL ではサポートされていません) |
| [...と...の間ではない](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_not-between)   | 値が範囲内にないか確認する                                                       |
| [!=, `&lt;&gt;`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_not-equal)    | 等しくない演算子                                                            |
| [ありませんで（）](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_not-in)             | 値が値セット内にないかどうかを確認する                                                 |
| [みたいではなく](https://dev.mysql.com/doc/refman/8.0/en/string-comparison-functions.html#operator_not-like)     | 単純なパターンマッチングの否定                                                     |
| [STRCMP()](https://dev.mysql.com/doc/refman/8.0/en/string-comparison-functions.html#function_strcmp)      | 2つの文字列を比較する                                                         |

詳細は[比較関数と演算子](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html)参照。

## 論理演算子 {#logical-operators}

| 名前                                                                                     | 説明       |
| -------------------------------------------------------------------------------------- | -------- |
| [そして、 ＆＆](https://dev.mysql.com/doc/refman/8.0/en/logical-operators.html#operator_and) | 論理積      |
| [ない、 ！](https://dev.mysql.com/doc/refman/8.0/en/logical-operators.html#operator_not)   | 価値を否定する  |
| [||、または](https://dev.mysql.com/doc/refman/8.0/en/logical-operators.html#operator_or)   | 論理和      |
| [排他的論理和](https://dev.mysql.com/doc/refman/8.0/en/logical-operators.html#operator_xor)  | 論理排他的論理和 |

詳細は[MySQL の GROUP BY の処理](https://dev.mysql.com/doc/refman/8.0/en/group-by-handling.html)参照。

## 代入演算子 {#assignment-operators}

| 名前                                                                                            | 説明                                                                                                                                                                   |
| --------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [=](https://dev.mysql.com/doc/refman/8.0/en/assignment-operators.html#operator_assign-equal)  | 値を割り当てる（ [`SET`](https://dev.mysql.com/doc/refman/8.0/en/set-variable.html)文の一部として、または[`UPDATE`](https://dev.mysql.com/doc/refman/8.0/en/update.html)文の`SET`節の一部として） |
| [:=](https://dev.mysql.com/doc/refman/8.0/en/assignment-operators.html#operator_assign-value) | 値を割り当てる                                                                                                                                                              |

詳細は[機能依存性の検出](https://dev.mysql.com/doc/refman/8.0/en/group-by-functional-dependence.html)参照。

## MySQL 互換性 {#mysql-compatibility}

-   MySQL は`ILIKE`演算子をサポートしていません。
