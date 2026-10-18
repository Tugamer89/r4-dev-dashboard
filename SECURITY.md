# Security Policy

We take the security of the R4 Dev Dashboard project seriously. This document outlines the supported versions, how to report vulnerabilities, and our disclosure process.

## Supported Versions

As this project is under active development, security fixes and updates are applied **exclusively to the latest stable version** available on the main branch (`main`). Older versions are not supported for security bug fixes.

| Version | Supported          |
| ------- | ------------------ |
| latest  | :white_check_mark: |
| < latest| :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability within this project (affecting either the C++ firmware, Python daemon, or build/release pipelines), please report it responsibly.

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via one of the following methods:

* **Private Vulnerability Reporting:** Use the [GitHub Security Advisories "Report a Vulnerability"](https://github.com/tugamer89/r4-dev-dashboard/security/advisories/new) tab in this repository.
* **Direct Contact:** Reach out directly to the maintainers via their profile email/contact information listed on the repository.

### What to Include in Your Report

To help us triage and fix the issue as quickly as possible, please provide:

1. **Description:** A summary of the vulnerability and its potential impact.
2. **Components Affected:** Specify whether it affects the `firmware/`, `daemon/`, or auxiliary scripts.
3. **Steps to Reproduce:** Clear instructions, proof-of-concept code, or logs to demonstrate the issue.
4. **Environment:** Hardware setup (e.g., Arduino R4 board model), operating system, and Python/PlatformIO versions if applicable.

## Disclosure Policy

We follow a coordinated disclosure process:

1. **Acknowledgment:** We will acknowledge receipt of your vulnerability report within 48-72 hours.
2. **Investigation:** The maintainers will investigate the issue and verify the impact.
3. **Fix & Release:** We will work on a patch and coordinate a release date with you.
4. **Public Disclosure:** Once the security patch is published, we will credit the reporter (unless requested otherwise) in the security advisory.
