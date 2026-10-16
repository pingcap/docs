---
title: TiDB Cloud Filesystem のトラブルシューティング
summary: ファイルシステムのトークン、リージョン、ランタイム、マウント、アクセスの失敗を診断し、安全なリカバリ手順を選択する方法を学びます。
---

# TiDB Cloud Filesystem のトラブルシューティング

以下の症状を使用して、ファイルシステムのアクセス障害やマウント障害を診断します。`--debug` は必要な場合にのみ追加し、共有する前にマスク済みの出力を確認してください。CLI のインストール、API キー認証、Starter、または SQL の障害については、[TiDB Cloud CLI のトラブルシューティング](/ai/ti/reference/ti-troubleshooting.md) を参照してください。

> **Note:**
>
> TiDB Cloud Filesystem は現在パブリックプレビューです。機能およびインターフェースは予告なく変更される場合があります。

## ファイルシステムトークンがない {#file-system-token-is-missing}

クリーンなサンドボックスでは、トークンとリージョンを指定してください。`ti` はトークンからファイルシステム ID を導出します。

```bash
export TI_FS_TOKEN="<owner-token>"
export TI_REGION_CODE="<filesystem-region-code>"
ti fs check-file-system
```

ファイルシステムトークンは TiDB Cloud API private key ではありません。トークンが指定されている場合、`TI_FS_FILE_SYSTEM_ID` は任意です。別途配布された ID がトークンと一致することを `ti` に検証させたい場合にのみ設定してください。

トークンは分かっているものの現在のマシンに保存されていない場合は、それをインポートしてから導出された ID を選択します。

```bash
# Store a known token without requiring TiDB Cloud API keys.
chmod 600 ./fs-token
ti fs import-file-system-token --from-file ./fs-token --region <filesystem-region-code>
ti fs list-files --file-system-id <file-system-id> --path /
```

既知のすべてのトークンが失われた、または失効した場合は、TiDB Cloud API キーを使用して別の owner token を生成します。

```bash
ti fs generate-file-system-token \
  --file-system-id "<file-system-id>" \
  --token-name recovery \
  --ttl 24h
```

新しい平文トークンはレスポンスに一度だけ表示されます。安全に保管するか、`--store-locally` を追加して現在のマシンで選択してください。

## ファイルシステムトークンが拒否される {#file-system-token-is-rejected}

ファイル操作で HTTP 401 または `invalid API key` エラーが返る場合、ファイルシステムトークンが無効化されている、期限切れである、別のマシンで更新された、または失効したことを示している可能性があります。この文脈では、`API key` はファイルシステムトークンを指す場合があり、必ずしも TiDB Cloud API キーに問題があることを意味しません。TiDB Cloud API キーを使用してトークンメタデータを確認してください。

```bash
ti fs list-file-system-tokens \
  --file-system-id "<file-system-id>" \
  --include-expired \
  --output text
```

トークン名は一意ではないため、有効化、無効化、削除の操作には、この出力にある不変の `token_id` を使用してください。トークンのライフサイクルメタデータなしで作成またはインポートされた古い認証情報も有効な場合がありますが、この一覧には行が表示されず、`ti` が一致を推測することはありません。

トークンの有効化、無効化、削除、更新の後は、認証キャッシュが収束するまで約 10 秒待ってください。

更新時に `fs.token_refresh_ambiguous` が報告された場合、レスポンスが失われて結果が不明です。ローテーションがコミットされていなければ古いトークンがまだ使える可能性がありますし、すでに無効になっていて置き換えトークンを復元できない可能性もあります。古いトークンで更新を再試行しないでください。代わりに TiDB Cloud 認証情報を使用して、独立した owner token を生成してください。

ファイルシステムトークンを渡しているときにファイルコマンドが `invalid API key` と終了コード 1 を報告した場合は、API キーペアを確認する前にトークンの状態を確認してください。削除済みまたは無効化されたトークンでは、API キーペアが正しくてもこのメッセージが表示されます。

