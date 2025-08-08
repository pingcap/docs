---
title: Enable Encryption for Disk Spill
summary: TiDB でディスク スピルの暗号化を有効にする方法を学習します。
---

# ディスク流出時の暗号化機能を有効にする {#enable-encryption-for-disk-spill}

システム変数[`tidb_enable_tmp_storage_on_oom`](/system-variables.md#tidb_enable_tmp_storage_on_oom) `ON`に設定されている場合、単一の SQL ステートメントのメモリ使用量がシステム変数[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)の制限を超えると、一部の演算子は実行中に中間結果を一時ファイルとしてディスクに保存し、クエリの完了後にそのファイルを削除することができます。

ディスクスピルの暗号化を有効にすると、攻撃者がこれらの一時ファイルを読み取ってデータにアクセスするのを防ぐことができます。

## 設定 {#configure}

ディスク スピル ファイルの暗号化を有効にするには、TiDB 構成ファイルのセクション`[security]`の項目[`spilled-file-encryption-method`](/tidb-configuration-file.md#spilled-file-encryption-method)構成します。

```toml
[security]
spilled-file-encryption-method = "aes128-ctr"
```

`spilled-file-encryption-method`値の選択肢は`aes128-ctr`と`plaintext`です。デフォルト値は`plaintext`で、暗号化が無効であることを意味します。
