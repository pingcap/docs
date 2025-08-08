---
title: TiDB 2.0 RC5 Release Notes
summary: TiDB 2.0 RC5は2018年4月17日にリリースされ、MySQLとの互換性、SQLの最適化、安定性が向上しました。TiDB、PD、TiKVの各コンポーネントに修正と最適化が施され、 Raft Learnerのサポート、スケジューリングのオーバーヘッド削減、新しいバッチ操作の追加などが行われました。また、メモリ使用量、エラー報告、設定調整に関する問題にも対処しました。
---

# TiDB 2.0 RC5 リリースノート {#tidb-2-0-rc5-release-notes}

2018年4月17日、TiDB 2.0 RC5がリリースされました。このリリースでは、MySQLとの互換性、SQLの最適化、そして安定性が大幅に向上しています。

## TiDB {#tidb}

-   `Top-N`プッシュダウンルールの適用に関する問題を修正
-   NULL値を含む列の行数の推定を修正
-   バイナリ型のゼロ値を修正する
-   取引内の`BatchGet`問題を修正する
-   消費スペースを削減するために、 `Add Index`操作をロールバックしながら書き込まれたデータをクリーンアップします。
-   `insert on duplicate key update`ステートメントを最適化すると、パフォーマンスが10倍向上します
-   `UNIX_TIMESTAMP`関数によって返される結果の型に関する問題を修正しました
-   NOT NULL列を追加するときにNULL値が挿入される問題を修正しました
-   `Show Process List`文目の実行文のメモリ使用量の表示をサポート
-   極端な状況で`Alter Table Modify Column`を報告する問題を修正
-   `Alter`文を使用してテーブルコメントの設定をサポートします

## PD {#pd}

-   Raft Learnerのサポートを追加
-   バランスリージョンスケジューラを最適化してスケジューリングのオーバーヘッドを削減します
-   `schedule-limit`構成のデフォルト値を調整する
-   IDを頻繁に割り当てる問題を修正
-   新しいスケジューラを追加する際の互換性の問題を修正

## TiKV {#tikv}

-   `tikv-ctl`分の`compact`で指定されたリージョンをサポート
-   RawKVClient でバッチ Put、バッチ Get、バッチ Delete、バッチ Scan をサポート
-   スナップショットが多すぎることによるOOM問題を修正
-   コプロセッサーでより詳細なエラー情報を返す
-   TiKVの`block-cache-size`から`tikv-ctl`の動的な変更をサポート
-   さらに改善`importer`
-   `ImportSST::Upload`インターフェースを簡素化
-   gRPCの`keepalive`プロパティを設定する
-   TiKVから`tikv-importer`独立したバイナリとして分割する
-   コプロセッサーごとにスキャンされた行`scan range`に関する統計情報を提供します
-   macOSシステムでのコンパイル問題を修正
-   RocksDB メトリックの誤用問題を修正
-   コプロセッサーの`overflow as warning`オプションをサポート
