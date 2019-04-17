---
title: Install from DBdeployer 
summary: Install TiDB using the DBdeployer package manager.
category: how-to
---

# Install from DBdeployer

DBdeployer is designed to allow multiple versions of TiDB deployed concurrently. It is recommended for advanced users who are testing out new builds of TiDB, or testing compatibility across releases.

Similar to [Homebrew](install-from-homebrew.md), the DBdeployer installation method installs the tidb-server **without** the tikv-server or pd-server. This is useful for development environments, since you can test your application's compatibility with TiDB without needing to deploy a full TiDB platform.

> **Note**: Internally this installation uses goleveldb as the storage engine. It is much slower than TiKV, and any benchmarks will be unreliable.

<main class="tabs">
  <input id="tabMacOS" type="radio" name="tabs" value="GoogleContent" checked>
  <label for="tabMacOS">
      <span><img src="https://cloud.google.com/_static/images/cloud/icons/favicons/onecloud/apple-icon.png" width="20"></img></span>
      <span class="label__title">macOS</span>
  </label>
  <input id="tabLinux" type="radio" name="tabs" value="AWSContent">
  <label for="tabLinux">
      <span><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Amazon_Web_Services_Logo.svg/2000px-Amazon_Web_Services_Logo.svg.png" width="20"></img></span>
      <span class="label__title">Linux</span>
  </label>
  <section id="MacOSContent">

<pre>
curl -O https://download.pingcap.org/tidb-master-darwin-amd64.tar.gz
dbdeployer unpack tidb-master-darwin-amd64.tar.gz --unpack-version=3.0.0
dbdeployer deploy single 3.0.0 --client-from=5.7.25
</pre>  

</section>
  <section id="LinuxContent">
 
<pre>
wget https://download.pingcap.org/tidb-master-linux-amd64.tar.gz
dbdeployer unpack tidb-master-linux-amd64.tar.gz --unpack-version=3.0.0
dbdeployer deploy single 3.0.0 --client-from=5.7.25
</pre>

  </section>
</main>
