---
title: TiDB 5.4.1 Release Notes
summary: "TiDB 5.4.1 リリースノート: このリリースには、TiDB、TiKV、PD、 TiFlash、およびさまざまなツールの互換性の変更、改善、バグ修正が含まれています。改善点には、PointGet プランの使用のサポート、ログとメトリックの追加、Grafana ダッシュボードでの複数の Kubernetes クラスターの表示が含まれます。バグ修正では、date_format の不適切な処理、データの書き込みエラー、クエリ結果の誤り、さまざまなパニックやエラーなどの問題に対処しています。TiKV、PD、 TiFlash、およびツールの修正も含まれています。"
---

# TiDB 5.4.1 リリースノート {#tidb-5-4-1-release-notes}

リリース日：2022年5月13日

TiDB バージョン: 5.4.1

## 互換性の変更 {#compatibility-changes}

TiDB v5.4.1では、製品設計上の互換性に関する変更は行われていません。ただし、このリリースでのバグ修正により、互換性に関する変更も発生する可能性がありますのでご注意ください。詳細については、 [バグ修正](#bug-fixes)ご覧ください。

## 改善点 {#improvements}

- TiDB

    - `_tidb_rowid`列列を読み取るクエリにPointGetプランの使用をサポート [#31543](https://github.com/pingcap/tidb/issues/31543)
    - `Apply`オペレーターのログとメトリクスを追加して、並列であるかどうかを確認します。 [#33887](https://github.com/pingcap/tidb/issues/33887)
    - 統計情報を収集するために使用される分析バージョン 2 の`TopN`プルーニング ロジックを改善します。 [#34256](https://github.com/pingcap/tidb/issues/34256)
    - Grafanaダッシュボードで複数のKubernetesクラスターの表示をサポート [#32593](https://github.com/pingcap/tidb/issues/32593)

- TiKV

    - Grafanaダッシュボードで複数のKubernetesクラスターの表示をサポート [#12104](https://github.com/tikv/tikv/issues/12104)

- PD

    - Grafanaダッシュボードで複数のKubernetesクラスターの表示をサポート [#4673](https://github.com/tikv/pd/issues/4673)

- TiFlash

    - Grafanaダッシュボードで複数のKubernetesクラスターの表示をサポート [#4129](https://github.com/pingcap/tiflash/issues/4129)

- ツール

    - TiCDC

        - Grafanaダッシュボードで複数のKubernetesクラスターをサポート[#4665](https://github.com/pingcap/tiflow/issues/4665)
        - Kafka プロデューサーの設定パラメータを公開して、TiCDC で設定できるようにします。 [#4385](https://github.com/pingcap/tiflow/issues/4385)

    - TiDB Data Migration (DM)

        - ログに「チェックポイントに変更はありません。同期フラッシュチェックポイントをスキップしてください」というメッセージが数百件出力され、レプリケーションが非常に遅くなる問題を修正しました[#4619](https://github.com/pingcap/tiflow/issues/4619)
        - 長いvarcharsがエラーを報告するバグを修正`Column length too big` [#4637](https://github.com/pingcap/tiflow/issues/4637)
        - セーフモードでの更新ステートメントの実行エラーにより、DM-workerがpanicになる可能性がある問題を修正しました[#4317](https://github.com/pingcap/tiflow/issues/4317)
        - 下流でフィルタリングされたDDLを手動で実行すると、タスク再開が失敗する場合がある問題を修正しました[#5272](https://github.com/pingcap/tiflow/issues/5272)
        - アップストリームでbinlogが有効になっていない場合に`query-status`コマンドでデータが返されないバグを修正 [#5121](https://github.com/pingcap/tiflow/issues/5121)
        - `SHOW CREATE TABLE`文によって返されるインデックスの先頭に主キーがない場合に発生する DM-workerがpanicする問題を修正しました。 [#5159](https://github.com/pingcap/tiflow/issues/5159)
        - GTID が有効になっているときやタスクが自動的に再開されたときに CPU 使用率が上昇し、大量のログが出力される問題を修正しました[#5063](https://github.com/pingcap/tiflow/issues/5063)
