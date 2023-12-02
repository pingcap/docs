---
title: tiup cluster audit cleanup
---

# tiup cluster auditクリーンアップ {#tiup-cluster-audit-cleanup}

`tiup cluster audit cleanup`コマンドは、 `tiup cluster`コマンドの実行時に生成されたログをクリーンアップするために使用されます。

## 構文 {#syntax}

```shell
tiup cluster audit cleanup [flags]
```

## オプション {#options}

### --保持日数 {#retain-days}

-   ログを保存する日数を指定します。
-   データ型: `INT`
-   デフォルト値: `60` (日単位)。
-   デフォルトでは、過去 60 日以内に生成されたログは保持されます。つまり、60 日より前に生成されたログは削除されます。

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   デフォルト値: `false`
-   このオプションを有効にするには、このオプションをコマンドに追加し、値`true`を渡すか、値を渡さないことができます。

## 出力 {#output}

```shell
clean audit log successfully
```

[&lt;&lt; 前のページに戻る - TiUPクラスタコマンド リスト](/tiup/tiup-component-cluster.md#command-list)
