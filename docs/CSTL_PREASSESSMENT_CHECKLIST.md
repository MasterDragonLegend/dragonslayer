# CSTL pre-assessment checklist

Vendor readiness before contracting a NVLAP-accredited Cryptographic and Security Testing Laboratory (CSTL) for FIPS 140-3 work.

This is a **preparation** list only. Completing it does **not** mean the module is validated.  
**CMVP / FIPS 140-3 certification is not claimed** until an Active certificate is issued.

## A. Scope

- [ ] Module name, version, and embodiment fixed (software / firmware / hardware / hybrid)
- [ ] Cryptographic boundary defined (what is inside / outside the module)
- [ ] Target overall security level (1–4) and per-area levels agreed
- [ ] Operational environments (OE) listed (OS, CPU, platform)
- [ ] Approved vs non-Approved modes of operation described

## B. Algorithms (CAVP path)

- [ ] Inventory of all Approved algorithms, modes, and key sizes inside the boundary
- [ ] Plan for CAVP certificates on each claimed OE (ACVTS via lab)
- [ ] No post-CAVP code changes without a retest plan
- [ ] PQC algorithms (e.g. ML-KEM, ML-DSA, SLH-DSA), if claimed, include CAST expectations per current FIPS 140-3 IG
- [ ] Deprecated or transitioning algorithms excluded or justified

## C. Entropy and RBG (SP 800-90A / 90B / 90C)

- [ ] Entropy source design documented (noise source, conditioning, interfaces)
- [ ] Health tests defined (start-up, continuous, on-demand; e.g. RCT / APT)
- [ ] Raw noise and restart datasets collectable on the real OE
- [ ] DRBG mechanism identified (SP 800-90A) and CAVP-testable
- [ ] Seeding, reseed, and error-state behavior documented
- [ ] RBG construction (SP 800-90C) identified if applicable

## D. Documentation package

- [ ] Finite State Model
- [ ] Security Policy (content aligned with SP 800-140 series expectations)
- [ ] Roles, services, and authentication
- [ ] Sensitive security parameter (SSP) management (generation, storage, zeroization)
- [ ] Self-tests (power-up CAST/KAT, conditional, periodic as required)
- [ ] Administrator and non-administrator guidance
- [ ] Mitigation of other attacks (as claimed)

## E. Engineering access for the lab

- [ ] Source code and/or HDL available under lab NDA
- [ ] Test harness / ACVP client path to exercise algorithms
- [ ] Software/firmware integrity mechanism
- [ ] Physical security evidence plan if Level ≥ 2
- [ ] Build reproducibility notes for the tested version

## F. Program and commercial

- [ ] NVLAP CSTL selected; statement of work clear
- [ ] Tracking ID (TID) and Web Cryptik submission ownership understood (lab-led)
- [ ] Cost recovery and schedule expectations set
- [ ] Modules In Process (MIP) display preference decided (public vs not displayed)
- [ ] **CMVP claim remains false** until Active certificate exists

## G. Validation timeline estimates (indicative only)

These are **planning ranges**, not guarantees. Actual duration depends on module complexity, security level, OE count, submission quality, lab queue, and CMVP backlog. CMVP may drop modules that exceed program deadlines in Review.

| Phase | Typical range | Notes |
|-------|----------------|--------|
| Vendor readiness (this checklist) | 1–6+ months | Boundary, docs, entropy data, CAVP prep |
| CSTL testing (IUT) | 3–9+ months | Algorithm tests, code/docs review, operational tests; longer for Level ≥3 or multi-OE |
| CAVP algorithm certificates | Often concurrent with lab work | ACVTS production access is lab-mediated |
| Entropy (SP 800-90B) evidence | Concurrent; can extend lab phase | Data collection + report review is often critical path |
| CMVP after report submission | Often **~12–18 months** end-to-end industry reports; early FIPS 140-3 averages near **~1.6 years** report→cert in published samples | Queue: Cost Recovery → Pending Review → Review → comment resolution |
| CMVP “Review” program limit | On the order of **24 months** in Review or risk drop (see Management Manual) | Plan resubmission strategy |
| **End-to-end (contract → Active cert)** | Commonly **12–24+ months** | High level, PQC-first, or incomplete packages trend longer |

**Faster paths (relative)**  
- Software Level 1, single OE, complete package, experienced lab  
- Rebrand / update scenarios (when applicable) vs full submission  

**Slower paths (relative)**  
- Level 3–4 physical security, many OEs, weak entropy documentation  
- First-time PQC claims while IG/review practice is still settling  

Automation efforts (e.g. NCCoE ACMVP work) aim to reduce review latency over time; do not assume shorter times until reflected in live MIP statistics.

Always confirm current MIP queue behavior and lab quotes for the specific module.

## H. CMVP testing phases (what the lab and CMVP actually do)

High-level phases after the vendor package is ready:

1. **Kickoff / intake** — SOW, TID, document delivery, optional IUT listing  
2. **Algorithm path (CAVP)** — ACVTS vectors, results, algorithm certificates on claimed OEs  
3. **Entropy path (SP 800-90B)** — raw/restart data, health tests, entropy report  
4. **Module conformance testing (CSTL)** — against ISO/IEC 19790 + 24759, SP 800-140x, and FIPS 140-3 IG  
   - Specification & interfaces  
   - Roles, services, authentication  
   - Software/firmware security & integrity  
   - Operating environment  
   - Physical / non-invasive (as required by level)  
   - SSP management  
   - Self-tests (including algorithm CASTs)  
   - Life-cycle assurance  
