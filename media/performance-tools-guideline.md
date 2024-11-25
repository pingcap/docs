---
title: TiDB Performance Troubleshooting Guide
summary: learn how to use performance tools in TiDB for efficiently performance troubleshooting 
---

# TiDB Performance Troubleshooting Guide

## Important Background

TiDB is designed with comprehensive instrumentation in mind, featuring a well-organized system of over 1000 metrics. Similar to MySQL, it provides essential monitoring capabilities through TopSQL views and slow query logs.
In real-world use cases, performance troubleshooting in distributed databases like TiDB still presents unique challenges that can overwhelm even experienced database administrators. While TiDB offers powerful features at its core, it operates on fundamental database principles that we can systematically analyze and optimize.

### Current Challenges

#### 1. Tool Complexity

TiDB provides various performance monitoring and debugging tools:

* **TiDB Dashboard** for visual monitoring
* **Grafana metrics** for detailed performance data
* **System views** for internal state analysis
* **Log files** for event tracking
* **Advanced tools** including:
  * Command-line utilities
  * Continuous profilers
  * Trace files

#### 2. Learning Curve
Many users, especially those new to distributed systems, find themselves:

* Overwhelmed by the variety of available tools
* Uncertain about which metrics matter most
* Struggling to correlate data from different sources
* Unable to identify true performance bottlenecks

#### 3. Common Pitfalls
A frequent trap for beginners is:
* Getting lost in the abundance of metrics, there are over 1000 existing metrics, and there are missing descriptions in user docs for metrics, tables, logs 
* Missing the holistic view of system performance and over-focusing on individual performance indicators
* Following incorrect troubleshooting paths

### Document Purpose

This guide aims to bridge the gap between TiDB's complexity and practical performance optimization by:

1. Providing a structured methodology for performance troubleshooting that's accessible to beginners
2. Focusing on real-world use cases rather than theoretical tool documentation
3. Teaching how to correlate different monitoring tools effectively
4. Building a systematic approach to identifying true bottlenecks

### Methodological Approach

We introduce two fundamental approaches that align with traditional database performance analysis while accounting for TiDB's distributed nature:

#### 1. Database Time Analysis



* Leverages both statement summaries and metrics
* Provides multiple perspectives on performance issues
* Helps identify whether bottlenecks are inside or outside TiDB
* Enables systematic drilling down from high-level symptoms to root causes

#### 2. Database CPU Analysis

* Focuses on resource utilization patterns
* Uses Top SQL features to identify high-impact queries
* Helps understand load distribution across nodes
* Enables targeted optimization of resource-intensive operations

---

This document emphasizes practical, actionable approaches over theoretical understanding, ensuring users can effectively troubleshoot performance issues while building their expertise with TiDB's advanced features.

[Rest of the document follows...]