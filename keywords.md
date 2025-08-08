---
title: Keywords
summary: キーワードと予約語
---

# キーワード {#keywords}

この記事では、TiDB のキーワード、予約語と非予約語の違いを紹介し、クエリのすべてのキーワードをまとめます。

キーワードとは、SQL文において特別な意味を持つ単語の[`UPDATE`](/sql-statements/sql-statement-update.md) [`SELECT`](/sql-statements/sql-statement-select.md) [`DELETE`](/sql-statements/sql-statement-delete.md)キーワードの中には、直接識別子として使用できるものもあり、これらは**非予約キーワード**と呼ばれます。また、識別子として使用する前に特別な処理が必要なものもあり、これらは**予約キーワード**と呼ばれます。

予約語を識別子として使用するには、バッククォート`` ` ``で囲む必要があります。

```sql
CREATE TABLE select (a INT);
```

    ERROR 1105 (HY000): line 0 column 19 near " (a INT)" (total length 27)

```sql
CREATE TABLE `select` (a INT);
```

    Query OK, 0 rows affected (0.09 sec)

予約されていないキーワードにはバックティックは必要ありません`BEGIN`や`END`など)。これらは次のステートメントで識別子として正常に使用できます。

```sql
CREATE TABLE `select` (BEGIN int, END int);
```

    Query OK, 0 rows affected (0.09 sec)

特別なケースでは、予約キーワードを`.`区切り文字とともに使用する場合はバッククォートは必要ありません。

```sql
CREATE TABLE test.select (BEGIN int, END int);
```

    Query OK, 0 rows affected (0.08 sec)

v7.5.3 および v7.6.0 以降、TiDB は[`INFORMATION_SCHEMA.KEYWORDS`](/information-schema/information-schema-keywords.md)テーブルにキーワードの完全なリストを提供します。

システム変数[`tidb_enable_window_function`](/system-variables.md#tidb_enable_window_function)使用すると、 [ウィンドウ関数](/functions-and-operators/window-functions.md)内のキーワードが構文ツリーで有効になるかどうかを制御できます。 `tidb_enable_window_function`を`OFF`に設定すると、ウィンドウ関数内の単語はキーワードとして扱われなくなります。

## キーワードリスト {#keyword-list}

以下のリストはTiDBのキーワードを示しています。予約語には`(R)`が付きます。3 [ウィンドウ関数](/functions-and-operators/window-functions.md)予約語には`(R-Window)`が付きます。

<TabsPanel letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ" />

<a id="A" class="letter" href="#A">あ</a>

-   アカウント
-   アクション
-   追加（R）
-   管理者
-   アドバイス
-   後
-   に対して
-   前
-   アルゴリズム
-   オール（R）
-   アルター（R）
-   いつも
-   分析（R）
-   そして（R）
-   どれでも
-   適用する
-   アレイ（R）
-   AS（R）
-   ASC（R）
-   アスキー
-   属性
-   属性
-   自動IDキャッシュ
-   自動インクリメント
-   自動ランダム
-   自動ランダムベース
-   平均
-   平均行の長さ

<a id="B" class="letter" href="#B">B</a>

-   バックエンド
-   バックアップ
-   バックアップ
-   バッチ
-   BDR
-   始める
-   ベルヌーイ
-   間（R）
-   ビッグイント（R）
-   バイナリ（R）
-   拘束力
-   バインディング
-   バインドキャッシュ
-   ビンログ
-   少し
-   ブロブ（R）
-   ブロック
-   ブール
-   ブール値
-   両方（R）
-   Bツリー
-   バケツ
-   ビルトイン
-   BY（R）
-   バイト

<a id="C" class="letter" href="#C">C</a>

-   キャッシュ
-   調整
-   コール（R）
-   キャンセル
-   捕獲
-   カーディナリティ
-   カスケード（R）
-   カスケード
-   ケース（R）
-   因果関係
-   鎖
-   チェンジ（R）
-   CHAR（R）
-   キャラクター（R）
-   文字セット
-   チェック（R）
-   チェックポイント
-   チェックサム
-   CHECKSUM_CONCURRENCY
-   暗号
-   掃除
-   クライアント
-   クライアントエラーの概要
-   近い
-   クラスタ
-   クラスター化された
-   CMスケッチ
-   合体
-   収集（R）
-   照合
-   コラム（右）
-   列フォーマット
-   列統計使用状況
-   コラム
-   コメント
-   専念
-   コミット
-   コンパクト
-   圧縮された
-   圧縮
-   圧縮レベル
-   圧縮タイプ
-   同時実行
-   設定
-   繋がり
-   一貫性
-   一貫性のある
-   制約（R）
-   コンテクスト
-   続行（R）
-   変換（R）
-   相関
-   CPU
-   クリエイト（R）
-   クロス（R）
-   CSV_バックスラッシュ_エスケープ
-   CSV_DELIMITER
-   CSV_ヘッダー
-   CSV_NOT_NULL
-   CSV_NULL
-   CSV_セパレーター
-   CSV_TRIM_LAST_SEPARATORS
-   CUME_DIST (Rウィンドウ)
-   現在
-   現在の日付（R）
-   現在の役割（R）
-   現在の時刻（R）
-   CURRENT_TIMESTAMP (R)
-   現在のユーザー (R)
-   カーソル（R）
-   サイクル

<a id="D" class="letter" href="#D">D</a>

-   データ
-   データベース（R）
-   データベース（R）
-   日付
-   日時
-   日
-   曜日_時間（R）
-   デイ_マイクロセカンド（R）
-   曜日_分（R）
-   DAY_SECOND（R）
-   DDL
-   割り当て解除
-   小数点（R）
-   宣言する
-   デフォルト（R）
-   定義者
-   DELAY_KEY_WRITE
-   遅延（R）
-   削除（R）
-   DENSE_RANK (Rウィンドウ)
-   依存
-   深さ
-   説明（R）
-   記述する（R）
-   ダイジェスト
-   ディレクトリ
-   無効にする
-   無効
-   破棄
-   ディスク
-   ディスティンクト（R）
-   ディスティンクトロウ（R）
-   DIV（右）
-   する
-   ダブル（R）
-   ドレイナー
-   ドロップ（R）
-   ドライ
-   デュアル（R）
-   重複
-   動的

<a id="E" class="letter" href="#E">E</a>

-   そうでなければ（R）
-   エルセイフ（R）
-   有効にする
-   有効
-   封入（R）
-   暗号化
-   暗号化キーファイル
-   暗号化方法
-   終わり
-   強制執行
-   エンジン
-   エンジン
-   列挙型
-   エラー
-   エラー
-   逃げる
-   エスケープド（R）
-   イベント
-   イベント
-   進化
-   除く（R）
-   交換
-   エクスクルーシブ
-   実行する
-   存在する（R）
-   出口（右）
-   拡大
-   期限切れ
-   EXPLAIN（R）
-   拡張

<a id="F" class="letter" href="#F">F</a>

-   ログイン試行失敗
-   誤り（R）
-   欠陥
-   フェッチ（R）
-   フィールド
-   ファイル
-   初め
-   FIRST_VALUE (Rウィンドウ)
-   修理済み
-   フロート（R）
-   フロート4（R）
-   フロート8（R）
-   フラッシュ
-   続く
-   賛成（R）
-   フォース（R）
-   外国（R）
-   形式
-   見つかった
-   （R）より
-   満杯
-   FULLTEXT (R)
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
-   時間_マイクロ秒（R）
-   時_分（R）
-   時間_秒（R）
-   ヒポ

<a id="I" class="letter" href="#I">私</a>

-   特定された
-   IF（R）
-   無視（R）
-   統計を無視
-   アイライク（R）
-   輸入
-   輸入品
-   IN（R）
-   インクリメント
-   増分
-   インデックス（R）
-   インデックス
-   インファイル（R）
-   インナー（右）
-   INOUT（右）
-   インサート（R）
-   挿入メソッド
-   実例
-   INT（R）
-   INT1（R）
-   INT2（R）
-   INT3（R）
-   INT4（R）
-   INT8（R）
-   整数（R）
-   インターセクト（R）
-   インターバル（R）
-   イントゥ（R）
-   見えない
-   召喚者
-   IO
-   IPC
-   IS（R）
-   分離
-   発行者
-   反復（R）

<a id="J" class="letter" href="#J">J</a>

-   仕事
-   求人
-   参加（R）
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
-   LAST_VALUE (Rウィンドウ)
-   ラストバル
-   LEAD（Rウィンドウ）
-   リーディング（右）
-   退出（R）
-   左（右）
-   少ない
-   レベル
-   いいね（R）
-   リミット（R）
-   リニア（R）
-   ラインズ（R）
-   リスト
-   ロード（R）
-   ロード統計
-   地元
-   現地時間（R）
-   ローカルタイムスタンプ (R)
-   位置
-   ロック（R）
-   ロック済み
-   ログ
-   ロング（右）
-   ロングブロブ（R）
-   ロングテキスト（R）
-   低優先度（R）

<a id="M" class="letter" href="#M">M</a>

-   マスター
-   マッチ（R）
-   マックスバリュー（R）
-   1時間あたりの最大接続数
-   MAX_IDXNUM
-   最大分
-   1時間あたりの最大クエリ数
-   最大行数
-   1時間あたりの最大更新回数
-   最大ユーザー接続数
-   MB
-   ミディアムブロブ（R）
-   ミディアムミント（R）
-   中テキスト（R）
-   メンバー
-   メモリ
-   マージ
-   マイクロ秒
-   ミドルイント（R）
-   分
-   分_マイクロ秒（R）
-   分_秒（R）
-   最小値
-   MIN_ROWS
-   MOD（R）
-   モード
-   修正する
-   月

<a id="N" class="letter" href="#N">北</a>

-   名前
-   全国
-   ナチュラル（R）
-   ンチャー
-   一度もない
-   次
-   ネクストバル
-   いいえ
-   ノキャッシュ
-   ノーサイクル
-   ノードグループ
-   ノードID
-   ノード状態
-   最大値なし
-   公称値
-   非クラスター化
-   なし
-   いいえ（R）
-   待ってください
-   バイナリログへの書き込みなし (R)
-   NTH_VALUE (Rウィンドウ)
-   NTILE（Rウィンドウ）
-   ヌル（R）
-   ヌル
-   数値（R）
-   ネヴァルチャー

<a id="O" class="letter" href="#O">お</a>

-   の（右）
-   オフ
-   オフセット
-   OLTP_読み取り専用
-   OLTP_読み取り_書き込み
-   OLTP_書き込み専用
-   オン（R）
-   複製オン
-   オンライン
-   のみ
-   開ける
-   楽観的
-   最適化（R）
-   オプション（R）
-   オプション
-   オプション（R）
-   または（R）
-   オーダー（R）
-   アウト（右）
-   アウター（右）
-   アウトファイル（R）
-   OVER（右ウィンドウ）

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
-   PERCENT_RANK (Rウィンドウ)
-   PER_DB
-   テーブルごと
-   悲観的
-   プラグイン
-   ポイント
-   ポリシー
-   前項
-   プレシジョン（R）
-   準備する
-   保存する
-   事前分割領域
-   プライマリー（R）
-   特権
-   手順（R）
-   プロセス
-   プロセスリスト
-   プロフィール
-   プロフィール
-   プロキシ
-   ポンプ
-   パージ

<a id="Q" class="letter" href="#Q">質問</a>

-   四半期
-   クエリ
-   クエリ
-   素早い

<a id="R" class="letter" href="#R">R</a>

-   レンジ（R）
-   RANK（Rウィンドウ）
-   レート制限
-   読む（R）
-   リアル（R）
-   再構築
-   推薦する
-   回復する
-   再帰的（R）
-   冗長
-   参考文献（R）
-   正規表現（R）
-   地域
-   地域
-   リリース（R）
-   リロード
-   取り除く
-   名前を変更 (R)
-   再編成
-   修理
-   リピート（R）
-   繰り返し可能
-   交換（R）
-   レプリカ
-   レプリカ
-   複製
-   必要 (R)
-   必須
-   リセット
-   リソース
-   尊敬
-   再起動
-   復元する
-   復元
-   制限（R）
-   再開する
-   再利用
-   逆行する
-   取り消し（R）
-   右（R）
-   RLIKE（R）
-   役割
-   ロールバック
-   ロールアップ
-   ルーティーン
-   ROW（右）
-   行数
-   行フォーマット
-   ROW_NUMBER (Rウィンドウ)
-   ROWS (Rウィンドウ)
-   RTREE
-   走る

<a id="S" class="letter" href="#S">S</a>

-   サンプルレート
-   サンプル
-   サン
-   セーブポイント
-   2番
-   秒_マイクロ秒 (R)
-   セカンダリー
-   セカンダリエンジン
-   セカンダリロード
-   セカンダリアンロード
-   安全
-   セレクト（R）
-   TIKVに資格情報を送信する
-   セパレーター
-   順序
-   シリアル
-   SERIALIZABLE
-   セッション
-   セッション状態
-   セット（R）
-   SETVAL
-   シャード行IDビット
-   共有
-   共有
-   ショー（R）
-   シャットダウン
-   署名
-   単純
-   スキップ
-   SKIP_SCHEMA_FILES
-   奴隷
-   遅い
-   スモールイント（R）
-   スナップショット
-   いくつかの
-   ソース
-   空間（R）
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
-   SQL_TSI_MONTH
-   SQL_TSI_QUARTER
-   SQL_TSI_SECOND
-   SQL_TSI_WEEK
-   SQL_TSI_YEAR
-   SQL例外 (R)
-   SQL状態 (R)
-   SQL警告 (R)
-   SSL（R）
-   始める
-   スターティング（R）
-   統計
-   統計
-   STATS_AUTO_RECALC
-   統計バケット
-   統計_列_選択
-   統計列リスト
-   統計_拡張
-   健康状態
-   統計ヒストグラム
-   統計がロックされています
-   統計メタ
-   統計オプション
-   統計_永続性
-   統計サンプルページ
-   統計サンプルレート
-   統計_トップ
-   状態
-   ストレージ
-   保管済み（R）
-   ストレート結合（R）
-   厳格なフォーマット
-   主題
-   サブパーティション
-   サブパーティション
-   素晴らしい
-   スワップ
-   スイッチ
-   システム
-   システム時間

<a id="T" class="letter" href="#T">T</a>

-   表（R）
-   テーブル
-   テーブルサンプル（R）
-   テーブルスペース
-   テーブルチェックサム
-   一時的
-   誘惑的
-   終了（R）
-   TEXT
-   よりも
-   それから（R）
-   TIDB
-   TIDB_CURRENT_TSO (R)
-   ティフラッシュ
-   TIKV_IMPORTER
-   時間
-   タイムスタンプ
-   タイニーブロブ（R）
-   タイニーイント（R）
-   タイニーテキスト（R）
-   宛先（右）
-   トークン発行者
-   トップン
-   TPCC
-   TPCH_10
-   トレース
-   伝統的
-   トレーリング（R）
-   取引
-   トリガー（R）
-   トリガー
-   トゥルー（R）
-   切り捨て
-   TSO
-   TTL
-   TTL_ENABLE
-   TTL_ジョブ間隔
-   タイプ

<a id="U" class="letter" href="#U">あなた</a>

-   無制限
-   未確定
-   未定義
-   ユニコード
-   ユニオン（R）
-   ユニーク（R）
-   未知
-   アンロック（R）
-   設定解除
-   署名なし（R）
-   アンティル（R）
-   アップデート（R）
-   使用法（R）
-   使用（R）
-   ユーザー
-   (R) の使用
-   UTC_DATE (R)
-   UTC_TIME（R）
-   UTC_TIMESTAMP (R)

<a id="V" class="letter" href="#V">V</a>

-   検証
-   価値
-   価値観（R）
-   ヴァービナリー（R）
-   ヴァルチャー（R）
-   ヴァーチャルキャラクター（R）
-   変数
-   変化する（R）
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
-   いつ（R）
-   どこ（R）
-   （R）の間
-   幅
-   WINDOW（R-ウィンドウ）
-   ウィズ（R）
-   WITH_SYS_TABLE
-   それなし
-   ワークロード
-   書き込み（R）

<a id="X" class="letter" href="#X">X</a>

-   X509
-   XOR（R）

<a id="Y" class="letter" href="#Y">Y</a>

-   年
-   年_月（R）

<a id="Z" class="letter" href="#Z">Z</a>

-   ゼロフィル（R）
