---
title: Keywords
summary: Keywords and Reserved Words
---

# キーワード {#keywords}

この記事では、TiDB のキーワード、予約語と非予約語の違いを紹介し、クエリのすべてのキーワードを要約します。

キーワードは、 SQL ステートメント内で特別な意味を持つ単語です ( `SELECT` 、 `UPDATE` 、 `DELETE`など)。それらの一部は、識別子として直接使用でき、**非予約キーワード**と呼ばれます。一部のキーワードは、識別子として使用する前に特別な処理が必要であり、**予約キーワード**と呼ばれます。ただし、特別な処理が必要な場合がある特別な予約されていないキーワードもあります。予約キーワードとして扱うことをお勧めします。

予約されたキーワードを識別子として使用するには、それらをバッククォート`` ` ``で囲む必要があります。

```sql
CREATE TABLE select (a INT);
```

    ERROR 1105 (HY000): line 0 column 19 near " (a INT)" (total length 27)

```sql
CREATE TABLE `select` (a INT);
```

    Query OK, 0 rows affected (0.09 sec)

予約されていないキーワードには、 `BEGIN`や`END`などのバッククォートは必要ありません。これらは、次のステートメントで識別子として正常に使用できます。

```sql
CREATE TABLE `select` (BEGIN int, END int);
```

    Query OK, 0 rows affected (0.09 sec)

特殊な場合では、予約キーワードが`.`区切り文字とともに使用される場合、バッククォートは必要ありません。

```sql
CREATE TABLE test.select (BEGIN int, END int);
```

    Query OK, 0 rows affected (0.08 sec)

## キーワードリスト {#keyword-list}

TiDB のキーワードを次のリストに示します。予約されたキーワードには`(R)`マークが付けられます。 [ウィンドウ関数](/functions-and-operators/window-functions.md)の予約キーワードには`(R-Window)`マークが付いています。バッククォート`` ` ``でエスケープする必要がある特別な予約されていないキーワードは、 `(S)`でマークされます。

<TabsPanel letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ" />

<a id="A" class="letter" href="#A">あ</a>

-   アカウント
-   アクション
-   アド(R)
-   アドミン(R)
-   アドバイスする
-   後
-   に対して
-   前
-   アルゴリズム
-   オール(R)
-   アルター(R)
-   いつも
-   アナライズ(R)
-   アンド(R)
-   どれでも
-   アレイ(R)
-   アズ(R)
-   アスク(R)
-   アスキー
-   属性
-   属性
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
-   ベルヌーイ
-   ビトゥイーン(R)
-   ビッグINT(R)
-   バイナリー(R)
-   バインディング
-   バインディング
-   BINDING_CACHE
-   ビンログ
-   少し
-   ブロブ(R)
-   ブロック
-   ブール
-   ブール値
-   両方(R)
-   Bツリー
-   バケット(R)
-   ビルティンズ(R)
-   BY(R)
-   バイト

<a id="C" class="letter" href="#C">C</a>

-   キャッシュ
-   校正する
-   コール(R)
-   キャンセル(R)
-   捕獲
-   カスケード(R)
-   カスケード接続
-   ケース(R)
-   因果関係
-   鎖
-   チェンジ(R)
-   チャー(R)
-   キャラクター(R)
-   文字コード
-   チェック(R)
-   チェックポイント
-   チェックサム
-   暗号
-   掃除
-   クライアント
-   CLIENT_ERRORS_SUMMARY
-   近い
-   集まる
-   クラスター化された
-   CMSスケッチ(R)
-   合体
-   コレート(R)
-   照合
-   コラム(R)
-   COLUMN_FORMAT
-   コラム
-   コメント
-   専念
-   関与する
-   コンパクト
-   圧縮された
-   圧縮
-   同時実行性
-   設定
-   繋がり
-   一貫性
-   一貫性のある
-   コンストレイント(R)
-   コンテクスト
-   コンティニュー(R)
-   コンバート(R)
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
-   現在の役割 (R)
-   CURRENT_TIME (R)
-   CURRENT_TIMESTAMP (R)
-   CURRENT_USER (R)
-   カーソル(R)
-   サイクル

