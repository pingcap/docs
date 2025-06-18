---
title: Import Local Files to TiDB Cloud Serverless
summary: ローカル ファイルをTiDB Cloud Serverless にインポートする方法を学びます。
---

# ローカルファイルをTiDB Cloud Serverlessにインポート {#import-local-files-to-tidb-cloud-serverless}

ローカルファイルをTiDB Cloud Serverlessに直接インポートできます。タスク設定は数回クリックするだけで完了し、ローカルCSVデータがTiDBクラスターに素早くインポートされます。この方法を使えば、クラウドstorageや認証情報を入力する必要はなく、インポートプロセス全体が迅速かつスムーズです。

現在、この方法では、1 つのタスクに対して 1 つの CSV ファイルを既存の空のテーブルまたは新しいテーブルにインポートすることがサポートされています。

## 制限事項 {#limitations}

-   現在、 TiDB Cloud は、1 つのタスクにつき 250 MiB 以内の CSV 形式のローカル ファイルのインポートのみをサポートしています。
-   ローカル ファイルのインポートは、 TiDB Cloud Serverless クラスターでのみサポートされ、 TiDB Cloud Dedicated クラスターではサポートされません。
-   複数のインポート タスクを同時に実行することはできません。

## ローカルファイルをインポートする {#import-local-files}

1.  ターゲット クラスターの**インポート**ページを開きます。

    1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動します。

        > **ヒント：**
        >
        > 左上隅のコンボ ボックスを使用して、組織、プロジェクト、クラスターを切り替えることができます。

    2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[データ]** &gt; **[インポート]**をクリックします。

