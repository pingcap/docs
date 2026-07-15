---
title: TiDB 3.1 Beta Release Notes
summary: TiDB 3.1ベータ版は2019年12月20日にリリースされました。SQLオプティマイザーの改良に加え、Follower Read機能もサポートされています。TiKVは、Follower Read機能に加え、分散バックアップとリストアをサポートするようになりました。PDも分散バックアップとリストアをサポートします。
---

# TiDB 3.1 ベータ版リリースノート {#tidb-3-1-beta-release-notes}

発売日：2019年12月20日

TiDB バージョン: 3.1.0-beta

TiDB Ansible バージョン: 3.1.0-beta

## TiDB {#tidb}

-   SQLオプティマイザー
    -   SQLヒントの強化[＃12192](https://github.com/pingcap/tidb/pull/12192)
-   新機能
    -   Follower Read機能サポートする [＃12535](https://github.com/pingcap/tidb/pull/12535)

## TiKV {#tikv}

-   分散バックアップおよび復元機能をサポート[＃5532](https://github.com/tikv/tikv/pull/5532)
-   Follower Read機能サポートする [＃5562](https://github.com/tikv/tikv/pull/5562)

## PD {#pd}

-   分散バックアップおよび復元機能をサポート[＃1896](https://github.com/pingcap/pd/pull/1896)
