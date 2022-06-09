---
title: TiUP Mirror Reference Guide
summary: Learn the general information of TiUP mirrors.
---

# TiUPミラーリファレンスガイド {#tiup-mirror-reference-guide}

TiUPミラーは、コンポーネントとそのメタデータを格納するTiUPのコンポーネントウェアハウスです。 TiUPミラーは、次の2つの形式を取ります。

-   ローカルディスク上のディレクトリ：このドキュメントではローカルミラーと呼ばれるローカルTiUPクライアントにサービスを提供します。
-   リモートディスクディレクトリに基づいて開始されたHTTPミラー：このドキュメントではリモートミラーと呼ばれるリモートTiUPクライアントにサービスを提供します。

## ミラーの作成と更新 {#create-and-update-mirror}

次の2つの方法のいずれかを使用して、TiUPミラーを作成できます。

-   `tiup mirror init`を実行して、ミラーを最初から作成します。
-   `tiup mirror clone`を実行して、既存のミラーからクローンを作成します。

ミラーの作成後、 `tiup mirror`コマンドを使用して、ミラーにコンポーネントを追加したり、ミラーからコンポーネントを削除したりできます。 TiUPは、ミラーからファイルを削除するのではなく、ファイルを追加して新しいバージョン番号を割り当てることにより、ミラーを更新します。

## ミラー構造 {#mirror-structure}

一般的なミラー構造は次のとおりです。

```
+ <mirror-dir>                                  # Mirror's root directory
|-- root.json                                   # Mirror's root certificate
|-- {2..N}.root.json                            # Mirror's root certificate
|-- {1..N}.index.json                           # Component/user index
|-- {1..N}.{component}.json                     # Component metadata
|-- {component}-{version}-{os}-{arch}.tar.gz    # Component binary package
|-- snapshot.json                               # Mirror's latest snapshot
|-- timestamp.json                              # Mirror's latest timestamp
|--+ commits                                    # Mirror's update log (deletable)
   |--+ commit-{ts1..tsN}
      |-- {N}.root.json
      |-- {N}.{component}.json
      |-- {N}.index.json
      |-- {component}-{version}-{os}-{arch}.tar.gz
      |-- snapshot.json
      |-- timestamp.json
|--+ keys                                       # Mirror's private key (can be moved to other locations)
   |-- {hash1..hashN}-root.json                 # Private key of the root certificate
   |-- {hash}-index.json                        # Private key of the indexes
   |-- {hash}-snapshot.json                     # Private key of the snapshots
   |-- {hash}-timestamp.json                    # Private key of the timestamps
```

> **ノート：**
>
> -   `commits`ディレクトリには、ミラーの更新プロセスで生成されたログが格納され、ミラーをロールバックするために使用されます。ディスク容量が不足している場合は、古いログディレクトリを定期的に削除できます。
> -   `keys`ディレクトリに保存されている秘密鍵は機密情報です。別々に保管することをお勧めします。

### ルートディレクトリ {#root-directory}

TiUPミラーでは、ルート証明書は他のメタデータファイルの公開鍵を格納するために使用されます。メタデータファイル（ `*.json` ）が取得されるたびに、TiUPクライアントは、メタデータファイルタイプ（ルート、インデックス、スナップショット、タイムスタンプ）に基づいて、インストールされた`root.json`で対応する公開鍵を見つける必要があります。次に、TiUPクライアントは公開鍵を使用して、署名が有効かどうかを確認します。

ルート証明書の形式は次のとおりです。

