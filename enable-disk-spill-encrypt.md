---
title: Enable Encryption for Disk Spill
summary: Learn how to enable encryption for disk spill in TiDB.
---

# ディスク流出時の暗号化機能を有効にする {#enable-encryption-for-disk-spill}

`oom-use-tmp-storage`構成項目が`true`に設定されている場合、単一のSQLステートメントのメモリ使用量がシステム変数[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)の制限を超えると、一部のオペレーターは実行中の中間結果を一時ファイルとしてディスクに保存し、その後ファイルを削除できます。クエリが完了しました。

ディスクスピルの暗号化を有効にして、攻撃者がこれらの一時ファイルを読み取ることでデータにアクセスするのを防ぐことができます。

## 構成、設定 {#configure}

ディスクスピルファイルの暗号化を有効にするには、TiDB構成ファイルの`[security]`セクションで項目[`spilled-file-encryption-method`](/tidb-configuration-file.md#spilled-file-encryption-method)を構成できます。

```toml
[security]
spilled-file-encryption-method = "aes128-ctr"
```

`spilled-file-encryption-method`の値オプションは`aes128-ctr`と`plaintext`です。デフォルト値は`plaintext`です。これは、暗号化が無効になっていることを意味します。
