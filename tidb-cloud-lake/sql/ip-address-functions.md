---
title: IP Address Functions
---

This page provides reference information for the IP address-related functions in Databend. These functions help convert between string and numeric representations of IP addresses.

## IP Address Conversion Functions

| Function | Description | Example |
|----------|-------------|--------|
| [INET_ATON](inet-aton.md) / [IPV4_STRING_TO_NUM](ipv4-string-to-num.md) | Converts an IPv4 address string to a 32-bit integer | `INET_ATON('192.168.1.1')` → `3232235777` |
| [INET_NTOA](inet-ntoa.md) / [IPV4_NUM_TO_STRING](ipv4-num-to-string.md) | Converts a 32-bit integer to an IPv4 address string | `INET_NTOA(3232235777)` → `'192.168.1.1'` |

## Safe IP Address Conversion Functions

These functions handle invalid inputs gracefully by returning NULL instead of raising an error.

| Function | Description | Example |
|----------|-------------|--------|
| [TRY_INET_ATON](try-inet-aton.md) / [TRY_IPV4_STRING_TO_NUM](try-ipv4-string-to-num.md) | Safely converts an IPv4 address string to a 32-bit integer | `TRY_INET_ATON('invalid')` → `NULL` |
| [TRY_INET_NTOA](try-inet-ntoa.md) / [TRY_IPV4_NUM_TO_STRING](try-ipv4-num-to-string.md) | Safely converts a 32-bit integer to an IPv4 address string | `TRY_INET_NTOA(-1)` → `NULL` |
