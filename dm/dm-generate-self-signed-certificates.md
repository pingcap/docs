---
title: Generate Self-signed Certificates for TiDB Data Migration
summary: openssl を使用して自己署名証明書を生成します。
---

# TiDB データ移行用の自己署名証明書を生成する {#generate-self-signed-certificates-for-tidb-data-migration}

このドキュメントでは、 `openssl`使用して TiDB データ移行 (DM) 用の自己署名証明書を生成する例を示します。また、必要に応じて要件を満たす証明書とキーを生成することもできます。

インスタンス クラスターのトポロジが次のとおりであると仮定します。

| 名前   | ホストIP        | サービス    |
| ---- | ------------ | ------- |
| ノード1 | 172.16.10.11 | DMマスター1 |
| ノード2 | 172.16.10.12 | DMマスター2 |
| ノード3 | 172.16.10.13 | DMマスター3 |
| ノード4 | 172.16.10.14 | DMワーカー1 |
| ノード5 | 172.16.10.15 | DMワーカー2 |
| ノード6 | 172.16.10.16 | DMワーカー3 |

## OpenSSLをインストールする {#install-openssl}

-   Debian または Ubuntu OS の場合:

    ```bash
    apt install openssl
    ```

-   RedHat または CentOS OS の場合:

    ```bash
    yum install openssl
    ```

インストールについては OpenSSL の公式[ドキュメントをダウンロード](https://www.openssl.org/source/)も参照してください。

## CA証明書を生成する {#generate-the-ca-certificate}

証明機関 (CA) は、デジタル証明書を発行する信頼できるエンティティです。実際には、管理者に連絡して証明書を発行するか、信頼できる CA を使用します。CA は複数の証明書ペアを管理します。ここでは、次のようにしてオリジナルの証明書ペアを生成するだけです。

1.  CA キーを生成します:

    ```bash
    openssl genrsa -out ca-key.pem 4096
    ```

2.  CA 証明書を生成します。

    ```bash
    openssl req -new -x509 -days 1000 -key ca-key.pem -out ca.pem
    ```

3.  CA 証明書を検証します。

    ```bash
    openssl x509 -text -in ca.pem -noout
    ```

## 個々のコンポーネントの証明書を発行する {#issue-certificates-for-individual-components}

### クラスターで使用される可能性のある証明書 {#certificates-that-might-be-used-in-the-cluster}

-   DM-master が他のコンポーネントに対して DM-master を認証するために使用する`master`証明書。
-   DM-worker が他のコンポーネントに対して DM-worker を認証するために使用する`worker`証明書。
-   DM マスターと DM ワーカーのクライアントを認証するために dmctl によって使用される`client`証明書。

### DMマスターの証明書を発行する {#issue-certificates-for-dm-master}

DM マスター インスタンスに証明書を発行するには、次の手順を実行します。

1.  証明書に対応する秘密鍵を生成します。

    ```bash
    openssl genrsa -out master-key.pem 2048
    ```

2.  OpenSSL 構成テンプレート ファイルのコピーを作成します (テンプレート ファイルは複数の場所にある可能性があるため、実際の場所を参照してください)。

    ```bash
    cp /usr/lib/ssl/openssl.cnf .
    ```

    実際の場所がわからない場合は、ルート ディレクトリで探します。

    ```bash
    find / -name openssl.cnf
    ```

3.  `openssl.cnf`を編集し、 `[ req ]`フィールドの下に`req_extensions = v3_req`を追加し、 `[ v3_req ]`フィールドの下に`subjectAltName = @alt_names`を追加します。最後に、新しいフィールドを作成し、上記のクラスター トポロジの説明に従って`Subject Alternative Name` (SAN) の情報を編集します。

        [ alt_names ]
        IP.1 = 127.0.0.1
        IP.2 = 172.16.10.11
        IP.3 = 172.16.10.12
        IP.4 = 172.16.10.13

    現在、SAN の次のチェック項目がサポートされています。

    -   `IP`

    -   `DNS`

    -   `URI`

    > **注記：**
    >
    > `0.0.0.0`のような特殊な IP を接続や通信に使用する場合は、 `alt_names`にも追加する必要があります。

4.  `openssl.cnf`ファイルを保存し、証明書要求ファイルを生成します。( `Common Name (e.g. server FQDN or YOUR name) []:`に入力するときに、証明書に`dm`などの共通名 (CN) を割り当てます。これは、サーバーがクライアントの ID を検証するために使用されます。各コンポーネントは、デフォルトでは検証を有効にしません。構成ファイルで有効にすることができます。)

    ```bash
    openssl req -new -key master-key.pem -out master-cert.pem -config openssl.cnf
    ```

5.  証明書を発行して生成します。

    ```bash
    openssl x509 -req -days 365 -CA ca.pem -CAkey ca-key.pem -CAcreateserial -in master-cert.pem -out master-cert.pem -extensions v3_req -extfile openssl.cnf
    ```

6.  証明書に SAN フィールドが含まれていることを確認します (オプション)。

    ```bash
    openssl x509 -text -in master-cert.pem -noout
    ```

7.  現在のディレクトリに次のファイルが存在することを確認します。

        ca.pem
        master-cert.pem
        master-key.pem

> **注記：**
>
> DM ワーカー インスタンスの証明書を発行するプロセスも同様であるため、このドキュメントでは繰り返しません。

### クライアントの証明書を発行する (dmctl) {#issue-certificates-for-the-client-dmctl}

クライアント (dmctl) に証明書を発行するには、次の手順を実行します。

1.  証明書に対応する秘密鍵を生成します。

    ```bash
    openssl genrsa -out client-key.pem 2048
    ```

2.  証明書要求ファイルを生成します (この手順では、証明書に共通名を割り当てることもできます。共通名は、サーバーがクライアントの ID を検証するために使用されます。各コンポーネントはデフォルトで検証を有効にしませんが、構成ファイルで有効にすることができます)。

    ```bash
    openssl req -new -key client-key.pem -out client-cert.pem
    ```

3.  証明書を発行して生成します。

    ```bash
    openssl x509 -req -days 365 -CA ca.pem -CAkey ca-key.pem -CAcreateserial -in client-cert.pem -out client-cert.pem
    ```
