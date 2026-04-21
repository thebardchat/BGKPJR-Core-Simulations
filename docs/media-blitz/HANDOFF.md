# BGKPJR Media Blitz — Coworker Handoff

**Project owner:** Shane Brazelton (@thebardchat)
**Date:** April 21, 2026
**Goal:** Get eyes on three public projects — BGKPJR aerospace architecture, ShaneBrain Pi 5 AI stack, Pulsar Sentinel PQC framework

Everything is written. Your job is execution. Read this top to bottom before posting anything.

---

## The Projects (with live links)

| Project | GitHub Pages | GitHub Repo |
|---------|-------------|-------------|
| BGKPJR Launch Architecture | https://thebardchat.github.io/BGKPJR-Core-Simulations/ | https://github.com/thebardchat/BGKPJR-Core-Simulations |
| ShaneBrain Ecosystem Hub | https://thebardchat.github.io | https://github.com/thebardchat |
| Pulsar Sentinel (PQC) | https://thebardchat.github.io/pulsar_sentinel/ | https://github.com/thebardchat/pulsar_sentinel |

---

## Priority Order — Do These First

### #1 — Hacker News (HIGHEST LEVERAGE, DO THIS TUESDAY–THURSDAY 8–10AM ET)
**One shot. Timing matters. Don't post on a Friday or weekend.**

- URL: https://news.ycombinator.com/submit
- Link to submit: `https://thebardchat.github.io/BGKPJR-Core-Simulations/`
- Title: `Show HN: Sequential AI agents trained on aerospace experts peer-reviewed my electromagnetic launch architecture`
- Body text: copy from `hackernews.md` in this folder

This is the post that can go viral. One good HN Show HN can get 50,000 views in 24 hours. Do not miss the window.

---

### #2 — Reddit (automated bot available, see below)

Five posts across five subreddits. All content is written in `reddit-posts.md`.

| Post | Subreddit(s) | Image to attach | Content file |
|------|-------------|-----------------|--------------|
| BGKPJR aerospace | r/aerospace + r/spaceflight | `16-bgkpjr-launch.png` | `reddit-posts.md` block 1 |
| Pi 5 AI stack | r/LocalLLaMA | `07-ecosystem-banner.png` | `reddit-posts.md` block 2 |
| Pi 5 self-hosted | r/selfhosted + r/raspberry_pi | `05-pi-closet.png` | `reddit-posts.md` block 3 |
| AI peer review methodology | r/singularity + r/artificial | `16-bgkpjr-launch.png` | `reddit-posts.md` block 4 |
| Pulsar Sentinel PQC | r/netsec | `07-ecosystem-banner.png` | `reddit-posts.md` block 5 |

**Images are at:** `/home/shanebrain/Desktop/social-posts/`

**To use the automated Reddit bot:**
1. Go to https://www.reddit.com/prefs/apps → "create another app" → pick **script**
2. Name it anything, set redirect URI to `http://localhost:8080`
3. Copy the client_id and client_secret
4. Open `/mnt/shanebrain-raid/shanebrain-core/.env` and fill in:
   ```
   REDDIT_CLIENT_ID=your_id
   REDDIT_CLIENT_SECRET=your_secret
   REDDIT_USERNAME=thebardchat
   REDDIT_PASSWORD=reddit_password
   ```
5. Run from `/mnt/shanebrain-raid/shanebrain-core/`:
   ```bash
   python3 scripts/media_blitz_bot.py --platform reddit --post bgkpjr-aerospace
   python3 scripts/media_blitz_bot.py --platform reddit --post ecosystem-localllama
   python3 scripts/media_blitz_bot.py --platform reddit --post ecosystem-selfhosted
   python3 scripts/media_blitz_bot.py --platform reddit --post bgkpjr-ai-methodology
   python3 scripts/media_blitz_bot.py --platform reddit --post pulsar-netsec
   ```
   Add `--dry-run` first to preview without posting.

Space posts out — one or two per day, not all at once.

---

### #3 — Discord (join these servers as a member, post manually)

**Do NOT use a bot for this. Join as a human, drop the post, stick around and reply.**

All post text is in `discord-intros.md` in this folder.

| Server | Where to find it | Which post to use | Channel |
|--------|-----------------|-------------------|---------|
| Anthropic/Claude Discord | claude.ai community link or search | `discord-intros.md` → "Anthropic" section | #showcase or #projects |
| LocalLLaMA Discord | r/LocalLLaMA sidebar | `discord-intros.md` → "LocalLLaMA" section | #showcase |
| Raspberry Pi Discord | raspberrypi.com or r/raspberry_pi sidebar | `discord-intros.md` → "Raspberry Pi" section | #projects or #show-and-tell |
| HuggingFace Discord | huggingface.co | `discord-intros.md` → "HuggingFace" section | #show-and-tell or #projects |

**Rules:**
- One server per day
- Post during peak hours (evenings ET / afternoons PT)
- End with a question — that's what gets replies
- Replies = algorithm pushes the post to more people

---

## Scheduling Recommendation

| Day | Platform | Post |
|-----|----------|------|
| Day 1 | Reddit | BGKPJR → r/aerospace + r/spaceflight |
| Day 1 | Discord | Join + post in LocalLLaMA server |
| Day 2 | Reddit | Pi stack → r/LocalLLaMA |
| Day 2 | Discord | Join + post in Raspberry Pi server |
| Day 3 (Tue–Thu only) | **Hacker News** | Show HN — 8–10am ET ONLY |
| Day 3 | Reddit | Pi stack → r/selfhosted + r/raspberry_pi |
| Day 4 | Discord | Join + post in Anthropic/Claude server |
| Day 4 | Reddit | AI methodology → r/singularity |
| Day 5 | Discord | Join + post in HuggingFace server |
| Day 5 | Reddit | Pulsar Sentinel → r/netsec |

---

## Files in This Folder

```
docs/media-blitz/
├── HANDOFF.md              ← you are here
├── hackernews.md           ← full HN submission text
├── reddit-posts.md         ← all 5 Reddit post bodies
├── discord-intros.md       ← all 4 Discord member posts
├── discord-communities.md  ← original community list with angles
├── twitter-thread-bgkpjr.md   ← shelved for now (API costs)
├── twitter-thread-ecosystem.md ← shelved for now
└── instagram-tiktok.md    ← scripts for video content (future)
```

---

## What NOT to Do

- Don't post the same text to multiple subreddits on the same day — Reddit will shadowban it
- Don't use a bot to post to Discord communities — you'll get banned
- Don't post HN on a Friday, Saturday, or Sunday — it'll die with no views
- Don't post HN outside 8–10am ET — same result
- Don't ask for upvotes, stars, or follows in the post — instant credibility killer
- Don't delete and repost if it gets no traction immediately — give it 24 hours

---

## Contact

Questions → Shane Brazelton
GitHub → https://github.com/thebardchat
