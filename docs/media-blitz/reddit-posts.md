# Reddit Posts — Full Blitz

Post these separately, spaced out over a few days. Don't cross-post the same text — each is tailored to its subreddit.

---

## r/aerospace + r/spaceflight

**Title:** I filed a patent on an electromagnetic launch architecture and published the full feasibility report — including every hard barrier and why it might not work

**Body:**
I want to share a project I've been developing for several years: BGKPJR (Brazelton Gryphon Kepler Propulsion Jump Revolution), a three-stage hybrid space launch architecture. Patent filed April 2025.

The three stages:
- **Maglev Jump:** 28.7km superconducting coilgun (LSM, not railgun) at 4g sustained → Mach 5 exit
- **Gryphon Ascent:** Hypersonic blended wing body spacecraft, Mach 5→8+, aerodynamic lift + hybrid propulsion
- **Kepler Sail:** Solar sail deploys at >300km stable orbit for deep-space operations

The novel IP is the **VacuumGate**: a liquid hydrogen cryogenic membrane at tube exit that maintains the vacuum-to-atmosphere pressure gradient, absorbs stagnation heat, and provides a controlled detonation thrust impulse when the vehicle breaches it at Mach 5. The engineering question: can the detonation wave be directed behind the vehicle? Patent-worthy if yes. Catastrophic if no.

**I want to be upfront about what the feasibility report says:**
- ~65% of the architecture is physically sound with aggressive but known engineering
- ~35% contains hard physics problems
- Seven documented hard barriers including 1.1×10¹⁰ N crushing force on the vacuum tube, 42 MW/m² peak heating (not 15 as originally estimated), and $85-120B total cost
- Generational timeline. Multi-agency coalition required. No single entity can fund this.

I'm not looking for investment or hype. I'm asking for engineering feedback from people who know this domain.

Full project: https://thebardchat.github.io/BGKPJR-Core-Simulations/
Feasibility report: https://github.com/thebardchat/BGKPJR-Core-Simulations/blob/main/docs/BGKPJR-VacuumGate-Feasibility-Report.md
GitHub: https://github.com/thebardchat/BGKPJR-Core-Simulations

---

## r/LocalLLaMA

**Title:** Running 17 autonomous AI bots on a Pi 5 — 4-node Ollama cluster, Weaviate RAG, custom MCP server with 42 tools, all local

**Body:**
Been building this for about two years. Here's the current state of my local AI stack, running entirely on a Raspberry Pi 5 (16GB) in my house in Alabama.

**Hardware:**
- Pi 5, 16GB RAM, Pironman 5-MAX chassis
- RAID 1: 2× 2TB NVMe via mdadm
- 4-node Ollama cluster: Pi 5 + 3 Windows machines via Tailscale mesh
- All model storage on RAID, not SD card

**AI Stack:**
- Ollama 0.17.7 with cluster proxy routing across all 4 nodes
- Custom shanebrain-3b model (llama3.2:3b base + system prompt)
- nomic-embed-text for 768-dim embeddings
- Weaviate 1.36.2 — 17 collections including LegacyKnowledge (210+ objects), Conversation, FriendProfile, SecurityLog, ExternalPerspectives (AI dialogue turns)
- Auto-ingest pipeline: daily 4 AM, voice transcripts + book chapters → chunked → embedded → Weaviate

**MCP Server v2.2:**
- 42 tools across 26 groups
- knowledge, chat, RAG, social, vault, notes, drafts, security, admin, Ollama, planning, system health
- Streamable HTTP transport, Pydantic v2, Docker
- Registered with Claude: `claude mcp add --scope user shanebrain --transport http http://localhost:8100/mcp`

**MEGA Crew — 17 bots:**
- Each has a name, personality, domain, persistent Weaviate memory
- All run on local Ollama (llama3.2:1b for lightweight tasks)
- 4-phase evolution: basic → code-aware → Docker-scaled → self-modifying
- 24/7 on systemd

Also running: Discord bot, Arcade bot, Social bot, Buddy Claude (Claude↔Gemini dialogue engine), Angel Cloud FastAPI gateway, morning briefing at 5 AM, SMS alerts via vtext, voice dump playback pipeline.

Happy to answer questions about any part of the stack.

