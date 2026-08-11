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

## Related references

- [CMVP](https://csrc.nist.gov/projects/cryptographic-module-validation-program)
- [CAVP / ACVP](https://csrc.nist.gov/projects/cryptographic-algorithm-validation-program)
- [FIPS 140-3 IG announcements](https://csrc.nist.gov/projects/cryptographic-module-validation-program/fips-140-3-ig-announcements)
- [SP 800-90B](https://csrc.nist.gov/publications/detail/sp/800-90b/final)
- Repo README: CMVP integration hooks vs certification non-claim

## Status for this repository

`dragonslayer` provides documentation and integration messaging only.  
It is **not** a cryptographic module under test and holds **no** CMVP certificate.
