---
title: tdc から TiDB Cloud CLI への移行
summary: サポートされているローカル状態と自動化を tdc v0.1.x から TiDB Cloud CLI に移行します。
---

# tdc から TiDB Cloud CLI への移行

この移行は、以前に `tdc` v0.1.x を使用していた場合にのみ適用されます。新規の TiDB Cloud CLI インストールでは、この作業は不要です。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 開始前に {#before-you-begin}

- `tdc` によって開始されたすべての file system マウントおよび Vault マウントをアンマウントし、書き込みプロセスを停止します。古いマウントがまだアクティブな場合、実行中の FUSE または WebDAV プロセスを移行できないため、移行は停止します。

    アクティブな各マウントに対応するコマンドを実行してください。FUSE file system マウントの場合は、まず `drain-file-system` を実行して保留中の書き込みをフラッシュし、その後 `unmount-file-system` を実行してマウントを切り離します。WebDAV file system マウントの場合は、書き込みプロセスを停止し、`unmount-file-system` のみを実行します。Vault マウントでは `unmount-vault` のみが必要です。

    ```bash
    # FUSE file system mount
    tdc fs drain-file-system --mount-path <filesystem-mount-path>
    tdc fs unmount-file-system --mount-path <filesystem-mount-path>

    # WebDAV file system mount
    tdc fs unmount-file-system --mount-path <filesystem-mount-path>

    # Vault mount
    tdc fs-vault unmount-vault --mount-path <vault-mount-path>
    ```

- ディレクトリの競合を解決する前に、`~/.tdc/` と既存の `~/.ti/` ディレクトリをバックアップしてください。

## ti をインストールしてローカル状態を移行する {#install-ti-and-migrate-local-state}

古い `tdc update` コマンドでは、名前が変更された `ti` 実行ファイルをインストールできず、`ti` も `tdc` コマンドエイリアスを提供しません。[TiDB Cloud CLI をインストールする](/ai/ti/reference/ti-install-configure-update.md#install-tidb-cloud-cli) に従って、`ti` を直接インストールしてください。

`~/.tdc/` が存在し、`~/.ti/` が存在しない場合、インストーラーおよび最初の `update` 以外の `ti` コマンドは、サポートされているローカル状態を自動的に移行します。移行では、ロールバック用コピーとして `~/.tdc/` を保持し、移行完了を記録するための所有者専用マーカーを `~/.ti/` 配下に作成します。

次の表は、どの状態が移行されるかをまとめたものです。

| 移行されるもの | 移行されないもの |
| --- | --- |
| プロファイルと TiDB Cloud API 認証情報 | バイナリ |
| グローバル設定とテレメトリーのインストール ID | ログとキャッシュ |
| データベース SQL 認証情報 | ローカルオーバーレイ |
| File system の登録情報と認証情報 | マウントロケーターおよび付随するランタイム状態 |

インストール後、新しい実行ファイルを確認し、使用しているリソースに対して読み取り専用コマンドを実行してください。例:

```bash
ti --version

# For TiDB Cloud Starter
ti db list-db-clusters --db-cluster-type starter --output text

# For TiDB Cloud Filesystem
ti fs list-file-systems --output text
```

移行を確認した後、ロールバック用コピーが不要になれば、古い `tdc` バイナリとローカル状態を削除できます。

## ローカル状態の競合を解決する {#resolve-a-local-state-conflict}

`~/.tdc/` と `~/.ti/` がそれぞれ独立して作成されていた場合、または移行マーカーが存在しない、無効である、あるいは別のソースを参照している場合、`ti` はどちらのディレクトリもマージまたは上書きせずに停止します。

どちらのディレクトリを正しいソースオブトゥルースとするかを判断し、もう一方のディレクトリをバックアップ場所へ移動してください。その後、インストーラーまたは `ti` コマンドを再度実行します。認証情報や file system レジストリディレクトリを手動で結合しないでください。

## 環境変数を更新する {#update-environment-variables}

自動化で使用する環境変数名を、次のように更新してください。

| `tdc` v0.1.x 変数 | `ti` 変数 |
| --- | --- |
| `TDC_PROFILE` | `TI_PROFILE` |
| `TDC_REGION_CODE` | `TI_REGION_CODE` |
| `TDC_PUBLIC_KEY` | `TIDB_CLOUD_PUBLIC_KEY` |
| `TDC_PRIVATE_KEY` | `TIDB_CLOUD_PRIVATE_KEY` |
| `TDC_FS_TOKEN` | `TI_FS_TOKEN` |
| `TDC_FS_FILE_SYSTEM_ID` | `TI_FS_FILE_SYSTEM_ID` |
| `TDC_LOGGING` | `TI_LOGGING` |
| `TDC_TELEMETRY` | `TI_TELEMETRY` |
| `TDC_TELEMETRY_TAG` | `TI_TELEMETRY_TAG` |
| `TDC_TELEMETRY_EXTRA` | `TI_TELEMETRY_EXTRA` |
| `TDC_VAULT_TOKEN` | `TI_VAULT_TOKEN` |
| `TDC_INSTALL_DIR` | `TI_INSTALL_DIR` |

v0.2.x の移行期間中、`ti` は対応する新しい変数が設定されていない場合にのみ、従来の `TDC_*` 環境変数を受け入れます。両方の形式が異なる値で設定されている場合、コマンドはローカルまたはリモートの状態を変更する前に失敗します。従来の `TDC_*` 変数のサポートは v0.3.0 で削除されます。

## 次のステップ {#what-s-next}

- [TiDB Cloud CLI のインストール、設定、更新](/ai/ti/reference/ti-install-configure-update.md)
- [TiDB Cloud CLI の設定と認証情報](/ai/ti/reference/ti-configuration-and-credentials.md)
- [TiDB Cloud Starter インスタンスを管理する](/ai/ti/guides/manage-starter-instances.md)
- [TiDB Cloud Filesystem を管理する](/ai/ti/guides/manage-filesystems-via-cli.md)
- [TiDB Cloud CLI のトラブルシューティング](/ai/ti/reference/ti-troubleshooting.md)