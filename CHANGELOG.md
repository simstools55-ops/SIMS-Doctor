## 1.0.0-sprint8.2-persistent-batch-queue — 2026-08-04

- Added storage-neutral persistent Batch Queue
- Added queue record contract
- Added idempotent enqueue
- Added lease-based worker locking and expired-lock recovery
- Added item-level durable checkpoints
- Added retry scheduling with backoff
- Added pause and resume
- Added Nightly Batch Worker cycle
- Added incomplete-batch discovery and lifecycle events
- Added contract, unit, integration, and regression tests
- Did not add production database, cron deployment, parallel workers, external notifications, or SBM batch UI

## 1.0.0-sprint8.1-batch-doctor-foundation — 2026-08-04

- Added Batch Doctor request and result contracts
- Added per-article Case isolation
- Added longitudinal, severity, recurrence, and traffic-opportunity priority scoring
- Added priority-ordered batch execution
- Added continue-after-case-failure behavior
- Added resume and retry-limit foundation
- Added aggregate Writer, Creator, Merge, and follow-up counts
- Added contract, unit, integration, and regression tests
- Did not add persistent queues, scheduling, parallel workers, or SBM batch UI

## 1.0.0-sprint7.4-longitudinal-medical-record — 2026-08-04

- Added Longitudinal Medical Record Analysis
- Added repeated diagnosis, dominant diagnosis, and recurrence counting
- Added chronic-case detection
- Added treatment responsiveness and resistance analysis
- Added repeated defer-pattern and recent-recurrence detection
- Added follow-up priority
- Added SIMS_DOCTOR_LONGITUDINAL_PROFILE_V1
- Added LONGITUDINAL_PROFILE_UPDATED event and Medical Record profile history
- Added contract, unit, integration, and regression tests
- Did not add batch diagnosis, scheduling, cross-site aggregation, or automatic treatment

## 1.0.0-sprint7.3-improvement-history — 2026-08-04

- Added Improvement History Comparison
- Added baseline and post-treatment checkpoint analysis
- Added weighted clicks, impressions, CTR, and position effect score
- Added improvement, no-effect, worsening, mixed-response, and insufficient-follow-up classifications
- Added treatment-response Evidence and Findings
- Added TREATMENT_SUCCESS, IMPROVEMENT_FAILURE, POST_IMPROVEMENT_WORSENING, MIXED_TREATMENT_RESPONSE, and FOLLOW_UP_REQUIRED diagnoses
- Added Writer review for ineffective or worsening treatment
- Added Observation routing for success and follow-up cases
- Added contract, unit, integration, and regression tests
- Did not add automatic rollback or article restoration

## 1.0.0-sprint7.2-long-term-decline — 2026-08-04

- Added long-term 365-day window analysis
- Added gradual decline, sharp decline, CTR decay, position decay, seasonality, and recovery classification
- Added Long-Term Observation contract
- Added long-term Evidence and Findings engines
- Added LONG_TERM_DECAY, SEASONAL_DECLINE, and RECOVERY_IN_PROGRESS diagnoses
- Added Writer and Observation routing
- Added contract, unit, integration, and regression tests
- Did not add core-update calendar correlation, external seasonality data, or batch diagnosis

## 1.0.0-sprint7.1-cross-article-cannibalization — 2026-08-04

- Added Cross-Article Observation contract and analyzer
- Added shared-query, title-similarity, and intent-similarity evaluation
- Added Cannibalization, Merge Candidate, and New Article Opportunity findings
- Added CANNIBALIZATION, ARTICLE_MERGE_REQUIRED, and NEW_ARTICLE_NEEDED diagnoses
- Activated Merge and Creator routing
- Added Cross-Article Findings Engine
- Added contract, unit, integration, and regression tests
- Did not add actual merge, creation, deletion, noindex, or batch diagnosis execution

## 1.0.0-sprint6.5-diagnosis-report-output — 2026-08-04

- Added user-facing Japanese Diagnosis Report
- Added SIMS_DOCTOR_SINGLE_CASE_RESULT_V1
- Added SIMS_DOCTOR_WRITER_REQUEST_V1
- Added Writer treatment goals and preservation constraints
- Added confirmed and deferred output handling
- Added OUTPUT_GENERATED event
- Added Medical Record output history and counters
- Added contract, unit, integration, and regression tests
- Did not add Creator, Merge, SBM import, or graphical UI implementations

## 1.0.0-sprint6.4-clinical-pipeline — 2026-08-04

- Added Clinical Pipeline Orchestrator
- Added end-to-end coordination from Observation through Referral
- Added partial Observation failure tolerance
- Added stop-on-clinical-step failure
- Added idempotent replay and resume foundation
- Added CLINICAL_PIPELINE_COMPLETED event
- Added SIMS_DOCTOR_CLINICAL_PIPELINE_RESULT_V1
- Added Medical Record pipeline history and counters
- Added unit and integration tests
- Did not add persistent queueing, scheduling, credentials, or user-facing report rendering

## 1.0.0-sprint6.3-article-snapshot — 2026-08-04

- Added SIMS_DOCTOR_ARTICLE_SNAPSHOT_INPUT_V1
- Added Article Snapshot models and Medical Record integration
- Added title, headings, FAQ, internal links, metrics, and freshness observations
- Added previous-snapshot structural comparison
- Enabled Content Integrity Vital Sign
- Completed availability path for all seven Vital Signs
- Added contract, unit, integration, and regression tests
- Did not add live crawling, CMS-specific parsing, or content editing

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
