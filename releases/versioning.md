---
title: TiDB Versioning
summary: Learn the version numbering system of TiDB.
---

# TiDB Versioning

<Important>
It is recommended to always upgrade to the latest patch release of your release series.
</Important>

Starting from TiDB v6.0.0, TiDB has introduced a new release series, DMR. Currently TiDB has two release series:

* Long-Term Support Releases (LTS)
* Development Milestone Releases (DMR)

For the versioning system of TiDB v5.0.0 and earlier versions, refer to [Historical versioning](#historical-versioning-deprecated).

## Release versioning

TiDB versioning has the form of `X.Y.Z`.

- Since TiDB 1.0, `X` increments every year. Each `X` release introduces new features and improvements.
- `Y` increments from 0. Each `Y` release introduces new features and improvements. `X.Y` represents a release series.
- `Z` is the patch release number. The first release of a release series `X.Y` has `Z` set to 0. For patch releases, `Z` increments from 1.

| Release series | Definition | Naming convention | Example |
| :--- | :----- | :---| :---|
| Long-Term Support Releases (LTS) | LTS are released approximately every six months and introduce new features, improvements and bug fixes. During its lifecycle, patch releases based on the current release series are released on demand. | `X.Y.Z`. `Z` defaults to 0. | 6.1.0<br/>5.4.0 |
| Development Milestone Releases (DMR) | DMR are released approximately every two months that do not contain LTS. DMR introduce new features, improvements and bug fixes. Patch releases based on DMR are not available, and any related bugs are fixed in the subsequent release series. | `X.Y.Z` with the `-DMR` suffix. `Z` defaults to 0. | 6.0.0-DMR |
| Patch Releases | Patch releases are made available on demand during the lifecycle of LTS. Patch releases contain bug fixes and security vulnerability fixes, and do not introduce new features. | `X.Y.Z`. `X.Y` follows the LTS naming, and `Z` increments from 1. | 6.1.1 |

## Versioning of TiDB ecosystem tools

Some TiDB tools are released together with TiDB server and use the same version numbering system. Some TiDB tools are released separately from the TiDB server and use their own version numbering system, such as TiUP and TiDB Operator.

## Historical versioning (deprecated)

### General Availability Releases

General Availability Releases (GA) are stable versions of the current release series of TiDB. GA are released after Release Candidate Releases (RC). GA can be used in production environments.

Example versions:

- 1.0
- 2.1 GA
- 5.0 GA

### Release Candidate Releases

Release Candidate Releases (RC) introduce new features and improvements. RC are significantly more stable than Beta releases. RC can be used for early testing, but are not suitable for production.

Example versions:

- RC1
- 2.0-RC1
- 3.0.0-rc.1

### Beta Releases

Beta Releases introduces new features and improvements. Beta Releases are greatly improved over Alpha Releases and have eliminated critical bugs, but still contain some bugs. Beta Releases are available for users to test the latest features.

Example versions:

- 1.1 Beta
- 2.1 Beta
- 4.0.0-beta.1

### Alpha Releases

Alpha Releases are internal releases for testing and introduce new features and improvements. Alpha releases are the initial versions of the current release series. Alpha Releases might have some bugs and are available for users to test the latest features.

Example versions:

- 1.1 Alpha