```
{
    "signatures": [                                             # Each metadata file has some signatures which are signed by several private keys corresponding to the file.
        {
            "keyid": "{id-of-root-key-1}",                      # The ID of the first private key that participates in the signature. This ID is obtained by hashing the content of the public key that corresponds to the private key.
            "sig": "{signature-by-root-key-1}"                  # The signed part of this file by this private key.
        },
        ...
        {
            "keyid": "{id-of-root-key-N}",                      # The ID of the Nth private key that participates in the signature.
            "sig": "{signature-by-root-key-N}"                  # The signed part of this file by this private key.
        }
    ],
    "signed": {                                                 # The signed part.
        "_type": "root",                                        # The type of this file. root.json's type is root.
        "expires": "{expiration-date-of-this-file}",            # The expiration time of the file. If the file expires, the client rejects the file.
        "roles": {                                              # Records the keys used to sign each metadata file.
            "{role:index,root,snapshot,timestamp}": {           # Each involved metadata file includes index, root, snapshot, and timestamp.
                "keys": {                                       # Only the key's signature recorded in `keys` is valid.
                    "{id-of-the-key-1}": {                      # The ID of the first key used to sign {role}.
                        "keytype": "rsa",                       # The key's type. Currently, the key type is fixed as rsa.
                        "keyval": {                             # The key's payload.
                            "public": "{public-key-content}"    # The public key's content.
                        },
                        "scheme": "rsassa-pss-sha256"           # Currently, the scheme is fixed as rsassa-pss-sha256.
                    },
                    "{id-of-the-key-N}": {                      # The ID of the Nth key used to sign {role}.
                        "keytype": "rsa",
                        "keyval": {
                            "public": "{public-key-content}"
                        },
                        "scheme": "rsassa-pss-sha256"
                    }
                },
                "threshold": {N},                               # Indicates that the metadata file needs at least N key signatures.
                "url": "/{role}.json"                           # The address from which the file can be obtained. For index files, prefix it with the version number (for example, /{N}.index.json).
            }
        },
        "spec_version": "0.1.0",                                # The specified version followed by this file. If the file structure is changed in the future, the version number needs to be upgraded. The current version number is 0.1.0.
        "version": {N}                                          # The version number of this file. You need to create a new {N+1}.root.json every time you update the file, and set its version to N + 1.
    }
}
```

### 索引 {#index}

インデックスファイルには、ミラー内のすべてのコンポーネントとコンポーネントの所有者情報が記録されます。

インデックスファイルの形式は次のとおりです。

```
{
    "signatures": [                                             # The file's signature.
        {
            "keyid": "{id-of-index-key-1}",                     # The ID of the first private key that participates in the signature.
            "sig": "{signature-by-index-key-1}",                # The signed part of this file by this private key.
        },
        ...
        {
            "keyid": "{id-of-root-key-N}",                      # The ID of the Nth private key that participates in the signature.
            "sig": "{signature-by-root-key-N}"                  # The signed part of this file by this private key.
        }
    ],
    "signed": {
        "_type": "index",                                       # The file type.
        "components": {                                         # The component list.
            "{component1}": {                                   # The name of the first component.
                "hidden": {bool},                               # Whether it is a hidden component.
                "owner": "{owner-id}",                          # The component owner's ID.
                "standalone": {bool},                           # Whether it is a standalone component.
                "url": "/{component}.json",                     # The address from which the component can be obtained. You need to prefix it with the version number (for example, /{N}.{component}.json).
                "yanked": {bool}                                # Indicates whether the component is marked as deleted.
            },
            ...
            "{componentN}": {                                   # The name of the Nth component.
                ...
            },
        },
        "default_components": ["{component1}".."{componentN}"], # The default component that a mirror must contain. Currently, this field defaults to empty (disabled).
        "expires": "{expiration-date-of-this-file}",            # The expiration time of the file. If the file expires, the client rejects the file.
        "owners": {
            "{owner1}": {                                       # The ID of the first owner.
                "keys": {                                       # Only the key's signature recorded in `keys` is valid.
                    "{id-of-the-key-1}": {                      # The first key of the owner.
                        "keytype": "rsa",                       # The key's type. Currently, the key type is fixed as rsa.
                        "keyval": {                             # The key's payload.
                            "public": "{public-key-content}"    # The public key's content.
                        },
                        "scheme": "rsassa-pss-sha256"           # Currently, the scheme is fixed as rsassa-pss-sha256.
                    },
                    ...
                    "{id-of-the-key-N}": {                      # The Nth key of the owner.
                        ...
                    }
                },
                "name": "{owner-name}",                         # The name of the owner.
                "threshod": {N}                                 # Indicates that the components owned by the owner must have at least N valid signatures.
            },
            ...
            "{ownerN}": {                                       # The ID of the Nth owner.
                ...
            }
        }
        "spec_version": "0.1.0",                                # The specified version followed by this file. If the file structure is changed in the future, the version number needs to be upgraded. The current version number is 0.1.0.
        "version": {N}                                          # The version number of this file. You need to create a new {N+1}.index.json every time you update the file, and set its version to N + 1.
    }
}
```

