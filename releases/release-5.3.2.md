---
title: TiDB 5.3.2 Release Notes
summary: TiDB 5.3.2は2022年6月29日にリリースされました。既知のバグが存在するため、このバージョンの使用は推奨されません。このバグはv5.3.3で修正されています。このリリースには、TiDB、PD、TiKV、 TiFlash、およびTiDB Data Migration、 TiDB Lightning、Backup & Restore、TiCDC、TiDB Data Migrationなどの各種ツールの互換性に関する変更、改善、バグ修正が含まれています。
---

# TiDB 5.3.2 リリースノート {#tidb-5-3-2-release-notes}

リリース日：2022年6月29日

TiDB バージョン: 5.3.2

> **Warning:**
>
> v5.3.2 には既知のバグがあるため、使用は推奨されません。詳細は [#12934](https://github.com/tikv/tikv/issues/12934) をご覧ください。このバグは v5.3.3 で修正されています。 [バージョン5.3.3](/releases/release-5.3.3.md)の使用を推奨します。

## 互換性の変更 {#compatibility-changes}

- TiDB

    - 自動IDが範囲外の場合に`REPLACE`文が他の行を誤って変更する問題を修正[#29483](https://github.com/pingcap/tidb/issues/29483)

- PD

    - デフォルトでSwaggerサーバーのコンパイルを無効にする[#4932](https://github.com/tikv/pd/issues/4932)

## 改善点 {#improvements}

- TiKV

    - Raftクライアントによるシステムコールを減らしCPU効率を上げる[#11309](https://github.com/tikv/tikv/issues/11309)
    - ヘルスチェックを改善して、利用できないRaftstoreを検出し、TiKV クライアントがリージョンキャッシュを時間内に更新できるようにします[#12398](https://github.com/tikv/tikv/issues/12398)
    - レイテンシージッタを削減するためにリーダーシップをCDCオブザーバーに移譲する[#12111](https://github.com/tikv/tikv/issues/12111)
    - モジュールのパフォーマンスの問題を特定するために、 Raftログのガベージコレクションモジュールのメトリックを追加します。 [#11374](https://github.com/tikv/tikv/issues/11374)

- ツール

    - TiDB Data Migration (DM)

        - タスクが自動的に再開された後にDMがより多くのディスクスペースを占有する問題を修正[#3734](https://github.com/pingcap/tiflow/issues/3734) [#5344](https://github.com/pingcap/tiflow/issues/5344)
        - `case-sensitive: true`が設定されていない場合、大文字テーブルを複製できない問題を修正[#5255](https://github.com/pingcap/tiflow/issues/5255)
        - 下流でフィルタリングされたDDLを手動で実行すると、タスク再開が失敗する場合がある問題を修正しました[#5272](https://github.com/pingcap/tiflow/issues/5272)
        - DM-workerが、`SHOW CREATE TABLE`文によって返されるインデックスの先頭に主キーがない場合にpanicする問題を修正しました。 [#5159](https://github.com/pingcap/tiflow/issues/5159)
        - GTID が有効になっているときやタスクが自動的に再開されたときに CPU 使用率が上昇し、大量のログが出力される問題を修正しました[#5063](https://github.com/pingcap/tiflow/issues/5063)
        - DM-masterの再起動後にリレーログが無効になる可能性がある問題を修正[#4803](https://github.com/pingcap/tiflow/issues/4803)
