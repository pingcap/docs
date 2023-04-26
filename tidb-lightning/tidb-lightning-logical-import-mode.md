---
title: Logical Import Mode Introduction
summary: Learn about the logical import mode in TiDB Lightning.
---

# 論理インポート モードの概要 {#logical-import-mode-introduction}

論理インポート モードは、 TiDB Lightningでサポートされている 2 つのインポート モードの 1 つです。論理インポート モードでは、 TiDB Lightning は最初にデータを SQL ステートメントにエンコードし、次に SQL ステートメントを実行してデータをインポートします。

TiDB クラスターに既にデータが含まれており、外部アプリケーションにサービスを提供している場合は、論理インポート モードでデータをインポートすることをお勧めします。論理インポート モードの動作は、通常の SQL ステートメントの実行と同じであるため、 ACID準拠が保証されます。

論理インポート モードのバックエンドは`tidb`です。

## 環境要件 {#environment-requirements}

**オペレーティング システム**:

新しい CentOS 7 インスタンスを使用することをお勧めします。仮想マシンは、ローカル ホストまたはクラウドにデプロイできます。 TiDB Lightning はデフォルトで必要なだけ多くの CPU リソースを消費するため、専用サーバーにデプロイすることをお勧めします。これが不可能な場合は、他の TiDB コンポーネント (tikv-server など) と共に単一のサーバーにデプロイし、 TiDB Lightningからの CPU 使用を制限するように`region-concurrency`を構成できます。通常、サイズは論理 CPU の 75% に設定できます。

**メモリと CPU** :

パフォーマンスを向上させるには、4 コアを超える CPU と 8 GiB を超えるメモリを割り当てることをお勧めします。論理インポート モードでは、 TiDB Lightning に大きなメモリ使用量 (5 GiB 以下) がないことが確認されています。ただし、 `region-concurrency`の値を増やすと、 TiDB Lightning がより多くのメモリを消費する可能性があります。

**ネットワーク**: 1 Gbps または 10 Gbps のイーサネット カードを推奨します。

## 制限事項 {#limitations}

複数のTiDB Lightning を使用して同じターゲットにデータをインポートする場合は、バックエンドを混在させないでください。つまり、物理インポート モードと論理インポート モードを使用して、データを単一の TiDB クラスターに同時にインポートしないでください。