### 成分 {#component}

コンポーネントのメタデータファイルには、コンポーネント固有のプラットフォームとバージョンの情報が記録されます。

コンポーネントメタデータファイルの形式は次のとおりです。

```
{
    "signatures": [                                             # The file's signature.
        {
            "keyid": "{id-of-index-key-1}",                     # The ID of the first private key that participates in the signature.
            "sig": "{signature-by-index-key-1}",                # The signed part of this file by this private key.
        },
        ...
        {
            "keyid": "{id-of-root-key-N}",                      # The ID of the Nth private key that participates in the signature.
            "sig": "{signature-by-root-key-N}"                  # The signed part of this file by this private key.
        }
    ],
    "signed": {
        "_type": "component",                                   # The file type.
        "description": "{description-of-the-component}",        # The description of the component.
        "expires": "{expiration-date-of-this-file}",            # The expiration time of the file. If the file expires, the client rejects the file.
        "id": "{component-id}",                                 # The globally unique ID of the component.
        "nightly": "{nightly-cursor}",                          # The nightly cursor, and the value is the latest nightly version number (for example, v5.0.0-nightly-20201209).
        "platforms": {                                          # The component's supported platforms (such as darwin/amd64, linux/arm64).
            "{platform-pair-1}": {
                "{version-1}": {                                # The semantic version number (for example, v1.0.0).
                    "dependencies": null,                       # Specifies the dependency relationship between components. The field is not used yet and is fixed as null.
                    "entry": "{entry}",                         # The relative path of the entry binary file in the tar package.
                    "hashs": {                                  # The checksum of the tar package. sha256 and sha512 are used.
                        "sha256": "{sum-of-sha256}",
                        "sha512": "{sum-of-sha512}",
                    },
                    "length": {length-of-tar},                  # The length of the tar package.
                    "released": "{release-time}",               # The release date of the version.
                    "url": "{url-of-tar}",                      # The download address of the tar package.
                    "yanked": {bool}                            # Indicates whether this version is disabled.
                }
            },
            ...
            "{platform-pair-N}": {
                ...
            }
        },
        "spec_version": "0.1.0",                                # The specified version followed by this file. If the file structure is changed in the future, the version number needs to be upgraded. The current version number is 0.1.0.
        "version": {N}                                          # The version number of this file. You need to create a new {N+1}.{component}.json every time you update the file, and set its version to N + 1.
}
```

### スナップショット {#snapshot}

スナップショットファイルには、各メタデータファイルのバージョン番号が記録されています。

スナップショットファイルの構造は次のとおりです。

```
{
    "signatures": [                                             # The file's signature.
        {
            "keyid": "{id-of-index-key-1}",                     # The ID of the first private key that participates in the signature.
            "sig": "{signature-by-index-key-1}",                # The signed part of this file by this private key.
        },
        ...
        {
            "keyid": "{id-of-root-key-N}",                      # The ID of the Nth private key that participates in the signature.
            "sig": "{signature-by-root-key-N}"                  # The signed part of this file by this private key.
        }
    ],
    "signed": {
        "_type": "snapshot",                                    # The file type.
        "expires": "{expiration-date-of-this-file}",            # The expiration time of the file. If the file expires, the client rejects the file.
        "meta": {                                               # Other metadata files' information.
            "/root.json": {
                "length": {length-of-json-file},                # The length of root.json
                "version": {version-of-json-file}               # The version of root.json
            },
            "/index.json": {
                "length": {length-of-json-file},
                "version": {version-of-json-file}
            },
            "/{component-1}.json": {
                "length": {length-of-json-file},
                "version": {version-of-json-file}
            },
            ...
            "/{component-N}.json": {
                ...
            }
        },
        "spec_version": "0.1.0",                                # The specified version followed by this file. If the file structure is changed in the future, the version number needs to be upgraded. The current version number is 0.1.0.
        "version": 0                                            # The version number of this file, which is fixed as 0.
    }
```

