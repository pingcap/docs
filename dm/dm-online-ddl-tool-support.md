---
title: TiDB Data Migration Support for Online DDL Tools
summary: DM における一般的なオンライン DDL ツールのサポート、使用方法、および注意事項について説明します。
---

# オンライン DDL ツールの TiDB データ移行サポート {#tidb-data-migration-support-for-online-ddl-tools}

MySQLエコシステムでは、gh-ostやpt-oscなどのツールが広く使用されています。TiDBデータ移行（DM）は、これらのツールをサポートし、不要な中間データの移行を回避します。

このドキュメントでは、DM における一般的なオンライン DDL ツールのサポート、使用方法、および注意事項について説明します。

オンライン DDL ツールにおける DM の動作原理と実装方法については、 [オンラインDDL](/dm/feature-online-ddl.md)を参照してください。

## 制限 {#restrictions}

-   DM は gh-ost と pt-osc のみをサポートします。
-   `online-ddl`有効にすると、増分レプリケーションに対応するチェックポイントは、オンライン DDL 実行中であってはなりません。例えば、上流のオンライン DDL 操作がbinlogの`position-A`で開始され、 `position-B`で終了する場合、増分レプリケーションの開始点は`position-A`より前、または`position-B`より後にする必要があります。それ以外の場合、エラーが発生します。詳細は[FAQ](/dm/dm-faq.md#how-to-handle-the-error-returned-by-the-ddl-operation-related-to-the-gh-ost-table-after-online-ddl-true-is-set)を参照してください。

## パラメータを設定する {#configure-parameters}

<SimpleTab>
<div label="v2.0.5 and later">

v2.0.5 以降のバージョンでは、 `task`構成ファイル内の`online-ddl`構成項目を使用する必要があります。

-   アップストリーム MySQL/MariaDB (同時に) が gh-ost または pt-osc ツールを使用する場合は、タスク構成ファイルで`online-ddl`から`true`設定します。

```yml
online-ddl: true
```

> **注記：**
>
> v2.0.5以降、 `online-ddl-scheme`非推奨となりました。そのため、 `online-ddl-scheme`ではなく`online-ddl`使用する必要があります。つまり、 `online-ddl: true`設定すると`online-ddl-scheme`上書きされ、 `online-ddl-scheme: "pt"`または`online-ddl-scheme: "gh-ost"`は`online-ddl: true`に変換されます。

</div>

<div label="earlier than v2.0.5">

v2.0.5 より前 (v2.0.5 を除く) では、 `task`設定ファイル内の`online-ddl-scheme`設定項目を使用する必要があります。

-   アップストリーム MySQL/MariaDB が gh-ost ツールを使用する場合は、タスク構成ファイルで設定します。

```yml
online-ddl-scheme: "gh-ost"
```

-   アップストリーム MySQL/MariaDB が pt ツールを使用する場合は、タスク構成ファイルで設定します。

```yml
online-ddl-scheme: "pt"
```

</div>
</SimpleTab>
