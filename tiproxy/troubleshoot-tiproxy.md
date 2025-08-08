---
title: Troubleshoot TiProxy
summary: TiProxy の一般的な問題、原因、および解決策について説明します。
---

# TiProxy のトラブルシューティング {#troubleshoot-tiproxy}

このドキュメントでは、TiProxy の一般的な問題、原因、および解決策について説明します。

## TiProxyに接続できません {#cannot-connect-to-tiproxy}

次の手順に従って、問題をトラブルシューティングできます。

1.  [コネクタバージョン](/tiproxy/tiproxy-overview.md#supported-connectors)がサポートされているかどうかを確認してください。コネクタがリストにない場合は、コネクタが[認証プラグイン](https://dev.mysql.com/doc/refman/8.0/en/pluggable-authentication.html)サポートしているかどうかを確認してください。
2.  クライアントが`No available TiDB instances, please make sure TiDB is available`報告する場合は、TiDBサーバーが存在するかどうか、および TiDBサーバーの SQL ポートと HTTP ステータス ポートに正常に接続できるかどうかを確認します。
3.  クライアントが`Require TLS enabled on TiProxy when require-backend-tls=true`報告する場合は、TiProxy が TLS 証明書で正しく構成されているかどうかを確認します。
4.  クライアントが`Verify TiDB capability failed, please upgrade TiDB`報告する場合は、TiDBサーバーのバージョンが v6.5.0 以降であるかどうかを確認します。
5.  クライアントが`TiProxy fails to connect to TiDB, please make sure TiDB is available`報告した場合は、 TiProxy ノードが TiDBサーバーに接続できるかどうかを確認します。
6.  クライアントが`Require TLS enabled on TiDB when require-backend-tls=true`報告する場合は、TiDB が TLS 証明書で正しく構成されているかどうかを確認します。
7.  クライアントが`TiProxy fails to connect to TiDB, please make sure TiDB proxy-protocol is set correctly`報告した場合は、 TiProxy で[`proxy.proxy-protocol`](/tiproxy/tiproxy-configuration.md#proxy-protocol)有効になっているかどうか、 TiDBサーバーで[`proxy-protocol`](/tidb-configuration-file.md#proxy-protocol)有効になっていないかどうかを確認します。
8.  TiProxy が[`max-connections`](/tiproxy/tiproxy-configuration.md#max-connections)に設定されており、TiProxy 上の接続数が最大接続制限を超えているかどうかを確認します。
9.  TiProxy ログでエラー メッセージを確認してください。

## TiProxyは接続を移行しません {#tiproxy-does-not-migrate-connections}

次の手順に従って、問題をトラブルシューティングできます。

1.  [TiProxyの制限](/tiproxy/tiproxy-overview.md#limitations)満たされていないかどうか。TiProxy ログを確認することで、これをさらに確認できます。
2.  [`security.session-token-signing-cert`](/tidb-configuration-file.md#session-token-signing-cert-new-in-v640) [`security.session-token-signing-key`](/tidb-configuration-file.md#session-token-signing-key-new-in-v640) [`graceful-wait-before-shutdown`](/tidb-configuration-file.md#graceful-wait-before-shutdown-new-in-v50)で正しく構成されているかどうか。

## TiDBサーバーの CPU 使用率が不均衡 {#unbalanced-cpu-usage-on-tidb-server}

次の手順に従って、問題をトラブルシューティングできます。

1.  TiDBサーバー間でCPU使用率に大きな差があるかどうかを確認します。TiProxyは、TiDBサーバー間でCPU使用率が同一であることを保証するものではありません。CPU使用率の差がクエリのレイテンシーに影響を与えるほど大きい場合にのみ、 [負荷分散](/tiproxy/tiproxy-load-balance.md)実行します。
2.  TiDBサーバーの接続数が徐々にゼロに減少する場合、他の負荷分散ポリシーの影響を受けている可能性があります。Grafanaで[`Session Migration Reasons`](/tiproxy/tiproxy-grafana.md#balance)メトリックを確認することで、他のポリシーに基づく移行が発生しているかどうかを確認できます。
3.  TiProxy 設定項目[`policy`](/tiproxy/tiproxy-configuration.md#policy) `location`に設定されているかどうかを確認してください。ロケーションベースの優先順位付けが有効になっている場合、TiProxy は異なるロケーション間で CPU 使用率を分散しません。
4.  TiProxyのバージョンを確認してください。CPUベースの負荷分散はv1.1.0以降のバージョンでのみサポートされます。それ以前のバージョンでは、最小接続数に基づく負荷分散ポリシーが使用されます。
5.  上記のいずれの状況にも該当しない場合は、接続の移行が失敗した可能性があります。さらにトラブルシューティングを行うには、 [TiProxyは接続を移行しません](#tiproxy-does-not-migrate-connections)参照してください。

## レイテンシーが大幅に増加 {#latency-is-significantly-increased}

次の手順に従って、問題をトラブルシューティングできます。

1.  Grafana を使って TiProxy のレイテンシーを確認します。TiProxy のレイテンシーが高くない場合は、クライアントの負荷が高いか、クライアントと TiProxy 間のネットワークレイテンシーが高いことを意味します。
2.  Grafanaを使用してTiDBサーバーのレイテンシーを確認します。TiDBサーバーのレイテンシーが高い場合は、手順[レイテンシーが大幅に増加する](/tidb-troubleshooting-map.md#2-latency-increases-significantly)に従ってトラブルシューティングを行ってください。
3.  Grafana を通じて[TiProxyとTiDBサーバー間のネットワーク継続時間](/tiproxy/tiproxy-grafana.md#backend)確認します。
4.  TiProxyのCPU使用率を確認してください。CPU使用率が90%を超える場合は、TiProxyをスケールアウトする必要があります。
