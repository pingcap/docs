---
title: TiDB 2.0 RC5 Release Notes
summary: TiDB 2.0 RC5 は、MySQL 互換性、SQL 最適化、安定性の向上を伴い、2018 年 4 月 17 日にリリースされました。TiDB、PD、TiKV コンポーネントに対して、 Raft Learnerのサポート、スケジューリング オーバーヘッドの削減、新しいバッチ操作の追加など、修正と最適化が行われました。このリリースでは、メモリ使用量、エラー報告、構成調整に関連する問題にも対処しました。
---

# TiDB 2.0 RC5 リリースノート {#tidb-2-0-rc5-release-notes}

2018 年 4 月 17 日に、TiDB 2.0 RC5 がリリースされました。このリリースでは、MySQL 互換性、SQL 最適化、安定性が大幅に向上しています。

## ティビ {#tidb}

-   `Top-N`プッシュダウンルールの適用に関する問題を修正
-   NULL値を含む列の行数の推定を修正
-   バイナリ型のゼロ値を修正
-   トランザクション内の`BatchGet`問題を修正する
-   `Add Index`操作をロールバックしながら書き込まれたデータをクリーンアップして、消費スペースを削減します。
-   `insert on duplicate key update`ステートメントを最適化するとパフォーマンスが10倍向上します
-   `UNIX_TIMESTAMP`関数によって返される結果の型に関する問題を修正しました
-   NOT NULL列を追加するときにNULL値が挿入される問題を修正
-   `Show Process List`ステートメントで実行中のステートメントのメモリ使用量を表示する機能をサポート
-   極端な状況で`Alter Table Modify Column`を報告する問題を修正
-   `Alter`ステートメントを使用してテーブルコメントの設定をサポートします

## PD {#pd}

-   Raft Learnerのサポートを追加
-   バランスリージョンスケジューラを最適化してスケジューリングのオーバーヘッドを削減する
-   `schedule-limit`の構成のデフォルト値を調整する
-   IDを頻繁に割り当てる問題を修正
-   新しいスケジューラを追加する際の互換性の問題を修正

## ティクヴ {#tikv}

-   `tikv-ctl`分の`compact`で指定されたリージョンをサポート
-   RawKVClient でバッチ Put、バッチ Get、バッチ Delete、バッチ Scan をサポート
-   スナップショットが多すぎることによるOOM問題を修正
-   コプロセッサーでより詳細なエラー情報を返す
-   TiKVの`block-cache-size`から`tikv-ctl`までの動的な変更をサポート
-   さらに改善`importer`
-   `ImportSST::Upload`インターフェースを簡素化
-   gRPCの`keepalive`プロパティを設定する
-   TiKVから`tikv-importer`独立したバイナリとして分割する
-   コプロセッサー内の各`scan range`行がスキャンした行数に関する統計情報を提供します。
-   macOSシステムでのコンパイル問題を修正
-   RocksDB メトリックの誤用問題を修正
-   コプロセッサーの`overflow as warning`オプションをサポート
