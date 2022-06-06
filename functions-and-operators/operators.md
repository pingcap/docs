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
| [=](https://dev.mysql.com/doc/refman/5.7/en/assignment-operators.html#operator_assign-equal)               | 値を割り当てます（ [`SET`](https://dev.mysql.com/doc/refman/5.7/en/set-variable.html)ステートメントの一部として、または[`UPDATE`](https://dev.mysql.com/doc/refman/5.7/en/update.html)ステートメントの`SET`句の一部として） |
| [：=](https://dev.mysql.com/doc/refman/5.7/en/assignment-operators.html#operator_assign-value)              | 値を割り当てる                                                                                                                                                                           |
| [間...と..。](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_between)             | 値が値の範囲内にあるかどうかを確認します                                                                                                                                                              |
| [バイナリ](https://dev.mysql.com/doc/refman/5.7/en/cast-functions.html#operator_binary)                        | 文字列をバイナリ文字列にキャストします                                                                                                                                                               |
| [＆](https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#operator_bitwise-and)                       | ビットごとのAND                                                                                                                                                                         |
| [〜](https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#operator_bitwise-invert)                    | ビット単位の反転                                                                                                                                                                          |
| [|](https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#operator_bitwise-or)                        | ビットごとのOR                                                                                                                                                                          |
| [^](https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#operator_bitwise-xor)                       | ビット単位のXOR                                                                                                                                                                         |
| [場合](https://dev.mysql.com/doc/refman/5.7/en/flow-control-functions.html#operator_case)                    | ケースオペレーター                                                                                                                                                                         |
| [DIV](https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_div)                      | 整数除算                                                                                                                                                                              |
| [/](https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_divide)                     | 除算演算子                                                                                                                                                                             |
| [=](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_equal)                      | 等しい演算子                                                                                                                                                                            |
| [`&#x3C;=>`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_equal-to)          | 演算子に等しいNULLセーフ                                                                                                                                                                    |
| [&gt;&gt;](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_greater-than)        | 演算子より大きい                                                                                                                                                                          |
| [&gt; =](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_greater-than-or-equal) | 以上の演算子                                                                                                                                                                            |
| [は](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_is)                         | ブール値に対して値をテストします                                                                                                                                                                  |
| [ではありません](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_is-not)               | ブール値に対して値をテストします                                                                                                                                                                  |
| [NULLではありません](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_is-not-null)      | NOTNULL値テスト                                                                                                                                                                       |
| [無効です](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_is-null)                 | NULL値テスト                                                                                                                                                                          |
| [-&gt;](https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#operator_json-column-path)      | パスを評価した後、JSON列から値を返します。 `JSON_EXTRACT()`に相当                                                                                                                                       |
| [-&gt;&gt;](https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#operator_json-inline-path)  | パスを評価し、結果の引用符を外した後、JSON列から値を返します。 `JSON_UNQUOTE(JSON_EXTRACT())`に相当                                                                                                               |
| [&lt;&lt;](https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#operator_left-shift)                 | 左方移動                                                                                                                                                                              |
| [&lt;](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_less-than)               | 演算子未満                                                                                                                                                                             |
| [&lt;=](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_less-than-or-equal)     | 以下の演算子                                                                                                                                                                            |
| [お気に入り](https://dev.mysql.com/doc/refman/5.7/en/string-comparison-functions.html#operator_like)            | シンプルなパターンマッチング                                                                                                                                                                    |
| [-](https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_minus)                      | マイナス演算子                                                                                                                                                                           |
| [％、 モッド](https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_mod)                   | モジュロ演算子                                                                                                                                                                           |
| [いいえ、 ！](https://dev.mysql.com/doc/refman/5.7/en/logical-operators.html#operator_not)                      | 値を無効にします                                                                                                                                                                          |
| [間ではありません...と..。](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_not-between)  | 値が値の範囲内にないかどうかを確認します                                                                                                                                                              |
| [！=、 `&lt;&gt;`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_not-equal)     | 等しくない演算子                                                                                                                                                                          |
| [好きじゃない](https://dev.mysql.com/doc/refman/5.7/en/string-comparison-functions.html#operator_not-like)       | 単純なパターンマッチングの否定                                                                                                                                                                   |
| [正規表現ではありません](https://dev.mysql.com/doc/refman/5.7/en/regexp.html#operator_not-regexp)                     | REGEXPの否定                                                                                                                                                                         |
| [||、または](https://dev.mysql.com/doc/refman/5.7/en/logical-operators.html#operator_or)                       | 論理和                                                                                                                                                                               |
| [+](https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_plus)                       | 加算演算子                                                                                                                                                                             |
| [正規表現](https://dev.mysql.com/doc/refman/5.7/en/regexp.html#operator_regexp)                                | 正規表現を使用したパターンマッチング                                                                                                                                                                |
| [&gt;&gt;](https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#operator_right-shift)                | 右シフト                                                                                                                                                                              |
| [RLIKE](https://dev.mysql.com/doc/refman/5.7/en/regexp.html#operator_regexp)                               | REGEXPの同義語                                                                                                                                                                        |
| [のように聞こえる](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#operator_sounds-like)             | 音を比較する                                                                                                                                                                            |
| [*](https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_times)                      | 乗算演算子                                                                                                                                                                             |
| [-](https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_unary-minus)                | 引数の符号を変更する                                                                                                                                                                        |
| [XOR](https://dev.mysql.com/doc/refman/5.7/en/logical-operators.html#operator_xor)                         | 論理XOR                                                                                                                                                                             |

## 演算子の優先順位 {#operator-precedence}

次のリストに、優先順位の高いものから低いものへと、演算子の優先順位を示します。 1行に一緒に表示される演算子は、同じ優先順位を持ちます。

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

| 名前                                                                                                         | 説明                        |
| ---------------------------------------------------------------------------------------------------------- | ------------------------- |
| [間...と..。](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_between)             | 値が値の範囲内にあるかどうかを確認します      |
| [COALESCE（）](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#function_coalesce)          | NULL以外の最初の引数を返します         |
| [=](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_equal)                      | 等しい演算子                    |
| [`&#x3C;=>`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_equal-to)          | 演算子に等しいNULLセーフ            |
| [&gt;&gt;](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_greater-than)        | 演算子より大きい                  |
| [&gt; =](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_greater-than-or-equal) | 以上の演算子                    |
| [最高の（）](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#function_greatest)               | 最大の引数を返す                  |
| [の（）](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#function_in)                       | 値が値のセット内にあるかどうかを確認します     |
| [間隔（）](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#function_interval)                | 最初の引数よりも小さい引数のインデックスを返します |
| [は](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_is)                         | ブール値に対して値をテストします          |
| [ではありません](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_is-not)               | ブール値に対して値をテストします          |
| [NULLではありません](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_is-not-null)      | NOTNULL値テスト               |
| [無効です](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_is-null)                 | NULL値テスト                  |
| [無効です（）](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#function_isnull)                | 引数がNULLかどうかをテストします        |
| [少しでも（）](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#function_least)                 | 最小の引数を返す                  |
| [&lt;](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_less-than)               | 演算子未満                     |
| [&lt;=](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_less-than-or-equal)     | 以下の演算子                    |
| [お気に入り](https://dev.mysql.com/doc/refman/5.7/en/string-comparison-functions.html#operator_like)            | シンプルなパターンマッチング            |
| [間ではありません...と..。](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_not-between)  | 値が値の範囲内にないかどうかを確認します      |
| [！=、 `&lt;&gt;`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_not-equal)     | 等しくない演算子                  |
| [ありませんで（）](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#function_not-in)              | 値が値のセット内にないかどうかを確認します     |
| [好きじゃない](https://dev.mysql.com/doc/refman/5.7/en/string-comparison-functions.html#operator_not-like)       | 単純なパターンマッチングの否定           |
| [STRCMP（）](https://dev.mysql.com/doc/refman/5.7/en/string-comparison-functions.html#function_strcmp)       | 2つの文字列を比較する               |

詳細については、 [比較関数と演算子](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html)を参照してください。

## 論理演算子 {#logical-operators}

| 名前                                                                                    | 説明       |
| ------------------------------------------------------------------------------------- | -------- |
| [と、 ＆＆](https://dev.mysql.com/doc/refman/5.7/en/logical-operators.html#operator_and)  | 論理積      |
| [いいえ、 ！](https://dev.mysql.com/doc/refman/5.7/en/logical-operators.html#operator_not) | 値を無効にします |
| [||、または](https://dev.mysql.com/doc/refman/5.7/en/logical-operators.html#operator_or)  | 論理和      |
| [XOR](https://dev.mysql.com/doc/refman/5.7/en/logical-operators.html#operator_xor)    | 論理XOR    |

詳細については、 [GROUPBYのMySQL処理](https://dev.mysql.com/doc/refman/5.7/en/group-by-handling.html)を参照してください。

## 代入演算子 {#assignment-operators}

| 名前                                                                                            | 説明                                                                                                                                                                                |
| --------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [=](https://dev.mysql.com/doc/refman/5.7/en/assignment-operators.html#operator_assign-equal)  | 値を割り当てます（ [`SET`](https://dev.mysql.com/doc/refman/5.7/en/set-variable.html)ステートメントの一部として、または[`UPDATE`](https://dev.mysql.com/doc/refman/5.7/en/update.html)ステートメントの`SET`句の一部として） |
| [：=](https://dev.mysql.com/doc/refman/5.7/en/assignment-operators.html#operator_assign-value) | 値を割り当てる                                                                                                                                                                           |

詳細については、 [関数従属性の検出](https://dev.mysql.com/doc/refman/5.7/en/group-by-functional-dependence.html)を参照してください。
