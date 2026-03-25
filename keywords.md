---
title: Keywords
summary: キーワードと予約語
---

# キーワード {#keywords}

この記事では、TiDBのキーワード、予約語と非予約語の違いを紹介し、クエリに使用するすべてのキーワードをまとめます。

キーワードとは、SQL文において特別な意味を持つ単語のことで、例えば[`SELECT`](/sql-statements/sql-statement-select.md)などが挙げ[`UPDATE`](/sql-statements/sql-statement-update.md)ます。これらの[`DELETE`](/sql-statements/sql-statement-delete.md)の中には、識別子として直接使用できるものがあり、これらは**非予約キーワード**と呼ばれます。一方、識別子として使用する前に特別な処理が必要なものもあり、これらは**予約キーワード**と呼ばれます。

予約語を識別子として使用するには、バッククォートで囲む必要があります`` ` `` :

```sql
CREATE TABLE select (a INT);
```

    ERROR 1105 (HY000): line 0 column 19 near " (a INT)" (total length 27)

```sql
CREATE TABLE `select` (a INT);
```

    Query OK, 0 rows affected (0.09 sec)

予約語ではないキーワードはバッククォートを必要としません。例えば、 `BEGIN`や`END`は、次の文で識別子として使用できます。

```sql
CREATE TABLE `select` (BEGIN int, END int);
```

    Query OK, 0 rows affected (0.09 sec)

特別な場合として、予約語を区切り文字`.`とともに使用する場合は、バッククォートは不要です。

```sql
CREATE TABLE test.select (BEGIN int, END int);
```

    Query OK, 0 rows affected (0.08 sec)

バージョン7.5.3および7.6.0以降、TiDBは[`INFORMATION_SCHEMA.KEYWORDS`](/information-schema/information-schema-keywords.md)テーブルにキーワードの完全なリストを提供します。

システム変数[`tidb_enable_window_function`](/system-variables.md#tidb_enable_window_function)を使用すると、構文ツリー内で[ウィンドウ関数](/functions-and-operators/window-functions.md)キーワードが有効になるかどうかを制御できます`tidb_enable_window_function`を`OFF`に設定すると、ウィンドウ関数内の単語はキーワードとして扱われなくなります。

## キーワードリスト {#keyword-list}

以下のリストは、TiDB のキーワードを示しています。予約語には`(R)`が付いています。3 [ウィンドウ関数](/functions-and-operators/window-functions.md)予約語には`(R-Window)`が付いています。

<TabsPanel letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ" />

<a id="A" class="letter" href="#A">A</a>

-   アカウント
-   アクション
-   追加（R）
-   管理者
-   アドバイス
-   後
-   親和性
-   に対して
-   前
-   アルゴリズム
-   すべて（R）
-   ALTER (R)
-   いつも
-   ANALYZE (R)
-   および（R）
-   どれでも
-   適用する
-   アレイ（R）
-   AS（R）
-   ASC（R）
-   ASCII
-   属性
-   属性
-   AUTO_ID_CACHE
-   自動インクリメント
-   自動乱数
-   自動乱数ベース
-   平均
-   平均行長

<a id="B" class="letter" href="#B">B</a>

-   バックエンド
-   バックアップ
-   バックアップ
-   バッチ
-   BDR
-   始める
-   ベルヌーイ
-   間（R）
-   BIGINT (R)
-   バイナリ（R）
-   バインディング
-   バインディング
-   バインディングキャッシュ
-   バイナリログ
-   少し
-   BLOB（R）
-   ブロック
-   ブール
-   ブール値
-   両方（R）
-   BTREE
-   バケツ
-   ビルトイン
-   BY (R)
-   バイト

<a id="C" class="letter" href="#C">C</a>

-   キャッシュ
-   校正
-   コール（R）
-   キャンセル
-   捕獲
-   基数
-   カスケード（R）
-   カスケード
-   ケース（R）
-   因果関係
-   鎖
-   チェンジ（R）
-   CHAR (R)
-   キャラクター（R）
-   文字セット
-   チェック（R）
-   チェックポイント
-   チェックサム
-   チェックサム同時実行
-   暗号
-   掃除
-   クライアント
-   クライアントエラーの概要
-   近い
-   クラスタ
-   クラスター化された
-   CMSKETCH
-   合体する
-   COLLATE (R)
-   照合
-   列（右）
-   列形式
-   列統計情報の使用状況
-   コラム
-   コメント
-   専念
-   コミット済み
-   コンパクト
-   圧縮
-   圧縮
-   圧縮レベル
-   圧縮タイプ
-   並行処理
-   設定
-   繋がり
-   一貫性
-   一貫性のある
-   制約（R）
-   コンテクスト
-   続ける（R）
-   CONVERT (R)
-   相関
-   CPU
-   CREATE (R)
-   クロス（右）
-   CSV_バックスラッシュ_エスケープ
-   CSV_DELIMITER
-   CSVヘッダー
-   CSV_NOT_NULL
-   CSV_NULL
-   CSV区切り文字
-   CSV_最後の区切り文字を削除
-   CUME_DIST (Rウィンドウ)
-   現在
-   CURRENT_DATE (R)
-   現在の役割 (R)
-   現在時刻 (R)
-   CURRENT_TIMESTAMP (R)
-   現在のユーザー (R)
-   カーソル（右）
-   サイクル

<a id="D" class="letter" href="#D">D</a>

-   データ
-   データベース（R）
-   データベース（R）
-   日付
-   日時
-   日
-   日時（R）
-   日数マイクロ秒 (R)
-   日_分 (R)
-   DAY_SECOND (R)
-   DDL
-   割り当て解除
-   十進法（R）
-   宣言する
-   デフォルト（R）
-   定義者
-   キー書き込み遅延
-   遅延（R）
-   削除（R）
-   DENSE_RANK (Rウィンドウ)
-   依存
-   深さ
-   説明（R）
-   説明（R）
-   ダイジェスト
-   ディレクトリ
-   無効にする
-   無効
-   破棄
-   ディスク
-   独特な（R）
-   ディスティンクトロウ（共和党）
-   配布する
-   分布
-   分布
-   DIV（R）
-   する
-   ダブル（R）
-   排水口
-   ドロップ（R）
-   ドライ
-   デュアル（R）
-   重複
-   動的

<a id="E" class="letter" href="#E">E</a>

-   それ以外の場合（R）
-   ELSEIF (R)
-   有効にする
-   有効
-   同封（R）
-   暗号化
-   暗号化キーファイル
-   暗号化方式
-   終わり
-   強制
-   エンジン
-   エンジン
-   列挙型
-   エラー
-   エラー
-   逃げる
-   脱出（R指定）
-   イベント
-   イベント
-   進化
-   ただし（R）
-   交換
-   エクスクルーシブ
-   実行する
-   存在する（R）
-   終了（R）
-   拡大
-   期限切れ
-   EXPLAIN (R)
-   拡張版

<a id="F" class="letter" href="#F">F</a>

-   ログイン試行失敗
-   偽（R）
-   欠陥
-   FETCH（R）
-   分野
-   ファイル
-   初め
-   最初の値（Rウィンドウ）
-   修理済み
-   フロート（R）
-   FLOAT4 (R)
-   FLOAT8 (R)
-   フラッシュ
-   続く
-   (R)のために
-   フォース（R）
-   外国語（R）
-   形式
-   見つかった
-   (R)より
-   満杯
-   全文（R）
-   関数

<a id="G" class="letter" href="#G">G</a>

-   一般的な
-   生成（R）
-   グローバル
-   グラント（共和党）
-   助成金
-   グループ（R）
-   グループ（Rウィンドウ）

<a id="H" class="letter" href="#H">H</a>

-   ハンドラ
-   ハッシュ
-   持つ（R）
-   ヘルプ
-   高優先度（R）
-   ヒストグラム
-   飛行中のヒストグラム
-   歴史
-   ホスト
-   時間
-   時・秒 (R)
-   時分（R）
-   時_秒 (R)
-   低酸素

<a id="I" class="letter" href="#I">私</a>

-   特定された
-   IF (R)
-   無視（R）
-   IGNORE_STATS
-   ILIKE (R)
-   輸入
-   輸入品
-   IN (R)
-   インクリメント
-   増分
-   インデックス（R）
-   索引
-   INFILE (R)
-   内側（右）
-   INOUT (R)
-   挿入（R）
-   挿入方法
-   実例
-   INT (R)
-   INT1 (R)
-   INT2 (R)
-   INT3 (R)
-   INT4 (R)
-   INT8 (R)
-   INTEGER (R)
-   交差（R）
-   間隔（R）
-   （右へ）
-   見えない
-   呼び出し元
-   IO
-   IPC
-   IS（R）
-   分離
-   発行者
-   ITERATE (R)

<a id="J" class="letter" href="#J">J</a>

-   仕事
-   求人情報
-   参加する（R）
-   JSON

<a id="K" class="letter" href="#K">K</a>

-   キー（R）
-   キーズ（R）
-   キーブロックサイズ
-   キル（R）

<a id="L" class="letter" href="#L">L</a>

-   ラベル
-   LAG（Rウィンドウ）
-   言語
-   最後
-   最終バックアップ
-   最終値（Rウィンドウ）
-   ラストバル
-   リード（右窓）
-   リーディング（R）
-   退出（右）
-   左（右）
-   少ない
-   レベル
-   いいね！(R)
-   制限（R）
-   リニア（R）
-   ラインズ（R）
-   リスト
-   負荷（R）
-   ロード統計
-   地元
-   現地時間（R）
-   ローカルタイムスタンプ (R)
-   位置
-   ロック（R）
-   ロック済み
-   ログ
-   ロング（R）
-   ロングブロブ（R）
-   ロングテキスト(R)
-   優先度低（R）

<a id="M" class="letter" href="#M">M</a>

-   マスキング
-   マスター
-   マッチ（R）
-   最大値（R）
-   1時間あたりの最大接続数
-   MAX_IDXNUM
-   最大分数
-   1時間あたりの最大クエリ数
-   最大行数
-   1時間あたりの最大更新回数
-   最大ユーザー接続数
-   MB
-   MEDIUMBLOB (R)
-   ミディアミント（R）
-   中文テキスト（R）
-   メンバー
-   メモリ
-   マージ
-   マイクロ秒
-   ミドルネット（右）
-   分
-   分_マイクロ秒 (R)
-   分_秒 (R)
-   最小値
-   最小行数
-   MOD (R)
-   モード
-   修正する
-   モニター
-   月

<a id="N" class="letter" href="#N">N</a>

-   名前
-   全国
-   ナチュラル（R）
-   NCHAR
-   一度もない
-   次
-   ネクストバル
-   いいえ
-   キャッシュなし
-   ノーサイクル
-   ノードグループ
-   ノードID
-   ノード状態
-   最大値なし
-   名目値
-   非クラスター化
-   なし
-   （R）ではありません
-   待って
-   NO_WRITE_TO_BINLOG (R)
-   NTH_VALUE (R-Window)
-   タイル（Rウィンドウ）
-   NULL（R）
-   NULL
-   数値（R）
-   NVARCHAR

<a id="O" class="letter" href="#O">O</a>

-   （R）の
-   オフ
-   オフセット
-   OLTP_読み取り専用
-   OLTP_READ_WRITE
-   OLTP_書き込み専用
-   オン（R）
-   重複なし
-   オンライン
-   のみ
-   開ける
-   楽観的
-   オプティマイズ（R）
-   オプション（R）
-   オプション
-   オプション（R）
-   または（R）
-   命令（R）
-   アウト（R）
-   外側（右）
-   OUTFILE (R)
-   オーバー（Rウィンドウ）

<a id="P" class="letter" href="#P">P</a>

-   パックキー
-   ページ
-   パーサー
-   部分的
-   パーティション（R）
-   パーティショニング
-   パーティション
-   パスワード
-   パスワードロック時間
-   一時停止
-   パーセント
-   パーセントランク（Rウィンドウ）
-   PER_DB
-   PER_TABLE
-   悲観的
-   プラグイン
-   ポイント
-   ポリシー
-   ポリシー
-   前の
-   プレシジョン（R）
-   準備する
-   保存する
-   分割前リージョン
-   予備選挙（共和党）
-   特権
-   手順（R）
-   プロセス
-   プロセスリスト
-   プロフィール
-   プロフィール
-   プロキシ
-   ポンプ
-   パージ

<a id="Q" class="letter" href="#Q">Q</a>

-   四半期
-   お問い合わせ
-   クエリ
-   素早い

<a id="R" class="letter" href="#R">R</a>

-   レンジ（R）
-   ランク（Rウィンドウ）
-   レート制限
-   読む（R）
-   リアル（R）
-   再建する
-   推薦する
-   回復する
-   再帰的 (R)
-   重複
-   参考文献（R）
-   正規表現（R）
-   地域
-   地域
-   リリース（R）
-   リロード
-   取り除く
-   名前変更（R）
-   再編成する
-   修理
-   繰り返し（R）
-   繰り返し可能
-   置換（R）
-   レプリカ
-   レプリカ
-   複製
-   要求する（R）
-   必須
-   リセット
-   リソース
-   尊敬
-   再起動
-   復元する
-   修復する
-   制限（R）
-   再開する
-   再利用
-   逆行する
-   取り消す（R）
-   右（R）
-   RLIKE (R)
-   役割
-   ロールバック
-   ロールアップ
-   ルーティーン
-   ROW (R)
-   行数
-   行フォーマット
-   行番号（Rウィンドウ）
-   行（右ウィンドウ）
-   RTREE
-   ルール
-   走る

<a id="S" class="letter" href="#S">S</a>

-   サンプルレート
-   サンプル
-   SAN
-   セーブポイント
-   2番
-   秒マイクロ秒 (R)
-   中等教育
-   セカンダリーエンジン
-   セカンダリーロード
-   二次荷降ろし
-   安全
-   選択（R）
-   TIKVに認証情報を送信
-   分離器
-   順序
-   シリアル
-   SERIALIZABLE
-   セッション
-   セッション状態
-   セット（R）
-   SETVAL
-   SHARD_ROW_ID_BITS
-   共有
-   共有済み
-   ショー（R）
-   シャットダウン
-   署名済み
-   単純
-   スキップ
-   スキーマファイルをスキップする
-   奴隷
-   遅い
-   スモールイント（R）
-   スナップショット
-   いくつかの
-   ソース
-   SPATIAL (R)
-   スプリット
-   SQL（R）
-   SQL_BIG_RESULT (R)
-   SQL_BUFFER_RESULT
-   SQL_CACHE
-   SQL_CALC_FOUND_ROWS (R)
-   SQL_NO_CACHE
-   SQL_SMALL_RESULT (R)
-   SQL_TSI_DAY
-   SQL_TSI_HOUR
-   SQL_TSI_分
-   SQL_TSI_月
-   SQL_TSI_四半期
-   SQL_TSI_SECOND
-   SQL_TSI_WEEK
-   SQL_TSI_YEAR
-   SQLEXCEPTION (R)
-   SQLSTATE (R)
-   SQL警告 (R)
-   SSL（R）
-   始める
-   スタート（R）
-   統計
-   統計
-   統計_自動再計算
-   統計_バケツ
-   統計_色選択
-   統計列リスト
-   統計情報（拡張版）
-   統計_健康
-   統計ヒストグラム
-   統計ロック済み
-   統計情報
-   統計オプション
-   統計情報_永続的
-   統計サンプルページ
-   統計サンプル率
-   統計トップ
-   状態
-   ストレージ
-   保存済み（R）
-   STRAIGHT_JOIN (R)
-   厳密な形式
-   主題
-   サブパーティション
-   サブパーティション
-   素晴らしい
-   スワップ
-   スイッチ
-   システム
-   システム時刻

<a id="T" class="letter" href="#T">T</a>

-   表（R）
-   表
-   テーブルサンプル（R）
-   テーブルスペース
-   テーブルチェックサム
-   一時的
-   一時的なもの
-   終了（R）
-   TEXT
-   よりも
-   それから（R）
-   TIDB
-   TIDB_CURRENT_TSO (R)
-   ティフラッシュ
-   TIKV_IMPORTER
-   時間
-   タイムアウト
-   タイムスタンプ
-   タイニーブロブ（R）
-   TINYINT (R)
-   TINYTEXT (R)
-   （R）へ
-   トークン発行者
-   トポン
-   TPCC
-   TPCH_10
-   トレース
-   伝統的
-   トレーリング（R）
-   取引
-   トリガー（R）
-   トリガー
-   真（R）
-   切り捨てる
-   TSO
-   TTL
-   TTL_ENABLE
-   TTL_JOB_INTERVAL
-   タイプ

<a id="U" class="letter" href="#U">U</a>

-   無限
-   未決定
-   未定義
-   ユニコード
-   ユニオン（共和党）
-   ユニーク（R）
-   未知
-   ロック解除（R）
-   未設定
-   署名なし（R）
-   まで（R）
-   アップデート（R）
-   USAGE (R)
-   USE (R)
-   ユーザー
-   使用（R）
-   UTC_DATE (R)
-   UTC_TIME (R)
-   UTC_TIMESTAMP (R)

<a id="V" class="letter" href="#V">V</a>

-   検証
-   価値
-   値（R）
-   VARBINARY (R)
-   VARCHAR (R)
-   VARCHARACTER (R)
-   変数
-   可変（R）
-   ベクター
-   ビュー
-   バーチャル（R）
-   見える

<a id="W" class="letter" href="#W">W</a>

-   待って
-   WAIT_TIFLASH_READY
-   警告
-   週
-   重量文字列
-   （R）
-   場所（R）
-   一方（R）
-   幅
-   ウィンドウ（Rウィンドウ）
-   （R）付き
-   WITH_SYS_TABLE
-   それなし
-   作業負荷
-   書き込み（R）

<a id="X" class="letter" href="#X">X</a>

-   X509
-   XOR（R）

<a id="Y" class="letter" href="#Y">Y</a>

-   年
-   年月（R）

<a id="Z" class="letter" href="#Z">Z</a>

-   ゼロフィル（R）
