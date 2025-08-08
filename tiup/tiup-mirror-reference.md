---
title: TiUP Mirror Reference Guide
summary: TiUPミラーの一般情報を学びます。
---

# TiUPミラーリファレンスガイド {#tiup-mirror-reference-guide}

TiUPミラーは、コンポーネントとそのメタデータを保存するTiUPのコンポーネントウェアハウスです。TiUPTiUPには、次の2つの形式があります。

-   ローカル ディスク上のディレクトリ: このドキュメントではローカル ミラーと呼ばれるローカルTiUPクライアントを提供します。
-   リモート ディスク ディレクトリに基づいて開始された HTTP ミラー: このドキュメントではリモート ミラーと呼ばれるリモートTiUPクライアントにサービスを提供します。

## ミラーの作成と更新 {#create-and-update-mirror}

次の 2 つの方法のいずれかを使用してTiUPミラーを作成できます。

-   ミラーを最初から作成するには、 `tiup mirror init`実行します。
-   既存のミラーからクローンを作成するには、 `tiup mirror clone`実行します。

ミラーを作成した後、 `tiup mirror`コマンドを使用してミラーにコンポーネントを追加したり、ミラーからコンポーネントを削除したりできます。TiUPは、ミラーからファイルを削除するのではなく、ファイルを追加して新しいバージョン番号を割り当てることでミラーを更新します。

## ミラー構造 {#mirror-structure}

一般的なミラー構造は次のとおりです。

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

> **注記：**
>
> -   `commits`ディレクトリには、ミラー更新プロセスで生成されたログが保存され、ミラーのロールバックに使用されます。ディスク容量が不足している場合は、古いログディレクトリを定期的に削除できます。
> -   `keys`ディレクトリに保存されている秘密鍵は機密情報です。別途保管することをお勧めします。

### ルートディレクトリ {#root-directory}

TiUPミラーでは、ルート証明書は他のメタデータファイルの公開鍵の保存に使用されます。メタデータファイル（ `*.json` ）を取得するたびに、 TiUPクライアントはメタデータファイルの種類（ルート、インデックス、スナップショット、タイムスタンプ）に基づいて、インストールされた`root.json`から対応する公開鍵を見つける必要があります。その後、 TiUPクライアントは公開鍵を使用して署名の有効性を検証します。

ルート証明書の形式は次のとおりです。

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

### 索引 {#index}

インデックス ファイルには、ミラー内のすべてのコンポーネントとコンポーネントの所有者情報が記録されます。

インデックス ファイルの形式は次のとおりです。

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
                    "threshold": {N}                                 # Indicates that the components owned by the owner must have at least N valid signatures.
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

### 成分 {#component}

コンポーネントのメタデータ ファイルには、コンポーネント固有のプラットフォームとバージョンの情報が記録されます。

コンポーネントメタデータ ファイルの形式は次のとおりです。

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

### スナップショット {#snapshot}

スナップショット ファイルには、各メタデータ ファイルのバージョン番号が記録されます。

スナップショット ファイルの構造は次のとおりです。

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

### タイムスタンプ {#timestamp}

タイムスタンプ ファイルには、現在のスナップショットのチェックサムが記録されます。

タイムスタンプ ファイルの形式は次のとおりです。

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

## クライアントワークフロー {#client-workflow}

クライアントは次のロジックを使用して、ミラーからダウンロードされたファイルが安全であることを確認します。

-   クライアントがインストールされると、バイナリに`root.json`ファイルが含まれます。
-   実行中のクライアントは、既存の`root.json`に基づいて次のタスクを実行します。
    1.  `root.json`からバージョンを取得し、 `N`としてマークします。
    2.  ミラーに`{N+1}.root.json`要求します。要求が成功した場合、 `root.json`で記録した公開鍵を使用して、ファイルが有効かどうかを検証します。
    3.  ミラーから`timestamp.json`要求し、 `root.json`に記録された公開鍵を使用してファイルが有効かどうかを確認します。
    4.  `timestamp.json`に記録された`snapshot.json`のチェックサムがローカルの`snapshot.json`のチェックサムと一致するかどうかを確認します。一致しない場合は、ミラーから最新の`snapshot.json`要求し、 `root.json`に記録された公開鍵を使用してファイルの有効性を検証します。
    5.  `snapshot.json`からファイル`index.json`のバージョン番号`N`を取得し、ミラーに`{N}.index.json`要求します。次に、 `root.json`に記録されている公開鍵を使用して、ファイルが有効かどうかを検証します。
    6.  `tidb.json`や`tikv.json`などのコンポーネントについては、クライアントは`snapshot.json`からコンポーネントのバージョン番号`N`を取得し、ミラーに`{N}.{component}.json`要求します。次に、クライアントは`index.json`に記録されている公開鍵を使用して、ファイルの有効性を検証します。
    7.  コンポーネントのtarファイルの場合、クライアントは`{component}.json`からファイルのURLとチェックサムを取得し、tarパッケージのURLを要求します。そして、クライアントはチェックサムが正しいかどうかを検証します。
