---
title: dbt を使用したデータのロード
summary: dbt は、より高品質な結果を生み出しながら、より多くの作業をこなせるようにする変換ワークフローです。dbt を使用すると、分析コードをモジュール化して一元管理できるほか、ソフトウェアエンジニアリングのワークフローで一般的なガードレールをデータチームに提供できます。データモデルでコラボレーションし、バージョン管理を行い、クエリを安全に本番へデプロイする前にテストとドキュメント化を実施できます。さらに、監視と可視性も備えています。
---

# dbt を使用したデータのロード

[dbt](https://www.getdbt.com/) は、より高品質な結果を生み出しながら、より多くの作業をこなせるようにする変換ワークフローです。dbt を使用すると、分析コードをモジュール化して一元管理できるほか、ソフトウェアエンジニアリングのワークフローで一般的なガードレールをデータチームに提供できます。データモデルでコラボレーションし、バージョン管理を行い、クエリを安全に本番へデプロイする前にテストとドキュメント化を実施できます。さらに、監視と可視性も備えています。

[tidbcloudlake-dbt](https://github.com/tidbcloud/lake-dbt) は、dbt と {{{ .lake }}} のスムーズな統合を実現することを主な目的として、{{{ .lake }}} によって開発されたプラグインです。このプラグインを使用すると、dbt を使ってデータモデリング、変換、クレンジングのタスクをシームレスに実行し、その出力を便利に {{{ .lake }}} にロード (load) できます。以下の表は、tidbcloudlake-dbt プラグインが dbt の一般的によく使われる機能に対して提供するサポートレベルを示しています。

| 機能                      | サポート対象 ? |
|----------------------------- |----------- |
| テーブルのマテリアライズ        | はい        |
| ビューのマテリアライズ          | はい        |
| インクリメンタルマテリアライズ   | はい        |
| エフェメラルマテリアライズ      | いいえ      |
| Seeds                        | はい        |
| Sources                      | はい        |
| カスタムデータテスト            | はい        |
| Docs Generate                | はい        |
| Snapshots                    | はい        |
| Connection Retry             | はい        |

## tidbcloudlake-dbt のインストール {#install-tidbcloudlake-dbt}

tidbcloudlake-dbt プラグインのインストールは、必須依存関係として dbt が含まれるようになったため、より簡単になりました。dbt と tidbcloudlake-dbt プラグインの両方を簡単にセットアップするには、次のコマンドを実行します。

```shell
pip3 install tidbcloudlake-dbt
```

ただし、dbt を個別にインストールしたい場合は、詳細な手順について公式の dbt インストールガイドを参照してください。

## チュートリアル: dbt プロジェクト jaffle_shop を実行する {#tutorial-run-dbt-project-jaffle-shop}

dbt を初めて使用する場合、{{{ .lake }}} では <https://github.com/dbt-labs/jaffle_shop> で提供されている公式 dbt チュートリアルを完了することを推奨します。開始する前に、[tidbcloudlake-dbt のインストール](#install-tidbcloudlake-dbt) に従って dbt と tidbcloudlake-dbt をインストールしてください。

このチュートリアルでは、"jaffle_shop" というサンプル dbt プロジェクトを提供しており、dbt ツールを実践的に体験できます。接続に必要な情報を含めてデフォルトのグローバルプロファイル (~/.dbt/profiles.yml) を設定すると、このプロジェクトは dbt モデルで定義されたテーブルとビューを、{{{ .lake }}} データベース内に直接生成します。以下は、{{{ .lake }}} インスタンスに接続する profiles.yml ファイルの例です。

```yml title="~/.dbt/profiles.yml"
jaffle_shop_lake:
  target: dev
  outputs:
    dev:
      type: tidbcloudlake
      host: tnxxxx.gw.aws-us-east-2.default.tidbcloud.com
      port: 443
      schema: sjh_dbt
      user: <username>
      pass: ********
      warehouse: default
      secure: true
```

アダプターの設定方法と使用方法の詳細については、[lake-dbt リポジトリ](https://github.com/tidbcloud/lake-dbt) を参照してください。