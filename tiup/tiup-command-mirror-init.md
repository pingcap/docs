---
title: tiup mirror init
summary: tiup mirror init コマンドは空のミラーを初期化し、root.json、1.index.json、snapshot.json、timestamp.json ファイルを生成します。ミラー ファイルのローカル ディレクトリを指定するには、`tiup mirror init <path>` を使用します。秘密鍵ファイルのディレクトリを指定するには、-k または --key-dir オプションを使用します。指定したディレクトリが空でない場合は、エラーが報告されます。
---

# tiup mirror init {#tiup-mirror-init}

コマンド`tiup mirror init`は、空のミラーを初期化するために使用されます。初期化されたミラーには、コンポーネントまたはコンポーネント所有者は含まれません。このコマンドは、初期化されたミラーに対して次のファイルのみを生成します。

    + <mirror-dir>                                  # Mirror's root directory
    |-- root.json                                   # Mirror's root certificate
    |-- 1.index.json                                # Component/user index
    |-- snapshot.json                               # Mirror's latest snapshot
    |-- timestamp.json                              # Mirror's latest timestamp
    |--+ keys                                       # Mirror's private key (can be moved to other locations)
       |-- {hash1..hashN}-root.json                 # Private key of the root certificate
       |-- {hash}-index.json                        # Private key of the indexes
       |-- {hash}-snapshot.json                     # Private key of the snapshots
       |-- {hash}-timestamp.json                    # Private key of the timestamps

上記ファイルの具体的な使用方法や内容の形式については、 [TiUPミラーリファレンスガイド](/tiup/tiup-mirror-reference.md)を参照してください。

## 構文 {#syntax}

```shell
tiup mirror init <path> [flags]
```

`<path>` 、 TiUP がミラー ファイルを生成して保存するローカル ディレクトリを指定するために使用されます。ローカル ディレクトリは相対パスにすることができます。指定されたディレクトリがすでに存在する場合は、空である必要があります。存在しない場合は、 TiUP自動的に作成されます。

## オプション {#options}

### -k, --key-dir {#k-key-dir}

-   TiUP が秘密鍵ファイルを生成するディレクトリを指定します。指定されたディレクトリが存在しない場合は、 TiUPによって自動的に作成されます。
-   データ型: `STRING`
-   コマンドでこのオプションが指定されていない場合、 TiUP はデフォルトで`{path}/keys`に秘密鍵ファイルを生成します。

### 出力 {#outputs}

-   コマンドが正常に実行された場合、出力はありません。
-   指定された`<path>`空でない場合、 TiUP はエラー`Error: the target path '%s' is not an empty directory`を報告します。
-   指定された`<path>`ディレクトリでない場合、 TiUP はエラー`Error: fdopendir: not a directory`を報告します。

[&lt;&lt; 前のページに戻る - TiUPミラーコマンドリスト](/tiup/tiup-command-mirror.md#command-list)
