---
title: tiup mirror init
---

# tiup mirror init {#tiup-mirror-init}

コマンド`tiup mirror init`は、空のミラーを初期化するために使用されます。初期化されたミラーには、コンポーネントまたはコンポーネント所有者は含まれていません。このコマンドは、初期化されたミラーに対して次のファイルのみを生成します。

```
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
```

上記のファイルの具体的な使用法とコンテンツ形式については、 [TiUPミラーリファレンスガイド](/tiup/tiup-mirror-reference.md)を参照してください。

## 構文 {#syntax}

```shell
tiup mirror init <path> [flags]
```

`<path>`は、TiUPがミラーファイルを生成および保存するローカルディレクトリを指定するために使用されます。ローカルディレクトリは相対パスにすることができます。指定されたディレクトリがすでに存在する場合は、空である必要があります。存在しない場合、TiUPは自動的に作成します。

## オプション {#options}

### -k、-key-dir {#k-key-dir}

-   TiUPが秘密鍵ファイルを生成するディレクトリを指定します。指定されたディレクトリが存在しない場合、TiUPは自動的にそれを作成します。
-   データ型： `STRING`
-   このオプションがコマンドで指定されていない場合、TiUPはデフォルトで秘密鍵ファイルを`{path}/keys`で生成します。

### 出力 {#outputs}

-   コマンドが正常に実行された場合、出力はありません。
-   指定された`<path>`が空でない場合、TiUPはエラー`Error: the target path '%s' is not an empty directory`を報告します。
-   指定された`<path>`がディレクトリでない場合、TiUPはエラー`Error: fdopendir: not a directory`を報告します。

[&lt;&lt;前のページに戻る-TiUPミラーコマンドリスト](/tiup/tiup-command-mirror.md#command-list)
