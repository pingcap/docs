---
title: TiDB Cloud Filesystem CLI コマンドリファレンス
summary: file system リソース、ファイル、レイヤー、パック、マウント向けのすべての `ti fs` コマンドを参照します。
---

# TiDB Cloud Filesystem CLI コマンドリファレンス

`ti fs` を使用して TiDB Cloud Filesystem リソースをプロビジョニングし、コマンドまたはローカルマウントからそのデータにアクセスできます。

コマンド構文では、角括弧（`[]`）は省略可能な項目を囲みます。丸括弧は必須の選択肢をグループ化し、縦棒（`|`）は代替候補を区切ります。たとえば、`(--ttl <duration> | --no-expiration)` は、2 つのオプションのうちちょうど 1 つを指定する必要があることを意味します。

## リソースとトークンのコマンド {#resource-and-token-commands}

| コマンド | 説明 |
| --- | --- |
| [`create-file-system`](/ai/ti/reference/ti-fs-create-file-system.md) | file system とその初期オーナートークンを作成します。 |
| [`list-file-systems`](/ai/ti/reference/ti-fs-list-file-systems.md) | 有効なリージョン内の file system を一覧表示します。 |
| [`describe-file-system`](/ai/ti/reference/ti-fs-describe-file-system.md) | ID で 1 つの file system の詳細を表示します。 |
| [`check-file-system`](/ai/ti/reference/ti-fs-check-file-system.md) | file system の選択、ルーティング、認証情報、およびデータプレーンアクセスを確認します。 |
| [`delete-file-system`](/ai/ti/reference/ti-fs-delete-file-system.md) | file system を完全に削除します。 |
| [`import-file-system-token`](/ai/ti/reference/ti-fs-import-file-system-token.md) | 既存の file system トークンをローカルにインポートして選択します。 |
| [`generate-file-system-token`](/ai/ti/reference/ti-fs-generate-file-system-token.md) | 追加のオーナートークンを生成します。 |
| [`generate-file-system-scoped-token`](/ai/ti/reference/ti-fs-generate-file-system-scoped-token.md) | パス、操作、および有効期間で制限されたトークンを生成します。 |
| [`list-file-system-tokens`](/ai/ti/reference/ti-fs-list-file-system-tokens.md) | シークレットを含まないトークンメタデータを一覧表示します。 |
| [`enable-file-system-token`](/ai/ti/reference/ti-fs-enable-file-system-token.md) | 無効化されたトークンを再度有効にします。 |
| [`disable-file-system-token`](/ai/ti/reference/ti-fs-disable-file-system-token.md) | トークンを一時的に無効にします。 |
| [`delete-file-system-token`](/ai/ti/reference/ti-fs-delete-file-system-token.md) | トークンを完全に失効させます。 |
| [`refresh-file-system-token`](/ai/ti/reference/ti-fs-refresh-file-system-token.md) | トークンをローテーションし、その置き換えトークンを 1 回だけ返します。 |

### トークン管理の認可 {#token-management-authorization}

オーナートークンがトークン管理を認可している場合、そのトークンはトークンの一覧表示、スコープ付きトークンの作成、およびオーナートークンまたはスコープ付きトークンの失効を実行できます。有効化または無効化できるのはスコープ付きトークンのみです。TiDB Cloud API 認証情報は、どちらの種類のトークンでも有効化、無効化、または失効できます。

## AI プロバイダー設定コマンド {#ai-provider-configuration-commands}

これらのコマンドは、メディアファイルからコンテンツを抽出し、埋め込みを生成するためのオプションのプロバイダーを設定します。通常の file system リソース操作およびファイル操作では、AI プロバイダー設定は不要です。

