---
title: TiFlash Command-line Flags
summary: Learn the command-line startup flags of TiFlash.
---

# TiFlashコマンドラインフラグ {#tiflash-command-line-flags}

このドキュメントでは、TiFlashを起動するときに使用できるコマンドラインフラグを紹介します。

## <code>server --config-file</code> {#code-server-config-file-code}

-   TiFlash構成ファイルのパスを指定します
-   デフォルト： &quot;&quot;
-   構成ファイルを指定する必要があります。構成項目の詳細については、 [TiFlash構成パラメーター](/tiflash/tiflash-configuration.md)を参照してください。

## <code>dttool migrate</code> {#code-dttool-migrate-code}

-   DTFileのファイル形式を移行します（テストまたはダウングレード用）。データは、単一のDTFileの単位で移行されます。テーブル全体を移行する場合は、 `<data dir>/t_<table id>/stable/dmf_<file id>`に類似したすべてのパスを見つけて、それらを1つずつ移行する必要があります。スクリプトを使用して移行を自動化できます。

-   ユーザーシナリオ：

    -   データ検証を有効にしたバージョン&gt;=v5.4.0からバージョン&lt;v5.4.0にTiFlashをダウングレードする必要がある場合は、このツールを使用してDTFileのデータ形式をダウングレードできます。
    -   TiFlashをバージョン&gt;=v5.4.0にアップグレードし、既存のデータのデータ検証を有効にしたい場合は、このツールを使用してDTFileのデータ形式をアップグレードできます。
    -   さまざまな構成でDTFileのスペース使用量と読み取り速度をテストします。

-   パラメーター：
    -   `--imitative` ：DTFileの暗号化機能を使用しない場合、このフラグを使用して、構成ファイルの使用とPDへの接続を回避できます。
    -   `--version` ：DTFileのバージョン。値のオプションは`1`と`2` （デフォルト）です。 `1`は古いバージョンで、 `2`は新しいチェックサムに対応するバージョンです。
    -   `--algorithm` ：データ検証に使用されるハッシュアルゴリズム。値のオプションは、 `xxh3` （デフォルト）、 `city128` 、 `none` `crc32` `crc64`このパラメーターは、 `version`が`2`の場合にのみ有効です。
    -   `--frame` ：検証フレームのサイズ。デフォルト値は`1048576`です。このパラメータは、 `version`が`2`の場合にのみ有効です。
    -   `--compression` ：ターゲット圧縮アルゴリズム。値のオプションは、 `lz4` （デフォルト）、 `lz4hc` 、および`zstd` `none` 。
    -   `--level` ：目標圧縮レベル。デフォルト値は`-1`で、これは自動モードを意味します。値の範囲は、圧縮アルゴリズムによって異なります。
    -   `--config-file` ： `dttool migrate`の設定ファイルは[`server`の構成ファイル](/tiflash/tiflash-command-line-flags.md#server---config-file)と同じです。構成ファイルを使用する場合は、ローカルTiFlashサーバーインスタンスを終了します。詳細については、 `--imitative`を参照してください。
    -   `--file-id` ：DTFileのID。たとえば、 `dmf_123`のIDは`123`です。
    -   `--workdir` ： `dmf_xxx`の親ディレクトリ。
    -   `--dry` ：ドライランモード。移行プロセスのみが出力されます。
    -   `--nokeep` ：元のデータを保持しません。このオプションを有効にしない場合、 `dmf_xxx.old`のファイルが作成されます。

> **警告：**
>
> TiFlashは、カスタム圧縮アルゴリズムと圧縮レベルを使用するDTFileを読み取ることができます。ただし、デフォルトの圧縮レベルを持つ`lz4`のアルゴリズムのみが公式にサポートされています。カスタム圧縮パラメータは徹底的にテストされておらず、実験的ものにすぎません。

> **ノート：**
>
> セキュリティ上の理由から、DTToolは移行モードで作業ディレクトリにロックを追加しようとします。したがって、同じディレクトリ内で、同時に移行タスクを実行できるのは1つのDTToolだけです。ロックが解除されていない状態でDTToolを強制的に停止した場合、後でDTToolを再実行しようとすると、移行タスクの実行が拒否される可能性があります。
>
> このような状況が発生し、LOCKファイルを削除してもデータが破損しないことがわかっている場合は、作業ディレクトリのLOCKファイルを手動で削除してロックを解除できます。

## <code>dttool bench</code> {#code-dttool-bench-code}

-   DTFileの基本的なI/O速度テストを提供します。
-   パラメーター：

    -   `--version` ：DTFileのバージョン。 [`--version`のバージョンは<code>dttool migrate</code>します](#dttool-migrate)を参照してください。
    -   `--algorithm` ：データ検証に使用されるハッシュアルゴリズム。 [`--algorithm`のアルゴリズムは<code>dttool migrate</code>します](#dttool-migrate)を参照してください。
    -   `--frame` ：検証フレームのサイズ。 [`--frame`のフレームは<code>dttool migrate</code>します](#dttool-migrate)を参照してください。
    -   `--column` ：テストするテーブルの列。デフォルト値は`100`です。
    -   `--size` ：テストするテーブルの行。デフォルト値は`1000`です。
    -   `--field` ：テストするテーブルのフィールド長制限。デフォルト値は`1024`です。
    -   `--random` ：ランダムシード。このパラメーターを指定しない場合、ランダムシードはシステムエントロピープールから取得されます。
    -   `--encryption` ：暗号化機能を有効にします。
    -   `--repeat` ：テストを繰り返す回数。デフォルト値は`5`です。
    -   `--workdir` ：テストするファイルシステム内のパスを指す一時データディレクトリ。デフォルト値は`/tmp/test`です。

## <code>dttool inspect</code> {#code-dttool-inspect-code}

-   DTFileの整合性をチェックします。データ検証は、単一のDTFileの単位で実行されます。テーブル全体を検証する場合は、 `<data dir>/t_<table id>/stable/dmf_<file id>`に類似したすべてのパスを見つけて、それらを1つずつ検証する必要があります。スクリプトを使用して検証を自動化できます。

-   ユーザーシナリオ：

    -   フォーマットのアップグレードまたはダウングレードを実行した後、DTFileのデータ整合性を検証できます。
    -   DTFileを新しい環境に移行した後、DTFileのデータ整合性を検証できます。

-   パラメーター：

    -   `--config-file` ： `dttool bench`の構成ファイル。 [`--config-file` <code>dttool migrate</code>します](#dttool-migrate)を参照してください。
    -   `--check` ：ハッシュ検証を実行します。
    -   `--file-id` ：DTFileのID。 [`dttool migrate` <code>--file-id</code>](#dttool-migrate)を参照してください。
    -   `--imitative` ：データベースコンテキストを模倣します。 [`--imitative`の<code>dttool migrate</code>](#dttool-migrate)を参照してください。
    -   `--workdir` ：データディレクトリ。 [`--workdir`のworkdirは<code>dttool migrate</code>します](#dttool-migrate)を参照してください。
