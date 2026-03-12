---
title: Compliance & Security
---

# Databend Security Design

Databend Cloud is built with security at its core, providing comprehensive protection for your data through multiple security layers, encryption standards, and compliance certifications.

## Security

Databend Cloud implements multiple security layers to protect your data and control access to your resources:

### Access Control

Databend uses a comprehensive access control system that combines:

- **Role-Based Access Control (RBAC)**: Manages permissions through roles assigned to users
- **Discretionary Access Control (DAC)**: Allows resource owners to directly grant permissions

### Data Protection

**Masking Policy**
Protects sensitive data by controlling how it's displayed to different users, helping you comply with privacy regulations while still allowing authorized access.

**Network Policy**
Controls which IP addresses can connect to your Databend resources, allowing you to restrict access to specific networks or locations.

**Password Policy**
Enforces strong passwords with customizable requirements for length, complexity, and rotation to prevent unauthorized access.

### Secure Connectivity

**AWS PrivateLink**
Enables private connections between your VPC and Databend Cloud without exposing traffic to the public internet. Currently available on AWS only.

## Encryption

### TLS 1.2

We provide end-to-end encryption for all communication. All customer data flows are solely over HTTPS. Connections are encrypted using TLS 1.2 from clients through to the Databend API gateway, ensuring:

- Data confidentiality during transit
- Protection against man-in-the-middle attacks
- Secure client-server communication

### Storage Encryption

Databend Enterprise supports server-side encryption in Object Storage Service (OSS). This feature enables you to enhance data security and privacy by activating server-side encryption for data stored in OSS. You can choose the encryption method that best suits your needs:

- AES-256 encryption
- Customer-managed keys (CMK)
- Hardware security module (HSM) integration options

## Compliance

At Databend, we prioritize data security and privacy, and have achieved key compliances that validate our commitment to protecting your data. Our security practices are regularly audited by independent third parties to ensure we meet the highest industry standards.

### SOC 2 Type II

We have successfully attained SOC 2 Type II compliance, validated by independent auditors. This certification confirms that our systems adhere to the American Institute of Certified Public Accountants (AICPA) trust service criteria for security, availability, processing integrity, confidentiality, and privacy. We continuously monitor and enhance our operational controls to maintain this standard.

### GDPR

Databend adheres to the General Data Protection Regulation (GDPR), the European Union's regulation designed to protect individuals' privacy and personal data. Our compliance includes strict data privacy enforcement, robust encryption, and regular privacy audits to ensure the rights and data privacy of our users across the EU are protected.
