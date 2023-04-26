---
title: TiDB 2.0 RC5 Release Notes
---

# TiDB 2.0 RC5 リリースノート {#tidb-2-0-rc5-release-notes}

2018 年 4 月 17 日に、TiDB 2.0 RC5 がリリースされました。このリリースでは、MySQL の互換性、SQL の最適化、および安定性が大幅に改善されています。

## TiDB {#tidb}

-   `Top-N`プッシュダウン ルールの適用に関する問題を修正
-   NULL 値を含む列の行数の見積もりを修正
-   Binary 型のゼロ値を修正
-   トランザクション内で`BatchGet`問題を修正する
-   `Add Index`回の操作をロールバックしながら、書き込まれたデータをクリーンアップして、消費スペースを削減します。
-   `insert on duplicate key update`ステートメントを最適化して、パフォーマンスを 10 倍向上させる
-   `UNIX_TIMESTAMP`関数によって返される結果のタイプに関する問題を修正します
-   NOT NULL 列を追加する際に NULL 値が挿入される問題を修正
-   `Show Process List`のステートメントで実行中のステートメントのメモリ使用量を表示するサポート
-   極端な状況で`Alter Table Modify Column`がエラーを報告する問題を修正
-   `Alter`ステートメントを使用したテーブル コメントの設定をサポート

## PD {#pd}

-   Raft Learnerのサポートを追加
-   Balance リージョン Scheduler を最適化してスケジューリングのオーバーヘッドを削減する
-   `schedule-limit`構成のデフォルト値を調整します
-   IDを頻繁に割り当てる問題を修正
-   新しいスケジューラを追加する際の互換性の問題を修正

## TiKV {#tikv}

-   `tikv-ctl`分の`compact`で指定されたリージョンをサポート
-   RawKVClient でバッチ プット、バッチ ゲット、バッチ削除、バッチ スキャンをサポート
-   スナップショットが多すぎるために発生する OOM の問題を修正
-   コプロセッサーでより詳細なエラー情報を返す
-   TiKV の`block-cache-size`から`tikv-ctl`までの動的な変更をサポート
-   さらに改善する`importer`
-   `ImportSST::Upload`インターフェースを簡素化
-   gRPC の`keepalive`のプロパティを構成する
-   独立したバイナリとして TiKV から`tikv-importer`を分割します。
-   コプロセッサーの各`scan range`によってスキャンされた行数に関する統計を提供します
-   macOS システムでのコンパイルの問題を修正
-   RocksDB メトリクスの誤用の問題を修正
-   コプロセッサーで`overflow as warning`オプションをサポート
