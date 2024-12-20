---
title: Troubleshoot TiProxy
summary: TiProxy の一般的な問題、原因、および解決策について説明します。
---

# TiProxy のトラブルシューティング {#troubleshoot-tiproxy}

このドキュメントでは、TiProxy の一般的な問題、原因、および解決策について説明します。

## TiProxyに接続できません {#cannot-connect-to-tiproxy}

次の手順に従って、問題をトラブルシューティングできます。

1.  [コネクタバージョン](/tiproxy/tiproxy-overview.md#supported-connectors)がサポートされているかどうかを確認します。コネクタがリストにない場合は、コネクタが[認証プラグイン](https://dev.mysql.com/doc/refman/8.0/en/pluggable-authentication.html)をサポートしているかどうかを確認します。
2.  クライアントが`No available TiDB instances, please make sure TiDB is available`報告する場合は、TiDBサーバーが存在するかどうか、および TiDBサーバーの SQL ポートと HTTP ステータス ポートに正常に接続できるかどうかを確認します。
3.  クライアントが`Require TLS enabled on TiProxy when require-backend-tls=true`報告する場合は、TiProxy が TLS 証明書で正しく構成されているかどうかを確認します。
4.  クライアントが`Verify TiDB capability failed, please upgrade TiDB`報告する場合は、TiDBサーバーのバージョンが v6.5.0 以降であるかどうかを確認します。
5.  クライアントが`TiProxy fails to connect to TiDB, please make sure TiDB is available`報告した場合は、 TiProxy ノードが TiDBサーバーに接続できるかどうかを確認します。
6.  クライアントが`Require TLS enabled on TiDB when require-backend-tls=true`報告する場合は、TiDB が TLS 証明書で正しく構成されているかどうかを確認します。
7.  クライアントが`TiProxy fails to connect to TiDB, please make sure TiDB proxy-protocol is set correctly`報告した場合は、 TiProxy で[`proxy.proxy-protocol`](/tiproxy/tiproxy-configuration.md#proxy-protocol)が有効になっているかどうか、 TiDBサーバーで[`proxy-protocol`](/tidb-configuration-file.md#proxy-protocol)有効になっていないかどうかを確認します。
8.  TiProxy が[`max-connections`](/tiproxy/tiproxy-configuration.md#max-connections)に設定され、TiProxy 上の接続数が最大接続制限を超えているかどうかを確認します。
9.  TiProxy ログでエラー メッセージを確認してください。

## TiProxyは接続を移行しません {#tiproxy-does-not-migrate-connections}

次の手順に従って、問題をトラブルシューティングできます。

1.  [TiProxy の制限](/tiproxy/tiproxy-overview.md#limitations)が満たされていないかどうか。TiProxy ログを確認することでこれをさらに確認できます。
2.  [`security.session-token-signing-cert`](/tidb-configuration-file.md#session-token-signing-cert-new-in-v640) [`security.session-token-signing-key`](/tidb-configuration-file.md#session-token-signing-key-new-in-v640) [`graceful-wait-before-shutdown`](/tidb-configuration-file.md#graceful-wait-before-shutdown-new-in-v50)で正しく構成されているかどうか。

## TiDBサーバー上の CPU 使用率の不均衡 {#unbalanced-cpu-usage-on-tidb-server}

次の手順に従って、問題をトラブルシューティングできます。

1.  TiDB サーバー間で CPU 使用率に大きな差があるかどうかを確認します。TiProxy は、TiDB サーバー間で同一の CPU 使用率を保証するものではありません。CPU 使用率の差がクエリのレイテンシーに影響を与えるほど大きい場合にのみ[負荷分散](/tiproxy/tiproxy-load-balance.md)実行します。
2.  TiDBサーバーの接続数が徐々にゼロに減少する場合は、他の負荷分散ポリシーの影響を受けている可能性があります。Grafana の[`Session Migration Reasons`](/tiproxy/tiproxy-grafana.md#balance)メトリックをチェックして、他のポリシーに基づく移行があるかどうかを確認できます。
3.  TiProxy 構成項目[`policy`](/tiproxy/tiproxy-configuration.md#policy)が`location`に設定されているかどうかを確認します。場所に基づく優先順位付けが有効になっている場合、TiProxy は異なる場所間で CPU 使用率を分散しません。
4.  TiProxy のバージョンを確認してください。CPU ベースの負荷分散をサポートするのは、v1.1.0 以降のバージョンのみです。それより前のバージョンでは、最小接続数に基づく負荷分散ポリシーが使用されます。
5.  上記のいずれの状況にも当てはまらない場合は、接続の移行が失敗した可能性があります。さらにトラブルシューティングするには、 [TiProxyは接続を移行しません](#tiproxy-does-not-migrate-connections)参照してください。

## レイテンシーが大幅に増加 {#latency-is-significantly-increased}

次の手順に従って、問題をトラブルシューティングできます。

1.  Grafana を通じて TiProxy のレイテンシーを確認します。TiProxy のレイテンシーが高くない場合は、クライアントの負荷が高いか、クライアントと TiProxy 間のネットワークレイテンシーが高いことを意味します。
2.  Grafana を使用して TiDBサーバーのレイテンシーを確認します。TiDBサーバーのレイテンシーが高い場合は、 [遅延が大幅に増加する](/tidb-troubleshooting-map.md#2-latency-increases-significantly)の手順に従ってトラブルシューティングを行います。
3.  Grafana で[TiProxyとTiDBサーバー間のネットワーク継続時間](/tiproxy/tiproxy-grafana.md#backend)確認します。
4.  TiProxy の CPU 使用率を確認します。CPU 使用率が 90% を超える場合は、TiProxy をスケールアウトする必要があります。
