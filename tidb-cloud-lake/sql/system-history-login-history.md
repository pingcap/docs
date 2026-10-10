---
title: system_history.login_history
summary: ログイン成功の SQL の例 `SELECT * FROM system_history.login_history LIMIT 1;`。
---

# system_history.login_history

**認証セキュリティ監査** - すべてのユーザーログイン試行（成功および失敗）を包括的に記録します。主な用途は次のとおりです。

- **セキュリティ監視**: ブルートフォース攻撃や不正アクセスの試行を検出
- **コンプライアンス監査**: 規制要件に対応するためにユーザー認証を追跡
- **アクセスパターン分析**: ユーザーがいつどのようにシステムへアクセスしているかを監視
- **インシデント調査**: セキュリティインシデントや認証の問題を調査

## フィールド {#fields}

| フィールド     | 型        | 説明                                                           |
|----------------|-----------|------------------------------------------------------------    |
| event_time     | TIMESTAMP | ログインイベントが発生したタイムスタンプ                      |
| handler        | VARCHAR   | ログインに使用されたプロトコルまたはハンドラー（例: `HTTP`）  |
| event_type     | VARCHAR   | ログインイベントの種類（例: `LoginSuccess`, `LoginFailed`）   |
| connection_uri | VARCHAR   | 接続に使用された URI                                          |
| auth_type      | VARCHAR   | 使用された認証方式（例: Password）                            |
| user_name      | VARCHAR   | ログインを試行したユーザー名                                  |
| client_ip      | VARCHAR   | クライアントの IP アドレス                                    |
| user_agent     | VARCHAR   | クライアントのユーザーエージェント文字列                      |
| session_id     | VARCHAR   | ログイン試行に関連付けられたセッション ID                     |
| node_id        | VARCHAR   | ログインが処理されたノード ID                                 |
| error_message  | VARCHAR   | ログインに失敗した場合のエラーメッセージ                      |

## 例 {#examples}

ログイン成功の例:

```sql
SELECT * FROM system_history.login_history LIMIT 1;

*************************** 1. row ***************************
    event_time: 2025-06-03 06:04:57.353108
       handler: HTTP
    event_type: LoginSuccess
connection_uri: /session/login?disable_session_token=true
     auth_type: Password
     user_name: root
     client_ip: 127.0.0.1
    user_agent: lakesql/0.26.2-unknown
    session_id: 9a3ba9d8-44d9-49ca-9446-501deaca15c9
       node_id: 765ChL6Ra949Ioeb5LrTs
 error_message:
```

ログイン失敗の例:

```sql
SELECT * FROM system_history.login_history LIMIT 1;

*************************** 1. row ***************************
    event_time: 2025-06-03 06:07:32.512021
       handler: MySQL
    event_type: LoginFailed
connection_uri:
     auth_type: Password
     user_name: root1
     client_ip: 127.0.0.1:62050
    user_agent:
    session_id: 4fb87258-865a-402c-8680-e3be1e01b4e6
       node_id: 765ChL6Ra949Ioeb5LrTs
 error_message: UnknownUser. Code: 2201, Text = User 'root1'@'%' does not exist..
```