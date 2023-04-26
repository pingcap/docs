---
title: TiFlash Command-line Flags
summary: Learn the command-line startup flags of TiFlash.
---

# TiFlashコマンドライン フラグ {#tiflash-command-line-flags}

このドキュメントでは、 TiFlash を起動するときに使用できるコマンドライン フラグを紹介します。

## <code>server --config-file</code> {#code-server-config-file-code}

-   TiFlash構成ファイルのパスを指定します
-   デフォルト： &quot;&quot;
-   構成ファイルを指定する必要があります。詳細な設定項目については、 [TiFlash構成パラメータ](/tiflash/tiflash-configuration.md)を参照してください。

## <code>dttool migrate</code> {#code-dttool-migrate-code}

-   DTFile のファイル形式を移行します (テストまたはダウングレード用)。データは 1 つの DTFile 単位で移行されます。テーブル全体を移行する場合は、 `<data dir>/t_<table id>/stable/dmf_<file id>`に類似したすべてのパスを見つけて、1 つずつ移行する必要があります。スクリプトを使用して移行を自動化できます。

-   ユーザー シナリオ:

    -   データ検証が有効になっているバージョン &gt;= v5.4.0 からバージョン &lt; v5.4.0 にTiFlashをダウングレードする必要がある場合は、このツールを使用して DTFile のデータ形式をダウングレードできます。
    -   TiFlash をバージョン &gt;= v5.4.0 にアップグレードし、既存のデータのデータ検証を有効にしたい場合は、このツールを使用して DTFile のデータ形式をアップグレードできます。
    -   さまざまな構成で DTFile のスペース使用量と読み取り速度をテストします。

-   パラメーター：
    -   `--imitative` : DTFile の暗号化機能を使用しない場合、このフラグを使用して構成ファイルの使用と PD への接続を回避できます。
    -   `--version` : DTFile のバージョン。値のオプションは`1`と`2` (デフォルト) です。 `1`が古いバージョンで、 `2`が新しいチェックサムに対応するバージョンです。
    -   `--algorithm` : データ検証に使用されるハッシュ アルゴリズム。値のオプションは`xxh3` (デフォルト)、 `city128` 、 `crc32` 、 `crc64` 、および`none`です。このパラメーターは、 `version`が`2`の場合にのみ有効です。
    -   `--frame` : 検証フレームのサイズ。デフォルト値は`1048576`です。このパラメーターは、 `version`が`2`の場合にのみ有効です。
    -   `--compression` : ターゲット圧縮アルゴリズム。値のオプションは`LZ4` (デフォルト)、 `LZ4HC` 、 `zstd` 、および`none`です。
    -   `--level` : ターゲットの圧縮レベル。指定しない場合、圧縮アルゴリズムに従って、推奨される圧縮レベルがデフォルトで使用されます。 `compression`が`LZ4`または`zstd`に設定されている場合、デフォルトのレベルは 1 です`compression`が`LZ4HC`に設定されている場合、デフォルトのレベルは 9 です。
    -   `--config-file` : `dttool migrate`の構成ファイルは[`server`の設定ファイル](/tiflash/tiflash-command-line-flags.md#server---config-file)と同じです。詳細については、 `--imitative`を参照してください。
    -   `--file-id` : DTFile の ID。たとえば、DTFile `dmf_123`の ID は`123`です。
    -   `--workdir` : `dmf_xxx`の親ディレクトリ。
    -   `--dry` : 予行演習モード。移行プロセスのみが出力されます。
    -   `--nokeep` : 元のデータを保持しません。このオプションが有効でない場合、 `dmf_xxx.old`ファイルが作成されます。

> **警告：**
>
> TiFlash は、カスタムの圧縮アルゴリズムと圧縮レベルを使用する DTFile を読み取ることができます。ただし、公式には圧縮レベルがデフォルトの`lz4`アルゴリズムのみがサポートされています。カスタム圧縮パラメータは十分にテストされておらず、実験的なものです。

> **ノート：**
>
> セキュリティ上の理由から、DTTool は移行モードで作業ディレクトリにロックを追加しようとします。したがって、同じディレクトリでは、移行タスクを同時に実行できる DTTool は 1 つだけです。ロックが解除されていない状態で DTTool を強制停止すると、後で DTTool を再実行しようとすると、移行タスクの実行が拒否されることがあります。
>
> このような状況が発生した場合、LOCK ファイルを削除してもデータが破損しないことがわかっている場合は、作業ディレクトリの LOCK ファイルを手動で削除してロックを解除できます。

## <code>dttool bench</code> {#code-dttool-bench-code}

-   DTFile の基本的な I/O 速度テストを提供します。
-   パラメーター：

    -   `--version` : DTFile のバージョン。 [`dttool migrate`の<code>--version</code>](#dttool-migrate)を参照してください。
    -   `--algorithm` : データ検証に使用されるハッシュ アルゴリズム。 [`dttool migrate`の<code>--algorithm</code>](#dttool-migrate)を参照してください。
    -   `--frame` : 検証フレームのサイズ。 [`dttool migrate`の<code>--frame</code>](#dttool-migrate)を参照してください。
    -   `--column` : テストするテーブルの列。デフォルト値は`100`です。
    -   `--size` : テストするテーブルの行。デフォルト値は`1000`です。
    -   `--field` : テストするテーブルのフィールド長制限。デフォルト値は`1024`です。
    -   `--random` : ランダム シード。このパラメーターを指定しない場合、ランダム シードはシステム エントロピー プールから取得されます。
    -   `--encryption` : 暗号化機能を有効にします。
    -   `--repeat` : テストを繰り返す回数。デフォルト値は`5`です。
    -   `--workdir` : テスト対象のファイル システム内のパスを指す一時データ ディレクトリ。デフォルト値は`/tmp/test`です。

## <code>dttool inspect</code> {#code-dttool-inspect-code}

-   DTFile の整合性をチェックします。データの検証は、1 つの DTFile 単位で実行されます。テーブル全体を検証する場合は、 `<data dir>/t_<table id>/stable/dmf_<file id>`に似たすべてのパスを見つけて、1 つずつ検証する必要があります。スクリプトを使用して検証を自動化できます。

-   ユーザー シナリオ:

    -   フォーマットのアップグレードまたはダウングレードを実行した後、DTFile のデータの整合性を検証できます。
    -   DTFile を新しい環境に移行した後、DTFile のデータ整合性を検証できます。

-   パラメーター：

    -   `--config-file` : `dttool bench`の構成ファイル。 [`--config-file` in <code>dttool migrate</code>](#dttool-migrate)を参照してください。
    -   `--check` : ハッシュ検証を実行します。
    -   `--file-id` : DTFile の ID。 [`dttool migrate`の<code>--file-id</code>](#dttool-migrate)を参照してください。
    -   `--imitative` : データベース コンテキストを模倣します。 [-- `dttool migrate`の<code>--imitative</code>](#dttool-migrate)を参照してください。
    -   `--workdir` : データ ディレクトリ。 [`dttool migrate`の<code>--workdir</code>](#dttool-migrate)を参照してください。