トークン変更操作で `fs.token_mount_active` が報告された場合は、マウントを使用しているアプリケーションを停止し、開いているファイルを閉じ、エラーに表示された正確なパスを使ってアンマウントしてください。

```bash
ti fs unmount-file-system --mount-path /path/to/workspace
```

CLI のエラーメッセージでは最初に `drain-file-system` を実行するよう提案されますが、正常な FUSE アンマウントでは保留中の書き込みがすでに排出されるため、別途 drain は不要です。`0` の終了ステータスを drain の証拠として扱う前に、マウントログで `reason=force_quit` を確認してください。詳細は [アンマウントは成功を返すが、マウントプロセスが異常終了する](#unmount-returns-success-but-the-mount-process-exits-abnormally) を参照してください。WebDAV は `drain-file-system` をサポートしていないため、WebDAV では正常なアンマウントを使用してください。

その後、トークン操作を再試行してください。別のマシン上のマウントはローカルからは見えないため、そのマシンとのローテーション調整は別途行う必要があります。

## スコープ付きトークンのアクセスが拒否される {#scoped-token-access-is-denied}

スコープ外でスコープ付きトークンを使用すると、コマンドは終了コード 1 で終了し、2 種類のメッセージのいずれかを報告します。ほとんどのコマンドでは `fs access denied` が報告されます。`ti fs copy-file` では代わりに空の `HTTP 403:` が報告されることがあります。

この文脈では、どちらのメッセージも、そのパスに対するその操作がトークンで許可されていないことを示します。どちらも接続性の問題でも、トークンが無効である兆候でもありません。何かを変更する前に、トークンで許可されている内容を確認してください。

```bash
ti fs list-file-system-tokens \
  --file-system-id "<file-system-id>" \
  --output text
```

トークンスコープを、使用したパスおよび操作と比較してください。`search` には `read` も必要です。許可されたパスが `/` でない限り、スコープ付きトークンはファイルシステムルートを一覧表示できません。スコープ付きトークンは自分自身の権限を拡張できないため、既存のトークンを変更しようとするのではなく、必要な操作を持つ新しいスコープ付きトークンを owner token で生成してください。

## ファイルシステムの選択がない {#file-system-selection-is-missing}

TiDB Cloud API キーを使用して、設定済みリージョン内のリモートリソースを一覧表示し、1 つを明示的に選択してください。

```bash
ti fs list-file-systems --output text
ti fs list-files --file-system-id <file-system-id> --path /
```

または、現在のシェルで後続のコマンド用にファイルシステムを選択します。

```bash
export TI_FS_FILE_SYSTEM_ID="<file-system-id>"
```

ローカルに保存されているトークンが 1 つだけであっても、ファイルシステムは明示的に選択してください。その ID またはそれを識別するトークンを指定します。

## ファイルシステムのリージョンがサポートされていない {#file-system-region-is-unsupported}

インストール済みの `ti` リリースが、ファイルシステムアクセス用に設定されたリージョンをサポートしていない可能性があります。[サポートされるリージョン](/tidb-cloud-filesystem/filesystem-regions-and-limitations.md#supported-regions) を確認してください。プロファイル内、またはコマンドの `--region` でサポート対象のリージョンを選択してください。生のサーバー URL は設定しないでください。

## ファイルシステムランタイムがない、または互換性がない {#file-system-runtime-is-missing-or-incompatible}

リリースインストーラーは、バンドルされたファイルシステムランタイム コンポーネントを `ti` の隣に配置します。このランタイムを直接呼び出すことはありません。CLI がランタイム コンポーネントの欠落を報告した場合は、現在のインストーラーを再実行してください。

```bash
curl -fsSL https://github.com/tidbcloud/ti-cli/releases/latest/download/install.sh | sh -s -- --yes
```

`PATH` が期待する `ti` を解決していることを確認してください。

```bash
command -v ti
ti --version
```

任意のスタンドアロンランタイムバイナリをその場所にコピーしないでください。

## ファイルシステム作成がクォータに達する {#file-system-creation-reaches-quota}

作成時にクォータまたは容量エラーが返る場合は、再試行する前に設定済みリージョン内の既存ファイルシステムを一覧表示してください。

```bash
ti fs list-file-systems --output text
```

自動化を通すためだけに無関係なファイルシステムを削除しないでください。支払い方法が必要なためにエラーが TiDB Cloud の請求ページへリンクしている場合は、再試行する前にその案内に従ってください。

## マウントが ready にならない {#mount-does-not-become-ready}

バックグラウンドマウントが正常に開始されると、CLI はランタイム起動メッセージなしで結果を出力します。起動に失敗した、またはタイムアウトした場合は、エラーで報告されたパスにあるログを確認してください。次の点を確認します。

- マウントパスが存在し、書き込み可能である。
- 既存のマウントがそのパスを使用していない。
- ファイルシステムトークンとリージョンが有効である。
- FUSE の前提条件または WebDAV ヘルパーがインストールされている。
- リモートリージョンに到達可能である。

macOS では、macFUSE がインストールされていても、`ti` はデフォルトで WebDAV を使用します。レイヤーおよび checkpoint マウントには FUSE が必要です。ファイルシステムマウントで明示的に FUSE を要求するには、次を実行します。

```bash
ti fs mount-file-system \
  --mount-path /path/to/workspace \
  --driver fuse
```

Linux では、FUSE サポート、`fuse3` パッケージ、および `/dev/fuse` へのアクセスが必要です。ファイルシステムおよび Vault マウントは Windows ではサポートされていません。代わりに `ti fs` のデータプレーンコマンド、またはマウントを使わない Vault コマンドを使用してください。

## マウントは成功するがファイルアクセスがハングする {#mount-succeeds-but-file-access-hangs}

`mounted` の結果は、マウントの起動が完了したことを示します。後続のファイル読み取りや書き込みが成功することまでは保証しません。ディレクトリ一覧は成功しても、ファイルの読み取りがハングすることがあります。

既知の小さなテストファイルに対して、次の手順を使用してください。

1. マウントされた読み取りまたは書き込みが 30 秒経っても戻らない場合は、Ctrl+C でコマンドを中断してください。それでもブロックされたままなら、診断のためにマウント外の別ターミナルを開いてください。マウント上で追加のワークロードを開始しないでください。
2. 同じトークンとリージョンを使用して、`ti fs read-file --path "<remote-file-path>"` で同じファイルを読み取ってください。マウントで `--remote-path` を使用している場合は、リモートファイルパスにそのプレフィックスを含めてください。この読み取りも失敗する場合は、まず報告された認証、リージョン、またはサービスエラーを解決してください。成功する場合は、ローカルのマウントパスに診断を集中してください。
3. `ti --version`、OS バージョン、選択したドライバー、経過時間、および利用可能であればマウント診断ログを記録してください。トークンやファイル内容は含めないでください。macOS では、macFUSE がインストールされていても、ファイルシステムマウントはデフォルトで WebDAV を使用します。問題を再現する際は `--driver webdav` または `--driver fuse` を指定してください。レイヤーおよび checkpoint マウントには FUSE が必要です。
4. マウントを使用しているアプリケーションを停止し、開いているファイルを閉じ、マウント内にいるシェルの作業ディレクトリをその外のパスに変更してください。その後、通常のアンマウントを試してください。

    ```bash
    ti fs unmount-file-system --mount-path /path/to/workspace
    ```

5. アンマウント成功後、必要な書き込みがあれば直接 CLI 読み取りで確認してください。マウントを調査している間は直接 `ti fs` コマンドを使い続け、置き換え用マウントを使用する前にファイル I/O を確認してください。

WebDAV では `drain-file-system` を使用しないでください。アンマウントに失敗した場合、またはリモートデータが欠落している場合は、リカバリのためにマシンとローカルマウントデータを保持してください。キャッシュ削除や強制アンマウントを通常の再試行手順として行わないでください。保留中の書き込みがまだローカルにしか存在しない可能性があります。上記の 30 秒の打ち切りは、小さなファイルのスモークテストにおける診断上の目安であり、サービスのレイテンシー保証ではありません。

## Ubuntu 26.04 で `/workspace` 配下の FUSE マウントが拒否される {#ubuntu-2604-rejects-a-fuse-mount-under-workspace}

Ubuntu 26.04 では、`fusermount3` に AppArmor プロファイルが適用されます。デフォルトのマウントパス許可リストには `/workspace` が含まれていないため、root ユーザーと非 root ユーザーの両方で次のエラーが発生することがあります。

```text
/usr/bin/fusermount3: mount failed: Permission denied
```

拒否を確認してください。

```bash
sudo journalctl -k --since "10 minutes ago" |
  grep 'profile="fusermount3"'
```

`operation="mount"`、`name="/workspace/"`、`info="failed mntpnt match"` を含むエントリは、この制限を示しています。代わりに `$HOME` または `/mnt` 配下にマウントしてください。

```bash
mkdir -p "$HOME/workspace"
ti fs mount-file-system --mount-path "$HOME/workspace"
```

`/workspace` の所有者やモードを変更しても AppArmor は回避できません。パスを変更できない場合は、[Ubuntu 26.04 のマウントパス制限](/tidb-cloud-filesystem/filesystem-mount-linux.md#ubuntu-2604-mount-path-restrictions) に記載されているように、`/etc/apparmor.d/local/fusermount3` に明示的な `/workspace` の mount および unmount ルールを追加してください。

## プロセスクラッシュ後にマウントが stale になる {#mount-becomes-stale-after-a-process-crash}

graceful unmount を行わずに companion が強制終了された場合、FUSE アクセスで `EIO` または `Transport endpoint is not connected` が返されることがあります。開いているファイルを持つプロセスを停止してから、次を試してください。

```bash
ti fs unmount-file-system \
  --mount-path /path/to/workspace \
  --force
```

locator が残っていない場合でもクリーンアップを成功させる必要があるときは、`--ignore-absent` を使用します。強制的なクリーンアップでは、削除されたローカルディスク上の保留中の書き込みのリカバリは保証されません。

## アンマウントで busy が報告される {#unmount-reports-busy}

エディタ、作業ディレクトリがマウント内にあるシェル、そのほか開いているファイルハンドルを閉じてから、再試行してください。

```bash
ti fs unmount-file-system --mount-path /path/to/workspace
```

graceful な FUSE アンマウントでは保留中の書き込みが自動的にフラッシュされますが、それはマウントプロセスが正常終了した場合に限られます。`unmount-file-system` の終了ステータス `0` を信用する前に、マウントログで `reason=force_quit` を確認してください。詳細は [アンマウントは成功を返すが、マウントプロセスが異常終了する](#unmount-returns-success-but-the-mount-process-exits-abnormally) を参照してください。`drain-file-system` を個別に実行しても、開いているファイルは閉じられず、busy なマウントも解消されません。これは、マウントを動作させたまま保留中の書き込みをフラッシュするために使用します。WebDAV は drain をサポートしていません。

## アンマウントは成功を返すが、マウントプロセスが異常終了する {#unmount-returns-success-but-the-mount-process-exits-abnormally}

`ti v0.2.6` では、レイヤーまたは checkpoint のマウントで、バックグラウンドプロセスが `late pending drain` に続いて `reason=force_quit` を報告し、終了コード `1` で終了している場合でも、約 30 秒後に `unmounted` が返されることがあります。この動作は、レイヤーから小さなファイルを読み取った後、およびレイヤーマウントに対して書き込み、fsync、drain を行った後に観測されています。

この問題は、`ti` v0.2.7 で使用される同梱ランタイム `60b63d6` にも存在します。CLI と同梱ランタイムは別々にバージョン管理されているため、CLI バージョンだけではマウントが影響を受けるかどうかは判断できません。修正状況については、[bundled mount runtime の修正 (Drive9 #1002)](https://github.com/mem9-ai/drive9/pull/1002) を参照してください。

レイヤーまたは checkpoint のアンマウント結果を信用する前に、そのバックグラウンドのマウントログを確認してください。`ti` v0.2.7 では、`mount-file-system` コマンドが成功してもログパスは表示されません。デフォルトでは、次のコマンドでログを見つけられます。

```bash
find "$HOME/.ti/drive9-home" -type f -path '*/drive9/mount-logs/mount-*.log'
```

Linux では、`XDG_CACHE_HOME` が設定されている場合は、代わりに `$XDG_CACHE_HOME/drive9/mount-logs` を確認してください。ログをマウントパスおよびマウント時刻に対応付けたうえで、`late pending drain`、`reason=force_quit`、またはバックグラウンドプロセスの非ゼロ終了コードを探してください。

これらのいずれかが見つかった場合:

1. 結果を異常シャットダウンとして扱い、マシンとローカルキャッシュを利用可能なままにしてください。
2. 必要なレイヤーファイルを、`--layer-id` を使用した直接の CLI 読み取りで検証してください。コミット済みの変更については、レイヤーを選択せずにベースファイルシステムを読み取ってください。checkpoint を検証するには、同じ `--layer-ref` と `--checkpoint-id` を使って新しいローカルパスにマウントし、必要なファイルを再度読み取ってください。書き込み可能なレイヤーを新しいパスに再マウントして、以前のマウントとは独立して内容を検証することもできます。
3. 検証が完了するまで、レイヤーの commit や discard、またはローカル状態の削除を行わないでください。問題を報告する際は、CLI バージョンと秘匿情報を除去したマウントログを含めてください。

## 終了コード {#exit-codes}

`ti fs` は次の終了コードを使用します。自動化では、エラーテキストに一致させる代わりに、これらに基づいて分岐できます。

| コード | 意味 | 対応方法 |
| --- | --- | --- |
| 0 | 成功 | 続行します。 |
| 1 | ランタイムまたはリモート API エラー | メッセージを読み、報告されたランタイム、ネットワーク、またはサービスのエラーに対処してください。scoped token の拒否や一部のその他のサービスエラーでもこのコードが使用されます。 |
| 2 | ローカルの使用方法、検証、または設定エラー | コマンドまたはプロファイルを修正してください。例として、不明なフラグ、必須入力の不足、未サポートのリージョン、または権限が緩い token ファイルがあります。 |
| 3 | 認証失敗 | token または API key pair を確認してください。 |
| 4 | アカウントにその操作を行う権限がない | 組織管理者に依頼してください。これは scoped-token の拒否とは異なり、scoped-token の拒否は終了コード 1 を返します。 |
| 5 | リクエストで指定された file system、token、またはその他のリソースが存在しない | ID を確認してください。file system 内に存在しないパスは 5 ではなく 1 を返します。 |

削除または無効化された file system token は、上記の表の例外です。file コマンドは 3 ではなく終了コード 1 を返します。詳細は [file system token が拒否される](#file-system-token-is-rejected) を参照してください。

## 問題を報告する {#report-a-problem}

`ti` のバージョン、OS とアーキテクチャ、コマンド名、安定したエラーコード、および秘匿情報を除去したログを含めてください。API keys、file system または Vault tokens、DB パスワード、秘密データを含む SQL、またはファイル内容は絶対に含めないでください。問題の報告先は [github.com/tidbcloud/ti-cli/issues](https://github.com/tidbcloud/ti-cli/issues) です。