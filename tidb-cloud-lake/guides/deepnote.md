---
title: Deepnote で TiDB Cloud Lake に接続する
summary: Deepnote を使うと、友人や同僚とリアルタイムで、1 か所で簡単にデータサイエンスプロジェクトに取り組むことができ、アイデアや分析をより速くプロダクトへとつなげられます。Deepnote はブラウザ向けに構築されているため、あらゆるプラットフォーム（Windows、Mac、Linux、または Chromebook）で利用できます。ダウンロードは不要で、更新は毎日自動的に提供されます。すべての変更は即座に保存されます。
---

# Deepnote で TiDB Cloud Lake に接続する

[Deepnote](https://deepnote.com) を使うと、友人や同僚とリアルタイムで、1 か所で簡単にデータサイエンスプロジェクトに取り組むことができ、アイデアや分析をより速くプロダクトへとつなげられます。Deepnote はブラウザ向けに構築されているため、あらゆるプラットフォーム（Windows、Mac、Linux、または Chromebook）で利用できます。ダウンロードは不要で、更新は毎日自動的に提供されます。すべての変更は即座に保存されます。

Deepnote の ClickHouse 互換インテグレーションを使用すると、安全な接続で Deepnote を {{{ .lake }}} に接続できます。

## チュートリアル: Deepnote との統合 {#tutorial-integrating-with-deepnote}

このチュートリアルでは、{{{ .lake }}} を Deepnote と統合する手順を説明します。

### Step 1. 環境をセットアップする {#step-1-set-up-environment}

{{{ .lake }}} アカウントにログインでき、Warehouse の接続情報を取得できることを確認してください。詳細は、[Warehouse への接続](/tidb-cloud-lake/guides/warehouse.md#connecting-to-a-warehouse) を参照してください。

### Step 2. {{{ .lake }}} に接続する {#step-2-connect-to-lake}

1. Deepnote にサインインします。アカウントを持っていない場合は作成してください。

2. 左側のサイドバーで **INTEGRATIONS** の右にある **+** をクリックし、**ClickHouse** を選択します。

    ![ClickHouse との統合](/media/tidb-cloud-lake/integration-clickhouse.png)

3. 接続情報を使用して各フィールドを入力します。

    | パラメータ | 説明 |
    | ---------------- | ---------------------------------- |
    | Integration name | 例えば、`TiDB Cloud Lake`     |
    | Host name        | 接続情報から取得します |
    | Port             | `443`                              |
    | Username         | `cloudapp`                         |
    | Password         | 接続情報から取得します |

4. ノートブックを作成します。

5. ノートブックで **SQL** セクションに移動し、先ほど作成した接続を選択します。

これで準備完了です。ツールの使い方については、Deepnote のドキュメントを参照してください。