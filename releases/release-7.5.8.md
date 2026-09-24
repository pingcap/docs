---
title: TiDB 7.5.8 リリースノート
summary: TiDB 7.5.8 の改善点とバグ修正について説明します。
---

# TiDB 7.5.8 リリースノート

リリース日: 2026年9月17日

TiDB version: 7.5.8

Quick access: [クイックスタート](https://docs.pingcap.com/tidb/v7.5/quick-start-with-tidb) | [本番デプロイ](https://docs.pingcap.com/tidb/v7.5/production-deployment-using-tiup)

## 改善点 {#improvements}

+ PD

    - `store` ラベルを `pd_cluster_status` メトリクスに追加し、PD がストアごとのステータスメトリクスをレポートできるようにしました。これにより、影響を受けた TiKV ストアを特定しやすくなり、必要に応じてクラスター全体の値を集計しやすくなります [#9855](https://github.com/tikv/pd/issues/9855) @[SerjKol80](https://github.com/SerjKol80) <!-- pr: https://github.com/tikv/pd/pull/10060 -->

## バグ修正 {#bug-fixes}

+ TiDB

    - `UNION` クエリのクリーンアップと worker goroutine の競合により、TiDB が `SIGSEGV` でクラッシュする可能性がある問題を修正しました [#66391](https://github.com/pingcap/tidb/issues/66391) @[bb7133](https://github.com/bb7133) <!-- pr: https://github.com/pingcap/tidb/pull/67003 -->
    - 一部のシナリオで、高コストな全範囲チェックが原因となり、クエリプランニング中に TiDB が過剰な CPU を消費する問題を修正しました [#63235](https://github.com/pingcap/tidb/issues/63235) @[terry1purcell](https://github.com/terry1purcell) @[qw4990](https://github.com/qw4990) <!-- pr: https://github.com/pingcap/tidb/pull/64058 --> <!-- pr: https://github.com/pingcap/tidb/pull/63813 -->
    - `tidb_opt_objective` が `determinate` に設定されている場合に、新しく追加されたインデックスの非同期統計情報読み込み中に発生する可能性がある panic を修正しました [#64274](https://github.com/pingcap/tidb/issues/64274) @[0xPoe](https://github.com/0xPoe) <!-- pr: https://github.com/pingcap/tidb/pull/64292 -->

+ TiKV

    - 外部 SST の取り込みとフォアグラウンド書き込みの競合により、TiKV が `txn record found but not expected` で panic する可能性がある問題を修正しました [#19891](https://github.com/tikv/tikv/issues/19891) @[gengliqi](https://github.com/gengliqi) <!-- pr: https://github.com/tikv/tikv/pull/19914 -->
    - TiCDC の再起動またはネットワーク障害の後に、TiKV と TiCDC 間の古い接続が完全にクリーンアップされず、TiKV CDC のメモリクォータを使い果たして changefeed が停止する問題を修正しました [#18169](https://github.com/tikv/tikv/issues/18169) [#19610](https://github.com/tikv/tikv/issues/19610) @[asddongmen](https://github.com/asddongmen) @[wk989898](https://github.com/wk989898) <!-- pr: https://github.com/tikv/tikv/pull/18864 --> <!-- pr: https://github.com/tikv/tikv/pull/19689 -->
    - PD 関連の処理が I/O 操作によってブロックされるため、TiKV の I/O ハング中に TiKV のスループットが継続的に低下する可能性がある問題を修正しました [#17939](https://github.com/tikv/tikv/issues/17939) @[LykxSassinator](https://github.com/LykxSassinator) <!-- pr: https://github.com/tikv/tikv/pull/18969 -->
    - TiDB Lightning によるデータインポート中に、null ポインタ参照によって TiKV がクラッシュする可能性がある問題を修正しました [#18671](https://github.com/tikv/tikv/issues/18671) [#18756](https://github.com/tikv/tikv/issues/18756) @[Dog-Du](https://github.com/Dog-Du) <!-- pr: https://github.com/tikv/tikv/pull/19908 -->

+ PD

    - TiDB Lightning がインポート中に `SetRegionLabelRule` を同時に呼び出すと、PD で goroutine が急増して不安定になる可能性がある問題を修正しました [#9854](https://github.com/tikv/pd/issues/9854) @[lhy1024](https://github.com/lhy1024) <!-- pr: https://github.com/tikv/pd/pull/9897 -->
    - TiKV のスケールイン後に、削除済みストアの古い `pd_cluster_status` メトリクスが残る可能性がある問題を修正しました [#9942](https://github.com/tikv/pd/issues/9942) @[okJiang](https://github.com/okJiang) <!-- pr: https://github.com/tikv/pd/pull/10188 -->

+ TiFlash

    - カラムの `NOT NULL` 制約を削除する DDL 文を実行した後に、TiFlash と TiKV の間でデータ不整合が発生する可能性がある問題を修正しました [#10680](https://github.com/pingcap/tiflash/issues/10680) @[JaySon-Huang](https://github.com/JaySon-Huang) <!-- pr: https://github.com/pingcap/tiflash/pull/10690 -->

+ Tools

    + BR

        - ログバックアップタスク停止後に BR が古い GC service safepoint を残し、その結果 GC が想定どおりに進行できなくなる可能性がある問題を修正しました [#19832](https://github.com/tikv/tikv/issues/19832) @[Leavrth](https://github.com/Leavrth) <!-- pr: https://github.com/tikv/tikv/pull/19913 -->

    + TiCDC

        - Kafka changefeed で失敗した DDL または checkpoint イベント配信を再試行すると Kafka クライアントがリークし、メモリ使用量が継続的に増加する問題を修正しました [#12666](https://github.com/pingcap/tiflow/issues/12666) @[3AceShowHand](https://github.com/3AceShowHand) <!-- pr: https://github.com/pingcap/tiflow/pull/12678 -->
        - admin または producer の初期化に失敗した場合、または admin と synchronous-producer ラッパーがクローズされた場合に、Kafka sink が基盤となる Sarama クライアントをリークする可能性がある問題を修正しました [#12572](https://github.com/pingcap/tiflow/issues/12572) @[wlwilliamx](https://github.com/wlwilliamx) <!-- pr: https://github.com/pingcap/tiflow/pull/12592 -->
