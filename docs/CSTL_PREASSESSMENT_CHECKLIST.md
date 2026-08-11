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

## Related references

- [CMVP](https://csrc.nist.gov/projects/cryptographic-module-validation-program)
- [CAVP / ACVP](https://csrc.nist.gov/projects/cryptographic-algorithm-validation-program)
- [FIPS 140-3 IG announcements](https://csrc.nist.gov/projects/cryptographic-module-validation-program/fips-140-3-ig-announcements)
- [SP 800-90B](https://csrc.nist.gov/publications/detail/sp/800-90b/final)
- Repo README: CMVP integration hooks vs certification non-claim

## Status for this repository

`dragonslayer` provides documentation and integration messaging only.  
It is **not** a cryptographic module under test and holds **no** CMVP certificate.
