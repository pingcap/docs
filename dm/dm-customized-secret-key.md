---
title: Customize a Secret Key for DM Encryption and Decryption
summary: DM（データ移行）データ ソースおよび移行タスク構成で使用されるパスワードを暗号化および復号化するための秘密キーをカスタマイズする方法を学習します。
---

# DM 暗号化と復号化用の秘密鍵をカスタマイズする {#customize-a-secret-key-for-dm-encryption-and-decryption}

バージョン8.0.0より前のバージョンでは、 [DM](/dm/dm-overview.md)データソースおよび移行タスク設定内のパスワードの暗号化と復号に[固定AES-256秘密鍵](https://github.com/pingcap/tiflow/blob/1252979421fc83ffa2a1548d981e505f7fc0b909/dm/pkg/encrypt/encrypt.go#L27)使用していました。しかし、固定の秘密鍵を使用すると、特にセキュリティが極めて重要な環境ではセキュリティリスクが生じる可能性があります。セキュリティを強化するため、バージョン8.0.0以降、DMは固定の秘密鍵を削除し、秘密鍵をカスタマイズできるようになりました。

## 使用法 {#usage}

1.  カスタムキーファイルを作成します。このファイルには、64文字の16進数AES-256秘密鍵が含まれている必要があります。この鍵を生成する方法の一つは、ランダムデータ（例えば`head -n 256 /dev/urandom | sha256sum`のSHA256チェックサムを計算することです。
2.  DM-master [コマンドラインフラグ](/dm/dm-command-line-flags.md)または[設定ファイル](/dm/dm-master-configuration-file.md)で、カスタム キー ファイルのパスとして`secret-key-path`指定します。

## v8.0.0 より前のバージョンからアップグレードする {#upgrade-from-a-version-earlier-than-v8-0-0}

DM はバージョン 8.0.0 以降では固定秘密キーを使用しなくなったため、バージョン 8.0.0 より前のバージョンから DM をアップグレードする場合は次の点に注意してください。

-   [データソース構成](/dm/dm-source-configuration-file.md)と[移行タスクの構成](/dm/task-configuration-file-full.md)両方でプレーンテキスト パスワードが使用されている場合、アップグレードに追加の手順は必要ありません。
-   [データソース構成](/dm/dm-source-configuration-file.md)と[移行タスクの構成](/dm/task-configuration-file-full.md)で暗号化されたパスワードが使用されている場合、または将来的に暗号化されたパスワードを使用する場合は、次の手順を実行する必要があります。
    1.  [DMマスター構成ファイル](/dm/dm-master-configuration-file.md)に`secret-key-path`パラメータを追加し、カスタムキーファイルのパスを指定します。ファイルには、64 文字の 16 進数 AES-256 キーが含まれている必要があります。アップグレード前に[固定AES-256秘密鍵](https://github.com/pingcap/tiflow/blob/1252979421fc83ffa2a1548d981e505f7fc0b909/dm/pkg/encrypt/encrypt.go#L27)使用して暗号化していた場合は、この秘密鍵をキーファイルにコピーできます。すべての DM マスターノードで同じ秘密鍵設定が使用されていることを確認してください。
    2.  まずDMマスターのローリングアップグレードを実行し、次にDMワーカーのローリングアップグレードを実行します。詳細については、 [ローリングアップグレード](/dm/maintain-dm-using-tiup.md#rolling-upgrade)参照してください。

## 暗号化と復号化の秘密鍵を更新する {#update-the-secret-key-for-encryption-and-decryption}

暗号化と復号化に使用される秘密キーを更新するには、次の手順を実行します。

1.  [DMマスター構成ファイル](/dm/dm-master-configuration-file.md)のアップデート`secret-key-path` 。

    > **注記：**
    >
    > -   すべての DM マスター ノードが同じ秘密キー構成に更新されていることを確認します。
    > -   秘密鍵の更新中は、新しい[データソース構成ファイル](/dm/dm-source-configuration-file.md)または[移行タスク構成ファイル](/dm/task-configuration-file-full.md)作成しないでください。

2.  DM マスターのローリング再起動を実行します。

3.  新しい[データソース構成ファイル](/dm/dm-source-configuration-file.md)と[移行タスク構成ファイル](/dm/task-configuration-file-full.md)作成するときは、 `tiup dmctl encrypt` (dmctl バージョン &gt;= v8.0.0) で暗号化されたパスワードを使用します。