### タイムスタンプ {#timestamp}

タイムスタンプファイルには、現在のスナップショットのチェックサムが記録されます。

タイムスタンプファイルの形式は次のとおりです。

```
{
    "signatures": [                                             # The file's signature.
        {
            "keyid": "{id-of-index-key-1}",                     # The ID of the first private key that participates in the signature.
            "sig": "{signature-by-index-key-1}",                # The signed part of this file by this private key.
        },
        ...
        {
            "keyid": "{id-of-root-key-N}",                      # The ID of the Nth private key that participates in the signature.
            "sig": "{signature-by-root-key-N}"                  # The signed part of this file by this private key.
        }
    ],
    "signed": {
        "_type": "timestamp",                                   # The file type.
        "expires": "{expiration-date-of-this-file}",            # The expiration time of the file. If the file expires, the client rejects the file.
        "meta": {                                               # The information of snapshot.json.
            "/snapshot.json": {
                "hashes": {
                    "sha256": "{sum-of-sha256}"                 # snapshot.json's sha256.
                },
                "length": {length-of-json-file}                 # The length of snapshot.json.
            }
        },
        "spec_version": "0.1.0",                                # The specified version followed by this file. If the file structure is changed in the future, the version number needs to be upgraded. The current version number is 0.1.0.
        "version": {N}                                          # The version number of this file. You need to overwrite timestamp.json every time you update the file, and set its version to N + 1.
```

## クライアントワークフロー {#client-workflow}

クライアントは次のロジックを使用して、ミラーからダウンロードされたファイルが安全であることを確認します。

-   クライアントのインストール時に、バイナリに`root.json`のファイルが含まれます。
-   実行中のクライアントは、既存の`root.json`に基づいて次のタスクを実行します。
    1.  `root.json`からバージョンを取得し、 `N`としてマークします。
    2.  ミラーから`{N+1}.root.json`を要求します。要求が成功した場合は、 `root.json`で記録された公開鍵を使用して、ファイルが有効かどうかを確認します。
    3.  ミラーから`timestamp.json`を要求し、 `root.json`で記録された公開鍵を使用して、ファイルが有効かどうかを確認します。
    4.  `timestamp.json`で記録された`snapshot.json`のチェックサムがローカル`snapshot.json`のチェックサムと一致するかどうかを確認します。 2つが一致しない場合は、ミラーに最新の`snapshot.json`を要求し、 `root.json`で記録された公開鍵を使用して、ファイルが有効かどうかを確認します。
    5.  `snapshot.json`から`index.json`ファイルのバージョン番号`N`を取得し、ミラーから`{N}.index.json`を要求します。次に、 `root.json`で記録された公開鍵を使用して、ファイルが有効かどうかを確認します。
    6.  `tidb.json`や`tikv.json`などのコンポーネントの場合、クライアントはコンポーネントのバージョン番号`N`を`snapshot.json`から取得し、ミラーから`{N}.{component}.json`を要求します。次に、クライアントは`index.json`で記録された公開鍵を使用して、ファイルが有効かどうかを確認します。
    7.  コンポーネントのtarファイルの場合、クライアントは`{component}.json`からファイルのURLとチェックサムを取得し、tarパッケージのURLを要求します。次に、クライアントはチェックサムが正しいかどうかを確認します。