<a id="D" class="letter" href="#D">D</a>

-   データ
-   データベース(R)
-   データベース(R)
-   日付
-   日付時刻
-   日
-   DAY_HOUR (R)
-   DAY_MICROSECOND(R)
-   DAY_MINUTE (R)
-   DAY_SECOND(R)
-   DDL(R)
-   割り当てを解除する
-   デシマル(R)
-   宣言する
-   デフォルト(R)
-   定義者
-   DELAY_KEY_WRITE
-   ディレイド(R)
-   削除(R)
-   DENSE_RANK (R ウィンドウ)
-   深さ(R)
-   DESC(R)
-   ディスクリブ(R)
-   ダイジェスト
-   ディレクトリ
-   無効にする
-   無効
-   破棄
-   ディスク
-   ディスティンクト(R)
-   ディスティンクトロウ(R)
-   ディヴ(R)
-   する
-   ダブル(R)
-   水切り(R)
-   ドロップ(R)
-   デュアル(R)
-   重複
-   動的

<a id="E" class="letter" href="#E">E</a>

-   エルス(R)
-   エルセイフ(R)
-   有効にする
-   有効
-   エンクローズド(R)
-   暗号化
-   終わり
-   強制
-   エンジン
-   エンジン
-   ENUM
-   エラー
-   エラー
-   逃げる
-   エスケープド(R)
-   イベント
-   イベント
-   進化
-   (R)を除く
-   交換
-   エクスクルーシブ
-   実行する
-   イグジスト(R)
-   イグジット(R)
-   拡大
-   期限切れ
-   EXPLAIN(R)
-   拡張された

<a id="F" class="letter" href="#F">F</a>

-   FAILED_LOGIN_ATTEMPTS
-   ファルス(R)
-   障害
-   フェッチ(R)
-   田畑
-   ファイル
-   初め
-   FIRST_VALUE (R ウィンドウ)
-   修理済み
-   フロート(R)
-   フロート4(R)
-   フロート8(R)
-   流す
-   続く
-   フォー(R)
-   フォース(R)
-   フォーリン(R)
-   フォーマット
-   見つかった
-   フロム(R)
-   満杯
-   フルテキスト(R)
-   関数

<a id="G" class="letter" href="#G">G</a>

-   一般的な
-   ジェネレイテッド(R)
-   グローバル
-   グラント(R)
-   助成金
-   グループ(R)
-   グループ (R ウィンドウ)

<a id="H" class="letter" href="#H">H</a>

-   ハンドラ
-   ハッシュ
-   ハビング(R)
-   ヘルプ
-   HIGH_PRIORITY (R)
-   ヒストグラム
-   歴史
-   ホスト
-   時間
-   HOUR_MICROSECOND(R)
-   HOUR_MINUTE (R)
-   HOUR_SECOND (R)
-   ハイポ

<a id="I" class="letter" href="#I">私</a>

-   特定されました
-   イフ(R)
-   無視(R)
-   アイライク(R)
-   輸入
-   輸入
-   イン(R)
-   インクリメント
-   増分
-   インデックス(R)
-   インデックス
-   インファイル(R)
-   インナー(R)
-   インアウト(R)
-   インサート(R)
-   INSERT_METHOD
-   実例
-   INT(R)
-   INT1(R)
-   INT2(R)
-   INT3(R)
-   INT4(R)
-   INT8(R)
-   インテジャー(R)
-   インターセクト(R)
-   インターバル(R)
-   イントー(R)
-   見えない
-   呼び出し者
-   IO
-   IPC
-   アイエス(R)
-   分離
-   発行者
-   イテレート(R)

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
-   LAG (R ウィンドウ)
-   言語
-   最後
-   LAST_BACKUP
-   LAST_VALUE (R ウィンドウ)
-   ラストヴァル
-   リード (R ウィンドウ)
-   リーディング(R)
-   リーブ(R)
-   左(R)
-   少ない
-   レベル
-   いいね(R)
-   リミット(R)
-   リニア(R)
-   ラインズ(R)
-   リスト
-   ロード(R)
-   地元
-   ローカルタイム(R)
-   ローカルタイムスタンプ(R)
-   位置
-   ロック(R)
-   ロック済み
-   ログ
-   ロング(R)
-   ロングブロブ(R)
-   ロングテキスト(R)
-   LOW_PRIORITY (R)

