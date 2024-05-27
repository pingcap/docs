---
title: TiDB Data Migration Support for Online DDL Tools
summary: DM における一般的なオンライン DDL ツールのサポート、使用方法、および注意事項について説明します。
---

# オンライン DDL ツールの TiDB データ移行サポート {#tidb-data-migration-support-for-online-ddl-tools}

MySQL エコシステムでは、gh-ost や pt-osc などのツールが広く使用されています。TiDB データ移行 (DM) は、不要な中間データの移行を回避するためにこれらのツールをサポートします。

このドキュメントでは、DM における一般的なオンライン DDL ツールのサポート、使用方法、および注意事項について説明します。

オンラインDDLツールにおけるDMの動作原理と実装方法については、 [オンラインDDL](/dm/feature-online-ddl.md)を参照してください。

## 制限 {#restrictions}

-   DM は gh-ost と pt-osc のみをサポートします。
-   `online-ddl`を有効にすると、増分レプリケーションに対応するチェックポイントは、オンライン DDL 実行プロセス中にあってはなりません。たとえば、アップストリームのオンライン DDL 操作がbinlogの`position-A`で開始され、 `position-B`で終了する場合、増分レプリケーションの開始点は`position-A`より前または`position-B`より後にする必要があります。そうでない場合は、エラーが発生します。詳細については、 [FAQ](/dm/dm-faq.md#how-to-handle-the-error-returned-by-the-ddl-operation-related-to-the-gh-ost-table-after-online-ddl-true-is-set)を参照してください。

## パラメータを設定する {#configure-parameters}

<SimpleTab>
<div label="v2.0.5 and later">

v2.0.5 以降のバージョンでは、 `task`構成ファイル内の`online-ddl`構成項目を使用する必要があります。

-   アップストリーム MySQL/MariaDB が (同時に) gh-ost または pt-osc ツールを使用する場合は、タスク構成ファイルで`online-ddl`から`true`設定します。

```yml
online-ddl: true
```

> **注記：**
>
> v2.0.5 以降、 `online-ddl-scheme`​​非推奨になったため、 `online-ddl-scheme`の代わりに`online-ddl`使用する必要があります。つまり、設定`online-ddl: true`は`online-ddl-scheme`を上書きし、設定`online-ddl-scheme: "pt"`または`online-ddl-scheme: "gh-ost"` `online-ddl: true`に変換されます。

</div>

<div label="earlier than v2.0.5">

v2.0.5 より前 (v2.0.5 は含まない) では、 `task`構成ファイル内の`online-ddl-scheme`構成項目を使用する必要があります。

-   アップストリーム MySQL/MariaDB が gh-ost ツールを使用する場合は、タスク構成ファイルで設定します。

```yml
online-ddl-scheme: "gh-ost"
```

-   アップストリームの MySQL/MariaDB が pt ツールを使用する場合は、タスク構成ファイルで設定します。

```yml
online-ddl-scheme: "pt"
```

</div>
</SimpleTab>
