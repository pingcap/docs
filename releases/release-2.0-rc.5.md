---
title: TiDB 2.0 RC5 Release Notes
---

# TiDB 2.0 RC5 リリースノート {#tidb-2-0-rc5-release-notes}

2018 年 4 月 17 日、TiDB 2.0 RC5 がリリースされました。このリリースでは、MySQL の互換性、SQL の最適化、安定性が大幅に向上しています。

## TiDB {#tidb}

-   `Top-N`プッシュダウン ルールの適用に関する問題を修正
-   NULL 値を含む列の行数の推定を修正しました。
-   Binary型のゼロ値を修正
-   トランザクション内の`BatchGet`件の問題を修正する
-   `Add Index`操作をロールバックしながら書き込まれたデータをクリーンアップして、消費スペースを削減します。
-   `insert on duplicate key update`ステートメントを最適化してパフォーマンスを 10 倍向上させる
-   `UNIX_TIMESTAMP`関数によって返される結果の型に関する問題を修正します。
-   NOT NULL 列を追加するときに NULL 値が挿入される問題を修正
-   `Show Process List`ステートメント内の実行ステートメントのメモリ使用量の表示をサポート
-   `Alter Table Modify Column`が極端な状況でエラーを報告する問題を修正
-   `Alter`ステートメントを使用したテーブル コメントの設定をサポート

## PD {#pd}

-   Raft Learnerのサポートを追加
-   バランスリージョンスケジューラを最適化して、スケジュールのオーバーヘッドを削減する
-   `schedule-limit`構成のデフォルト値を調整する
-   IDが頻繁に割り当てられる問題を修正
-   新しいスケジューラを追加するときの互換性の問題を修正

## TiKV {#tikv}

-   `compact`で指定されたリージョン`tikv-ctl`サポートします
-   RawKVClient でバッチ Put、バッチ Get、バッチ削除、バッチ スキャンをサポート
-   スナップショットが多すぎることによって引き起こされる OOM 問題を修正する
-   コプロセッサーでより詳細なエラー情報を返す
-   TiKV の`block-cache-size`から`tikv-ctl`までの動的変更をサポート
-   さらに改良`importer`
-   `ImportSST::Upload`インターフェースを簡素化する
-   gRPC の`keepalive`プロパティを構成する
-   TiKV から`tikv-importer`を独立したバイナリとして分割
-   コプロセッサーの各`scan range`によってスキャンされた行数に関する統計を提供します。
-   macOS システムでのコンパイルの問題を修正
-   RocksDB メトリクスの誤用の問題を修正する
-   コプロセッサーの`overflow as warning`オプションをサポート
