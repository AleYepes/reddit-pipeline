# NER Trigger Definitions — Refined 21 Labels

---

## A. EXPERIENCE_PAIN

1. PERFORMANCE_PAIN
   *Broken, slow, unstable system behavior.*
   Include: crashes, lag, errors, downtime.
   Exclude: confusing workflows (→ USABILITY_PAIN).
   Triggers: crash, freeze, lag, unresponsive, error code, down.

2. USABILITY_PAIN
   *Difficult navigation, workflows, or accessibility barriers.*
   Include: too many steps, confusing menus, inaccessible for disabilities.
   Exclude: content is wrong (→ CONTENT_PAIN).
   Triggers: hard to find, too many clicks, confusing menu, not accessible.

3. CONTENT_PAIN
   *Unclear, inaccurate, missing, or culturally inappropriate content.*
   Include: misleading info, bad translation, offensive wording.
   Exclude: irrelevant recommendations (→ PERSONALIZATION_PAIN).
   Triggers: unclear, wrong info, bad translation, offensive, no instructions.

4. AESTHETIC_PAIN
   *Unappealing visual/sensory design.*
   Include: ugly, cluttered, hard to read.
   Exclude: functional navigation problems (→ USABILITY_PAIN).
   Triggers: ugly, cluttered, jarring, too bright, tiny font.

5. PERSONALIZATION_PAIN
   *Irrelevant or non-customized experience.*
   Include: irrelevant recommendations, no saved preferences.
   Exclude: unclear content (→ CONTENT_PAIN).
   Triggers: irrelevant, not tailored, keeps recommending, no preferences.

6. TRUST_PAIN
   *Concerns about honesty, ethics, or safety.*
   Include: hidden terms, scam suspicion, unsafe practices.
   Exclude: public brand image issues (→ REPUTATION_PAIN).
   Triggers: hidden, fine print, scam, unsafe, dishonest.

7. SUPPORT_PAIN
   *Ineffective customer support or help channels.*
   Include: no reply, unhelpful agents, broken chatbots.
   Exclude: internal communication problems (→ COMMUNICATION_PAIN).
   Triggers: support never replied, useless chatbot, no help.

8. VALUE_PAIN
   *Perceived high cost or poor ROI.*
   Include: too expensive, hidden fees, not worth cost.
   Exclude: company budget issues (→ FINANCIAL_PAIN).
   Triggers: too expensive, overpriced, hidden fee, not worth.

9. DELIVERY_PAIN
   *Failures in physical/digital delivery or scheduling.*
   Include: damaged, delayed, wrong item, late arrival.
   Exclude: software crashes (→ PERFORMANCE_PAIN).
   Triggers: delayed, damaged, wrong order, late, lost shipment.

---

## B. OPERATIONAL_PAIN

10. WORKFLOW_PAIN
    *Inefficient processes or resistance to change.*
    Include: too many steps, long approvals, dislike of new system.
    Exclude: tool-specific usability (→ TOOLING_PAIN).
    Triggers: takes too long, approval delays, prefer old system.

11. COMMUNICATION_PAIN
    *Poor information flow between teams.*
    Include: misalignment, not informed, misunderstandings.
    Exclude: customer-facing support failures (→ SUPPORT_PAIN).
    Triggers: not aligned, didn’t know, no one told us.

12. TOOLING_PAIN
    *Internal software/tools lack features or integration.*
    Include: outdated systems, missing integration, clunky interfaces.
    Exclude: process inefficiency not tied to tools (→ WORKFLOW_PAIN).
    Triggers: outdated tool, no API, doesn’t sync, clunky software.

13. DATA_PAIN
    *Inaccurate, missing, or inaccessible data.*
    Include: wrong numbers, incomplete datasets, blocked access.
    Exclude: tool UX issues (→ TOOLING_PAIN).
    Triggers: inaccurate data, missing data, can’t access.

14. SECURITY_PAIN
    *Security or privacy vulnerabilities.*
    Include: breaches, hacks, permissions abuse.
    Exclude: general trust concerns without security angle (→ TRUST_PAIN).
    Triggers: data breach, hacked, security flaw.

15. TRAINING_PAIN
    *Lack of skills, onboarding, or training resources.*
    Include: no training, lack expertise, never taught.
    Exclude: staff shortages (→ STAFFING_PAIN).
    Triggers: no training, don’t know how, lack skills.

16. STAFFING_PAIN
    *Shortages, morale problems, or turnover.*
    Include: can’t hire, high turnover, low morale.
    Exclude: lack of skills but enough staff (→ TRAINING_PAIN).
    Triggers: short-staffed, high turnover, morale is low.

---

## C. MARKET_PAIN

17. COMPETITION_PAIN
    *Losing market position or falling behind competitors.*
    Include: new competitor, missing features, outdated tech.
    Exclude: customer perception only (→ REPUTATION_PAIN).
    Triggers: losing market share, behind competitors, no AI.

18. REPUTATION_PAIN
    *Negative public/brand perception.*
    Include: bad press, poor ratings, public backlash.
    Exclude: individual trust complaints (→ TRUST_PAIN).
    Triggers: bad press, negative reviews, PR crisis.

19. SUSTAINABILITY_PAIN
    *Environmental or social responsibility issues.*
    Include: pollution, unethical sourcing, ESG non-compliance.
    Exclude: general supply chain delays (→ DELIVERY_PAIN).
    Triggers: not sustainable, carbon footprint, unethical sourcing.

20. FINANCIAL_PAIN
    *Revenue, profitability, funding, or cash flow issues.*
    Include: no budget, running out of money, high burn rate.
    Exclude: customer price complaints (→ VALUE_PAIN).
    Triggers: no budget, negative cash flow, missed target.

21. LEGAL_PAIN
    *Compliance, regulatory, or contractual issues.*
    Include: lawsuits, non-compliance, contract disputes.
    Exclude: general trust concerns (→ TRUST_PAIN).
    Triggers: lawsuit, regulation, not compliant, cease and desist.

---
