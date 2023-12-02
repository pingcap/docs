---
title: TiFlash Command-line Flags
summary: Learn the command-line startup flags of TiFlash.
---

# TiFlashコマンドライン フラグ {#tiflash-command-line-flags}

このドキュメントでは、 TiFlash を起動するときに使用できるコマンドライン フラグを紹介します。

## <code>server --config-file</code> {#code-server-config-file-code}

-   TiFlash構成ファイルのパスを指定します
-   デフォルト： &quot;&quot;
-   構成ファイルを指定する必要があります。詳しい設定項目については[TiFlash設定パラメータ](/tiflash/tiflash-configuration.md)を参照してください。

## <code>dttool migrate</code> {#code-dttool-migrate-code}

-   DTFile のファイル形式を移行します (テストまたはダウングレード用)。データは 1 つの DTFile 単位で移行されます。テーブル全体を移行する場合は、 `<data dir>/t_<table id>/stable/dmf_<file id>`に類似したすべてのパスを見つけて、1 つずつ移行する必要があります。スクリプトを使用して移行を自動化できます。

-   ユーザーシナリオ:

    -   データ検証が有効になっているTiFlash をv5.4.0 以上のバージョンから v5.4.0 未満のバージョンにダウングレードする必要がある場合は、このツールを使用して DTFile のデータ形式をダウングレードできます。
    -   TiFlash をv5.4.0 以上のバージョンにアップグレードし、既存のデータのデータ検証を有効にしたい場合は、このツールを使用して DTFile のデータ形式をアップグレードできます。
    -   さまざまな構成で DTFile のスペース使用量と読み取り速度をテストします。
    -   TiFlash を、小さいファイルのマージ (つまり、 `storage.format_version` &gt;= 5) が有効になっているバージョン v7.3.0 以上からバージョン &lt; v7.3.0 にダウングレードする必要がある場合は、このツールを使用して DTFile のデータ形式をダウングレードできます。 。

-   パラメーター：
    -   `--imitative` : DTFile の暗号化機能を使用しない場合、このフラグを使用して、設定ファイルの使用と PD への接続を回避できます。
    -   `--version` : DTFile のターゲット バージョン。値のオプションは`1` 、 `2` (デフォルト)、および`3`です。 `1`は古いバージョン、 `2`は新しいチェックサムに対応するバージョン、 `3`は小さなファイルのマージをサポートするバージョンです。
    -   `--algorithm` : データ検証に使用されるハッシュ アルゴリズム。値のオプションは`xxh3` (デフォルト)、 `city128` 、 `crc32` 、 `crc64` 、および`none`です。このパラメータは、 `version`が`2`の場合にのみ有効です。
    -   `--frame` : 検証フレームのサイズ。デフォルト値は`1048576`です。このパラメータは`version`が`2`の場合にのみ有効です。
    -   `--compression` : ターゲットの圧縮アルゴリズム。値のオプションは`LZ4` (デフォルト)、 `LZ4HC` `zstd`および`none`です。
    -   `--level` : 目標の圧縮レベル。指定しない場合は、圧縮アルゴリズムに従って推奨圧縮レベルがデフォルトで使用されます。 `compression`が`LZ4`または`zstd`に設定されている場合、デフォルトのレベルは 1 です。 `compression`が`LZ4HC`に設定されている場合、デフォルトのレベルは 9 です。
    -   `--config-file` ： `dttool migrate`の設定ファイルは[`server`の設定ファイル](/tiflash/tiflash-command-line-flags.md#server---config-file)と同じです。詳細については、 `--imitative`を参照してください。
    -   `--file-id` : DTFile の ID。たとえば、DTFile `dmf_123`の ID は`123`です。
    -   `--workdir` : `dmf_xxx`の親ディレクトリ。
    -   `--dry` : ドライランモード。移行プロセスのみが出力されます。
    -   `--nokeep` : 元のデータを保持しません。このオプションが有効になっていない場合、 `dmf_xxx.old`ファイルが作成されます。

> **警告：**
>
> TiFlash は、カスタム圧縮アルゴリズムと圧縮レベルを使用する DTFile を読み取ることができます。ただし、正式にサポートされているのは、デフォルトの圧縮レベルを持つ`lz4`アルゴリズムのみです。カスタム圧縮パラメータは完全にはテストされておらず、実験的にすぎません。

> **注記：**
>
> セキュリティ上の理由から、DTTool は移行モードで作業ディレクトリにロックを追加しようとします。したがって、同じディレクトリ内では、同時に移行タスクを実行できる DTTool は 1 つだけです。ロックが解放されていない状態で DTTool を強制的に停止すると、後で DTTool を再実行しようとすると、移行タスクの実行が拒否される可能性があります。
>
> この状況が発生し、LOCK ファイルを削除してもデータが破損しないことがわかっている場合は、作業ディレクトリ内の LOCK ファイルを手動で削除してロックを解除できます。

## <code>dttool bench</code> {#code-dttool-bench-code}

-   DTFile の基本的な I/O 速度テストを提供します。
-   パラメーター：

    -   `--version` : DTFile のバージョン。 [`dttool migrate`の`--version`](#dttool-migrate)を参照してください。
    -   `--algorithm` : データ検証に使用されるハッシュ アルゴリズム。 [`dttool migrate`の`--algorithm`](#dttool-migrate)を参照してください。
    -   `--frame` : 検証フレームのサイズ。 [`dttool migrate`の`--frame`](#dttool-migrate)を参照してください。
    -   `--column` : テストするテーブルの列。デフォルト値は`100`です。
    -   `--size` : テストするテーブルの行。デフォルト値は`1000`です。
    -   `--field` : テストするテーブルのフィールド長制限。デフォルト値は`1024`です。
    -   `--random` : ランダムシード。このパラメーターを指定しない場合、ランダム シードはシステム エントロピー プールから抽出されます。
    -   `--encryption` : 暗号化機能を有効にします。
    -   `--repeat` : テストを繰り返す回数。デフォルト値は`5`です。
    -   `--workdir` : 一時データ ディレクトリ。テスト対象のファイル システム内のパスを指します。デフォルト値は`/tmp/test`です。

## <code>dttool inspect</code> {#code-dttool-inspect-code}

-   DTFile の整合性をチェックします。データ検証は 1 つの DTFile 単位で実行されます。テーブル全体を検証する場合は、 `<data dir>/t_<table id>/stable/dmf_<file id>`に類似したパスをすべて見つけて、それらを 1 つずつ検証する必要があります。スクリプトを使用して検証を自動化できます。

-   ユーザーシナリオ:

    -   フォーマットのアップグレードまたはダウングレードを実行した後、DTFile のデータの整合性を検証できます。
    -   DTFile を新しい環境に移行した後、DTFile のデータ整合性を検証できます。

-   パラメーター：

    -   `--config-file` : `dttool bench`の設定ファイル。 [`dttool migrate`の`--config-file`](#dttool-migrate)を参照してください。
    -   `--check` : ハッシュ検証を実行します。
    -   `--file-id` : DTFile の ID。 [`dttool migrate`の`--file-id`](#dttool-migrate)を参照してください。
    -   `--imitative` : データベースコンテキストを模倣します。 [`dttool migrate`の`--imitative`](#dttool-migrate)を参照してください。
    -   `--workdir` : データディレクトリ。 [`dttool migrate`の`--workdir`](#dttool-migrate)を参照してください。
