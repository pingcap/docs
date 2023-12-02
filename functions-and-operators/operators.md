---
title: Operators
summary: Learn about the operators precedence, comparison functions and operators, logical operators, and assignment operators.
---

# オペレーター {#operators}

このドキュメントでは、演算子の優先順位、比較関数と演算子、論理演算子、代入演算子について説明します。

-   [演算子の優先順位](#operator-precedence)
-   [比較関数と演算子](#comparison-functions-and-operators)
-   [論理演算子](#logical-operators)
-   [代入演算子](#assignment-operators)

| 名前                                                                                                         | 説明                                                                                                                                                                                 |
| ---------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [そして、 ＆＆](https://dev.mysql.com/doc/refman/8.0/en/logical-operators.html#operator_and)                     | 論理積                                                                                                                                                                                |
| [=](https://dev.mysql.com/doc/refman/8.0/en/assignment-operators.html#operator_assign-equal)               | 値を割り当てます ( [`SET`](https://dev.mysql.com/doc/refman/8.0/en/set-variable.html)ステートメントの一部として、または[`UPDATE`](https://dev.mysql.com/doc/refman/8.0/en/update.html)ステートメントの`SET`句の一部として) |
| [:=](https://dev.mysql.com/doc/refman/8.0/en/assignment-operators.html#operator_assign-value)              | 値を割り当てる                                                                                                                                                                            |
| [...と...の間](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_between)            | 値が値の範囲内にあるかどうかを確認します                                                                                                                                                               |
| [バイナリ](https://dev.mysql.com/doc/refman/8.0/en/cast-functions.html#operator_binary)                        | 文字列をバイナリ文字列にキャストします                                                                                                                                                                |
| [&amp;](https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html#operator_bitwise-and)                   | ビットごとの AND                                                                                                                                                                         |
| [～](https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html#operator_bitwise-invert)                    | ビットごとの反転                                                                                                                                                                           |
| [|](https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html#operator_bitwise-or)                        | ビットごとの OR                                                                                                                                                                          |
| [^](https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html#operator_bitwise-xor)                       | ビットごとの XOR                                                                                                                                                                         |
| [場合](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html#operator_case)                    | ケース演算子                                                                                                                                                                             |
| [ディビジョン](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_div)                   | 整数の除算                                                                                                                                                                              |
| [/](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_divide)                     | 除算演算子                                                                                                                                                                              |
| [=](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_equal)                      | 等号演算子                                                                                                                                                                              |
| [`&#x3C;=>`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_equal-to)          | NULL セーフな等しい演算子                                                                                                                                                                    |
| [&gt;](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_greater-than)            | 「より大きい」演算子                                                                                                                                                                         |
| [&gt;=](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_greater-than-or-equal)  | 以上演算子                                                                                                                                                                              |
| [は](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_is)                         | ブール値に対して値をテストする                                                                                                                                                                    |
| [ではありません](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_is-not)               | ブール値に対して値をテストする                                                                                                                                                                    |
| [NULL ではありません](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_is-not-null)     | NOT NULL 値のテスト                                                                                                                                                                     |
| [無効である](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_is-null)                | NULL値テスト                                                                                                                                                                           |
| [-&gt;](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#operator_json-column-path)      | パスを評価した後、JSON 列から値を返します。 `JSON_EXTRACT()`に相当                                                                                                                                       |
| [-&gt;&gt;](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#operator_json-inline-path)  | パスを評価し、結果の引用を解除した後、JSON 列から値を返します。 `JSON_UNQUOTE(JSON_EXTRACT())`に相当                                                                                                               |
| [&lt;&lt;](https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html#operator_left-shift)                 | 左方移動                                                                                                                                                                               |
| [&lt;](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_less-than)               | 「未満」演算子                                                                                                                                                                            |
| [&lt;=](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_less-than-or-equal)     | 以下演算子                                                                                                                                                                              |
| [のように](https://dev.mysql.com/doc/refman/8.0/en/string-comparison-functions.html#operator_like)             | 簡単なパターンマッチング                                                                                                                                                                       |
| [好き](https://www.postgresql.org/docs/current/functions-matching.html)                                      | 大文字と小文字を区別しない単純なパターン マッチング (TiDB ではサポートされていますが、MySQL ではサポートされていません)                                                                                                                |
| [-](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_minus)                      | マイナス演算子                                                                                                                                                                            |
| [％、 モッド](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_mod)                   | モジュロ演算子                                                                                                                                                                            |
| [ない、 ！](https://dev.mysql.com/doc/refman/8.0/en/logical-operators.html#operator_not)                       | 値を否定します                                                                                                                                                                            |
| [...と...の間ではありません](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_not-between) | 値が値の範囲内にないかどうかを確認します                                                                                                                                                               |
| [!=、 `&lt;&gt;`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_not-equal)     | 等しくない演算子                                                                                                                                                                           |
| [みたいではなく](https://dev.mysql.com/doc/refman/8.0/en/string-comparison-functions.html#operator_not-like)      | 単純なパターンマッチングの否定                                                                                                                                                                    |
| [正規表現ではありません](https://dev.mysql.com/doc/refman/8.0/en/regexp.html#operator_not-regexp)                     | REGEXP の否定                                                                                                                                                                         |
| [||、または](https://dev.mysql.com/doc/refman/8.0/en/logical-operators.html#operator_or)                       | 論理和                                                                                                                                                                                |
| [+](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_plus)                       | 加算演算子                                                                                                                                                                              |
| [正規表現](https://dev.mysql.com/doc/refman/8.0/en/regexp.html#operator_regexp)                                | 正規表現を使用したパターン マッチング                                                                                                                                                                |
| [&gt;&gt;](https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html#operator_right-shift)                | 右シフト                                                                                                                                                                               |
| [いいね](https://dev.mysql.com/doc/refman/8.0/en/regexp.html#operator_regexp)                                 | REGEXP の同義語                                                                                                                                                                        |
| [*](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_times)                      | 乗算演算子                                                                                                                                                                              |
| [-](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_unary-minus)                | 引数の符号を変更する                                                                                                                                                                         |
| [XOR](https://dev.mysql.com/doc/refman/8.0/en/logical-operators.html#operator_xor)                         | 論理XOR                                                                                                                                                                              |

## サポートされていない演算子 {#unsupported-operators}

-   [`SOUNDS LIKE`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#operator_sounds-like)

## 演算子の優先順位 {#operator-precedence}

演算子の優先順位を、最高の優先順位から最低の優先順位まで、次のリストに示します。 1 行にまとめて表示される演算子は同じ優先順位を持ちます。

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

詳細は[演算子の優先順位](https://dev.mysql.com/doc/refman/8.0/en/operator-precedence.html)を参照してください。

## 比較関数と演算子 {#comparison-functions-and-operators}

| 名前                                                                                                         | 説明                                                                  |
| ---------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| [...と...の間](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_between)            | 値が値の範囲内にあるかどうかを確認します                                                |
| [合体()](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#function_coalesce)                | 最初の非 NULL 引数を返します                                                   |
| [=](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_equal)                      | 等号演算子                                                               |
| [`&#x3C;=>`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_equal-to)          | NULL セーフな等しい演算子                                                     |
| [&gt;](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_greater-than)            | 「より大きい」演算子                                                          |
| [&gt;=](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_greater-than-or-equal)  | 以上演算子                                                               |
| [最高の（）](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#function_greatest)               | 最大の引数を返します                                                          |
| [で（）](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_in)                       | 値が値のセット内にあるかどうかを確認する                                                |
| [間隔（）](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#function_interval)                | 最初の引数より小さい引数のインデックスを返します。                                           |
| [は](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_is)                         | ブール値に対して値をテストする                                                     |
| [ではありません](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_is-not)               | ブール値に対して値をテストする                                                     |
| [NULL ではありません](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_is-not-null)     | NOT NULL 値のテスト                                                      |
| [無効である](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_is-null)                | NULL値テスト                                                            |
| [無効である（）](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#function_isnull)               | 引数が NULL かどうかをテストする                                                 |
| [少しでも（）](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#function_least)                 | 最小の引数を返します                                                          |
| [&lt;](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_less-than)               | 「未満」演算子                                                             |
| [&lt;=](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_less-than-or-equal)     | 以下演算子                                                               |
| [のように](https://dev.mysql.com/doc/refman/8.0/en/string-comparison-functions.html#operator_like)             | 簡単なパターンマッチング                                                        |
| [好き](https://www.postgresql.org/docs/current/functions-matching.html)                                      | 大文字と小文字を区別しない単純なパターン マッチング (TiDB ではサポートされていますが、MySQL ではサポートされていません) |
| [...と...の間ではありません](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_not-between) | 値が値の範囲内にないかどうかを確認します                                                |
| [!=、 `&lt;&gt;`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_not-equal)     | 等しくない演算子                                                            |
| [ありませんで（）](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_not-in)              | 値が値のセット内にないかどうかを確認する                                                |
| [みたいではなく](https://dev.mysql.com/doc/refman/8.0/en/string-comparison-functions.html#operator_not-like)      | 単純なパターンマッチングの否定                                                     |
| [STRCMP()](https://dev.mysql.com/doc/refman/8.0/en/string-comparison-functions.html#function_strcmp)       | 2 つの文字列を比較する                                                        |

詳細は[比較関数と演算子](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html)を参照してください。

## 論理演算子 {#logical-operators}

| 名前                                                                                     | 説明      |
| -------------------------------------------------------------------------------------- | ------- |
| [そして、 ＆＆](https://dev.mysql.com/doc/refman/8.0/en/logical-operators.html#operator_and) | 論理積     |
| [ない、 ！](https://dev.mysql.com/doc/refman/8.0/en/logical-operators.html#operator_not)   | 値を否定します |
| [||、または](https://dev.mysql.com/doc/refman/8.0/en/logical-operators.html#operator_or)   | 論理和     |
| [XOR](https://dev.mysql.com/doc/refman/8.0/en/logical-operators.html#operator_xor)     | 論理XOR   |

詳細は[MySQL での GROUP BY の処理](https://dev.mysql.com/doc/refman/8.0/en/group-by-handling.html)を参照してください。

## 代入演算子 {#assignment-operators}

| 名前                                                                                            | 説明                                                                                                                                                                                 |
| --------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [=](https://dev.mysql.com/doc/refman/8.0/en/assignment-operators.html#operator_assign-equal)  | 値を割り当てます ( [`SET`](https://dev.mysql.com/doc/refman/8.0/en/set-variable.html)ステートメントの一部として、または[`UPDATE`](https://dev.mysql.com/doc/refman/8.0/en/update.html)ステートメントの`SET`句の一部として) |
| [:=](https://dev.mysql.com/doc/refman/8.0/en/assignment-operators.html#operator_assign-value) | 値を割り当てる                                                                                                                                                                            |

詳細は[機能的依存の検出](https://dev.mysql.com/doc/refman/8.0/en/group-by-functional-dependence.html)を参照してください。

## MySQLの互換性 {#mysql-compatibility}

-   MySQL は`ILIKE`演算子をサポートしていません。
