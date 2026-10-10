---
title: ユーザー定義関数タイプを選択する
summary: 戻り値の形状、ランタイム、運用要件に基づいて、TiDB Cloud Lake で SQL、集計、テーブル、または外部 UDF を選択する方法を学びます。
---

# ユーザー定義関数タイプを選択する

ユーザー定義関数（UDF）を使用すると、組み込み SQL 関数では提供されていない再利用可能なロジックをパッケージ化できます。これにより、ビジネスルールの標準化、複雑なクエリの簡素化、カスタム集計の実装、値の行への展開、または SQL クエリと独立してホストされる Python サービスとの接続が可能になります。

UDF を作成する前に、[SQL 関数リファレンス](/tidb-cloud-lake/sql/sql-function-reference.md)を確認してください。通常、組み込み関数は最もシンプルな実装、最も低い実行オーバーヘッド、そして最も小さい運用負荷を提供します。

## UDF を使用する理由 {#why-use-udfs}

分析ワークロードが増えるにつれて、同じ変換処理が多くのクエリで繰り返し現れることがよくあります。すべてのクエリに式をコピーすると、動作の一貫性を保つことや、安全に変更を展開することが難しくなります。

UDF は、次のようなタスクに役立ちます。

- データクレンジング、検証、ビジネス計算を標準化する。
- パラメーター化された SQL クエリをカプセル化する。
- 中間状態を必要とするカスタム集計を実装する。
- Python ライブラリ、独自ロジック、または機械学習モデルを呼び出す。
- Warehouse とは独立して特化したコンピュートをスケールさせる。

UDF は 1 つの明確な責務だけを持つべきです。データ移動、スケジューリング、ストリーミング状態、継続的なイベントストリーム間のテーブル結合、ワークフローオーケストレーションは、UDF の内部ではなく、対応する Lake SQL、Stream、Task、または統合機能に属します。

## UDF エコシステムを理解する {#understand-the-udf-ecosystem}

{{{ .lake }}} は複数の UDF 実行モデルを提供します。これらは、戻り値の形状、言語、ホスティング、運用責任の点で異なります。

| UDF タイプ | 実装 | 出力 | ホスティング | 典型的な用途 |
| --- | --- | --- | --- | --- |
| SQL scalar UDF | SQL 式 | 各入力行に対して 1 つの値 | {{{ .lake }}} により管理 | 書式設定、計算、再利用可能な条件 |
| Script scalar UDF | Python または JavaScript | 各入力行に対して 1 つの値 | {{{ .lake }}} により管理 | ビジネスルール、検証、構造化データ処理 |
| WebAssembly scalar UDF | WebAssembly モジュール | 各入力行に対して 1 つの値 | {{{ .lake }}} により管理 | WebAssembly にコンパイルされた計算集約型ロジック |
| Aggregate UDF | Python または JavaScript | 各グループに対して 1 つの値 | {{{ .lake }}} により管理 | カスタムの状態を持つ集計 |
| SQL table UDF | SQL クエリ | 結果セット | {{{ .lake }}} により管理 | 再利用可能なパラメーター化クエリ |
| External scalar UDF | Python UDF Server | 各入力行に対して 1 つの値 | ユーザーがホスト | ライブラリ、モデル、独自サービス |
| External table UDF | Python UDF Server | 複数のカラムまたは行 | ユーザーがホスト | トークン化、展開、レコード生成 |

Aggregate UDF と table UDF は異なる問題を解決します。Aggregate UDF は複数行を消費して 1 つの値を返します。table UDF は結果セットを返します。{{{ .lake }}} は、これら 2 つの実行モデルを組み合わせた Python table aggregate UDF を提供していません。

## 最もシンプルな実行モデルを選択する {#choose-the-simplest-execution-model}

実装を選択する際は、次の順序を使用してください。

1. 必要な動作をすでに提供している場合は、組み込み関数を使用します。
2. SQL でロジックを明確に表現できる場合は、SQL scalar UDF または table UDF を使用します。
3. {{{ .lake }}} 内で実行すべきスクリプトロジックには、組み込みの Python または JavaScript scalar UDF を使用します。
4. コンパイル済みモジュールとして提供される計算集約型の scalar ロジックには、WebAssembly を使用します。
5. 計算にカスタム集計状態が必要な場合は、Aggregate UDF を使用します。
6. ロジックがリモートサービス、GPU、または独立したスケーリングに依存する場合は、外部 UDF を使用します。

次の質問は、選択肢を絞り込むのに役立ちます。

