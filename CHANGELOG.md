## 1.0.0-sprint6.2-serp-observation — 2026-08-04

- Added provider-neutral SERP acquisition interface
- Added SIMS_DOCTOR_SERP_OBSERVATION_INPUT_V1
- Added intent inference and SERP feature recording
- Added normalized competition metrics
- Added previous SERP comparison
- Added SERP Medical Record Observation integration
- Enabled Competition Resilience Vital Sign
- Added contract, unit, and integration tests
- Did not add provider credentials, browser scraping, or Article Snapshot Observation

## 1.0.0-sprint6.1-search-console-acquisition — 2026-08-04

- Added provider-neutral Search Console acquisition interface
- Added Google Search Console API adapter
- Added 28, 90, and 365-day aggregate retrieval
- Added query-level paging and policy limits
- Added retry for transient provider errors
- Added COMPLETE, PARTIAL, FAILED, and NO_DATA acquisition states
- Added conversion to SIMS_DOCTOR_SEARCH_CONSOLE_OBSERVATION_INPUT_V1
- Added unit and end-to-end Observation integration tests
- Did not add credential storage, OAuth UI, scheduling, or SERP acquisition

## 1.0.0-sprint5.1-treatment-referral — 2026-08-04

- Added Treatment Recommendation Engine
- Added Referral Routing Engine
- Preserved separation between diagnosis, treatment recommendation, and referral
- Added Writer routing for confirmed diagnoses
- Added Observation routing for deferred diagnoses
- Added TREATMENT_RECOMMENDED and REFERRAL_ISSUED events
- Added SIMS_DOCTOR_REFERRAL_V1 schema
- Extended Medical Record counters
- Added unit and integration tests
- Reserved Creator, Merge, noindex, and delete routing for later diagnosis expansion

## 1.0.0-sprint4.3-final-diagnosis — 2026-08-04

- Added Diagnosis Validation and Final Diagnosis Engine
- Added CONFIRMED and DEFERRED outcomes
- Added review dates and event logging

## 1.0.0-sprint4.2-differential-diagnosis — 2026-08-04

- Added Differential Diagnosis Engine
- Added versioned Diagnosis Code Registry
- Added supporting and contradicting Finding rules
- Added confidence scoring, ranking, and low-sample penalty
- Added context-sensitive UPDATE_FAILURE candidate
- Added idempotent DIFFERENTIAL_UPDATED event
- Extended Medical Record schema and counters
- Added unit and integration tests
- Did not add Final Diagnosis, treatment, or referral generation

## 1.0.0-sprint4.1-findings-engine — 2026-08-04

- Added Findings Engine foundation
- Added versioned Finding rules to CKB
- Added severity and confidence calculation
- Linked every Finding to Evidence and Vital Profile
- Added LOW_SAMPLE confidence penalty
- Added deterministic Finding fingerprint and duplicate prevention
- Added FINDING_RECORDED event
- Extended Medical Record schema and counters
- Added unit and integration tests
- Did not add Differential or Final Diagnosis

## 1.0.0-sprint3.4-vital-signs-profile — 2026-08-04

- Added Vital Signs Engine
- Added seven-sign Vital Profile
- Added versioned formula registry to CKB
- Implemented Visibility, Traffic, CTR Health, Ranking Stability, and Freshness
- Marked Competition Resilience and Content Integrity as UNAVAILABLE pending observations
- Added normal-range classification and overall profile score
- Added LOW_SAMPLE confidence and score adjustments
- Added idempotent VITAL_SIGNS_CALCULATED event
- Extended Medical Record schema and counters
- Added unit and integration tests
- Did not add Findings or Diagnosis

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
