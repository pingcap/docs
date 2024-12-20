---
title: TiDB 3.1 Beta Release Notes
summary: TiDB 3.1 ベータ版は、2019 年 12 月 20 日にリリースされました。SQL オプティマイザーの改善が含まれ、フォロワーFollower Read機能がサポートされています。TiKV は、Follower Read機能だけでなく、分散バックアップと復元もサポートするようになりました。PD も分散バックアップと復元をサポートしています。
---

# TiDB 3.1 ベータ リリース ノート {#tidb-3-1-beta-release-notes}

発売日: 2019年12月20日

TiDB バージョン: 3.1.0-beta

TiDB Ansible バージョン: 3.1.0-beta

## ティビ {#tidb}

-   SQL オプティマイザー
    -   SQLヒントの強化[＃12192](https://github.com/pingcap/tidb/pull/12192)
-   新機能
    -   Follower Read機能をサポート[＃12535](https://github.com/pingcap/tidb/pull/12535)

## ティクヴ {#tikv}

-   分散バックアップおよび復元機能をサポート[＃5532](https://github.com/tikv/tikv/pull/5532)
-   Follower Read機能をサポート[＃5562](https://github.com/tikv/tikv/pull/5562)

## PD {#pd}

-   分散バックアップおよび復元機能をサポート[＃1896](https://github.com/pingcap/pd/pull/1896)