| 質問 | 推奨オプション |
| --- | --- |
| 1 つの SQL 式で結果を生成できますか。 | SQL scalar UDF |
| 行レベルのロジックに Python または JavaScript が必要ですか。 | Script scalar UDF |
| 計算集約型の行レベルロジックに、コンパイル済みでポータブルなモジュールが必要ですか。 | WebAssembly scalar UDF |
| SQL クエリが複数行を返す必要がありますか。 | SQL table UDF |
| 複数の入力行を 1 つのカスタム結果にまとめる必要がありますか。 | Aggregate UDF |
| 1 つの入力から Python によって生成された複数行を生成する必要がありますか。 | External table UDF |
| ロジックに Python パッケージ、モデル、ネットワーク呼び出し、または別個のコンピュートが必要ですか。 | External scalar または table UDF |

## 再利用可能な変換には SQL scalar UDF を使用する {#use-sql-scalar-udfs-for-reusable-transformations}

SQL scalar UDF は、各入力行を 1 つの値にマッピングします。これは、計算、文字列の正規化、条件付きビジネスルールに適しています。

### 電話番号を正規化する {#normalize-phone-numbers}

次の関数は書式文字を削除し、後続のクエリで 1 つの電話番号表現を使用できるようにします。

```sql
CREATE FUNCTION normalize_phone(phone VARCHAR)
RETURNS VARCHAR
AS $$ REGEXP_REPLACE(phone, '[^0-9]', '') $$;

SELECT normalize_phone('+1 (415) 555-0100');
```

### 割引を適用する {#apply-a-discount}

次の関数は割引計算を一元化します。

```sql
CREATE FUNCTION apply_discount(
    price DECIMAL(10, 2),
    rate DECIMAL(5, 2)
)
RETURNS DECIMAL(10, 2)
AS $$ price * (1 - rate) $$;

SELECT apply_discount(100, 0.15);
```

共有ビジネスルールが変更された場合は、[ALTER FUNCTION](/tidb-cloud-lake/sql/alter-function.md)を使用します。そうすることで、その関数を呼び出すクエリは式を重複させることなく新しい定義を使用できます。

完全な構文については、[CREATE SCALAR FUNCTION](/tidb-cloud-lake/sql/create-scalar-function.md)を参照してください。

## データ処理ロジックには Python scalar UDF を使用する {#use-python-scalar-udfs-for-data-processing-logic}

Python scalar UDF は、ロジックに制御フロー、Python 標準ライブラリ、または SQL で表現しにくいパッケージが必要な場合に役立ちます。

次の関数は、住所内の空白と大文字小文字を標準化します。

```sql
CREATE FUNCTION normalize_address(value VARCHAR)
RETURNS VARCHAR
LANGUAGE python
HANDLER = 'normalize_address'
AS $$
def normalize_address(value):
    return " ".join(value.strip().upper().split())
$$;

SELECT normalize_address('  123 Main Street  ');
```

Python UDF は、PyPI 依存関係に `PACKAGES` を、stage に保存されたファイルに `IMPORTS` を使用することもできます。依存関係は必要最小限に絞ることで、関数環境の再現と管理が容易になります。

## JSON 変換には JavaScript scalar UDF を使用する {#use-javascript-scalar-udfs-for-json-transformations}

JavaScript は、オブジェクトや JSON の変換に自然に適しており、特にそのロジックがすでにアプリケーションコードベースに存在する場合に有効です。

次の関数は、メールアドレスを正規化し、機密フィールドを削除します。

```sql
CREATE FUNCTION clean_profile(value VARIANT)
RETURNS VARIANT
LANGUAGE javascript
HANDLER = 'cleanProfile'
AS $$
export function cleanProfile(value) {
    const result = { ...value };
    if (typeof result.email === 'string') {
        result.email = result.email.trim().toLowerCase();
    }
    delete result.ssn;
    return result;
}
$$;
```

入力スキーマと戻り値スキーマは安定させてください。オブジェクト形状の変更は、その関数を呼び出すすべてのクエリに影響する可能性があります。

## コンパイル済みロジックには WebAssembly UDF を使用する {#use-webassembly-udfs-for-compiled-logic}

WebAssembly UDF は、コンパイル済みコードをポータブルなモジュールとしてパッケージ化します。これは、スクリプトランタイムよりもコンパイル済み実装が望ましい計算集約型の scalar ロジックに適しています。

必要な Arrow UDF インターフェースを実装したモジュールを stage にアップロードし、その後ハンドラーを登録します。

```sql
CREATE FUNCTION fib_wasm(value INT)
RETURNS INT
LANGUAGE wasm
HANDLER = 'fib'
AS $$ @my_wasm_stage/arrow_udf_example.wasm $$;

SELECT fib_wasm(10);
```

