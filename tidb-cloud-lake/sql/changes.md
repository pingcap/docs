---
title: CHANGES
summary: CHANGES 句を使用すると、定義した時間区間内におけるテーブルの変更追跡メタデータをクエリできます。時間区間は、データ保持期間（デフォルトは 24 時間）内に収まっている必要があります。時間区間を定義するには、`AT` キーワードを使用して区間の開始時点となる時刻を指定します。区間の終了時点には、デフォルトで現在時刻が適用されます。過去の時刻を区間の終了時点として指定する場合は、`AT` キーワードとあわせて `END` キーワードを使用して区間を設定します。
---

# CHANGES

CHANGES 句を使用すると、定義した時間区間内におけるテーブルの変更追跡メタデータをクエリできます。時間区間は、データ保持期間（デフォルトは 24 時間）内に収まっている必要があります。時間区間を定義するには、`AT` キーワードを使用して区間の開始時点となる時刻を指定します。区間の終了時点には、デフォルトで現在時刻が適用されます。過去の時刻を区間の終了時点として指定する場合は、`AT` キーワードとあわせて `END` キーワードを使用して区間を設定します。

![alt text](/media/tidb-cloud-lake/changes.png)

## 構文 {#syntax}

```sql
SELECT ...
FROM ...
   CHANGES ( INFORMATION => { DEFAULT | APPEND_ONLY } )
   AT ( { TIMESTAMP => <timestamp> |
          OFFSET => <time_interval> |
          SNAPSHOT => '<snapshot_id>' |
          STREAM => <stream_name> } )

    [ END ( { TIMESTAMP => <timestamp> |
             OFFSET => <time_interval> |
             SNAPSHOT => '<snapshot_id>' } ) ]
```

| パラメータ | 説明 |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| INFORMATION | 取得する変更追跡メタデータの種類を指定します。`DEFAULT` または `APPEND_ONLY` のいずれかに設定できます。`DEFAULT` は、挿入、更新、削除を含むすべての DML 変更を返します。`APPEND_ONLY` に設定すると、追加された行のみが返されます。 |
| AT          | 変更追跡メタデータをクエリする時間区間の開始時点を指定します。 |
| END         | 変更追跡メタデータをクエリする時間区間の終了時点を指定するオプションのパラメータです。指定しない場合、現在時刻がデフォルトの終了時点として使用されます。 |
| TIMESTAMP   | 変更追跡メタデータをクエリする基準点として、特定のタイムスタンプを指定します。 |
| OFFSET      | 変更追跡メタデータをクエリする基準点として、現在時刻からの相対的な秒単位の時間間隔を指定します。負の整数の形式で指定する必要があり、その絶対値が秒単位の時間差を表します。たとえば、`-3600` は 1 時間（3,600 秒）前にさかのぼることを表します。 |
| SNAPSHOT    | 変更追跡メタデータをクエリする基準点として、スナップショット ID を指定します。 |
| STREAM      | 変更追跡メタデータをクエリする基準点として、ストリーム名を指定します。 |

## 変更追跡の有効化 {#enabling-change-tracking}

