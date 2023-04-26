---
title: Keywords
summary: Keywords and Reserved Words
---

# キーワード {#keywords}

この記事では、TiDB のキーワード、予約語と非予約語の違いを紹介し、クエリのすべてのキーワードをまとめます。

キーワードは、 `SELECT` 、 `UPDATE` 、 `DELETE`など、SQL ステートメントで特別な意味を持つ単語です。それらの一部は、**非予約キーワード**と呼ばれる識別子として直接使用できます。一部のキーワードは、<strong>予約済みキーワード</strong>と呼ばれる識別子として使用する前に特別な処理が必要です。ただし、特別な処理が必要な場合がある、予約されていない特別なキーワードがあります。これらは予約済みキーワードとして扱うことをお勧めします。

予約済みキーワードを識別子として使用するには、それらをバッククォート`` ` ``で囲む必要があります。

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

予約されていないキーワードは、次のステートメントで識別子として正常に使用できる`BEGIN`や`END`などのバッククォートを必要としません。

{{< copyable "" >}}

```sql
CREATE TABLE `select` (BEGIN int, END int);
```

```
Query OK, 0 rows affected (0.09 sec)
```

特殊なケースでは、予約済みキーワードが`.`区切り文字で使用されている場合、バッククォートは必要ありません。

{{< copyable "" >}}

```sql
CREATE TABLE test.select (BEGIN int, END int);
```

```
Query OK, 0 rows affected (0.08 sec)
```

## キーワード一覧 {#keyword-list}

次のリストは、TiDB のキーワードを示しています。予約済みキーワードは`(R)`でマークされます。 [ウィンドウ関数](/functions-and-operators/window-functions.md)の予約済みキーワードは`(R-Window)`でマークされています。バッククォート`` ` ``でエスケープする必要がある特別な非予約キーワードは、 `(S)`でマークされています。

<TabsPanel letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ" />

<a id="A" class="letter" href="#A">あ</a>

-   アカウント
-   アクション
-   追加(R)
-   管理者 (R)
-   アドバイス
-   後
-   に対して
-   前
-   アルゴリズム
-   すべて (R)
-   アルター(R)
-   いつも
-   アナライズ(R)
-   と (R)
-   どれでも
-   AS(R)
-   ASC(R)
-   アスキー
-   AUTO_ID_CACHE
-   自動増加
-   自動ランダム
-   AUTO_RANDOM_BASE
-   平均
-   AVG_ROW_LENGTH

<a id="B" class="letter" href="#B">B</a>

-   バックエンド
-   バックアップ
-   バックアップ
-   始める
-   間 (R)
-   BIGINT(R)
-   バイナリ (R)
-   バインディング
-   ビンディング
-   ビンログ
-   少し
-   ブロブ(R)
-   ブロック
-   ブール
-   ブール値
-   両方 (R)
-   Bツリー
-   バケット(R)
-   BUILTINS(R)
-   BY (R)
-   バイト

<a id="C" class="letter" href="#C">C</a>

-   キャッシュ
-   キャンセル (R)
-   捕獲
-   カスケード(R)
-   カスケード
-   ケース(R)
-   鎖
-   変更 (R)
-   シャア(R)
-   キャラクター(R)
-   文字コード
-   チェック(R)
-   チェックポイント
-   チェックサム
-   サイファー
-   掃除
-   クライアント
-   CMSKETCH(R)
-   合体
-   コレート(R)
-   照合
-   コラム(R)
-   列
-   COLUMN_FORMAT
-   コメント
-   専念
-   関与する
-   コンパクト
-   圧縮された
-   圧縮
-   同時実行
-   設定
-   繋がり
-   一貫性のある
-   制約 (R)
-   コンテクスト
-   変換 (R)
-   CPU
-   クリエイト(R)
-   クロス(R)
-   CSV_BACKSLASH_ESCAPE
-   CSV_DELIMITER
-   CSV_HEADER
-   CSV_NOT_NULL
-   CSV_NULL
-   CSV_SEPARATOR
-   CSV_TRIM_LAST_SEPARATORS
-   CUME_DIST (R ウィンドウ)
-   現在
-   CURRENT_DATE (R)
-   CURRENT_ROLE (R)
-   CURRENT_TIME (右)
-   CURRENT_TIMESTAMP (R)
-   CURRENT_USER (R)
-   サイクル

