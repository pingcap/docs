---
title: 複数マシン間で TiDB Cloud Filesystem を共有する
summary: 1 つの Filesystem を作成し、2 台目のマシンから安全にアクセスして、データプレーンとマウントの可視性を確認します。
---

# 複数マシン間で TiDB Cloud Filesystem を共有する

このワークフローでは、2 台のマシン上のユーザー、自動化処理、またはエージェントに対して、1 つの共有ワークスペースを提供します。`scp` やアーカイブのアップロードによる特定時点のコピーをやり取りすることなく、変更内容を両方のマシンから見える状態に保つ必要がある場合に使用します。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 仕組み {#how-it-works}

マシン A が Filesystem を作成し、マシン B 用に別個のオーナートークンを生成します。その後、両方のマシンはデータプレーンコマンドまたはマウントされたディレクトリを通じて同じリモート名前空間にアクセスするため、書き込みはフラッシュ後にどちらのインターフェースからも見えるようになります。これにより、手動でのスナップショット同期やオブジェクトストレージ固有の転送ロジックなしで、共有ディレクトリのような動作を実現できます。

| 参加者 | 認証情報 | ワークフローでの役割 |
| --- | --- | --- |
| Machine A | 設定済みの `ti` プロファイルとその FS オーナートークン | Filesystem を作成および管理し、初期データを書き込み、マシン B 用のトークンを生成する |
| Machine B | 自身の FS オーナートークンと Filesystem のリージョンコード | TiDB Cloud API キーやコピーしたプロファイルなしで Filesystem にアクセスする |
| TiDB Cloud Filesystem | 該当なし | 両方のマシンが使用する共有リモート名前空間を提供する |

マシンごとに別のトークンを使用すると、マシン A を中断することなくマシン B のアクセスを取り消せます。両方のトークンはオーナーアクセスを付与するため、シークレットとして転送および保管してください。

## 前提条件 {#prerequisites}

- マシン A で `ti` が設定済みであること。
- 両方のマシンに `ti` がインストールされていること。
- マシン A に `jq` がインストールされていること。
- 安全なシークレット転送チャネルがあること。

## Step 1. マシン A で Filesystem を作成する {#step-1-create-the-filesystem-on-machine-a}

```bash
umask 077
ti fs create-file-system --wait > ./filesystem.json
export FILE_SYSTEM_ID="$(jq -r '.file_system_id' ./filesystem.json)"
export TI_FS_TOKEN="$(jq -r '.fs_token' ./filesystem.json)"

ti fs generate-file-system-token \
  --file-system-id "$FILE_SYSTEM_ID" \
  --token-name machine-b \
  --ttl 720h > ./machine-b-token.json

printf 'from machine A\n' | ti fs copy-file \
  --from-stdin \
  --to-remote /shared/origin.txt
```

`machine-b-token.json` の `fs_token` はシークレットマネージャーを通じて転送し、正規のリージョンコードを伝えてください。コントロールプレーン操作のために `FILE_SYSTEM_ID` はマシン A に保持し、トークンを安全に保管した後は両方の JSON ファイルを削除してください。

## Step 2. マシン B をメモリ内で設定する {#step-2-configure-machine-b-in-memory}

```bash
export TI_FS_TOKEN="<owner-token-from-secret-manager>"
export TI_REGION_CODE="<filesystem-region-code>"
```

`TI_REGION_CODE` には、Filesystem を作成したリージョンを設定します。`ti configure` は不要です。

## Step 3. マシン B で直接可視性を確認する {#step-3-verify-direct-visibility-on-machine-b}

```bash
ti fs read-file --path /shared/origin.txt
printf 'from machine B\n' | ti fs copy-file --from-stdin --to-remote /shared/second.txt
```

## Step 4. マウントとデータプレーンの可視性を確認する {#step-4-verify-mount-and-data-plane-visibility}

```bash
mkdir -p /path/to/shared-workspace
ti fs mount-file-system \
  --mount-path /path/to/shared-workspace

cat /path/to/shared-workspace/shared/origin.txt
printf 'written through mount\n' > /path/to/shared-workspace/shared/mounted.txt

# Graceful unmount flushes pending writes before the data-plane read.
ti fs unmount-file-system --mount-path /path/to/shared-workspace
ti fs read-file --path /shared/mounted.txt
```

最初の読み取りにより、データプレーン経由の書き込みがマウント経由で見えることを確認できます。最後の読み取りにより、マウント経由の書き込みがフラッシュ後にデータプレーンから見えることを確認できます。

## クリーンアップ {#cleanup}

### マシン B での作業 {#on-machine-b}

Step 4 の graceful アンマウント後、現在のシェルから認証情報を削除します。

```bash
unset TI_FS_TOKEN TI_REGION_CODE
```

### マシン A での作業 {#on-machine-a}

```bash
rm -f ./filesystem.json ./machine-b-token.json

ti fs list-file-system-tokens --file-system-id "$FILE_SYSTEM_ID" --output text
ti fs delete-file-system-token \
  --file-system-id "$FILE_SYSTEM_ID" \
  --token-id "<machine-b-token-id>"
ti fs delete-file-system \
  --file-system-id "$FILE_SYSTEM_ID"
```

## セキュリティに関する注意事項 {#security-notes}

- 各 FS トークンはオーナーアクセスを付与します。チャットやコマンド履歴ではなく、シークレットとして転送し、マシンごとに別のトークンを使用してください。
- 複数のライターが同じパスを上書きする可能性があるため、ワークフローレベルで所有権を調整してください。
- graceful アンマウントが完了する前にマシンを終了しないでください。FUSE マウントをオンラインのまま維持しつつリモート永続性が必要な場合にのみ、明示的な drain を使用してください。

## 次のステップ {#what-s-next}

- [TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md)
- [Agent Sandbox で Filesystem を使用する](/ai/ti/guides/ti-agent-sandbox-example.md)
