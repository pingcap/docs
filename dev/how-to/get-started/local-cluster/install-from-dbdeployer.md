---
title: Install from DBdeployer 
summary: Install TiDB using the DBdeployer package manager.
category: how-to
---

# Install from DBdeployer

DBdeployer is designed to allow multiple versions of TiDB deployed concurrently. It is recommended for advanced users who are testing out new builds of TiDB, or testing compatibility across releases.

Similar to [Homebrew](/how-to/get-started/local-cluster/install-from-homebrew.md), the DBdeployer installation method installs the tidb-server **without** the tikv-server or pd-server. This is useful for development environments, since you can test your application's compatibility with TiDB without needing to deploy a full TiDB platform.

> **Note:**
>
> Internally this installation uses goleveldb as the storage engine. It is much slower than TiKV, and any benchmarks will be unreliable.

<main class="tabs">
  <input id="tabMacOS" type="radio" name="tabs" value="MacOSContent" checked>
  <label for="tabMacOS">
      <span><img src="/images/docs/mac-os-20.png" width="20"></img></span>
      <span class="label__title">macOS</span>
  </label>
  <input id="tabLinux" type="radio" name="tabs" value="LinuxContent">
  <label for="tabLinux">
      <span><img src="/images/docs/linux-20.png" width="20"></img></span>
      <span class="label__title">Linux</span>
  </label>
  <section id="MacOSContent">

After <a href="https://github.com/datacharmer/dbdeployer">installing DBdeployer</a>, install a MySQL 5.7 client:
<pre>
dbdeployer downloads get-unpack --overwrite --delete-after-unpack mysql-5.7.26-macos10.14-x86_64.tar.gz
</pre>

Install TiDB using the installed MySQL 5.7 client:
<pre>
dbdeployer downloads get-unpack tidb-master-darwin-amd64.tar.gz --prefix=tidb --unpack-version=3.0.0 --overwrite --delete-after-unpack
</pre>  

</section>
  <section id="LinuxContent">

After <a href="https://github.com/datacharmer/dbdeployer">installing DBdeployer</a>, install a MySQL 5.7 client:
<pre>
dbdeployer downloads get-unpack --overwrite --delete-after-unpack mysql-5.7.26-linux-glibc2.12-x86_64.tar.gz
</pre>

Install TiDB 3.0 using the installed MySQL 5.7 client:
<pre>
dbdeployer downloads get-unpack tidb-master-linux-amd64.tar.gz --prefix=tidb --unpack-version=3.0.0 --overwrite --delete-after-unpack
</pre>

  </section>
</main>