<a id="M" class="letter" href="#M">M</a>

-   マスター
-   マッチ(R)
-   マックスバリュー(R)
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
-   ミディアムテキスト(R)
-   メンバー
-   メモリ
-   マージ
-   マイクロ秒
-   ミドルINT(R)
-   分
-   MINUTE_MICROSECOND(R)
-   分秒 (R)
-   最小値
-   MIN_ROWS
-   モッド(R)
-   モード
-   修正する
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
-   ノキャッシュ
-   ノサイクル
-   ノードグループ
-   ノードID(R)
-   ノードステート(R)
-   NOMAXVALUE
-   公称値
-   非クラスター化
-   なし
-   ない(R)
-   ちょっと待ってください
-   NO_WRITE_TO_BINLOG (R)
-   NTH_VALUE (R ウィンドウ)
-   NTILE (R ウィンドウ)
-   NULL(R)
-   NULL
-   数値(R)
-   NVARCHAR

<a id="O" class="letter" href="#O">○</a>

-   オブ(R)
-   オフ
-   オフセット
-   OLTP_READ_ONLY
-   OLTP_READ_WRITE
-   OLTP_WRITE_ONLY
-   オン(R)
-   ON_DUPLICATE
-   オンライン
-   のみ
-   開ける
-   オプティミスティック(R)
-   オプティマイズ(R)
-   オプション(R)
-   オプション
-   オプションで (R)
-   または(R)
-   オーダー(R)
-   アウト(R)
-   アウター(R)
-   アウトファイル(R)
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
-   PASSWORD_LOCK_TIME
-   一時停止
-   パーセント
-   PERCENT_RANK (R ウィンドウ)
-   PER_DB
-   PER_TABLE
-   ペシミスティック(R)
-   配置 (S)
-   プラグイン
-   ポイント
-   ポリシー
-   前に
-   プレシジョン(R)
-   準備する
-   保存する
-   PRE_SPLIT_REGIONS
-   プライマリー(R)
-   特権
-   手順(R)
-   プロセス
-   プロセスリスト
-   プロフィール
-   プロフィール
-   プロキシ
-   ポンプ(R)
-   パージ

<a id="Q" class="letter" href="#Q">Q</a>

-   四半期
-   質問
-   クエリ
-   素早い

<a id="R" class="letter" href="#R">R</a>

-   部隊）
-   RANK (R-ウィンドウ)
-   RATE_LIMIT
-   読む(R)
-   リアル(R)
-   リビルド
-   回復する
-   リカーシブ(R)
-   冗長
-   参考資料(R)
-   正規表現(R)
-   地域(R)
-   リージョンズ(R)
-   リリース(R)
-   リロード
-   取り除く
-   リネーム(R)
-   再編成する
-   修理
-   リピート(R)
-   反復可能
-   リプレイス(R)
-   レプリカ
-   レプリカ
-   レプリケーション
-   要求(R)
-   必須
-   リソース
-   尊敬
-   再起動
-   復元する
-   復元
-   制限(R)
-   再開する
-   再利用
-   逆行する
-   リヴォーク(R)
-   右(R)
-   アールライク(R)
-   役割
-   ロールバック
-   巻き上げる
-   ルーティーン
-   ロウ(R)
-   ROW_COUNT
-   ROW_FORMAT
-   ROW_NUMBER (R ウィンドウ)
-   ROWS (R ウィンドウ)
-   Rツリー

<a id="S" class="letter" href="#S">S</a>