<a id="D" class="letter" href="#D">D</a>

-   データ
-   データベース(R)
-   データベース (R)
-   日にち
-   日付時刻
-   日
-   DAY_HOUR (R)
-   DAY_MICROSECOND (R)
-   DAY_MINUTE (R)
-   DAY_SECOND (右)
-   DDL(R)
-   割り当て解除
-   10 進数 (R)
-   デフォルト (R)
-   定義者
-   遅延 (R)
-   DELAY_KEY_WRITE
-   削除 (R)
-   DENSE_RANK (R ウィンドウ)
-   深さ (R)
-   DESC (R)
-   記述 (R)
-   ディレクトリ
-   無効にする
-   破棄
-   ディスク
-   DISTINCT (R)
-   DISTINCTROW(R)
-   DIV (右)
-   する
-   ダブル(R)
-   ドレイナー(R)
-   ドロップ(R)
-   デュアル(R)
-   複製
-   動的

<a id="E" class="letter" href="#E">え</a>

-   その他 (R)
-   有効
-   同封 (R)
-   暗号化
-   終わり
-   強制された
-   エンジン
-   エンジン
-   列挙型
-   エラー
-   エラー
-   エスケープ
-   エスケープ (R)
-   イベント
-   イベント
-   進化
-   例外 (R)
-   交換
-   エクスクルーシブ
-   実行する
-   存在する (R)
-   拡張
-   期限切れ
-   EXPLAIN(R)
-   拡張された

<a id="F" class="letter" href="#F">ふ</a>

-   偽 (R)
-   故障
-   田畑
-   ファイル
-   初め
-   FIRST_VALUE (R ウィンドウ)
-   修理済み
-   フロート(R)
-   流す
-   続く
-   フォー(R)
-   フォース(R)
-   外国語 (R)
-   フォーマット
-   から (R)
-   満杯
-   フルテキスト (R)
-   関数

<a id="G" class="letter" href="#G">G</a>

-   全般的
-   ジェネレーテッド (R)
-   グローバル
-   グラント (R)
-   助成金
-   グループ (R)
-   グループ (R ウィンドウ)

<a id="H" class="letter" href="#H">H</a>

-   ハッシュ
-   持つ (R)
-   高優先度 (R)
-   歴史
-   ホスト
-   時間
-   HOUR_MICROSECOND (R)
-   HOUR_MINUTE (R)
-   HOUR_SECOND (R)

<a id="I" class="letter" href="#I">私</a>

-   識別された
-   IF(R)
-   無視 (R)
-   輸入
-   輸入
-   に (R)
-   インクリメント
-   増分
-   索引(R)
-   インデックス
-   インファイル(R)
-   インナー(R)
-   インサート (R)
-   INSERT_METHOD
-   実例
-   INT(R)
-   INT1(R)
-   INT2(R)
-   INT3(R)
-   INT4(R)
-   INT8(R)
-   整数 (R)
-   間隔 (R)
-   に (R)
-   見えない
-   呼び出し元
-   IO
-   IPC
-   イズ(R)
-   隔離
-   発行者

<a id="J" class="letter" href="#J">J</a>

-   ジョブ(R)
-   ジョブズ(R)
-   ジョイン(R)
-   JSON

<a id="K" class="letter" href="#K">K</a>

-   キー(R)
-   キーズ(R)
-   KEY_BLOCK_SIZE
-   キル(R)

<a id="L" class="letter" href="#L">L</a>

-   ラベル
-   LAG (R-ウィンドウ)
-   言語
-   最後
-   ラストヴァル
-   LAST_BACKUP
-   LAST_VALUE (R ウィンドウ)
-   LEAD (Rウィンドウ)
-   リーディング (R)
-   左（右）
-   以下
-   レベル
-   いいね(R)
-   リミット(R)
-   リニア(R)
-   LINES(R)
-   リスト
-   ロード (R)
-   地元
-   ローカルタイム (R)
-   ローカルタイムスタンプ (R)
-   位置
-   ロック (R)
-   ログ
-   ロング(R)
-   ロングブロブ(R)
-   ロングテキスト(R)
-   LOW_PRIORITY (R)

