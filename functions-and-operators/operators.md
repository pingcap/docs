---
title: Operators
summary: Learn about the operators precedence, comparison functions and operators, logical operators, and assignment operators.
---

# オペレーター {#operators}

このドキュメントでは、演算子の優先順位、比較関数と演算子、論理演算子、および代入演算子について説明します。

-   [演算子の優先順位](#operator-precedence)
-   [比較関数と演算子](#comparison-functions-and-operators)
-   [論理演算子](#logical-operators)
-   [代入演算子](#assignment-operators)

| 名前                                                                                                         | 説明                                                                                                                                                                                |
| ---------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [と、 ＆＆](https://dev.mysql.com/doc/refman/5.7/en/logical-operators.html#operator_and)                       | 論理積                                                                                                                                                                               |
| [=](https://dev.mysql.com/doc/refman/5.7/en/assignment-operators.html#operator_assign-equal)               | 値を割り当てる ( [`SET`](https://dev.mysql.com/doc/refman/5.7/en/set-variable.html)ステートメントの一部として、または[`UPDATE`](https://dev.mysql.com/doc/refman/5.7/en/update.html)ステートメントの`SET`句の一部として) |
| [:=](https://dev.mysql.com/doc/refman/5.7/en/assignment-operators.html#operator_assign-value)              | 値を割り当てる                                                                                                                                                                           |
| [... と ... の間](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_between)         | 値が値の範囲内にあるかどうかを確認する                                                                                                                                                               |
| [バイナリ](https://dev.mysql.com/doc/refman/5.7/en/cast-functions.html#operator_binary)                        | 文字列をバイナリ文字列にキャストする                                                                                                                                                                |
| [&amp;](https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#operator_bitwise-and)                   | ビット演算 AND                                                                                                                                                                         |
| [〜](https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#operator_bitwise-invert)                    | ビット反転                                                                                                                                                                             |
| [| |](https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#operator_bitwise-or)                      | ビットごとの OR                                                                                                                                                                         |
| [^](https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#operator_bitwise-xor)                       | ビット単位の XOR                                                                                                                                                                        |
| [場合](https://dev.mysql.com/doc/refman/5.7/en/flow-control-functions.html#operator_case)                    | ケースオペレーター                                                                                                                                                                         |
| [DIV](https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_div)                      | 整数除算                                                                                                                                                                              |
| [/](https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_divide)                     | 部門演算子                                                                                                                                                                             |
| [=](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_equal)                      | 等しい演算子                                                                                                                                                                            |
| [`&#x3C;=>`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_equal-to)          | 演算子と等しい NULL セーフ                                                                                                                                                                  |
| [&gt;](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_greater-than)            | 大なり演算子                                                                                                                                                                            |
| [&gt;=](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_greater-than-or-equal)  | 以上演算子                                                                                                                                                                             |
| [は](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_is)                         | ブール値に対して値をテストする                                                                                                                                                                   |
| [ではありません](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_is-not)               | ブール値に対して値をテストする                                                                                                                                                                   |
| [NULL ではありません](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_is-not-null)     | NOT NULL 値テスト                                                                                                                                                                     |
| [無効である](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_is-null)                | NULL 値テスト                                                                                                                                                                         |
| [-&gt;](https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#operator_json-column-path)      | パスを評価した後、JSON 列から値を返します。 `JSON_EXTRACT()`に相当                                                                                                                                      |
| [-&gt;&gt;](https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#operator_json-inline-path)  | パスを評価し、結果の引用符を外した後、JSON 列から値を返します。 `JSON_UNQUOTE(JSON_EXTRACT())`に相当                                                                                                              |
| [&lt;&lt;](https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#operator_left-shift)                 | 左方移動                                                                                                                                                                              |
| [&lt;](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_less-than)               | 小なり演算子                                                                                                                                                                            |
| [&lt;=](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_less-than-or-equal)     | 以下演算子                                                                                                                                                                             |
| [好き](https://dev.mysql.com/doc/refman/5.7/en/string-comparison-functions.html#operator_like)               | シンプルなパターンマッチング                                                                                                                                                                    |
| [-](https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_minus)                      | マイナス演算子                                                                                                                                                                           |
| [％、 モッド](https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_mod)                   | モジュロ演算子                                                                                                                                                                           |
| [いいえ、 ！](https://dev.mysql.com/doc/refman/5.7/en/logical-operators.html#operator_not)                      | 値を否定します                                                                                                                                                                           |
| [... と ... の間ではない](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_not-between) | 値が値の範囲内にないかどうかを確認します                                                                                                                                                              |
| [!=, `&lt;&gt;`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_not-equal)     | 等しくない演算子                                                                                                                                                                          |
| [みたいではなく](https://dev.mysql.com/doc/refman/5.7/en/string-comparison-functions.html#operator_not-like)      | 単純なパターン マッチングの否定                                                                                                                                                                  |
| [非正規表現](https://dev.mysql.com/doc/refman/5.7/en/regexp.html#operator_not-regexp)                           | REGEXP の否定                                                                                                                                                                        |
| [||、または](https://dev.mysql.com/doc/refman/5.7/en/logical-operators.html#operator_or)                       | 論理和                                                                                                                                                                               |
| [+](https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_plus)                       | 加算演算子                                                                                                                                                                             |
| [正規表現](https://dev.mysql.com/doc/refman/5.7/en/regexp.html#operator_regexp)                                | 正規表現を使用したパターン マッチング                                                                                                                                                               |
| [&gt;&gt;](https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#operator_right-shift)                | 右シフト                                                                                                                                                                              |
| [好き](https://dev.mysql.com/doc/refman/5.7/en/regexp.html#operator_regexp)                                  | REGEXP の同義語                                                                                                                                                                       |
| [*](https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_times)                      | 乗算演算子                                                                                                                                                                             |
| [-](https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_unary-minus)                | 引数の符号を変更する                                                                                                                                                                        |
| [XOR](https://dev.mysql.com/doc/refman/5.7/en/logical-operators.html#operator_xor)                         | 論理 XOR                                                                                                                                                                            |

## サポートされていない演算子 {#unsupported-operators}

-   [`SOUNDS LIKE`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#operator_sounds-like)

## 演算子の優先順位 {#operator-precedence}

演算子の優先順位は、次のリストに、優先順位の高いものから順に示されています。 1 行にまとめて表示されている演算子の優先順位は同じです。

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

詳細については、 [演算子の優先順位](https://dev.mysql.com/doc/refman/5.7/en/operator-precedence.html)を参照してください。

## 比較関数と演算子 {#comparison-functions-and-operators}

| 名前                                                                                                         | 説明                       |
| ---------------------------------------------------------------------------------------------------------- | ------------------------ |
| [... と ... の間](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_between)         | 値が値の範囲内にあるかどうかを確認する      |
| [合体()](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#function_coalesce)                | 最初の非 NULL 引数を返します        |
| [=](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_equal)                      | 等しい演算子                   |
| [`&#x3C;=>`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_equal-to)          | 演算子と等しい NULL セーフ         |
| [&gt;](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_greater-than)            | 大なり演算子                   |
| [&gt;=](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_greater-than-or-equal)  | 以上演算子                    |
| [最高の（）](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#function_greatest)               | 最大の引数を返す                 |
| [の（）](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_in)                       | 値が一連の値の範囲内にあるかどうかを確認する   |
| [間隔（）](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#function_interval)                | 最初の引数より小さい引数のインデックスを返します |
| [は](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_is)                         | ブール値に対して値をテストする          |
| [ではありません](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_is-not)               | ブール値に対して値をテストする          |
| [NULL ではありません](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_is-not-null)     | NOT NULL 値テスト            |
| [無効である](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_is-null)                | NULL 値テスト                |
| [無効である（）](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#function_isnull)               | 引数が NULL かどうかをテストする      |
| [少しでも（）](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#function_least)                 | 最小の引数を返します               |
| [&lt;](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_less-than)               | 小なり演算子                   |
| [&lt;=](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_less-than-or-equal)     | 以下演算子                    |
| [好き](https://dev.mysql.com/doc/refman/5.7/en/string-comparison-functions.html#operator_like)               | シンプルなパターンマッチング           |
| [... と ... の間ではない](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_not-between) | 値が値の範囲内にないかどうかを確認します     |
| [!=, `&lt;&gt;`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_not-equal)     | 等しくない演算子                 |
| [ありませんで（）](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_not-in)              | 値が値のセット内にないかどうかを確認します    |
| [みたいではなく](https://dev.mysql.com/doc/refman/5.7/en/string-comparison-functions.html#operator_not-like)      | 単純なパターン マッチングの否定         |
| [STRCMP()](https://dev.mysql.com/doc/refman/5.7/en/string-comparison-functions.html#function_strcmp)       | 2 つの文字列を比較する             |

詳細については、 [比較関数と演算子](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html)を参照してください。

## 論理演算子 {#logical-operators}

| 名前                                                                                    | 説明      |
| ------------------------------------------------------------------------------------- | ------- |
| [と、 ＆＆](https://dev.mysql.com/doc/refman/5.7/en/logical-operators.html#operator_and)  | 論理積     |
| [いいえ、 ！](https://dev.mysql.com/doc/refman/5.7/en/logical-operators.html#operator_not) | 値を否定します |
| [||、または](https://dev.mysql.com/doc/refman/5.7/en/logical-operators.html#operator_or)  | 論理和     |
| [XOR](https://dev.mysql.com/doc/refman/5.7/en/logical-operators.html#operator_xor)    | 論理 XOR  |

詳細については、 [GROUP BY の MySQL の処理](https://dev.mysql.com/doc/refman/5.7/en/group-by-handling.html)を参照してください。

## 代入演算子 {#assignment-operators}

| 名前                                                                                            | 説明                                                                                                                                                                                |
| --------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [=](https://dev.mysql.com/doc/refman/5.7/en/assignment-operators.html#operator_assign-equal)  | 値を割り当てる ( [`SET`](https://dev.mysql.com/doc/refman/5.7/en/set-variable.html)ステートメントの一部として、または[`UPDATE`](https://dev.mysql.com/doc/refman/5.7/en/update.html)ステートメントの`SET`句の一部として) |
| [:=](https://dev.mysql.com/doc/refman/5.7/en/assignment-operators.html#operator_assign-value) | 値を割り当てる                                                                                                                                                                           |

詳細については、 [機能依存の検出](https://dev.mysql.com/doc/refman/5.7/en/group-by-functional-dependence.html)を参照してください。