モジュールは、指定されたハンドラーをエクスポートし、SQL 互換の入力型と出力型を使用する必要があります。他のユーザーに関数を公開する前に、代表的な値でコンパイル済みアーティファクトをテストしてください。

## カスタムな状態を持つ計算に集計 UDF を使用する {#use-aggregate-udfs-for-custom-stateful-calculations}

集計 UDF は、次の方法を定義します。

1. 初期の集計状態を作成する。
2. 各入力行を状態に追加する。
3. 分散実行で生成された部分状態をマージする。
4. 最終状態を 1 つの結果に変換する。

次の Python 集計は値を加算します。この特定の計算では組み込みの `SUM` を使うほうが適していますが、この例はカスタム集計に必要なライフサイクルを示しています。

```sql
CREATE FUNCTION py_total(value BIGINT)
STATE { total BIGINT }
RETURNS BIGINT
LANGUAGE python
AS $$
class State:
    def __init__(self):
        self.total = 0

def create_state():
    return State()

def accumulate(state, value):
    state.total += value
    return state

def merge(left, right):
    left.total += right.total
    return left

def finish(state):
    return state.total
$$;

SELECT py_total(number) FROM numbers(5);
```

集計 UDF は Python と JavaScript をサポートしています。必要な状態遷移や最終化ロジックを組み込みの集計関数で表現できない場合にのみ使用してください。その他の例については、[CREATE AGGREGATE FUNCTION](/tidb-cloud-lake/sql/create-aggregate-function.md) を参照してください。

## 再利用可能な結果セットに SQL テーブル UDF を使用する {#use-sql-table-udfs-for-reusable-result-sets}

SQL テーブル UDF は SQL クエリをカプセル化し、行とカラムを返します。再利用可能なフィルター、小規模なレポート用データセット、パラメーター化された変換に役立ちます。

```sql
CREATE FUNCTION small_numbers(max_value INT)
RETURNS TABLE(value UINT64, doubled UINT64)
AS $$
    SELECT number AS value, number * 2 AS doubled
    FROM numbers(10)
    WHERE number < max_value
$$;

SELECT * FROM small_numbers(3);
```

関数本体は SQL クエリです。`LANGUAGE python` は受け付けません。Python で生成した行を使用する場合は、外部テーブル UDF を使用してください。

完全な構文については、[CREATE TABLE FUNCTION](/tidb-cloud-lake/sql/create-table-function.md) を参照してください。

## 特殊なロジックに外部 Python UDF を使用する {#use-external-python-udfs-for-specialized-logic}

