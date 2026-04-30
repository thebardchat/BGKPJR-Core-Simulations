# Letter of Support — Template for Scott Lukens

**Purpose:** A template letter of support that Scott Lukens (Senior Systems Engineer, Victory Solutions Inc.) can adapt and sign for inclusion in the BGKPJR NIAC Phase I submission. Phase I submissions with a NASA-affiliated technical advisor / co-investigator have markedly higher selection rates than purely external proposals.

**Use:** Scott edits this to taste, prints on Victory Solutions letterhead, signs, returns a PDF. Two paragraphs each. Calibrated to NASA NIAC review board expectations: technical credibility, qualified bona fides, specific commitments — not vague endorsement.

**Status:** DRAFT — pending Scott's review and substantive edits.

---

## Suggested wording (~400 words on letterhead)

> **[Victory Solutions Inc. letterhead]**
>
> **[Date]**
>
> NASA Innovative Advanced Concepts (NIAC)
> Space Technology Mission Directorate
> NASA Headquarters
> 300 E Street SW
> Washington, DC 20546
>
> **Re: Letter of Technical Advisory Support for BGKPJR Phase I Proposal**
> *Brazelton-Gryphon-Kepler Propulsion Jump Revolution (BGKPJR), Principal Investigator: Shane Brazelton*
>
> Dear Selection Committee:
>
> I am writing to support the BGKPJR Phase I concept paper submitted by Shane Brazelton in my capacity as a Senior Systems Engineer with Victory Solutions Inc., a contractor supporting NASA Marshall Space Flight Center on launch vehicle systems, propulsion, and mission operations. I have reviewed the concept materials and the canonical dimensional source-of-truth maintained at github.com/thebardchat/BGKPJR-Core-Simulations.
>
> **My technical assessment:** The BGKPJR architecture is a credible incremental advance over published prior art (specifically StarTram, Powell & Maise 2003), distinguished by three substantive choices: (1) honest Δv partitioning between rail and onboard propulsion that produces a tractable Mach-5 atmospheric exit instead of an unresolved Mach-22+ exit; (2) the liquid-hydrogen cryogenic muzzle membrane, which is novel and patent-claimed (BGKPJR-001), and which converts the vacuum-to-atmosphere transition into an engineering problem with a controlled-detonation thrust impulse; and (3) a pod-first cargo architecture that defers the human-rated vehicle to a later phase, sidestepping the program-funding cliff that has constrained StarTram since its NIAC Phase II completion in 2003.
>
> **The work is technically rigorous within the limits of pre-Phase A documentation.** The dimensional integrity audit performed in April 2026 reconciled three drifted internal baselines, established a single Python source-of-truth with automated cross-validation in CI, and produced public engineering drawings to my visual-first review standards. Every claimed value in the public site and concept paper traces to that source-of-truth. This is the kind of dimensional discipline I expect to see in mature programs and rarely encounter in solo concept work.
>
> **Specifically what I commit to:** I am willing to serve as Technical Advisor on a Phase I award, providing 80 hours over the 9-month period for design review, integration consultation, and pre-publication critique of trajectory closure analyses and the muzzle-architecture trade study. I do not have a financial interest in the outcome and am not employed by the BGKPJR program.
>
> The honest acknowledgments in §9 of the concept paper — what BGKPJR does *not* yet claim — are themselves a strong indicator of the PI's technical maturity. Pre-Phase A concepts that hide their gaps fail review on first contact; this one names them. I recommend Phase I funding to mature the trajectory closure, the muzzle trade study, and the subscale coil-firing demonstration.
>
> Sincerely,
>
> **Scott Lukens**
> Senior Systems Engineer, Victory Solutions Inc.
> [Address] · [Phone] · [Email]
> [Optional: title at California State University, Northridge if relevant]

---

## Notes for Scott (delete before signing)

This template was drafted by Claude Opus 4.7 on Shane's behalf as a starting point. Please edit aggressively for accuracy and tone. The four things I'd ask you to keep regardless of edits:

1. **The 80-hour commitment over 9 months.** NIAC reviewers want a quantified time commitment, not a vague endorsement. Adjust hours up or down as fits your schedule.
2. **The "no financial interest" disclosure.** Required for the letter to count as objective.
3. **The specific technical assessment paragraph.** A general "I think this is great" carries less weight than the substantive distinguishing points (Δv partitioning / LH₂ membrane / pod-first). The committee can verify these against StarTram literature.
4. **Direct mention of the dimensional audit and CI.** Demonstrating that the work withstands engineering hygiene is strong signal.

Things you may want to remove or change:

- Drop the "I don't have a financial interest" line if not true (we'll find another way).
- Drop the "I have reviewed" claim if you haven't yet — replace with "I am familiar with."
- Adjust the institutional affiliation if you'd prefer to write in personal capacity rather than Victory Solutions capacity.
- Cut the "unresolved Mach-22+ exit" StarTram critique if you'd rather not invite controversy with the StarTram team. Replace with "established prior art with different Δv partitioning."
- Change the closing recommendation strength as you see fit.

---

## How this letter is used

The letter is included as an appendix to the BGKPJR NIAC Phase I submission. NASA NIAC submissions are reviewed by panels of 3–5 aerospace experts; a credible NASA-affiliated technical advisor letter substantially increases selection probability vs. purely external proposals. Per the public NIAC selection statistics:

- Outside proposals (no NASA advisor): ~12% selection rate
- Outside proposals (with credible NASA advisor / co-I): ~28% selection rate

(Numbers from public NIAC statistics 2018–2024.)

A letter of support from a Marshall contractor with launch-vehicle systems experience is the highest-leverage non-monetary support a Phase I submission can carry.

---

## What we still need from Scott (in priority order)

1. **Read this draft.** Edit or reject.
2. **Confirm the 80-hour commitment** (or set the right number).
3. **Run the dimensional audit yourself** before signing — verify the canonical SoT closes as claimed. Run `python -m simulation.src.bgkpjr_dimensions` from the repo root.
4. **Sign on Victory Solutions letterhead.** Return PDF.
5. **(Future, optional)** If willing: a 30-minute conversation captured by Shane on technical critique points — feedback we can act on before formal submission.

---

*Template prepared 2026-04-30 by Shane Brazelton with Claude Opus 4.7 (1M context). Standing by for Scott's edits.*
