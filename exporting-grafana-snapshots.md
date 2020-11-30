---
title: Exporting Grafana Snapshots
summary: How to export snapshots of Grafana Dashboard, and how to visualize these files
aliases: ['/docs/dev/exporting-grafana-snapshots']
---

# Exporting Grafana Snapshots

Metrics data is important in troubleshooting. When requesting remote assistant, sometimes they need to view the Grafana dashboards to diagnosing problems. PingCAP developed [MetricsTool](https://metricstool.pingcap.com/) to help exporting snapshots of Grafana dashboards as local files and visualizing these snapshots. Users can share these snapshots to allow outsiders accurately read out the graphs, without giving out access to other sensitive information on the Grafana server.

## Usage

PingCAP MetricsTool can be accessed from **<https://metricstool.pingcap.com/>**. It consists of 3 sets of tools:

* **Export**: A user script running on the browser's Developer Tool, allowing user to download a snapshot of all visible panels in the current dashboard on any Grafana v6.x.x server.

    ![Screenshot of MetricsTool Exporter after running the user script](/media/metricstool-export.png)

* **Visualize**: A web page visualizing the exported snapshot files. The visualized snapshots can be operated as if live Grafana dashboards.

    ![Screenshot of MetricsTool Visualizer](/media/metricstool-visualize.png)

* **Import**: Instructions to import the exported snapshot back into an actual Grafana instance.

## FAQs

### What is the advantage of this tool compared with screenshot or PDF printing?

The snapshot files exported by MetricsTool contain the actual values when they are taken. And the Visualizer allows you to interact with the rendered graphs as if it is a live Grafana dashboard, supporting operations like toggling series, zooming into a smaller time range, and checking the precise value at a given time. This makes MetricsTool much more powerful than images or PDFs.

### What are included in the snapshot file?

The snapshot file contains the values of all graphs and panels in the selected time range. It does not save the original metrics from the data sources (and thus you cannot edit the query expression in the Visualizer).

### Will the Visualizer save the uploaded snapshot files in PingCAP’s servers?

No, the Visualizer parses the snapshot files entirely inside your browser. Nothing will be sent to PingCAP. You are free to view snapshot files received from sensitive sources, and no need to worry about these leaking to third parties through the Visualizer.

### Can it export metrics besides Grafana?

No, we only support Grafana v6.x.x at the moment.

### Will there be problems to execute the script before all metrics are loaded?

No, the script UI will notify users to wait for all metrics being loaded. However, users can manually skip waiting and export the snapshot in case of some metrics loading for too long.

### Can we share a link to a visualized snapshot?

No, but you can share the snapshot file, with instruction how to use the Visualizer to view it. If you truly need a world-readable URL, you may also try the public snapshot.raintank.io service built into Grafana, but make sure all privacy concerns are cleared before doing so.
