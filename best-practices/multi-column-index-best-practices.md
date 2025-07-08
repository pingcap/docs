---
title: Best Practices for Optimizing Multi-Column Indexes
summary: Learn how to use multi-column indexes effectively in TiDB and apply advanced optimization techniques.
---

# Best Practices for Optimizing Multi-Column Indexes

In today's data-driven world, efficiently handling complex queries on large datasets is critical to keeping applications responsive and performant. For TiDB, a distributed SQL database designed to manage high-scale and high-demand environments, optimizing data access paths is essential to delivering smooth and efficient queries.

Indexes are a powerful tool for improving query performance by avoiding the need to scan all rows in a table. TiDB's query optimizer leverages multi-column indexes to intelligently filter data, handling complex query conditions that traditional databases such as MySQL cannot process as effectively.

This document walks you through how multi-column indexes function, why they are crucial, and how TiDB's optimization transforms intricate query conditions into efficient access paths. After optimization, you can achieve faster responses, minimized table scans, and streamlined performance, even at massive scale.

Without these optimizations, query performance in large TiDB databases can degrade quickly. Full table scans and inadequate filtering can turn milliseconds into minutes. Additionally, excessive memory use can lead to out-of-memory (OOM) errors, especially in constrained environments. TiDB's targeted approach ensures only relevant data is accessed. This keeps latency low and memory usage efficient, even for the most complex queries.

## Prerequisites