[`tidbcloudlake-udf`](https://pypi.org/project/tidbcloudlake-udf/) パッケージは、外部スカラー UDF およびテーブル UDF 用の Python UDF Server を提供します。Python プロセスはお使いのインフラストラクチャ上で実行されるため、カスタムパッケージ、独自コード、GPU コンピュート、および独立したスケーリングを利用できます。

### Python で住所を正規化する {#normalize-addresses-with-python}

SDK をインストールします。

```shell
python3 -m pip install tidbcloudlake-udf
```

ハンドラーを定義してサーバーを起動します。

```python
from tidbcloudlake_udf import UDFServer, udf


@udf(
    input_types=["VARCHAR"],
    result_type="VARCHAR",
    skip_null=True,
)
def normalize_address(value: str) -> str:
    return " ".join(value.strip().upper().split())


if __name__ == "__main__":
    server = UDFServer("0.0.0.0:8815")
    server.add_function(normalize_address)
    server.serve()
```

サーバーをデプロイして allowlist に追加した後、ハンドラーを登録します。

```sql
CREATE FUNCTION normalize_address(value VARCHAR)
RETURNS VARCHAR
LANGUAGE python
HANDLER = 'normalize_address'
ADDRESS = 'https://udf.example.com';
```

### テキストを行に展開する {#expand-text-into-rows}

外部テーブル UDF は、`result_type` に出力カラムのリストを使用します。

```python
@udf(
    input_types=["VARCHAR"],
    result_type=[("token", "VARCHAR")],
    skip_null=True,
)
def split_words(value: str):
    return [{"token": token} for token in value.split()]
```

テーブルハンドラーを登録して呼び出します。

```sql
CREATE FUNCTION split_words(value VARCHAR)
RETURNS TABLE(token VARCHAR)
LANGUAGE python
HANDLER = 'split_words'
ADDRESS = 'https://udf.example.com';

SELECT * FROM split_words('external UDF server');
```

完全なサーバー、デプロイ、並行性、登録のワークフローについては、[CREATE FUNCTION](/tidb-cloud-lake/sql/create-function.md) を参照してください。

## 外部 UDF を安全にデプロイする {#deploy-external-udfs-securely}

外部関数を登録する前に、次を実施してください。

- UDF Server を公開 HTTPS エンドポイントにデプロイする。
- エンドポイントのホスト名をテナント UDF server allowlist に追加するため、TiDB Cloud Support に連絡する。
- ゲートウェイで認証、容量、タイムアウト、高可用性、アップグレード、監視を設定する。
- 認証情報は SQL 関数定義ではなく、サーバーのデプロイ環境に保持する。

SQL の `ADDRESS` には公開エンドポイントを含める必要があります。サーバープロセスはデプロイ環境内で `0.0.0.0` を listen できますが、Cloud クエリサービスが呼び出すアドレスとして `localhost` と `0.0.0.0` は無効です。

外部 UDF はネットワーク レイテンシーを追加します。レイテンシーに敏感な行ごとの呼び出しは小さく保ち、可能な場合は作業をバッチ化し、1 つのクエリ内で同じ高コストな関数を繰り返し呼び出すことは避けてください。

## パフォーマンスと運用を比較する {#compare-performance-and-operations}

パフォーマンスは、関数の複雑さ、入力サイズ、パッケージ起動、Warehouse リソース、ネットワーク レイテンシー、バッチサイズ、UDF Server の容量に依存します。別の製品やデプロイで測定した結果から Lake のパフォーマンスを予測することはできません。

| UDF の種類 | 主なオーバーヘッド | 運用責任 |
| --- | --- | --- |
| SQL scalar UDF | SQL 式の評価 | {{{ .lake }}} により管理 |
| Python or JavaScript scalar UDF | スクリプトランタイムと依存関係の初期化 | {{{ .lake }}} により管理 |
| WebAssembly scalar UDF | モジュールのロードとコンパイル済み関数の実行 | {{{ .lake }}} により管理 |
| Aggregate UDF | スクリプトランタイムと状態のシリアル化 | {{{ .lake }}} により管理 |
| SQL table UDF | クエリ実行 | {{{ .lake }}} により管理 |
| External UDF | ネットワーク転送と外部コンピュート | {{{ .lake }}} とお使いの UDF Server デプロイで分担 |

実際の関数を、代表的なデータと並行性でベンチマークしてください。クエリ レイテンシー、スループット、エラーハンドリング、コールドスタート、外部サービスの飽和を測定してください。

## UDF のベストプラクティスに従う {#follow-udf-best-practices}

- スクリプトやサービスを導入する前に、まず組み込み関数と SQL を優先する。
- 可能な限り、各関数は決定的で単一目的に保つ。
- NULL の動作を明示的に定義し、NULL 許容入力をテストする。
- 不要な変換を避けるため、正確な入力型と戻り値型を使用する。
- 集計 UDF では、部分状態を安全に結合できるように `merge` を結合則を満たすようにする。
- 外部 UDF では、バッチ指向ライブラリには `batch_mode` を、I/O バウンドな行処理には `io_threads` を使用する。
- 外部依存関係の過負荷を防ぐために `max_concurrency` を設定する。
- 外部ハンドラーの変更はサービス API の変更として扱い、登録済み SQL 定義との互換性を保ってデプロイする。
- ユーザーホスト型サーバーについて、エラー、レイテンシー、飽和、依存関係の健全性を監視する。
- 未使用の UDF 登録とサーバーハンドラーは一緒に削除する。

## はじめに {#get-started}

必要な出力に応じて、次のステップを選択してください。

- 再利用可能な SQL 式には [CREATE SCALAR FUNCTION](/tidb-cloud-lake/sql/create-scalar-function.md)
- カスタム Python または JavaScript の集計状態には [CREATE AGGREGATE FUNCTION](/tidb-cloud-lake/sql/create-aggregate-function.md)
- 再利用可能な SQL 結果セットには [CREATE TABLE FUNCTION](/tidb-cloud-lake/sql/create-table-function.md)
- 外部 Python のスカラーおよびテーブルハンドラーには [CREATE FUNCTION](/tidb-cloud-lake/sql/create-function.md)
- モデル推論の例には [外部 AI 関数](/tidb-cloud-lake/guides/external-ai-functions.md)

## 関連リソース {#related-resources}

- [ユーザー定義関数](/tidb-cloud-lake/sql/user-defined-function.md)
- [External Function](/tidb-cloud-lake/sql/external-function.md)
- [GitHub 上の `tidbcloud/lake-udf`](https://github.com/tidbcloud/lake-udf)