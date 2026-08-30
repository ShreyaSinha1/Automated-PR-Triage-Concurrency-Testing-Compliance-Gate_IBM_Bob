# 🛡️ Enterprise Engineering Compliance Manifest (v2.1)

This document contains strict structural, architectural, and security constraints for all applications. Any Pull Request that violates these rules must be rejected, patched, and verified before merging.

## 1. Security & Authentication Constraints
*   **Token Enforcement:** All application routes (excluding health checks `/health`) must enforce authentication. No open endpoints are allowed.
*   **Secrets Exposure:** Hardcoded credentials, plain-text API keys, or simulated bearer tokens (e.g., strings containing "secret_key_123") are strictly forbidden. All configurations must pull from environment variables.

## 2. Code Resiliency & Error Handling
*   **Unhandled Exceptions:** Bare `except:` or global catches that suppress errors without returning structured JSON responses to the client are banned.
*   **Database Rollbacks:** (If applicable) Every schema modification or execution pathway must wrap database operations in a try/except block ensuring transaction cleanup.

## 3. CI/CD Validation Requirements
*   **Pre-Merge Unit Tests:** All test suites must execute successfully with zero failures before a merge.
*   **Automated Validation:** If compliance rules are broken, an automated patch must be generated, checked for basic syntax health, and re-tested using the test suite.