- The multi-column index feature is available in TiDB v8.3 and later versions.
- Before using this feature, you must set the value of the [optimizer fix control **54337**](/optimizer-fix-controls.md#54337-new-in-v830) to `ON`.

## Background: multi-column indexes

This document takes an example of a rental listings table defined as follows. In this example, each listing contains a unique ID, city, number of bedrooms, rent price, and availability date:

```sql
CREATE TABLE listings (
    listing_id INT PRIMARY KEY AUTO_INCREMENT,
    city VARCHAR(100) NOT NULL,
    bedrooms INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    availability_date DATE NOT NULL
);
```

Suppose this table has 20 million listings across the United States. If you want to find all listings with a price under $2,000, you can add an index on the price column. This index allows the optimizer to filter out rows, scanning only the range `[-inf, 2000.00)`. This helps reduce the search to about 14 million rows (assuming 70% of rentals are priced above `$2,000`). In the query execution plan, TiDB performs an index range scan on price. This limits the need for a full table scan and improves efficiency.

```sql
-- Query 1: Find listings with price < 2000
EXPLAIN FORMAT = "brief" SELECT * FROM listings WHERE price < 2000;
```

```
+-----------------------------+---------+----------------------------------------------+---------------------------+
| id                          | task    | access object                                | operator info             |
+-----------------------------+---------+----------------------------------------------+---------------------------+
| IndexLookUp                 | root    |                                              |                           |
| ├─IndexRangeScan(Build)     | root    | table: listings, index: price_idx(price)     | range: [-inf, 2000.00)    |
| └─TableRowIDScan(Probe)     | root    | table: listings                              |                           |
+-----------------------------+---------+----------------------------------------------+---------------------------+
```

While this filter improves performance, it might still return a large number of rows. This is not ideal for a user looking for more specific listings. Adding filters, such as specifying the city, number of bedrooms, and a maximum price, narrows the results significantly. For example, a query to find two-bedroom listings in San Francisco under `$2,000` is more useful, likely returning only a few dozen rows.

To optimize this query, you can create a multi-column index on `city`, `bedrooms`, and `price` as follows:

```sql
CREATE INDEX idx_city_bedrooms_price ON listings (city, bedrooms, price);
```

Multi-column indexes in SQL are ordered lexicographically. In the case of an index on `(city, bedrooms, price)`, the data is first sorted by `city`, then by `bedrooms` within each city, and finally by `price` within each `(city, bedrooms)` combination. This ordering lets TiDB efficiently access rows based on each condition:

1. Filter by `city`, which is the primary filter.
2. Optionally filter by `bedrooms` within that city.
3. Optionally filter by `price` within the city-bedroom grouping.

## Sample data

The following table shows a sample dataset that illustrates how multi-column indexing refines search results:

| City          | Bedrooms | Price |
| ------------- | -------- | ----- |
| San Diego     | 1        | 1000  |
| San Diego     | 1        | 1500  |
| San Diego     | 2        | 1000  |
| San Diego     | 2        | 2500  |
| San Diego     | 3        | 1000  |
| San Diego     | 3        | 2500  |
| San Francisco | 1        | 1000  |
| San Francisco | 1        | 1500  |
| San Francisco | 2        | 1000  |
| San Francisco | 2        | 1500  |
| San Francisco | 3        | 2500  |
| San Francisco | 3        | 3000  |

## Optimized queries and results

Using the multi-column index, TiDB can efficiently narrow the scan range to find listings in San Francisco with two bedrooms and a price under $2,000:

```sql
-- Query 2: Find two-bedroom listings in San Francisco under $2,000
EXPLAIN FORMAT = "brief"
    SELECT * FROM listings
    WHERE city = 'San Francisco' AND bedrooms = 2 AND price < 2000;
```

```
+------------------------+------+---------------------------------------------------------------------------------------------+---------------------------------+
| id                     | task | access object                                                                               | operator info                   |
+------------------------+------+---------------------------------------------------------------------------------------------+---------------------------------+
| IndexLookUp            | root |                                                                                             |                                 |
| ├─IndexRangeScan(Build)| root |table:listings,index:idx_city_bedrooms_price ["San Francisco" 2 -inf,(city, bedrooms, price)]|range:["San Francisco" 2 2000.00)|
| └─TableRowIDScan(Probe)| root |table:listings                                                                               |                                 |
+------------------------+------+---------------------------------------------------------------------------------------------+---------------------------------+
```

This query returns the following filtered results from the sample data:

| City          | Bedrooms | Price |
|---------------|----------|-------|
| San Francisco |    2     | 1000  |
| San Francisco |    2     | 1500  |

By using a multi-column index, TiDB avoids unnecessary row scanning and significantly boosts query performance.

## Index range derivation

The TiDB optimizer includes a powerful range derivation component. It is designed to take a query's conditions and relevant index columns and generate efficient index ranges for table access. This derived range then feeds into TiDB's table access component, which determines the most resource-efficient way to access the table.

For each table in a query, the table access component evaluates all applicable indexes to identify the optimal access method—whether through a full table scan or an index scan. It calculates the range for each relevant index, assesses the access cost, and selects the path with the lowest cost. This process combines range derivation with a cost assessment subsystem to find the most efficient way to retrieve data, balancing performance and resource usage.

The diagram below illustrates how the range derivation and cost assessment work together within TiDB's table access logic to achieve optimal data retrieval.

![Table Access Path Selection](/media/best-practices/multi-column-index-table-access-path-selection.png)

Multi-column filters are often more complex than the basic examples discussed earlier. They might include **AND** conditions, **OR** conditions, or a combination of both. TiDB's range derivation subsystem is designed to handle these cases efficiently, generating the most selective (and therefore, most effective) index ranges.

In general, the subsystem applies a **UNION** operation for ranges generated from **OR** conditions and an **INTERSECT** operation for ranges derived from **AND** conditions. This approach ensures that TiDB can filter data as precisely as possible, even with complex filtering logic.

## Disjunctive conditions (`OR` conditions) in multi-column indexes

When there are `OR` conditions in a query (known as "disjunctive predicates"), the optimizer handles each condition separately, creating a range for each part of the `OR` condition. If any of these ranges overlap, the optimizer merges them into one continuous range. If they do not overlap, they remain as separate ranges, both of which can still be used for an index scan.

### Example 1: overlapping ranges

Consider a query that looks for listings in New York with two bedrooms, where the price falls into one of two overlapping ranges:

- Price between `$1,000` and `$2,000`
- Price between `$1,500` and `$2,500`

In this case, the two ranges overlap, so the optimizer combines them into a single range from `$1,000` to `$2,500`. Here is the query and its execution plan:

```sql
-- Query 3: Overlapping price ranges
EXPLAIN FORMAT = "brief"
    SELECT * FROM listings
    WHERE (city = 'New York' AND bedrooms = 2 AND price >= 1000 AND price < 2000)
       OR (city = 'New York' AND bedrooms = 2 AND price >= 1500 AND price < 2500);
```

```
+-------------------------+------+----------------------------------------------------------------------+--------------------------------------------------+
| id                      | task | access object                                                        | operator info                                    |
+-------------------------+------+----------------------------------------------------------------------+--------------------------------------------------+
| IndexLookUp             | root |                                                                      |                                                  |
| ├─IndexRangeScan(Build) | root | table:listings,index:idx_city_bedrooms_price(city, bedrooms, price)  | range:["New York" 2 1000.00,"New York" 2 2500.00)|
| └─TableRowIDScan(Probe) | root | table:listings                                                       |                                                  |
+-------------------------+------+----------------------------------------------------------------------+--------------------------------------------------+
```

### Example 2: non-overlapping ranges

In a different scenario, imagine a query that looks for affordable single-bedroom listings in either San Francisco or San Diego. Here, the `OR` condition specifies two distinct ranges for different cities:

- Listings in San Francisco, 1 bedroom, priced between `$1,500` and `$2,500`
- Listings in San Diego, 1 bedroom, priced between `$1,000` and `$1,500`

Because the index ranges do not overlap, they remain separate in the execution plan, with each city having its own index range:

```sql
-- Query 4: Non-overlapping ranges for different cities

EXPLAIN FORMAT = "brief"
    SELECT * FROM listings
    WHERE
        (city = 'San Francisco' AND bedrooms = 1 AND price >= 1500 AND price < 2500)
     OR (city = 'San Diego' AND bedrooms = 1 AND price >= 1000 AND price < 1500);
```

```
+-------------------------+------+--------------------------------------------------------------------+------------------------------------------------------------+
| id                      | task | access object                                                      | operator info                                              |
+-------------------------+------+--------------------------------------------------------------------+------------------------------------------------------------+
| IndexLookUp             | root |                                                                    |                                                            |
| ├─IndexRangeScan(Build) | root | table:listings,index:idx_city_bedrooms_price(city, bedrooms, price)| range:["San Francisco" 1 1500.00,"San Francisco" 1 2500.00)|
| └─TableRowIDScan(Probe) | root | table:listings                                                     |       ["San Diego" 1 1000.00,"San Diego" 1 1500.00)        |
+-------------------------+------+--------------------------------------------------------------------+------------------------------------------------------------+
```

By creating either merged or distinct ranges based on overlap, the optimizer can efficiently use indexes for `OR` conditions, avoiding unnecessary scans and improving query performance.

## Conjunctive conditions (`AND` conditions) in multi-column indexes

For queries with **AND** conditions (also known as conjunctive conditions), the TiDB optimizer creates a range for each condition. It then finds the overlap (intersection) of these ranges to get a precise result for index access. If each condition has only one range, this is straightforward, but it becomes more complex if any condition contains multiple ranges. In such cases, TiDB combines these ranges to produce the most selective, efficient result.

### Example 1: table setup

Consider a table `t1` that is defined as follows:

```sql
CREATE TABLE t1 (
    a1 INT,
    b1 INT,
    c1 INT,
    KEY iab (a1,b1)
);
```

Suppose you have a query with the following conditions:

```sql
(a1, b1) > (1, 10) AND (a1, b1) < (10, 20)
```

This query involves comparing multiple columns, and requires the TiDB optimizer to process it in the following two steps:

1. Translate the expressions.

    The TiDB optimizer breaks down these complex conditions into simpler parts.

    - `(a1, b1) > (1, 10)` translates to `(a1 > 1) OR (a1 = 1 AND b1 > 10)`, meaning it includes all cases where `a1` is greater than `1` or where `a1` is exactly `1` and `b1` is greater than `10`.
    - `(a1, b1) < (10, 20)` translates to `(a1 < 10) OR (a1 = 10 AND b1 < 20)`, covering cases where `a1` is less than `10` or where `a1` is exactly `10` and `b1` is less than `20`.

    These expressions are then combined using `AND`:

    ```sql
    ((a1 > 1) OR (a1 = 1 AND b1 > 10)) AND ((a1 < 10) OR (a1 = 10 AND b1 < 20))
    ```

2. Derive and combine ranges.

    After breaking down the conditions, the TiDB optimizer calculates ranges for each part and combines them. For this example, it derives:

    - For `(a1, b1) > (1, 10)`: it creates ranges such as `(1, +inf]` for cases where `a1 > 1` and `(1, 10, 1, +inf]` for cases where `a1 = 1` and `b1 > 10`.
    - For `(a1, b1) < (10, 20)`: it creates ranges `[-inf, 10)` for cases where `a1 < 10` and `[10, -inf, 10, 20)` for cases where `a1 = 10` and `b1 < 20`.

    The final result combines these to get a refined range: `(1, 10, 1, +inf] UNION (1, 10) UNION [10, -inf, 10, 20)`.

### Example 2: query plan

The following query plan shows the derived ranges:

```sql
-- Query 5: Conjunctive conditions on (a1, b1)
EXPLAIN FORMAT = "brief"
    SELECT * FROM t1
    WHERE (a1, b1) > (1, 10) AND (a1, b1) < (10, 20);
```

```
+-------------------------+------+----------------------------+-------------------------------------------+
| id                      | task | access object              | operator info                             |
+-------------------------+------+----------------------------+-------------------------------------------+
| IndexLookUp             | root |                            |                                           |
| ├─IndexRangeScan(Build) | root | table:t1,index:iab(a1, b1) | range:(1 10,1 +inf],(1,10)[10 -inf,10 20) |
| └─TableRowIDScan(Probe) | root | table:t1                   |                                           |
+-------------------------+------+----------------------------+-------------------------------------------+
```

In this example, the table has about 500 million rows. However, this optimization allows TiDB to narrow down the access to only around 4,000 rows, just 0.0008% of the total data. This refinement drastically reduces query latency to a few milliseconds, as opposed to over two minutes without optimization.

Unlike MySQL, which requires a full table scan for such conditions, the TiDB optimizer can handle complex row expressions efficiently by leveraging these derived ranges.

## Conclusion

The TiDB optimizer uses multi-column indexes and advanced range derivation to significantly lower data access costs for complex SQL queries. By effectively managing both conjunctive (`AND`) and disjunctive (`OR`) conditions, TiDB converts row-based expressions into optimal access paths, reducing query times and enhancing performance. Unlike MySQL, TiDB supports union and intersection operations on multi-column indexes, allowing efficient processing of intricate filters. In practical use, this optimization enables TiDB to complete queries in just a few milliseconds—compared to over two minutes without it, demonstrating a substantial reduction in latency.

Check out the [comparison white paper](https://www.pingcap.com/ebook-whitepaper/tidb-vs-mysql-product-comparison-guide/) to discover even more differences between MySQL and TiDB's architecture, and why this matters for scalability, reliability, and hybrid transactional and analytical workloads.