| コマンド | 説明 |
| --- | --- |
| [`describe-file-system-extract-configuration`](/ai/ti/reference/ti-fs-describe-file-system-extract-configuration.md) | メディア抽出プロバイダーの設定を表示します。 |
| [`update-file-system-extract-configuration`](/ai/ti/reference/ti-fs-update-file-system-extract-configuration.md) | メディアコンテンツの抽出に使用するプロバイダーを更新します。 |
| [`describe-file-system-embedding-configuration`](/ai/ti/reference/ti-fs-describe-file-system-embedding-configuration.md) | 埋め込みプロバイダーの設定を表示します。 |
| [`update-file-system-embedding-configuration`](/ai/ti/reference/ti-fs-update-file-system-embedding-configuration.md) | 埋め込みの生成に使用するプロバイダーを更新します。 |

## データおよび名前空間のコマンド {#data-and-namespace-commands}

| コマンド | 説明 |
| --- | --- |
| [`copy-file`](/ai/ti/reference/ti-fs-copy-file.md) | ローカルストレージと file system の間、または file system 内でファイルをコピーします。 |
| [`read-file`](/ai/ti/reference/ti-fs-read-file.md) | リモートファイルまたはバイト範囲を読み取ります。 |
| [`list-files`](/ai/ti/reference/ti-fs-list-files.md) | リモートパス配下のエントリを一覧表示します。 |
| [`describe-file`](/ai/ti/reference/ti-fs-describe-file.md) | リモートファイルまたはディレクトリの詳細を表示します。 |
| [`move-file`](/ai/ti/reference/ti-fs-move-file.md) | リモートパスを移動または名前変更します。 |
| [`delete-file`](/ai/ti/reference/ti-fs-delete-file.md) | リモートファイルまたはディレクトリを削除します。 |
| [`create-directory`](/ai/ti/reference/ti-fs-create-directory.md) | リモートディレクトリを作成します。 |
| [`chmod-file`](/ai/ti/reference/ti-fs-chmod-file.md) | POSIX スタイルのモードメタデータを変更します。 |
| [`create-symlink`](/ai/ti/reference/ti-fs-create-symlink.md) | シンボリックリンクを作成します。 |
| [`create-hardlink`](/ai/ti/reference/ti-fs-create-hardlink.md) | ハードリンクを作成します。 |
| [`search-file-content`](/ai/ti/reference/ti-fs-search-file-content.md) | 抽出されたファイルコンテンツと説明を検索します。 |
| [`find-files`](/ai/ti/reference/ti-fs-find-files.md) | 名前、タグ、日付、サイズ、またはタイプでファイルを検索します。 |

## レイヤーとポータビリティのコマンド {#layer-and-portability-commands}

| コマンド | 説明 |
| --- | --- |
| [`create-layer`](/ai/ti/reference/ti-fs-create-layer.md) | 分離された書き込み可能なレイヤーを作成します。 |
| [`list-layers`](/ai/ti/reference/ti-fs-list-layers.md) | file system 内のレイヤーを一覧表示します。 |
| [`fork-layer`](/ai/ti/reference/ti-fs-fork-layer.md) | 親の tip またはチェックポイントから子レイヤーをフォークします。 |
| [`list-layer-chain`](/ai/ti/reference/ti-fs-list-layer-chain.md) | レイヤーの固定された祖先チェーンを一覧表示します。 |
| [`describe-layer`](/ai/ti/reference/ti-fs-describe-layer.md) | ID でレイヤーの詳細を表示します。 |
| [`diff-layer`](/ai/ti/reference/ti-fs-diff-layer.md) | レイヤーに記録された変更を一覧表示します。 |
| [`create-layer-checkpoint`](/ai/ti/reference/ti-fs-create-layer-checkpoint.md) | レイヤー内に永続的なチェックポイントを作成します。 |
| [`delete-layer`](/ai/ti/reference/ti-fs-delete-layer.md) | レイヤーを論理的に破棄します。 |
| [`rollback-layer`](/ai/ti/reference/ti-fs-rollback-layer.md) | 変更をコミットせずにレイヤーをロールバックします。 |
| [`commit-layer`](/ai/ti/reference/ti-fs-commit-layer.md) | レイヤーの変更をベース file system に適用します。 |
| [`pack-file-system`](/ai/ti/reference/ti-fs-pack-file-system.md) | 選択したローカルオーバーレイ状態を file system にアーカイブします。 |
| [`unpack-file-system`](/ai/ti/reference/ti-fs-unpack-file-system.md) | アーカイブからローカルオーバーレイ状態を復元します。 |