-   サンプル(R)
-   さん
-   セーブポイント
-   2番
-   SECOND_MICROSECOND(R)
-   SECONDARY_ENGINE
-   SECONDARY_LOAD
-   SECONDARY_UNLOAD
-   安全
-   セレクト(R)
-   SEND_CREDENTIALS_TO_TIKV
-   セパレーター
-   順序
-   シリアル
-   SERIALIZABLE
-   セッション
-   セット(R)
-   セトヴァル
-   SHARD_ROW_ID_BITS
-   共有
-   共有
-   ショー(R)
-   シャットダウン
-   署名入り
-   単純
-   スキップ
-   SKIP_SCHEMA_FILES
-   奴隷
-   遅い
-   スモールント(R)
-   スナップショット
-   いくつかの
-   ソース
-   スペーシャル(R)
-   スプリット(R)
-   SQL(R)
-   SQL_BIG_RESULT(R)
-   SQL_BUFFER_RESULT
-   SQL_CACHE
-   SQL_CALC_FOUND_ROWS(R)
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
-   SQL例外(R)
-   SQLSTATE(R)
-   SQL警告(R)
-   SSL(R)
-   始める
-   スターティング(R)
-   スタッツ(R)
-   STATS_AUTO_RECALC
-   STATS_BUCKETS (R)
-   STATS_COL_CHOICE
-   STATS_COL_LIST
-   STATS_EXTENDED (R)
-   STATS_HEALTHY(R)
-   STATS_HISTOGRAMS (R)
-   STATS_META(R)
-   STATS_OPTIONS
-   STATS_PERSISTENT
-   STATS_SAMPLE_PAGES
-   STATS_SAMPLE_RATE
-   状態
-   ストレージ
-   ストアド(R)
-   ストレートジョイン(R)
-   STRICT_FORMAT
-   主題
-   サブパーティション
-   サブパーティション
-   素晴らしい
-   スワップ
-   スイッチ
-   システム
-   システム時刻

<a id="T" class="letter" href="#T">T</a>

-   テーブル(R)
-   テーブル
-   テーブルサンプル(R)
-   テーブルスペース
-   TABLE_CHECKSUM
-   一時的
-   誘惑しやすい
-   終了(R)
-   TEXT
-   よりも
-   ザエン(R)
-   TIDB(R)
-   TiDB_CURRENT_TSO(R)
-   ティフラッシュ(R)
-   TIKV_IMPORTER
-   時間
-   タイムスタンプ
-   タイニーブロブ(R)
-   タイニント(R)
-   タイニーテキスト(R)
-   TO(R)
-   TOKEN_ISSUER
-   トップン(R)
-   TPCC
-   TPCH_10
-   痕跡
-   伝統的
-   トレーリング(R)
-   取引
-   トリガー(R)
-   トリガー
-   TRUE(R)
-   切り詰める
-   TTL
-   TTL_ENABLE
-   TTL_JOB_INTERVAL
-   タイプ

<a id="U" class="letter" href="#U">U</a>

-   無制限
-   コミットされていない
-   未定義
-   ユニコード
-   ユニオン(R)
-   ユニーク(R)
-   未知
-   アンロック(R)
-   サインなし(R)
-   (R)まで
-   アップデート(R)
-   使用法(R)
-   ユーズ(R)
-   ユーザー
-   (R)を使用する
-   UTC_DATE (R)
-   UTC_TIME(R)
-   UTC_TIMESTAMP(R)

<a id="V" class="letter" href="#V">V</a>

-   検証
-   価値
-   バリューズ(R)
-   ヴァービナリー(R)
-   VARCHAR(R)
-   ヴァーキャラクター(R)
-   変数
-   ヴァリアント(R)
-   ビュー
-   バーチャル(R)
-   見える

<a id="W" class="letter" href="#W">W</a>

-   待って
-   警告
-   週
-   WEIGHT_STRING
-   いつ(R)
-   どこに(R)
-   ながら(R)
-   幅(R)
-   ウィンドウ (R ウィンドウ)
-   (R)付き
-   それなし
-   仕事量
-   ライト(R)

<a id="X" class="letter" href="#X">バツ</a>

-   X509
-   XOR(R)

<a id="Y" class="letter" href="#Y">Y</a>

-   年
-   YEAR_MONTH (R)

<a id="Z" class="letter" href="#Z">Z</a>

-   ゼロフィル(R)
