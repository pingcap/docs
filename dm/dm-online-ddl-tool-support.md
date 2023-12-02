---
title: TiDB Data Migration Support for Online DDL Tools
summary: Learn about the support for common online DDL tools, usage, and precautions in DM.
---

# オンライン DDL ツールの TiDB データ移行サポート {#tidb-data-migration-support-for-online-ddl-tools}

MySQL エコシステムでは、gh-ost や pt-osc などのツールが広く使用されています。 TiDB Data Migration (DM) は、不要な中間データの移行を回避するために、これらのツールのサポートを提供します。

このドキュメントでは、DM における一般的なオンライン DDL ツールのサポート、使用方法、注意事項について紹介します。

オンライン DDL ツールの DM の動作原理と実装方法については、 [オンライン-ddl](/dm/feature-online-ddl.md)を参照してください。

## 制限 {#restrictions}

-   DM は gh-ost と pt-osc のみをサポートします。
-   `online-ddl`が有効な場合、増分レプリケーションに対応するチェックポイントはオンライン DDL 実行のプロセスにあってはなりません。たとえば、アップストリームのオンライン DDL 操作がbinlogの`position-A`で開始し、 `position-B`で終了する場合、増分レプリケーションの開始点は`position-A`より前か`position-B`より後である必要があります。そうしないとエラーが発生します。詳細は[FAQ](/dm/dm-faq.md#how-to-handle-the-error-returned-by-the-ddl-operation-related-to-the-gh-ost-table-after-online-ddl-true-is-set)を参照してください。

## パラメータを設定する {#configure-parameters}

<SimpleTab>
<div label="v2.0.5 and later">

v2.0.5 以降のバージョンでは、 `task`設定ファイルの`online-ddl`設定項目を使用する必要があります。

-   アップストリームの MySQL/MariaDB が (同時に) gh-ost または pt-osc ツールを使用する場合は、タスク構成ファイルで`online-ddl`から`true`を設定します。

```yml
online-ddl: true
```

> **注記：**
>
> v2.0.5 以降、 `online-ddl-scheme`​​非推奨になったので、 `online-ddl-scheme`の代わりに`online-ddl`使用する必要があります。つまり、設定`online-ddl: true` `online-ddl-scheme`を上書きし、設定`online-ddl-scheme: "pt"`または`online-ddl-scheme: "gh-ost"`は`online-ddl: true`に変換されます。

</div>

<div label="earlier than v2.0.5">

v2.0.5 より前 (v2.0.5 を除く) は、 `task`構成ファイルの`online-ddl-scheme`構成項目を使用する必要があります。

-   アップストリームの MySQL/MariaDB が gh-ost ツールを使用する場合は、それをタスク構成ファイルに設定します。

```yml
online-ddl-scheme: "gh-ost"
```

-   アップストリームの MySQL/MariaDB が pt ツールを使用する場合は、それをタスク構成ファイルに設定します。

```yml
online-ddl-scheme: "pt"
```

</div>
</SimpleTab>