2.  **インポート**ページでは、ローカルファイルをアップロードエリアに直接ドラッグ＆ドロップするか、 **「ローカルファイルをアップロード」**をクリックして対象のローカルファイルを選択してアップロードできます。1つのタスクにつき、250MiB未満のCSVファイルを1つだけアップロードできます。ローカルファイルが250MiBを超える場合は、 [250 MiB を超えるローカル ファイルをインポートするにはどうすればよいでしょうか?](#how-to-import-a-local-file-larger-than-250-mib)参照してください。

3.  **「宛先」**セクションで、ターゲットデータベースとターゲットテーブルを選択するか、名前を直接入力して新しいデータベースまたはテーブルを作成します。名前には、Unicode BMP（Basic Multilingual Plane）の文字のみを使用し、ヌル文字`\u0000`と空白文字は含めず、最大64文字まで使用できます。 **「テーブルの定義」を**クリックすると、 **「テーブル定義」**セクションが表示されます。

4.  表を確認してください。

    設定可能なテーブル列のリストが表示されます。各行には、 TiDB Cloudによって推定されたテーブル列名、推定されたテーブル列の型、および CSV ファイルからプレビューされたデータが表示されます。

    -   TiDB Cloudの既存のテーブルにデータをインポートする場合、テーブル定義から列リストが抽出され、プレビューされたデータが列名によって対応する列にマップされます。

    -   新しいテーブルを作成する場合、CSVファイルから列リストが抽出され、 TiDB Cloudによって列の型が推測されます。例えば、プレビューされたデータがすべて整数の場合、推測される列の型は整数になります。

5.  列名とデータ型を構成します。

    CSV ファイルの最初の行に列名が記録されている場合は、デフォルトで選択されている**「最初の行を列名として使用する**」が選択されていることを確認します。

    CSVファイルに列名用の行がない場合は、 **「最初の行を列名として使用」**を選択しないでください。この場合、次のようになります。

    -   対象テーブルが既に存在する場合、CSVファイル内の列が順番に対象テーブルにインポートされます。余分な列は切り捨てられ、不足している列にはデフォルト値が設定されます。

    -   TiDB Cloud でターゲットテーブルを作成する必要がある場合は、各列の名前を入力してください。列名は、以下の要件を満たす必要があります。

        -   名前は、ヌル文字`\u0000`と空白文字を除く、Unicode BMP の文字で構成されている必要があります。
        -   名前の長さは 65 文字未満にする必要があります。

        必要に応じてデータ型を変更することもできます。

    > **注記：**
    >
    > TiDB Cloudの既存のテーブルに CSV ファイルをインポートし、ターゲット テーブルにソース ファイルよりも多くの列がある場合、状況に応じて余分な列が異なって処理されます。
    >
    > -   追加列が主キーまたは一意キーでない場合、エラーは報告されません。代わりに、これらの追加列には[デフォルト値](/data-type-default-values.md)設定されます。
    > -   追加列が主キーまたは一意キーであり、属性`auto_increment`または`auto_random`を持たない場合、エラーが報告されます。その場合は、以下のいずれかの戦略を選択することをお勧めします。
    >     -   これらの主キーまたは一意キーの列を含むソース ファイルを提供します。
    >     -   ターゲット テーブルの主キーと一意キーの列を、ソース ファイル内の既存の列と一致するように変更します。
    >     -   主キーまたは一意キー列の属性を`auto_increment`または`auto_random`に設定します。

6.  新しいターゲットテーブルでは、主キーを設定できます。主キーとして列を選択するか、複数の列を選択して複合主キーを作成できます。複合主キーは、列名を選択した順序で作成されます。

    > **注記：**
    >
    > テーブルの主キーはクラスター化インデックスであり、作成後に削除することはできません。

7.  必要に応じて CSV 構成を編集します。

    **「CSV設定の編集」を**クリックすると、バックスラッシュエスケープ、セパレーター、区切り文字を設定して、よりきめ細かな制御を行うことができます。CSV設定の詳細については、 [データのインポートのためのCSV構成](/tidb-cloud/csv-config-for-import-data.md)参照してください。

8.  **[インポートの開始]を**クリックします。

    **インポートタスクの詳細**ページでインポートの進行状況を確認できます。警告や失敗したタスクがある場合は、詳細を確認して解決できます。

9.  インポートタスクが完了したら、 **「SQLエディタでデータを**探索」をクリックして、インポートしたデータに対してクエリを実行できます。SQLエディタの使用方法の詳細については、 [AI支援SQLエディターでデータを探索](/tidb-cloud/explore-data-with-chat2query.md)ご覧ください。

10. **[インポート]**ページで、 **[アクション**] 列の**[...** ] &gt; **[ビュー]**をクリックして、インポート タスクの詳細を確認できます。

## FAQ {#faq}

### TiDB Cloudのインポート機能を使用して、指定した列のみをインポートできますか? {#can-i-only-import-some-specified-columns-by-the-import-feature-in-tidb-cloud}

いいえ。現在、インポート機能を使用する場合、CSV ファイルのすべての列を既存のテーブルにインポートすることしかできません。

特定の列のみをインポートするには、MySQLクライアントを使用してTiDBクラスタに接続し、 [`LOAD DATA`](https://docs.pingcap.com/tidb/stable/sql-statement-load-data)使用してインポートする列を指定します。例：

```sql
CREATE TABLE `import_test` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `address` varchar(64) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB;
LOAD DATA LOCAL INFILE 'load.txt' INTO TABLE import_test FIELDS TERMINATED BY ',' (name, address);
```

`mysql`使用していて`ERROR 2068 (HY000): LOAD DATA LOCAL INFILE file request rejected due to restrictions on access.`遭遇した場合は、接続文字列に`--local-infile=true`追加できます。

### TiDB Cloudにデータをインポートした後、予約キーワードを含む列をクエリできないのはなぜですか? {#why-can-t-i-query-a-column-with-a-reserved-keyword-after-importing-data-into-tidb-cloud}

列名がTiDBで予約済みの[キーワード](/keywords.md)である場合、その列をクエリする際には、列名を囲むバッククォート`` ` ``を追加する必要があります。例えば、列名が`order`場合、 `` `order` ``で列をクエリする必要があります。

### 250 MiB を超えるローカル ファイルをインポートするにはどうすればよいでしょうか? {#how-to-import-a-local-file-larger-than-250-mib}

ファイルが250MiBより大きい場合は、 [TiDB CloudCLI](/tidb-cloud/get-started-with-cli.md)使用してファイルをインポートできます。詳細については、 [`ticloud serverless import start`](/tidb-cloud/ticloud-import-start.md)参照してください。

あるいは、 `split [-l ${line_count}]`ユーティリティを使って複数の小さなファイルに分割することもできます（LinuxまたはmacOSのみ）。例えば、 `split -l 100000 tidb-01.csv small_files`実行すると、 `tidb-01.csv`というファイルが行長`100000`で分割され、分割後のファイルの名前は`small_files${suffix}`なります。その後、これらの小さなファイルをTiDB Cloudに1つずつインポートできます。

次のスクリプトを参照してください。

```bash
#!/bin/bash
n=$1
file_path=$2
file_extension="${file_path##*.}"
file_name="${file_path%.*}"
total_lines=$(wc -l < $file_path)
lines_per_file=$(( (total_lines + n - 1) / n ))
split -d -a 1 -l $lines_per_file $file_path $file_name.
for (( i=0; i<$n; i++ ))
do
    mv $file_name.$i $file_name.$i.$file_extension
done
```

`n`とファイル名を入力してスクリプトを実行すると、元のファイル拡張子を維持しながら、ファイルを`n`均等な部分に分割します。例：

```bash
> sh ./split.sh 3 mytest.customer.csv
> ls -h | grep mytest
mytest.customer.0.csv
mytest.customer.1.csv
mytest.customer.2.csv
mytest.customer.csv
```