<a id="M" class="letter" href="#M">M</a>

-   マスター
-   マッチ(R)
-   MAXVALUE (R)
-   MAX_CONNECTIONS_PER_HOUR
-   MAX_IDXNUM
-   MAX_MINUTES
-   MAX_QUERIES_PER_HOUR
-   MAX_ROWS
-   MAX_UPDATES_PER_HOUR
-   MAX_USER_CONNECTIONS
-   MB
-   ミディアムブロブ(R)
-   ミディアムミント(R)
-   MEDIUMTEXT (R)
-   メモリー
-   マージ
-   マイクロ秒
-   分
-   MINUTE_MICROSECOND (R)
-   MINUTE_SECOND (右)
-   MINVALUE
-   MIN_ROWS
-   モッド(R)
-   モード
-   変更
-   月

<a id="N" class="letter" href="#N">N</a>

-   名前
-   全国
-   ナチュラル(R)
-   NCHAR
-   一度もない
-   次
-   ネクストヴァル
-   いいえ
-   ノカシェ
-   ノサイクル
-   ノードグループ
-   NODE_ID (R)
-   NODE_STATE (R)
-   NOMAXVALUE
-   名目値
-   なし
-   ない (R)
-   今すぐ
-   NO_WRITE_TO_BINLOG (R)
-   NTH_VALUE (R ウィンドウ)
-   NTILE (R-ウィンドウ)
-   ヌル (R)
-   ヌル
-   数値 (R)
-   NVARCHAR

<a id="O" class="letter" href="#O">〇</a>

-   オフセット
-   オン(R)
-   オンライン
-   それだけ
-   ON_DUPLICATE
-   開ける
-   オプティミスティック(R)
-   最適化 (R)
-   オプション(R)
-   オプションで (R)
-   または (R)
-   オーダー (R)
-   アウター(R)
-   アウトファイル (R)
-   OVER (R-ウィンドウ)

<a id="P" class="letter" href="#P">P</a>

-   PACK_KEYS
-   ページ
-   パーサー
-   部分的
-   パーティション(R)
-   パーティショニング
-   パーティション
-   パスワード
-   PERCENT_RANK (R ウィンドウ)
-   PER_DB
-   PER_TABLE
-   ペシミスティック(R)
-   配置 (S)
-   プラグイン
-   前に
-   プレシジョン(R)
-   準備
-   PRE_SPLIT_REGIONS
-   プライマリー (R)
-   特典
-   手順 (R)
-   プロセス
-   プロセスリスト
-   プロフィール
-   プロファイル
-   ポンプ(R)

<a id="Q" class="letter" href="#Q">Q</a>

-   クォーター
-   クエリ
-   クエリ
-   素早い

<a id="R" class="letter" href="#R">R</a>

-   部隊）
-   RANK (R-ウィンドウ)
-   RATE_LIMIT
-   読み取り (R)
-   リアル(R)
-   再構築
-   回復
-   冗長
-   参考文献 (R)
-   REGEXP (R)
-   地域 (R)
-   地域 (R)
-   リリース (R)
-   リロード
-   削除
-   リネーム(R)
-   再編成する
-   修理
-   リピート(R)
-   繰り返し可能
-   リプレイス(R)
-   レプリカ
-   複製
-   要求する (R)
-   尊敬
-   戻す
-   復元する
-   制限 (R)
-   逆行
-   REVOKE(R)
-   右 (R)
-   RLIKE(R)
-   役割
-   ロールバック
-   ルーティーン
-   行 (R)
-   ROWS (R-ウィンドウ)
-   ROW_COUNT
-   ROW_FORMAT
-   ROW_NUMBER (R-ウィンドウ)
-   RTREE

<a id="S" class="letter" href="#S">S</a>

