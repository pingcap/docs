---
title: Keywords
summary: Keywords and Reserved Words
---

# キーワード {#keywords}

この記事では、TiDBのキーワード、予約語と非予約語の違いを紹介し、クエリのすべてのキーワードを要約します。

キーワードは、 `SELECT`などのSQLステートメントで特別な意味を持つ`DELETE` `UPDATE` 。それらのいくつかは、**非予約キーワード**と呼ばれる識別子として直接使用できます。それらのいくつかは、<strong>予約キーワード</strong>と呼ばれる識別子として使用される前に特別な処理を必要とします。

予約されたキーワードを識別子として使用するには、それらをバッククォート`` ` ``で囲む必要があります。

{{< copyable "" >}}

```sql
CREATE TABLE select (a INT);
```

```
ERROR 1105 (HY000): line 0 column 19 near " (a INT)" (total length 27)
```

{{< copyable "" >}}

```sql
CREATE TABLE `select` (a INT);
```

```
Query OK, 0 rows affected (0.09 sec)
```

予約されていないキーワードには、 `BEGIN`や`END`などのバッククォートは必要ありません。これらは、次のステートメントで識別子として正常に使用できます。

{{< copyable "" >}}

```sql
CREATE TABLE `select` (BEGIN int, END int);
```

```
Query OK, 0 rows affected (0.09 sec)
```

特別な場合、予約されたキーワードが`.`の区切り文字とともに使用される場合、バッククォートは必要ありません。

{{< copyable "" >}}

```sql
CREATE TABLE test.select (BEGIN int, END int);
```

```
Query OK, 0 rows affected (0.08 sec)
```

次のリストは、TiDBのキーワードを示しています。予約済みのキーワードは`(R)`でマークされています。 [ウィンドウ関数](/functions-and-operators/window-functions.md)の予約キーワードは`(R-Window)`でマークされています：

<TabsPanel letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ" />

<a id="A" class="letter" href="#A">A</a>

-   アカウント
-   アクション
-   追加（R）
-   管理者（R）
-   アドバイス
-   後
-   に対して
-   前に
-   アルゴリズム
-   ALL（R）
-   ALTER（R）
-   いつも
-   分析（R）
-   AND（R）
-   どれか
-   AS（R）
-   ASC（R）
-   ASCII
-   AUTO_ID_CACHE
-   自動増加
-   AUTO_RANDOM
-   AUTO_RANDOM_BASE
-   AVG
-   AVG_ROW_LENGTH

<a id="B" class="letter" href="#B">B</a>

-   バックエンド
-   バックアップ
-   バックアップ
-   始める
-   間（R）
-   BIGINT（R）
-   バイナリ（R）
-   バインディング
-   バインディング
-   BINLOG
-   少し
-   BLOB（R）
-   ブロック
-   BOOL
-   ブール
-   両方（R）
-   BTREE
-   バケツ（R）
-   ビルティンズ（R）
-   BY（R）
-   バイト

<a id="C" class="letter" href="#C">C</a>

-   キャッシュ
-   キャンセル（R）
-   捕獲
-   カスケード（R）
-   カスケード
-   ケース（R）
-   鎖
-   変更（R）
-   CHAR（R）
-   キャラクター（R）
-   文字コード
-   チェック（R）
-   チェックポイント
-   チェックサム
-   暗号
-   掃除
-   クライアント
-   CMSKETCH（R）
-   COALESCE
-   照合（R）
-   照合
-   列（R）
-   列
-   COLUMN_FORMAT
-   コメント
-   専念
-   関与する
-   コンパクト
-   圧縮
-   圧縮
-   並行性
-   CONFIG
-   繋がり
-   一貫性のある
-   制約（R）
-   環境
-   変換（R）
-   CPU
-   CREATE（R）
-   クロス（R）
-   CSV_BACKSLASH_ESCAPE
-   CSV_DELIMITER
-   CSV_HEADER
-   CSV_NOT_NULL
-   CSV_NULL
-   CSV_SEPARATOR
-   CSV_TRIM_LAST_SEPARATORS
-   CUME_DIST（Rウィンドウ）
-   現在
-   CURRENT_DATE（R）
-   CURRENT_ROLE（R）
-   CURRENT_TIME（R）
-   CURRENT_TIMESTAMP（R）
-   CURRENT_USER（R）
-   サイクル

<a id="D" class="letter" href="#D">D</a>

-   データ
-   データベース（R）
-   データベース（R）
-   日にち
-   日付時刻
-   日
-   DAY_HOUR（R）
-   DAY_MICROSECOND（R）
-   DAY_MINUTE（R）
-   DAY_SECOND（R）
-   DDL（R）
-   割り当て解除
-   10進数（R）
-   デフォルト（R）
-   定義者
-   遅延（R）
-   DELAY_KEY_WRITE
-   削除（R）
-   DENSE_RANK（Rウィンドウ）
-   深さ（R）
-   DESC（R）
-   説明（R）
-   ディレクトリ
-   無効にする
-   破棄
-   ディスク
-   DISTINCT（R）
-   DISTINCTROW（R）
-   DIV（R）
-   行う
-   ダブル（R）
-   ドレイナー（R）
-   ドロップ（R）
-   デュアル（R）
-   複製
-   動的

<a id="E" class="letter" href="#E">E</a>

-   ELSE（R）
-   有効
-   同封（R）
-   暗号化
-   終わり
-   強制
-   エンジン
-   エンジン
-   ENUM
-   エラー
-   エラー
-   エスケープ
-   エスケープ（R）
-   イベント
-   イベント
-   進化
-   （R）を除く
-   両替
-   エクスクルーシブ
-   実行する
-   EXISTS（R）
-   拡張
-   期限切れ
-   EXPLAIN（R）
-   拡張

<a id="F" class="letter" href="#F">F</a>

-   FALSE（R）
-   障害
-   田畑
-   ファイル
-   最初
-   FIRST_VALUE（Rウィンドウ）
-   修繕
-   フロート（R）
-   流す
-   続く
-   FOR（R）
-   フォース（R）
-   外国人（R）
-   フォーマット
-   FROM（R）
-   満杯
-   フルテキスト（R）
-   関数

<a id="G" class="letter" href="#G">G</a>

-   全般的
-   生成された（R）
-   グローバル
-   GRANT（R）
-   助成金
-   グループ（R）
-   グループ（Rウィンドウ）

<a id="H" class="letter" href="#H">H</a>

-   ハッシュ
-   HAVING（R）
-   HIGH_PRIORITY（R）
-   歴史
-   ホスト
-   時間
-   HOUR_MICROSECOND（R）
-   HOUR_MINUTE（R）
-   HOUR_SECOND（R）

<a id="I" class="letter" href="#I">私</a>

-   識別された
-   IF（R）
-   イグノア（R）
-   輸入
-   輸入
-   IN（R）
-   インクリメント
-   増分
-   インデックス（R）
-   インデックス
-   INFILE（R）
-   インナー（R）
-   挿入（R）
-   INSERT_METHOD
-   実例
-   INT（R）
-   INT1（R）
-   INT2（R）
-   INT3（R）
-   INT4（R）
-   INT8（R）
-   整数（R）
-   インターバル（R）
-   INTO（R）
-   見えない
-   INVOKER
-   IO
-   IPC
-   IS（R）
-   隔離
-   発行者

<a id="J" class="letter" href="#J">J</a>

-   JOB（R）
-   JOBS（R）
-   参加（R）
-   JSON

<a id="K" class="letter" href="#K">K</a>

-   キー（R）
-   キー（R）
-   KEY_BLOCK_SIZE
-   キル（R）

<a id="L" class="letter" href="#L">L</a>

-   ラベル
-   LAG（Rウィンドウ）
-   言語
-   過去
-   LASTVAL
-   LAST_BACKUP
-   LAST_VALUE（Rウィンドウ）
-   LEAD（Rウィンドウ）
-   リーディング（R）
-   左（R）
-   以下
-   レベル
-   いいね（R）
-   LIMIT（R）
-   リニア（R）
-   LINES（R）
-   リスト
-   負荷（R）
-   ローカル
-   現地時間（R）
-   LOCALTIMESTAMP（R）
-   位置
-   LOCK（R）
-   ログ
-   ロング（R）
-   LONGBLOB（R）
-   ロングテキスト（R）
-   LOW_PRIORITY（R）

<a id="M" class="letter" href="#M">M</a>

-   主人
-   マッチ（R）
-   最大値（R）
-   MAX_CONNECTIONS_PER_HOUR
-   MAX_IDXNUM
-   MAX_MINUTES
-   MAX_QUERIES_PER_HOUR
-   MAX_ROWS
-   MAX_UPDATES_PER_HOUR
-   MAX_USER_CONNECTIONS
-   MB
-   MEDIUMBLOB（R）
-   MEDIUMINT（R）
-   MEDIUMTEXT（R）
-   メモリー
-   マージ
-   マイクロ秒
-   分
-   MINUTE_MICROSECOND（R）
-   MINUTE_SECOND（R）
-   最小値
-   MIN_ROWS
-   MOD（R）
-   モード
-   変更
-   月

<a id="N" class="letter" href="#N">N</a>

-   名前
-   全国
-   ナチュラル（R）
-   NCHAR
-   一度もない
-   次
-   NEXTVAL
-   いいえ
-   NOCACHE
-   NOCYCLE
-   ノードグループ
-   NODE_ID（R）
-   NODE_STATE（R）
-   NOMAXVALUE
-   公称値
-   なし
-   NOT（R）
-   NOWAIT
-   NO_WRITE_TO_BINLOG（R）
-   NTH_VALUE（Rウィンドウ）
-   NTILE（Rウィンドウ）
-   NULL（R）
-   NULLS
-   NUMERIC（R）
-   NVARCHAR

<a id="O" class="letter" href="#O">O</a>

-   オフセット
-   オン（R）
-   オンライン
-   それだけ
-   ON_DUPLICATE
-   開いた
-   楽観的（R）
-   最適化（R）
-   オプション（R）
-   オプションで（R）
-   または（R）
-   注文（R）
-   アウター（R）
-   アウトファイル（R）
-   OVER（Rウィンドウ）

<a id="P" class="letter" href="#P">P</a>

-   PACK_KEYS
-   ページ
-   パーサー
-   部分的
-   パーティション（R）
-   パーティショニング
-   パーティション
-   パスワード
-   PERCENT_RANK（Rウィンドウ）
-   PER_DB
-   PER_TABLE
-   悲観的（R）
-   プラグイン
-   先行
-   プレシジョン（R）
-   準備
-   PRE_SPLIT_REGIONS
-   プライマリー（R）
-   特権
-   手順（R）
-   処理する
-   プロセスリスト
-   プロフィール
-   プロファイル
-   ポンプ（R）

<a id="Q" class="letter" href="#Q">Q</a>

-   クォーター
-   クエリ
-   QUERY
-   素早い

<a id="R" class="letter" href="#R">R</a>

-   部隊）
-   ランク（Rウィンドウ）
-   RATE_LIMIT
-   読む（R）
-   リアル（R）
-   再構築
-   回復します
-   冗長
-   参考文献（R）
-   正規表現（R）
-   地域（R）
-   地域（R）
-   リリース（R）
-   リロード
-   削除する
-   名前を変更（R）
-   再編成
-   修理
-   リピート（R）
-   再現性
-   交換（R）
-   レプリカ
-   複製
-   要求（R）
-   尊敬する
-   戻す
-   復元
-   制限（R）
-   逆行する
-   REVOKE（R）
-   右（R）
-   RLIKE（R）
-   役割
-   ロールバック
-   ルーティーン
-   ROW（R）
-   ROWS（Rウィンドウ）
-   ROW_COUNT
-   ROW_FORMAT
-   ROW_NUMBER（Rウィンドウ）
-   RTREE

<a id="S" class="letter" href="#S">S</a>

-   サンプル（R）
-   2番目
-   SECONDARY_ENGINE
-   SECONDARY_LOAD
-   SECONDARY_UNLOAD
-   SECOND_MICROSECOND（R）
-   安全
-   SELECT（R）
-   SEND_CREDENTIALS_TO_TIKV
-   セパレーター
-   順序
-   シリアル
-   シリアル化可能
-   セッション
-   セット（R）
-   SETVAL
-   SHARD_ROW_ID_BITS
-   シェア
-   共有
-   ショー（R）
-   シャットダウン
-   署名済み
-   単純
-   SKIP_SCHEMA_FILES
-   奴隷
-   スロー
-   SMALLINT（R）
-   スナップショット
-   いくつか
-   ソース
-   空間（R）
-   スプリット（R）
-   SQL（R）
-   SQL_BIG_RESULT（R）
-   SQL_BUFFER_RESULT
-   SQL_CACHE
-   SQL_CALC_FOUND_ROWS（R）
-   SQL_NO_CACHE
-   SQL_SMALL_RESULT（R）
-   SQL_TSI_DAY
-   SQL_TSI_HOUR
-   SQL_TSI_MINUTE
-   SQL_TSI_MONTH
-   SQL_TSI_QUARTER
-   SQL_TSI_SECOND
-   SQL_TSI_WEEK
-   SQL_TSI_YEAR
-   SSL（R）
-   始める
-   開始（R）
-   統計（R）
-   STATS_AUTO_RECALC
-   STATS_BUCKETS（R）
-   STATS_HEALTHY（R）
-   STATS_HISTOGRAMS（R）
-   STATS_META（R）
-   STATS_PERSISTENT
-   STATS_SAMPLE_PAGES
-   状態
-   保管所
-   STORED（R）
-   STRAIGHT_JOIN（R）
-   STRICT_FORMAT
-   主題
-   サブパーティション
-   サブパーティション
-   素晴らしい
-   スワップ
-   スイッチ
-   システム時刻

<a id="T" class="letter" href="#T">T</a>

-   表（R）
-   テーブル
-   テーブルスペース
-   TABLE_CHECKSUM
-   一時的
-   誘惑
-   終了（R）
-   文章
-   よりも
-   THEN（R）
-   TIDB（R）
-   TIFLASH（R）
-   TIKV_IMPORTER
-   時間
-   タイムスタンプ
-   TINYBLOB（R）
-   TINYINT（R）
-   TINYTEXT（R）
-   TO（R）
-   TOPN（R）
-   痕跡
-   伝統的
-   トレーリング（R）
-   取引
-   トリガー（R）
-   トリガー
-   真（R）
-   切り捨てる
-   タイプ

<a id="U" class="letter" href="#U">U</a>

-   無制限
-   コミットされていません
-   未定義
-   UNICODE
-   ユニオン（R）
-   ユニーク（R）
-   わからない
-   ロック解除（R）
-   未署名（R）
-   更新（R）
-   使用法（R）
-   使用（R）
-   ユーザー
-   使用（R）
-   UTC_DATE（R）
-   UTC_TIME（R）
-   UTC_TIMESTAMP（R）

<a id="V" class="letter" href="#V">V</a>

-   検証
-   価値
-   値（R）
-   VARBINARY（R）
-   VARCHAR（R）
-   VARCHARACTER（R）
-   変数
-   変化する（R）
-   見る
-   仮想（R）
-   見える

<a id="W" class="letter" href="#W">W</a>

-   警告
-   週
-   WEIGHT_STRING
-   いつ（R）
-   WHERE（R）
-   幅（R）
-   ウィンドウ（Rウィンドウ）
-   WITH（R）
-   それなし
-   書き込み（R）

<a id="X" class="letter" href="#X">バツ</a>

-   X509
-   XOR（R）

<a id="Y" class="letter" href="#Y">Y</a>

-   年
-   YEAR_MONTH（R）

<a id="Z" class="letter" href="#Z">Z</a>

-   ゼロフィル（R）
