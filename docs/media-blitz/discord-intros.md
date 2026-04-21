# Discord Server Intro Posts — Human-Written, Drop as a Member

These are NOT bot posts. Join each server manually, lurk for a few minutes, then drop these.
One server per day max. Don't cross-post the same message.

---

## Anthropic / Claude Discord — #showcase

Hey all — been building with Claude for about a year and wanted to share what it actually unlocked for me.

I'm a dump truck dispatcher in Alabama. Father of 5. I used Claude to build sequential AI agents — each one trained on a real aerospace expert's published body of work — and ran my electromagnetic launch architecture through them in a chain before contacting the real people.

Agent 1 (trained on Dr. Ian McNab's research) told me my whole architecture was wrong. Railgun fails at those current levels. Coilgun required. That correction dropped the cost estimate by $10 billion.

I also built a local AI stack on a Raspberry Pi 5 — 17 bots, 42 MCP tools, Weaviate RAG, 4-node Ollama cluster. Claude is registered via MCP and has 42 tools it can call against my local knowledge base.

The AI methodology is documented here if anyone wants to dig in:
https://github.com/thebardchat/BGKPJR-Core-Simulations/tree/main/docs/ai-peer-review

Full ecosystem: https://thebardchat.github.io

Happy to talk through either the MCP setup or the agent chain methodology — both were genuinely non-obvious to get right.

---

## LocalLLaMA Discord — #showcase

Sharing my Pi 5 local AI stack — been building this for two years, figured this was the right crowd.

**The setup:**
- Raspberry Pi 5 (16GB) + Pironman 5-MAX chassis
- RAID 1: 2× 2TB NVMe via mdadm — all models and Docker on RAID, SD card at 44% usage
- 4-node Ollama cluster: Pi 5 + 3 Windows machines over Tailscale mesh
- Ollama cluster proxy on port 11435 — all services route through it, load balanced
- Weaviate 1.36.2 (Docker) — 17 collections, nomic-embed-text 768-dim, 210+ knowledge objects
- Custom MCP server — 42 tools across 26 groups, Pydantic v2, streamable HTTP
- 17 autonomous bots (MEGA Crew) — each has a name, personality, Weaviate memory, runs on llama3.2:1b
- Auto-ingest at 4 AM: voice memos → transcribed → chunked → embedded → searchable by morning
- 5 AM morning briefing: weather, sobriety counter, service health, disk, cluster status, Pico 2 temp from my closet

No cloud. Nothing leaves the house. I dispatch trucks during the day and build this at night.

GitHub: https://github.com/thebardchat
Hub: https://thebardchat.github.io

Happy to go deep on any part — the cluster proxy routing, the RAG ingest pipeline, the MCP server setup, any of it.

---

## Raspberry Pi Discord — #projects

Hey — sharing a project I've been putting together on a Pi 5 for the past two years.

Running a full local AI stack: 17 autonomous bots, Weaviate vector database, custom API server with 42 tools, 4-node Ollama compute cluster (Pi 5 + 3 Windows machines via Tailscale). Everything on RAID 1 NVMe — SD card is basically just the OS now at 44% usage.

The bots run 24/7 on systemd. Every morning at 5am I get a briefing: weather, sobriety tracker, service health, disk usage, closet temperature from a Pico 2 sensor, GitHub stars, Ollama cluster status. My voice memos from the day get auto-transcribed and embedded into the knowledge base by 4am so the AI already knows what I was thinking yesterday.

I'm a dump truck dispatcher in Alabama. Father of 5. Do this at night because I genuinely believe regular people should be able to run their own AI — local, private, on hardware they own.

Full write-up and GitHub: https://thebardchat.github.io

If anyone's done similar stuff with Pi RAID + Ollama I'd love to compare notes on what's working.

---

## HuggingFace Discord — find #show-and-tell or #projects channel

Hey — sharing a RAG + embedding setup I've been running on a Raspberry Pi 5 that might be interesting here.

Stack:
- nomic-embed-text for 768-dim embeddings (via Ollama)
- Weaviate 1.36.2 as the vector store — 17 collections, text2vec-ollama vectorizer
- Custom auto-ingest pipeline: voice memos → Whisper transcription → chunked → embedded → Weaviate, runs nightly at 4am
- 210+ knowledge objects across personal notes, book chapters, engineering docs, AI dialogue turns

I also built a sequential AI agent peer review chain — each agent trained on a real domain expert's published body of work, passed the case file down the chain. Used it to stress-test a patent-filed aerospace architecture before contacting the real experts. The nomic embeddings were part of how each agent accessed domain knowledge.

Methodology docs: https://github.com/thebardchat/BGKPJR-Core-Simulations/tree/main/docs/ai-peer-review
Full stack: https://thebardchat.github.io

Curious if anyone's compared nomic-embed-text to other local embedding models at this scale — I've stuck with it but haven't done a rigorous benchmark.

---

## Notes on delivery

- **Tone:** Talk like a person, not a press release. These are written that way — keep it.
- **Timing:** Post during active hours. Check when people are online in the server first.
- **Follow up:** Stick around and actually answer replies. That's what builds the relationship.
- **Don't double-post:** If you post in LocalLLaMA Discord, wait before posting the same angle in r/LocalLLaMA. Space them out by a day or two.
- **One ask per post:** Don't ask people to follow, subscribe, and star all at once. Let the content speak.