CHANGES 句を使用するには、テーブルで Fuse エンジンオプション `change_tracking` を `true` に設定しておく必要があります。`change_tracking` オプションの詳細については、[Fuse Engine Options](/tidb-cloud-lake/sql/table-engines.md#available-engines) を参照してください。

```sql title='Example:'
-- Enable change tracking for table 't'
ALTER TABLE t SET OPTIONS(change_tracking = true);
```

## 例 {#examples}

この例では、CHANGES 句を使用して、テーブルに対して行われた変更を追跡およびクエリする方法を示します。

1. ユーザープロファイル情報を保存するテーブルを作成し、変更追跡を有効にします。

    ```sql
    CREATE TABLE user_profiles (
        user_id INT,
        username VARCHAR(255),
        bio TEXT
    ) change_tracking = true;
    
    INSERT INTO user_profiles VALUES (1, 'john_doe', 'Software Engineer');
    INSERT INTO user_profiles VALUES (2, 'jane_smith', 'Marketing Specialist');
    ```

2. プロファイル更新をキャプチャするストリームを作成し、既存のプロファイルを更新して新しいプロファイルを挿入します。

    ```sql
    CREATE STREAM profile_updates ON TABLE user_profiles APPEND_ONLY = TRUE;
    
    UPDATE user_profiles SET bio = 'Data Scientist' WHERE user_id = 1;
    INSERT INTO user_profiles VALUES (3, 'alex_wong', 'Data Analyst');
    ```

3. ストリームによってユーザープロファイルの変更をクエリします。

    ```sql
    -- Return all changes in user profiles captured in the stream
    SELECT *
    FROM user_profiles
    CHANGES (INFORMATION => DEFAULT)
    AT (STREAM => profile_updates);
    
    ┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
    │     user_id     │     username     │        bio        │   change$action  │              change$row_id             │ change$is_update │
    ├─────────────────┼──────────────────┼───────────────────┼──────────────────┼────────────────────────────────────────┼──────────────────┤
    │               1 │ john_doe         │ Data Scientist    │ INSERT           │ 69cffb02264144c384d56f7b6cedee41000000 │ true             │
    │               3 │ alex_wong        │ Data Analyst      │ INSERT           │ 59f315c8655c49eab35ba1959e269430000000 │ false            │
    │               1 │ john_doe         │ Software Engineer │ DELETE           │ 69cffb02264144c384d56f7b6cedee41000000 │ true             │
    └───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
    
    -- Return appended rows in user profiles captured in the stream
    SELECT *
    FROM user_profiles
    CHANGES (INFORMATION => APPEND_ONLY)
    AT (STREAM => profile_updates);
    
    ┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
    │     user_id     │     username     │        bio       │ change$action │ change$is_update │              change$row_id             │
    ├─────────────────┼──────────────────┼──────────────────┼───────────────┼──────────────────┼────────────────────────────────────────┤
    │               3 │ alex_wong        │ Data Analyst     │ INSERT        │ false            │ 59f315c8655c49eab35ba1959e269430000000 │
    └───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
    ```

4. `AT` キーワードと `END` キーワードの両方を使用して、スナップショットとタイムスタンプの間の変更をクエリします。

```sql
-- Step 6: Take a snapshot of the user profile data.
SELECT snapshot_id, timestamp
FROM FUSE_SNAPSHOT('default', 'user_profiles');

┌───────────────────────────────────────────────────────────────┐
│            snapshot_id           │          timestamp         │
├──────────────────────────────────┼────────────────────────────┤
│ 6a11c94433714970895edd38577ac8b0 │ 2024-04-10 02:51:39.422832 │
│ 53dc4750af92423da91c50dcee547cfb │ 2024-04-10 02:51:39.399568 │
│ 910af7424f764891b0c6fa60aa99fc3a │ 2024-04-10 02:50:14.522416 │
│ 1225000916f44819a0d23178b2d0d1af │ 2024-04-10 02:50:14.500417 │
└───────────────────────────────────────────────────────────────┘

SELECT *
FROM user_profiles
CHANGES (INFORMATION => DEFAULT)
AT (SNAPSHOT => '1225000916f44819a0d23178b2d0d1af')
END (TIMESTAMP => '2024-04-10 02:51:39.399568'::TIMESTAMP);

┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│     user_id     │     username     │          bio         │   change$action  │              change$row_id             │ change$is_update │
├─────────────────┼──────────────────┼──────────────────────┼──────────────────┼────────────────────────────────────────┼──────────────────┤
│               1 │ john_doe         │ Data Scientist       │ INSERT           │ 69cffb02264144c384d56f7b6cedee41000000 │ true             │
│               1 │ john_doe         │ Software Engineer    │ DELETE           │ 69cffb02264144c384d56f7b6cedee41000000 │ true             │
│               2 │ jane_smith       │ Marketing Specialist │ INSERT           │ 3db484ac18174223851dc9de22f6bfec000000 │ false            │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```