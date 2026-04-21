# Twitter/X Thread — ShaneBrain Ecosystem

Post from @BGKPJRevolution or personal account.

---

**Tweet 1 (hook)**
I run 17 autonomous AI bots on a Raspberry Pi 5 in my living room in Alabama.

No cloud. No subscriptions. No data leaving my house.

Here's the full stack. 🧵

---

**Tweet 2**
Hardware:
- Raspberry Pi 5, 16GB RAM
- Pironman 5-MAX chassis (NVMe RAID)
- RAID 1: 2× 2TB NVMe
- 4-node Ollama cluster (Pi + 3 Windows machines via Tailscale)
- 8TB external backup

Total inference capacity: distributed across 4 nodes, zero cloud billing.

---

**Tweet 3**
The AI stack:
- Ollama 0.17.7 (local LLM inference)
- Cluster proxy routing across all 4 nodes
- Weaviate 1.36.2 — 17 collections, 210+ knowledge objects
- nomic-embed-text (768-dim vectors)
- Custom MCP server with 42 tools across 26 groups

All local. All mine.

---

**Tweet 4**
The 17 MEGA Crew bots run 24/7.

Each one has:
- A distinct name and personality
- A specific domain
- Persistent Weaviate memory
- Local Ollama inference (llama3.2:1b)

They self-evolved through 4 phases: basic → code-aware → Docker-scaled → self-modifying.

---

**Tweet 5**
The morning briefing runs at 5 AM every day.

Weather. Sobriety counter. Active services. Disk health. Ollama models. Weaviate collections. GitHub stars. Voice dumps. Book progress. Cluster status. Closet temperature from a Pico 2 sensor.

All on one dashboard. All local.

---

**Tweet 6**
The auto-ingest pipeline runs daily at 4 AM.

Voice transcripts, book chapters, daily notes → chunked → embedded → stored to Weaviate LegacyKnowledge.

My thoughts from the day become searchable RAG context by morning.

---

**Tweet 7**
Also on the Pi:
- Discord bot, Arcade bot, Social bot (systemd)
- Angel Cloud wellness platform (FastAPI, public HTTPS via Tailscale Funnel)
- Buddy Claude (Claude↔Gemini 12hr dialogue engine)
- SMS alerts via vtext gateway
- Facebook promo automation with random image rotation

---

**Tweet 8**
All of it documented. All of it public (where it can be).

Built by a dump truck dispatcher, father of 5, Hazel Green Alabama.

Pi before cloud. Privacy before convenience.

🔗 https://thebardchat.github.io
📁 https://github.com/thebardchat
