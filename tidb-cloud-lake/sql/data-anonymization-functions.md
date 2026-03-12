---
title: Data Anonymization Functions
---

Data anonymization is the process of altering or removing personally identifiable information (PII) from data sets to protect individual privacy. Its goal is to transform data so it cannot be linked back to specific individuals, while preserving the data's utility for analysis, research, and testing.

### Common Data Categories for Anonymization

Effective anonymization strategies typically target specific categories of sensitive data:

*   **Direct Identifiers (PII)**: Information that explicitly identifies a person, such as full names, email addresses, phone numbers, and government IDs.
*   **Indirect Identifiers (Quasi-Identifiers)**: Attributes that can identify individuals when combined with other data sources, such as dates of birth, gender, zip codes, or job titles.
*   **Sensitive Business Data**: Confidential information like financial transactions, salary details, or proprietary internal records that need protection in non-production environments.

### Databend Anonymization Techniques

Databend provides a set of functions to implement various anonymization techniques, including data masking, pseudonymization, and synthetic data generation:

- **Data Masking**: Use the [`OBFUSCATE` table function](obfuscate.md) to automatically apply masking rules to columns, replacing original values with artificial ones that appear genuine.
- **Pseudonymization**: Use [FEISTEL_OBFUSCATE](feistel_obfuscate.md) to replace identifiers with deterministic substitutes. This preserves data integrity and cardinality, making it suitable for maintaining join keys.
- **Synthetic Data**: Use [MARKOV_TRAIN](../07-aggregate-functions/aggregate-markov-train.md) and [MARKOV_GENERATE](markov_generate.md) to produce machine-generated data that statistically resembles the original dataset but has no direct connection to real records.

| Function | Description |
|----------|-------------|
| [MARKOV_GENERATE](markov_generate.md) | Generate anonymized strings based on a Markov model |
| [FEISTEL_OBFUSCATE](feistel_obfuscate.md) | Obfuscate numbers using a Feistel cipher |
| [OBFUSCATE](obfuscate.md) | Table-level masking using built-in rules |