GitHub: https://github.com/thebardchat
Ecosystem hub: https://thebardchat.github.io

---

## r/selfhosted + r/raspberry_pi

**Title:** My Pi 5 home AI stack after 2 years — Ollama cluster, Weaviate RAG, 17 bots, 42 MCP tools, all self-hosted

**Body:**
Sharing the current state of my setup after two years of building. I'm a dispatcher by day, I do this at night.

**The Pi 5 runs:**
- Ollama (port 11434) + cluster proxy routing to 3 additional nodes (port 11435)
- Weaviate 1.36.2 in Docker (port 8080) — 17 collections
- Custom MCP server Docker container (port 8100) — 42 tools
- Mega dashboard on systemd (port 8300) — weather, sobriety counter, service health, disk, ollama models, weaviate stats, github stars, cluster status, Pico 2 temp sensor from closet
- Angel Cloud Gateway FastAPI (port 4200) — public HTTPS via Tailscale Funnel
- Buddy Claude FastAPI (port 8008) — Claude↔Gemini dialogue engine
- Open WebUI (port 3000), Portainer (port 9000)
- Discord bot, Arcade bot, Social bot — all systemd services
- ShaneBrain Alerter — 5 AM morning briefing, weekly Sunday report

**Storage:**
- RAID 1: 2× WD Blue SN5000 2TB NVMe via mdadm at `/mnt/shanebrain-raid/`
- Docker data-root on RAID
- Ollama models on RAID
- 8TB Seagate external for backup

**Network:**
- Tailscale VPN mesh across all 4 nodes
- Tailscale Funnel for public HTTPS
- Caddy 2.11.2 reverse proxy

SD card freed to 44% — everything heavy moved to RAID.

Full ecosystem: https://thebardchat.github.io
GitHub: https://github.com/thebardchat

---

## r/singularity + r/artificial

**Title:** I built an AI methodology to stress-test my own engineering: sequential Claude agents trained on real experts reviewed my patent-filed aerospace project

**Body:**
I want to share an AI methodology I developed for engineering validation.

I'm building BGKPJR — a patent-filed electromagnetic launch architecture. Before reaching out to real experts, I needed to stress-test the design from multiple expert perspectives simultaneously.

**The methodology:**
1. Build a Claude AI agent loaded with a real expert's published body of work, papers, known positions, and domain expertise
2. Submit the engineering case file to Agent 1
3. Pass the original + Agent 1's output to Agent 2
4. Pass everything to Agent 3
5. Each agent compounds on the prior analysis

**The three agents:**
- McNab persona (EM launch, 40+ years, 200+ publications)
- Boyd persona (hypersonic CFD, NASA consultant)
- Shotwell persona (SpaceX systems integration philosophy)

**What the chain produced:**
- Critical architecture correction: railgun fails at 2.71 MA → coilgun (LSM) required
- Thermal load was 3× underestimated (15 → 42 MW/m²)
- Phased development roadmap: $50M subscale first

The simulation files are fully documented with explicit disclaimers — these are AI simulations, not real words from these people. The real individuals have no connection to my project. I've since contacted them directly.

This is a legitimate engineering research methodology: using AI trained on domain expert knowledge to systematically identify problems in your own work before committing resources.

Full repo with methodology docs: https://github.com/thebardchat/BGKPJR-Core-Simulations
AI peer review folder: https://github.com/thebardchat/BGKPJR-Core-Simulations/tree/main/docs/ai-peer-review

---

## r/netsec (Pulsar Sentinel)

**Title:** Post-quantum cryptography framework on a Pi 5 — ML-KEM lattice encryption, blockchain audit trails, MetaMask auth

**Body:**
Built a PQC security framework called Pulsar Sentinel as part of my broader home AI infrastructure.

Stack:
- ML-KEM (CRYSTALS-Kyber) lattice-based encryption via liboqs
- Blockchain audit trails on Polygon
- MetaMask wallet authentication
- Cyberpunk-style dashboard
- Python / FastAPI / Web3 / Discord.py

Still active development. Planning to deploy across all 4 nodes of my Ollama cluster.

GitHub: https://github.com/thebardchat/pulsar_sentinel
Pages: https://thebardchat.github.io/pulsar_sentinel/