### レイヤー参照 {#layer-references}

レイヤー参照には、レイヤー ID、一意のレイヤー名、または `tag:<key>=<value>` 形式のタグ参照を使用できます。たとえば `tag:run=123` です。名前とタグ参照は曖昧になる可能性があるため、自動化ではレイヤー ID を使用してください。

### マウントプロファイルとローカルオーバーレイ {#mount-profiles-and-local-overlays}

ローカルオーバーレイには、マウントプロファイルがリモート名前空間ではなくローカルマシン上に保持するファイルが保存されます。マウントプロファイルは、どのパスでそのオーバーレイを使用するかを定義します。

| マウントプロファイル | 動作 |
| --- | --- |
| `coding-agent` | バージョン管理メタデータ、依存関係ディレクトリ、キャッシュ、ビルド出力、および一般的な一時パスをローカルオーバーレイに保持します。自動パックパスは選択しません。 |
| `portable` | `coding-agent` と同じローカルパスルールを使用し、デフォルトで完全なオーバーレイをパックまたは unpack するため、マシン間やサンドボックスセッション間で移動できます。 |
| `none` | ローカルオーバーレイのパスルーティングと、自動パックまたは unpack の動作を無効にします。 |

## マウントコマンド {#mount-commands}

| コマンド | 説明 |
| --- | --- |
| [`mount-file-system`](/ai/ti/reference/ti-fs-mount-file-system.md) | ローカルパスに file system をマウントします。 |
| [`drain-file-system`](/ai/ti/reference/ti-fs-drain-file-system.md) | 稼働中の FUSE マウントから保留中の書き込みをフラッシュします。 |
| [`unmount-file-system`](/ai/ti/reference/ti-fs-unmount-file-system.md) | file system をフラッシュしてアンマウントします。 |

## コマンドエイリアス {#command-aliases}

以下の `ti fs` コマンドには Unix スタイルのエイリアスがあります。たとえば、`ti fs cp` は `ti fs copy-file` と同等です。表に記載されていないコマンド（`pack-file-system` や `unpack-file-system` を含む）にはエイリアスがありません。

| エイリアス | 正規コマンド |
| --- | --- |
| `cp` | `copy-file` |
| `cat` | `read-file` |
| `ls` | `list-files` |
| `stat` | `describe-file` |
| `mv` | `move-file` |
| `rm` | `delete-file` |
| `mkdir` | `create-directory` |
| `chmod` | `chmod-file` |
| `symlink` | `create-symlink` |
| `hardlink` | `create-hardlink` |
| `grep` | `search-file-content` |
| `find` | `find-files` |
| `mount` | `mount-file-system` |
| `drain` | `drain-file-system` |
| `umount` | `unmount-file-system` |

エイリアスは、正規コマンドと同じオプション、認証、出力、クエリ、およびエラー動作を使用します。

## 関連情報 {#see-also}

- [Manage File Systems](/tidb-cloud-filesystem/manage-filesystem-resources.md)
- [Configure AI Providers for a File System](/tidb-cloud-filesystem/configure-filesystem-ai-providers.md)
- [Manage File System Tokens](/tidb-cloud-filesystem/manage-filesystem-tokens.md)
- [Work with Files and Directories](/tidb-cloud-filesystem/work-with-filesystem-data.md)
- [Manage File System Layers and Checkpoints](/tidb-cloud-filesystem/manage-filesystem-layers.md)
- [Mount a File System](/tidb-cloud-filesystem/filesystem-mount.md)
- [Manage Git Workspaces on TiDB Cloud Filesystem](/tidb-cloud-filesystem/manage-git-workspaces.md)
- [Use Journals in a File System](/tidb-cloud-filesystem/use-filesystem-journals.md)
- [Manage Vault Secrets for a File System](/tidb-cloud-filesystem/manage-filesystem-vault-secrets.md)
