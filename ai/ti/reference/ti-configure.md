---
title: ti configure
summary: ローカルの TiDB Cloud CLI プロファイルを対話形式または非対話形式で設定します。
---

# ti configure

ローカルの TiDB Cloud CLI プロファイルを設定します。フラグを指定しない場合、これは対話形式で実行できる唯一の TiDB Cloud CLI コマンドです。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti configure
  [--help]
  [--non-interactive]
  [--region-code <string>]
  [--tidb-cloud-private-key <string>]
  [--tidb-cloud-public-key <string>]
  [--version]
```

## オプション {#options}

- `--help`: ヘルプ情報を表示します。
- `--non-interactive`: プロンプトを表示しません。対応するコマンドオプションまたは環境変数を使用して、リージョンコード、公開鍵、秘密鍵を指定します。これは、スクリプトまたは自動化環境で `ti` を実行する場合に便利です。
- `--region-code <string>`: デフォルトのリージョンコード。たとえば `aws-us-east-1` または `aws-ap-southeast-1` です。
- `--tidb-cloud-private-key <string>`: TiDB Cloud API 秘密鍵。
- `--tidb-cloud-public-key <string>`: TiDB Cloud API 公開鍵。
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 設定値のソース {#configuration-value-sources}

次のコマンドオプションと環境変数は、同じ設定値を提供します。

| 設定値 | コマンドオプション | 環境変数 |
| --- | --- | --- |
| デフォルトのリージョンコード | `--region-code` | `TI_REGION_CODE` |
| TiDB Cloud API 公開鍵 | `--tidb-cloud-public-key` | `TIDB_CLOUD_PUBLIC_KEY` |
| TiDB Cloud API 秘密鍵 | `--tidb-cloud-private-key` | `TIDB_CLOUD_PRIVATE_KEY` |

各値について、明示的に指定されたコマンドオプションは、対応する環境変数よりも優先されます。`--non-interactive` を使用する場合、3 つすべての値がこれらのソースから解決される必要があります。

## 例 {#examples}

- `ti` を対話形式で設定する場合:

    ```bash
    # Enter the default region code and TiDB Cloud API keys when prompted.
    ti configure
    ```

- 自動化向けに `ti` を設定する場合:

    ```bash
    # Supply all required values without interactive prompts.
    TI_REGION_CODE="aws-us-east-1" \
    TIDB_CLOUD_PUBLIC_KEY="<public-key>" \
    TIDB_CLOUD_PRIVATE_KEY="<private-key>" \
    ti configure --profile ci --non-interactive
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud CLI のインストール、設定、および更新](/ai/ti/reference/ti-install-configure-update.md)
- [TiDB Cloud CLI の設定と認証情報](/ai/ti/reference/ti-configuration-and-credentials.md)