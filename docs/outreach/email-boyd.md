# Outreach Email — Dr. Iain Boyd

**To:** Dr. Iain Boyd
**Find contact via:** University of Colorado Boulder — Ann and H.J. Smead Department of Aerospace Engineering Sciences (faculty directory)
**Subject:** BGKPJR Hypersonic Launch Architecture — Thermal Analysis Feedback Requested

---

Dr. Boyd,

My name is Shane Brazelton. I am an independent engineer and systems architect based in
Hazel Green, Alabama. I have been developing an electromagnetic launch architecture called
BGKPJR — Brazelton Gryphon Kepler Propulsion Jump Revolution — a three-stage hybrid
space launch system built around a superconducting maglev acceleration tube (28.7 km,
4g sustained, Mach 3.5–5.0 exit), a hypersonic lifting-body spacecraft called the Gryphon,
and an orbital solar sail called Kepler.

A patent application is on file. The full architecture is publicly documented at:
https://github.com/thebardchat/BGKPJR-Core-Simulations

**Why I am contacting you specifically:**

Your work in computational fluid dynamics and hypersonic aerothermal environments — including
your research on hypersonic vehicle design and your consulting work with NASA — is directly
relevant to the single hardest unsolved problem in my architecture: what happens to the
Gryphon spacecraft in the first seconds after it exits a near-vacuum tube at Mach 3.5–5.0
into full atmospheric density.

I want to be transparent: before reaching out to real experts, I built an AI agent trained
on your published research and known positions to simulate how you might analyze this
problem. That simulation — which is explicitly labeled throughout as an AI simulation and
does not contain your actual words — identified that my original thermal load estimate
of 15 MW/m² was approximately 3× too low, with the corrected figure around 42 MW/m².
It also flagged that my 0.5m nose radius is insufficient and should be at least 1.2m,
and that passive tile TPS alone cannot handle sustained hypersonic exposure at this
speed and altitude.

I want to know if those corrections are accurate.

**What I am asking:**

A brief technical reaction to the thermal environment my vehicle faces — specifically:

1. Is the 42 MW/m² peak heating figure in the right order of magnitude for a Mach 5
   vehicle transitioning from 10⁻³ atm to full atmospheric density?
2. Is a hybrid ablative + active transpiration cooling system the right approach for
   sustained exposure at these conditions?
3. Is there a thermal problem in this architecture that my simulation missed entirely?

The AI simulation of your review (explicitly labeled as such) is here:
https://github.com/thebardchat/BGKPJR-Core-Simulations/blob/main/docs/ai-peer-review/02-boyd-hypersonics.md

The VacuumGate feasibility report documenting the full thermal analysis is here:
https://github.com/thebardchat/BGKPJR-Core-Simulations/blob/main/docs/BGKPJR-VacuumGate-Feasibility-Report.md

I am not asking for endorsement or a formal review. I am asking whether the architecture
survives first contact with someone who actually knows this problem.

Thank you for your time.

Shane Brazelton
Hazel Green, Alabama
brazeltonshane@gmail.com
GitHub: https://github.com/thebardchat
