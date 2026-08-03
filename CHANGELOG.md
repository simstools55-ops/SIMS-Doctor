## 1.0.0-sprint3.3-evidence-engine — 2026-08-04

- Added Evidence Engine foundation
- Added four initial Evidence extraction rules
- Added versioned Evidence thresholds and sample policy to CKB
- Added LOW_SAMPLE retention and flagging
- Added Evidence IDs, Observation linkage, measured values, and comparison basis
- Added deterministic Evidence fingerprint and duplicate prevention
- Added EVIDENCE_RECORDED Medical Record events
- Extended Medical Record schema and counters
- Added unit and integration tests
- Did not add Vital Signs, Findings, or Diagnosis

## 1.0.0-sprint3.2-observation-event-log — 2026-08-04

- Added append-only Medical Record Event Log
- Added sequence, idempotency, and SHA-256 payload integrity checks
- Added Search Console 28/90/365-day Observation input contract
- Added retrieval states COMPLETE, PARTIAL, FAILED, and NO_DATA
- Added Search Console domain models and Observation recording service
- Added Medical Record schema support for events and typed observations
- Added unit, integration, and contract tests
- Did not add live Search Console API retrieval or diagnostic evaluation

## 1.0.0-sprint3.1-ckb — 2026-08-04

- Added Clinical Knowledge Base v1.0
- Added Observation, Evidence, Vital Signs, Findings, and event registries
- Standardized all Vital Signs as “higher is healthier”
- Added normal-range classifications from NORMAL to SEVERE
- Added CKB loader and structural validation
- Added immutable clinical data model foundations
- Added CKB and observation model tests
- Kept diagnosis, scoring formulas, and referrals out of Sprint3.1

# Changelog

## 1.0.0-sprint2.2-foundation — 2026-08-04

- Added Request Receiver, validator and normalizer
- Added Request ID and Case ID generation
- Added active-case reuse by site and article identity
- Added Case Registry and Medical Record reference repositories
- Added initial medical-record generation and request history append
- Added acceptance/rejection result generation
- Added unit and integration tests
- Preserved existing catalog importer, contracts and SBM safety boundary

## 1.0.0-sprint2.1-design — 2026-08-04

- Added provisional JSON Schemas for the four approved Doctor contracts
- Added Case Lifecycle v1
- Added valid and invalid contract fixtures
- Added fixture validation script
- Added SBM compatibility checklist