5. **Report assembly** — Security Policy, test evidence, Web Cryptik submission  
6. **CMVP MIP states** — Cost Recovery → Pending Review → Review → comment resolution / coordination  
7. **Outcome** — Active certificate **or** drop / fix / resubmit  

Vendors should budget iteration loops in steps 4 and 6; incomplete entropy or self-test evidence is a common delay.

## I. FIPS 140-3 standards map (quick reference)

| Document | Role |
|----------|------|
| **FIPS 140-3** | US federal standard; points at ISO requirements |
| **ISO/IEC 19790** | Security requirements for cryptographic modules |
| **ISO/IEC 24759** | Test requirements (lab assertions) |
| **SP 800-140** series | CMVP-allowed modifications / annex control |
| **FIPS 140-3 IG** | Binding interpretations (self-tests, boundaries, PQC CAST, etc.) |
| **CMVP Management Manual** | Process, MIP states, submission scenarios |
| **CAVP / ACVP** | Algorithm testing (prerequisite) |
| **SP 800-90A/B/C** | DRBG, entropy sources, RBG constructions |

Security levels **1–4** increase assurance (especially physical and identity-based authentication at higher levels). Most software library modules target Level 1.

## J. Risk mitigation strategies

| Risk | Mitigation |
|------|------------|
| Unclear cryptographic boundary | Freeze boundary diagram and service list before lab start; avoid “moving walls” mid-test |
| CAVP / OE mismatch | Run algorithm tests on **every** claimed OE; keep build flags identical to shipping bit |
| Entropy (90B) failure or delay | Collect raw + restart datasets early; document noise source; use vetted conditioning where possible |
| Self-test gaps (esp. PQC) | Map each Approved algorithm to CAST/KAT per current IG before submission |
| Doc churn during Review | Treat Security Policy as controlled; version every lab-facing drop |
| CMVP queue / 24‑month Review limit | Complete package first time; respond to comments on a clock; plan UPDT vs full resubmit |
| Over-claiming “FIPS validated” | Public wording: **not claimed** until Active cert; never say “FIPS compliant” as a substitute |
| Scope creep (extra OEs, Level jump) | Change control with lab; repriced SOW for new OEs or physical level |
| Staff / knowledge loss | Single validation lead + lab-shared evidence index |
| Post-cert changes | Know submission scenarios (UPDT, OEUP, ALG, CVE, …) before shipping hotfixes |

**Program rule for this repository:** integration documentation only — **no CMVP certificate**, **no validation claim**.

## K. ACVP capability registration (algorithm testing)

Official CAVP testing uses **ACVP** against NIST **ACVTS** (demo or production).

**Access**
- **Demo** (`demo.acvts.nist.gov`): request via NIST (CSR for TLS client cert + TOTP); sandbox for client and IUT practice  
- **Prod**: NVLAP **17ACVT** / CST labs only; proficiency on demo required first  

**Registration flow (simplified)**
1. Authenticate (mTLS + TOTP → access token)  
2. Create **test session** with a **capability registration** JSON (algorithms, revisions, modes, key sizes, prereqVals, OE metadata as required)  
3. Server returns **vector set** IDs and prompts  
4. IUT processes prompts → submit results JSON  
5. Server validates → lab continues toward CAVP certificate issuance  

Registration must list only what the **module under test** actually implements on the claimed OE. Over-registering unsupported modes causes failures.

Protocol docs: [pages.nist.gov/ACVP](https://pages.nist.gov/ACVP/) · [github.com/usnistgov/ACVP](https://github.com/usnistgov/ACVP)

## L. NIST PQC standards (module relevance)

| ID | Name | Origin | Role | Status |
|----|------|--------|------|--------|
| **FIPS 203** | ML-KEM | CRYSTALS-Kyber | Key encapsulation | Final (Aug 2024) |
| **FIPS 204** | ML-DSA | CRYSTALS-Dilithium | Signatures | Final (Aug 2024) |
| **FIPS 205** | SLH-DSA | SPHINCS+ | Hash-based signatures (backup) | Final (Aug 2024) |
| **FIPS 206** | FN-DSA | FALCON | Signatures | In development |
| — | **HQC** | Code-based KEM | Backup KEM to ML-KEM | Selected Mar 2025; standard drafting |

For CMVP modules claiming PQC:
- Obtain **CAVP** coverage for each parameter set used  
- Implement **CAST** self-tests per current **FIPS 140-3 IG**  
- Keep public claims aligned: this repo still **does not claim** CMVP validation  

Timeline estimates remain in **§G** (end-to-end commonly 12–24+ months).

## Related references

- [CMVP](https://csrc.nist.gov/projects/cryptographic-module-validation-program)
- [CAVP / ACVP](https://csrc.nist.gov/projects/cryptographic-algorithm-validation-program)
- [FIPS 140-3 IG announcements](https://csrc.nist.gov/projects/cryptographic-module-validation-program/fips-140-3-ig-announcements)
- [SP 800-90B](https://csrc.nist.gov/publications/detail/sp/800-90b/final)
- Repo README: CMVP integration hooks vs certification non-claim

## Status for this repository

`dragonslayer` provides documentation and integration messaging only.  
It is **not** a cryptographic module under test and holds **no** CMVP certificate.
