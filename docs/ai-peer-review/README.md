# AI Agent Peer Review Simulations

## What This Is — Read Before Using Any Document In This Folder

The documents in this folder are **AI-generated simulations** produced by Shane Brazelton
using Claude (Anthropic). They are **not real expert reviews, not real communications,
not real endorsements, and contain no actual words from the individuals named.**

This must be stated plainly and without ambiguity:

> **Dr. Ian McNab, Dr. Iain Boyd, and Gwynne Shotwell have no affiliation with
> Project BGKPJR. They have not reviewed this project. They have not been contacted.
> Nothing in these documents represents their actual opinions, findings, or words.**

---

## The Methodology

Shane Brazelton built a series of AI agents inside Claude (Anthropic), each one
named after and trained on a real, prominent expert in a relevant field. Each agent
was loaded with:

- The expert's published research papers and known findings
- Their documented positions on related engineering problems
- Their known methodological approach and professional philosophy
- Their specific domain expertise and academic/industry history

The intent was to test **how accurately a Claude AI agent, given deep domain knowledge
from a specific expert's body of work, could simulate that expert's analytical style,
priorities, and likely conclusions** when presented with a novel engineering case file.

This is an experiment in AI-assisted engineering review — using AI agents as a
structured tool to stress-test an architecture from multiple expert perspectives
simultaneously, without access to the real individuals.

---

## The Review Chain

The BGKPJR case file was submitted sequentially through three agents:

```
[BGKPJR Case File]
        ↓
  Agent 1: McNab (EM Propulsion)
  — found railgun→coilgun architecture error
        ↓ (original + McNab analysis)
  Agent 2: Boyd (Hypersonic Aerodynamics)
  — found 3× thermal load underestimate
        ↓ (original + McNab + Boyd analysis)
  Agent 3: Shotwell (Systems Integration)
  — produced phased development roadmap
```

Each agent received all prior analysis before generating its own. The output of
each simulation informed the next, building a compounding review chain.

---

## Why These Three

| Agent | Real Person | Relevance |
|-------|-------------|-----------|
| McNab | Dr. Ian McNab — former Director, Institute for Advanced Technology, UT Austin. 40+ years EM launch research, 200+ publications, 15 patents including railgun and coilgun systems. | Direct domain: electromagnetic launch architecture |
| Boyd | Dr. Iain Boyd — former Director, Center for Predictive Engineering, University of Michigan. NASA consultant, 300+ publications on CFD and hypersonic vehicle design. | Direct domain: hypersonic aerodynamics and thermal analysis |
| Shotwell | Gwynne Shotwell — President & COO, SpaceX. Led Falcon 9 and Dragon development. Known for iterative development philosophy and manufacturing scale. | Direct domain: large-scale aerospace systems integration |

---

## What To Do With This Content

The technical corrections these simulations produced — the railgun→coilgun
architecture change, the thermal load re-estimate, the phased development
structure — are treated as valid engineering feedback on their merits,
regardless of their AI-generated origin.

They are preserved here as a record of the AI agent review methodology
and the specific corrections that shaped the architecture documented
in v2+ of the BGKPJR technical reports.

---

## Files In This Folder

| File | Agent | Review Domain | Position in Chain |
|------|-------|---------------|-------------------|
| `01-mcnab-em-propulsion.md` | McNab | Electromagnetic Propulsion | 1 of 3 |
| `02-boyd-hypersonics.md` | Boyd | Hypersonic Aerodynamics | 2 of 3 |
| `03-shotwell-integration.md` | Shotwell | Systems Integration | 3 of 3 |

---

*Project BGKPJR — Shane Brazelton · Hazel Green, AL*
*Built with Claude (Anthropic)*