-   サンプル (R)
-   2番
-   SECONDARY_ENGINE
-   SECONDARY_LOAD
-   SECONDARY_UNLOAD
-   SECOND_MICROSECOND (R)
-   安全
-   選択 (R)
-   SEND_CREDENTIALS_TO_TIKV
-   セパレーター
-   順序
-   シリアル
-   SERIALIZABLE
-   セッション
-   セット(R)
-   セットヴァル
-   SHARD_ROW_ID_BITS
-   共有
-   共有
-   ショー(R)
-   シャットダウン
-   署名済み
-   単純
-   SKIP_SCHEMA_FILES
-   スレーブ
-   遅い
-   SMALLINT(R)
-   スナップショット
-   いくつかの
-   ソース
-   空間(R)
-   スプリット(R)
-   SQL(R)
-   SQL_BIG_RESULT (R)
-   SQL_BUFFER_RESULT
-   SQL_CACHE
-   SQL_CALC_FOUND_ROWS (R)
-   SQL_NO_CACHE
-   SQL_SMALL_RESULT (R)
-   SQL_TSI_DAY
-   SQL_TSI_HOUR
-   SQL_TSI_MINUTE
-   SQL_TSI_MONTH
-   SQL_TSI_QUARTER
-   SQL_TSI_SECOND
-   SQL_TSI_WEEK
-   SQL_TSI_YEAR
-   SSL(R)
-   始める
-   スターティング (R)
-   スタッツ(R)
-   STATS_AUTO_RECALC
-   STATS_BUCKETS (R)
-   STATS_HEALTHY (R)
-   STATS_HISTOGRAMS (R)
-   STATS_META (R)
-   STATS_PERSISTENT
-   STATS_SAMPLE_PAGES
-   スターテス
-   保管所
-   ストアド (R)
-   STRAIGHT_JOIN (R)
-   STRICT_FORMAT
-   主題
-   サブパーティション
-   サブパーティション
-   素晴らしい
-   スワップ
-   スイッチ
-   システム時刻

<a id="T" class="letter" href="#T">T</a>

-   表 (右)
-   テーブル
-   テーブルスペース
-   TABLE_CHECKSUM
-   一時的
-   誘惑的
-   終了 (R)
-   TEXT
-   よりも
-   それから (R)
-   TIDB(R)
-   ティフラッシュ(R)
-   TIKV_IMPORTER
-   時間
-   タイムスタンプ
-   TINYBLOB(R)
-   TINYINT(R)
-   タイニーテキスト(R)
-   に (R)
-   TOKEN_ISSUER
-   トップン(R)
-   痕跡
-   伝統的
-   トレーリング (R)
-   取引
-   トリガー(R)
-   トリガー
-   真 (R)
-   トランケート
-   タイプ

<a id="U" class="letter" href="#U">う</a>

-   無制限
-   未コミット
-   未定義
-   ユニコード
-   ユニオン(R)
-   ユニーク(R)
-   知らない
-   アンロック (R)
-   未署名 (R)
-   更新 (R)
-   使用法 (R)
-   使用 (R)
-   ユーザー
-   使用 (R)
-   UTC_DATE (R)
-   UTC_TIME (R)
-   UTC_TIMESTAMP (R)

<a id="V" class="letter" href="#V">Ⅴ</a>

-   検証
-   価値
-   値 (R)
-   バービナリー (R)
-   VARCHAR (R)
-   VARCHARACTER(R)
-   変数
-   可変 (R)
-   意見
-   バーチャル(R)
-   見える

<a id="W" class="letter" href="#W">W</a>

-   警告
-   週
-   WEIGHT_STRING
-   いつ (R)
-   どこで (R)
-   幅 (R)
-   WINDOW (R-ウィンドウ)
-   と (R)
-   それなし
-   書き込み (R)

<a id="X" class="letter" href="#X">バツ</a>

-   X509
-   XOR (R)

<a id="Y" class="letter" href="#Y">Y</a>

-   年
-   YEAR_MONTH (右)

<a id="Z" class="letter" href="#Z">Z</a>

-   ゼロフィル(R)
