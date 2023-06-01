---
title: TiDB 6.1.2 Release Notes
---

# TiDB 6.1.2 リリースノート {#tidb-6-1-2-release-notes}

発売日：2022年10月24日

TiDB バージョン: 6.1.2

クイックアクセス: [<a href="https://docs.pingcap.com/tidb/v6.1/quick-start-with-tidb">クイックスタート</a>](https://docs.pingcap.com/tidb/v6.1/quick-start-with-tidb) | [<a href="https://docs.pingcap.com/tidb/v6.1/production-deployment-using-tiup">本番展開</a>](https://docs.pingcap.com/tidb/v6.1/production-deployment-using-tiup) | [<a href="https://www.pingcap.com/download/?version=v6.1.2#version-list">インストールパッケージ</a>](https://www.pingcap.com/download/?version=v6.1.2#version-list)

## 改善点 {#improvements}

-   TiDB

    -   1 つのテーブルで配置ルールとTiFlashレプリカを同時に設定できるようにします[<a href="https://github.com/pingcap/tidb/issues/37171">#37171</a>](https://github.com/pingcap/tidb/issues/37171) @ [<a href="https://github.com/lcwangchao">ルクワンチャオ</a>](https://github.com/lcwangchao)

-   TiKV

    -   1 つのピアが到達不能になった後にRaftstore が大量のメッセージをブロードキャストすることを避けるための`unreachable_backoff`項目の設定をサポート[<a href="https://github.com/tikv/tikv/issues/13054">#13054</a>](https://github.com/tikv/tikv/issues/13054) @ [<a href="https://github.com/5kbpers">5kbps</a>](https://github.com/5kbpers)
    -   RocksDB 書き込み停止設定をフロー制御しきい値[<a href="https://github.com/tikv/tikv/issues/13467">#13467</a>](https://github.com/tikv/tikv/issues/13467) @ [<a href="https://github.com/tabokie">タボキー</a>](https://github.com/tabokie)よりも小さい値に構成することをサポート

-   ツール

    -   TiDB Lightning

        -   チェックサム中に再試行可能なエラーを追加して堅牢性を向上[<a href="https://github.com/pingcap/tidb/issues/37690">#37690</a>](https://github.com/pingcap/tidb/issues/37690) @ [<a href="https://github.com/D3Hunter">D3ハンター</a>](https://github.com/D3Hunter)

    -   TiCDC

        -   解決された TS をバッチ[<a href="https://github.com/pingcap/tiflow/issues/7078">#7078</a>](https://github.com/pingcap/tiflow/issues/7078) @ [<a href="https://github.com/sdojjy">スドジ</a>](https://github.com/sdojjy)で処理することで、リージョン ワーカーのパフォーマンスを向上させます。

## バグの修正 {#bug-fixes}

-   TiDB

    -   データベースレベルの権限が誤ってクリーンアップされる問題を修正[<a href="https://github.com/pingcap/tidb/issues/38363">#38363</a>](https://github.com/pingcap/tidb/issues/38363) @ [<a href="https://github.com/dveeden">ドヴィーデン</a>](https://github.com/dveeden)
    -   `SHOW CREATE PLACEMENT POLICY` [<a href="https://github.com/pingcap/tidb/issues/37526">#37526</a>](https://github.com/pingcap/tidb/issues/37526) @ [<a href="https://github.com/xhebox">ゼボックス</a>](https://github.com/xhebox)の誤った出力を修正
    -   1 つの PD ノードがダウンすると、他の PD ノード[<a href="https://github.com/pingcap/tidb/issues/35708">#35708</a>](https://github.com/pingcap/tidb/issues/35708) @ [<a href="https://github.com/tangenta">タンジェンタ</a>](https://github.com/tangenta)が再試行されないために`information_schema.TIKV_REGION_STATUS`のクエリが失敗する問題を修正します。
    -   `UNION`演算子が予期しない空の結果[<a href="https://github.com/pingcap/tidb/issues/36903">#36903</a>](https://github.com/pingcap/tidb/issues/36903) @ [<a href="https://github.com/tiancaiamao">ティエンチャイアマオ</a>](https://github.com/tiancaiamao)を返す可能性がある問題を修正します。
    -   TiFlash [<a href="https://github.com/pingcap/tidb/issues/37254">#37254</a>](https://github.com/pingcap/tidb/issues/37254) @ [<a href="https://github.com/wshwsh12">wshwsh12</a>](https://github.com/wshwsh12)のパーティション化されたテーブルで動的モードを有効にしたときに発生する間違った結果を修正しました。
    -   リージョンが[<a href="https://github.com/pingcap/tidb/issues/37141">#37141</a>](https://github.com/pingcap/tidb/issues/37141) @ [<a href="https://github.com/sticnarf">スティックナーフ</a>](https://github.com/sticnarf)でマージされるときに、リージョンキャッシュが時間内にクリーンアップされない問題を修正します。
    -   KV クライアントが不要な ping メッセージを送信する問題を修正[<a href="https://github.com/pingcap/tidb/issues/36861">#36861</a>](https://github.com/pingcap/tidb/issues/36861) @ [<a href="https://github.com/jackysp">ジャッキースプ</a>](https://github.com/jackysp)
    -   DML エグゼキュータを使用した`EXPLAIN ANALYZE`ステートメントが、トランザクションのコミットが完了する前に結果を返す可能性がある問題を修正します[<a href="https://github.com/pingcap/tidb/issues/37373">#37373</a>](https://github.com/pingcap/tidb/issues/37373) @ [<a href="https://github.com/cfzjywxk">cfzjywxk</a>](https://github.com/cfzjywxk)
    -   `ORDER BY`句に相関サブクエリ[<a href="https://github.com/pingcap/tidb/issues/18216">#18216</a>](https://github.com/pingcap/tidb/issues/18216) @ [<a href="https://github.com/winoros">ウィノロス</a>](https://github.com/winoros)が含まれている場合、 `GROUP CONCAT` with `ORDER BY`が失敗する可能性がある問題を修正します。
    -   `UPDATE`ステートメントに共通テーブル式 (CTE) [<a href="https://github.com/pingcap/tidb/issues/35758">#35758</a>](https://github.com/pingcap/tidb/issues/35758) @ [<a href="https://github.com/AilinKid">アイリンキッド</a>](https://github.com/AilinKid)が含まれる場合に`Can't find column`が報告される問題を修正
    -   特定のシナリオ[<a href="https://github.com/pingcap/tidb/issues/37187">#37187</a>](https://github.com/pingcap/tidb/issues/37187) @ [<a href="https://github.com/Reminiscent">懐かしい</a>](https://github.com/Reminiscent)で`EXECUTE`予期しないエラーをスローする可能性がある問題を修正します。

-   TiKV

    -   リージョン[<a href="https://github.com/tikv/tikv/issues/13553">#13553</a>](https://github.com/tikv/tikv/issues/13553) @ [<a href="https://github.com/SpadeA-Tang">SpadeA-Tang</a>](https://github.com/SpadeA-Tang)にわたるバッチ スナップショットが原因でスナップショット データが不完全になる可能性がある問題を修正
    -   フロー制御が有効で、 `level0_slowdown_trigger`が明示的に[<a href="https://github.com/tikv/tikv/issues/11424">#11424</a>](https://github.com/tikv/tikv/issues/11424) @ [<a href="https://github.com/Connor1996">コナー1996</a>](https://github.com/Connor1996)に設定されている場合の QPS ドロップの問題を修正
    -   TiKV が Web ID プロバイダーからエラーを取得し、デフォルトのプロバイダー[<a href="https://github.com/tikv/tikv/issues/13122">#13122</a>](https://github.com/tikv/tikv/issues/13122) @ [<a href="https://github.com/3pointer">3ポインター</a>](https://github.com/3pointer)にフェイルバックすると、アクセス許可拒否エラーが発生する問題を修正します。
    -   TiKV インスタンスが隔離されたネットワーク環境[<a href="https://github.com/tikv/tikv/issues/12966">#12966</a>](https://github.com/tikv/tikv/issues/12966) @ [<a href="https://github.com/cosven">コスベン</a>](https://github.com/cosven)にある場合、TiKV サービスが数分間利用できなくなる問題を修正します。

-   PD

    -   リージョンツリーの統計が不正確になる可能性がある問題を修正[<a href="https://github.com/tikv/pd/issues/5318">#5318</a>](https://github.com/tikv/pd/issues/5318) @ [<a href="https://github.com/rleungx">ルルンクス</a>](https://github.com/rleungx)
    -   TiFlash学習者のレプリカが作成されないことがある問題を修正[<a href="https://github.com/tikv/pd/issues/5401">#5401</a>](https://github.com/tikv/pd/issues/5401) @ [<a href="https://github.com/HunDunDM">フンドゥンDM</a>](https://github.com/HunDunDM)
    -   PD がダッシュボード プロキシ リクエスト[<a href="https://github.com/tikv/pd/issues/5321">#5321</a>](https://github.com/tikv/pd/issues/5321) @ [<a href="https://github.com/HunDunDM">フンドゥンDM</a>](https://github.com/HunDunDM)を正しく処理できない問題を修正
    -   異常なリージョンにより PDpanic[<a href="https://github.com/tikv/pd/issues/5491">#5491</a>](https://github.com/tikv/pd/issues/5491) @ [<a href="https://github.com/nolouch">ノールーシュ</a>](https://github.com/nolouch)が発生する可能性がある問題を修正

-   TiFlash

    -   I/O リミッターが一括書き込み後にクエリ リクエストの I/O スループットを誤って調整し、クエリのパフォーマンスが低下する可能性がある問題を修正します[<a href="https://github.com/pingcap/tiflash/issues/5801">#5801</a>](https://github.com/pingcap/tiflash/issues/5801) @ [<a href="https://github.com/JinheLin">ジンヘリン</a>](https://github.com/JinheLin)
    -   クエリがキャンセルされたときにウィンドウ関数によってTiFlashがクラッシュする可能性がある問題を修正[<a href="https://github.com/pingcap/tiflash/issues/5814">#5814</a>](https://github.com/pingcap/tiflash/issues/5814) @ [<a href="https://github.com/SeaRise">シーライズ</a>](https://github.com/SeaRise)
    -   `NULL`値[<a href="https://github.com/pingcap/tiflash/issues/5859">#5859</a>](https://github.com/pingcap/tiflash/issues/5859) @ [<a href="https://github.com/JaySon-Huang">ジェイ・ソン・ファン</a>](https://github.com/JaySon-Huang)を含む列でプライマリ インデックスを作成した後に発生するpanicを修正します。

-   ツール

    -   TiDB Lightning

        -   無効なメトリック カウンター[<a href="https://github.com/pingcap/tidb/issues/37338">#37338</a>](https://github.com/pingcap/tidb/issues/37338) @ [<a href="https://github.com/D3Hunter">D3ハンター</a>](https://github.com/D3Hunter)によって引き起こされるTiDB Lightningのpanicを修正

    -   TiDB データ移行 (DM)

        -   DM タスクが同期ユニットに入って中断されると、上流のテーブル構造情報が失われる問題を修正します[<a href="https://github.com/pingcap/tiflow/issues/7159">#7159</a>](https://github.com/pingcap/tiflow/issues/7159) @ [<a href="https://github.com/lance6716">ランス6716</a>](https://github.com/lance6716)
        -   チェックポイント[<a href="https://github.com/pingcap/tiflow/issues/5010">#5010</a>](https://github.com/pingcap/tiflow/issues/5010) @ [<a href="https://github.com/lance6716">ランス6716</a>](https://github.com/lance6716)を保存するときに SQL ステートメントを分割することで、大規模なトランザクション エラーを修正しました。
        -   DM 事前チェックに`INFORMATION_SCHEMA` [<a href="https://github.com/pingcap/tiflow/issues/7317">#7317</a>](https://github.com/pingcap/tiflow/issues/7317) @ [<a href="https://github.com/lance6716">ランス6716</a>](https://github.com/lance6716)の`SELECT`権限が必要になる問題を修正
        -   高速/完全バリデータ[<a href="https://github.com/pingcap/tiflow/issues/7241">#7241</a>](https://github.com/pingcap/tiflow/issues/7241) @ [<a href="https://github.com/buchuitoudegou">ブチュイトデゴウ</a>](https://github.com/buchuitoudegou)で DM タスクを実行した後、DM ワーカーがデッドロック エラーを引き起こす問題を修正
        -   DM が`Specified key was too long`エラー[<a href="https://github.com/pingcap/tiflow/issues/5315">#5315</a>](https://github.com/pingcap/tiflow/issues/5315) @ [<a href="https://github.com/lance6716">ランス6716</a>](https://github.com/lance6716)を報告する問題を修正
        -   レプリケーション[<a href="https://github.com/pingcap/tiflow/issues/7028">#7028</a>](https://github.com/pingcap/tiflow/issues/7028) @ [<a href="https://github.com/lance6716">ランス6716</a>](https://github.com/lance6716)中に latin1 データが破損する可能性がある問題を修正

    -   TiCDC

        -   CDCサーバーが完全に起動する前に HTTP リクエストを受信すると、CDCサーバーがpanic可能性がある問題を修正します[<a href="https://github.com/pingcap/tiflow/issues/6838">#6838</a>](https://github.com/pingcap/tiflow/issues/6838) @ [<a href="https://github.com/asddongmen">東門</a>](https://github.com/asddongmen)
        -   アップグレード[<a href="https://github.com/pingcap/tiflow/issues/7235">#7235</a>](https://github.com/pingcap/tiflow/issues/7235) @ [<a href="https://github.com/hi-rustin">こんにちはラスティン</a>](https://github.com/hi-rustin)中のログフラッディング問題を修正
        -   ChangeFeed の REDO ログ ファイルが誤って削除される可能性がある問題を修正[<a href="https://github.com/pingcap/tiflow/issues/6413">#6413</a>](https://github.com/pingcap/tiflow/issues/6413) @ [<a href="https://github.com/hi-rustin">こんにちはラスティン</a>](https://github.com/hi-rustin)
        -   etcd トランザクションでコミットされる操作が多すぎると TiCDC が使用できなくなる可能性がある問題を修正[<a href="https://github.com/pingcap/tiflow/issues/7131">#7131</a>](https://github.com/pingcap/tiflow/issues/7131) @ [<a href="https://github.com/hi-rustin">こんにちはラスティン</a>](https://github.com/hi-rustin)
        -   REDO ログ内の非再入可能 DDL ステートメントが 2 回実行されるとデータの不整合が発生する可能性がある問題を修正[<a href="https://github.com/pingcap/tiflow/issues/6927">#6927</a>](https://github.com/pingcap/tiflow/issues/6927) @ [<a href="https://github.com/hicqu">ひっくり返る</a>](https://github.com/hicqu)

    -   バックアップと復元 (BR)

        -   復元中に同時実行数の設定が大きすぎるため、リージョンのバランスが取れない問題を修正[<a href="https://github.com/pingcap/tidb/issues/37549">#37549</a>](https://github.com/pingcap/tidb/issues/37549) @ [<a href="https://github.com/3pointer">3ポインター</a>](https://github.com/3pointer)
        -   外部storage[<a href="https://github.com/pingcap/tidb/issues/37469">#37469</a>](https://github.com/pingcap/tidb/issues/37469) @ [<a href="https://github.com/MoCuishle28">モクイシュル28</a>](https://github.com/MoCuishle28)の認証キーに特殊文字が存在する場合、バックアップと復元が失敗する可能性がある問題を修正
