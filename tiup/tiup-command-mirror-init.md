---
title: tiup mirror init
---

# tiup mirror init {#tiup-mirror-init}

コマンド`tiup mirror init`は、空のミラーを初期化するために使用されます。初期化されたミラーには、コンポーネントまたはコンポーネントの所有者が含まれません。このコマンドは、初期化されたミラーに対して次のファイルのみを生成します。

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

上記ファイルの具体的な使い方や内容形式については、 [TiUPミラー リファレンス ガイド](/tiup/tiup-mirror-reference.md)を参照してください。

## 構文 {#syntax}

```shell
tiup mirror init <path> [flags]
```

`<path>`は、 TiUP がミラー ファイルを生成および保存するローカル ディレクトリを指定するために使用されます。ローカル ディレクトリには相対パスを指定できます。指定したディレクトリがすでに存在する場合は、空にする必要があります。存在しない場合は、 TiUP が自動的に作成します。

## オプション {#options}

### -k、--キーディレクトリ {#k-key-dir}

-   TiUP が秘密鍵ファイルを生成するディレクトリを指定します。指定したディレクトリが存在しない場合は、 TiUP が自動的に作成します。
-   データ型: `STRING`
-   このオプションがコマンドで指定されていない場合、 TiUP はデフォルトで秘密鍵ファイルを`{path}/keys`に生成します。

### 出力 {#outputs}

-   コマンドが正常に実行された場合、出力はありません。
-   指定された`<path>`が空でない場合、 TiUP はエラー`Error: the target path '%s' is not an empty directory`を報告します。
-   指定された`<path>`ディレクトリではない場合、 TiUP はエラー`Error: fdopendir: not a directory`を報告します。

[&lt;&lt; 前のページに戻る - TiUP Mirror コマンド一覧](/tiup/tiup-command-mirror.md#command-list)
