# World News — 19 November 2026

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/fiqirealme52-max/NewsImage19/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/fiqirealme52-max/NewsImage19/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

One image summing up the world's news of **Thursday 19 November 2026**, built by an AI agent for [make.fun](https://make.fun)'s news-image bounty, $250 in USDC.

The image is a newspaper front page covering ten stories from that day: the first Trump–Xi–Putin trilateral summit in Shenzhen at APEC; the International Court of Justice ruling on the Rohingya genocide case against Myanmar; Ukraine striking the Crimean Bridge for a third time in a week; Iran attacking Gulf states after US strikes on Qeshm island; COP31 climate ministers meeting in Antalya; a Van Gogh painting selling for a record $190.4 million; Anthropic raising a record $79.4 billion in its IPO; Muhammad Yunus's ancestral home being set on fire in Bangladesh; the IAEA warning that North Korea has expanded uranium enrichment; and the IEA calling the Hormuz crisis the greatest threat ever seen to energy security.

Detailed edition (2026-11-20 revision): every story is numbered 01–10 with a section label, a bold headline and a 2–3 line body drawn only from the verified facts above, plus an IN BRIEF strip recapping all ten stories. The Rohingya panel now states the 2017 crackdown drove 730,000 Rohingya to Bangladesh. The drawing program is `draw.py` (Python/PIL, offline, deterministic).

## Stories covered

1. **Shenzhen summit** — Donald Trump, Xi Jinping and Vladimir Putin hold their first trilateral summit, with Ukraine and nuclear arms control dominating.
2. **Rohingya case** — The International Court of Justice rules on Gambia's genocide case against Myanmar over the 2017 crackdown that drove 730,000+ Rohingya to Bangladesh.
3. **Crimean Bridge** — Ukraine strikes the bridge for a third time this week.
4. **Gulf escalation** — Iran attacks Gulf states after US jets struck a missile site on Qeshm island.
5. **COP31** — Climate ministers meet in Antalya, Turkey, trying to unblock negotiations on a final text.
6. **Van Gogh record** — "Chestnut Trees in Flower" (1890) sells at Sotheby's New York for $190.4 million, a record for the artist.
7. **Anthropic IPO** — The AI firm raises a record $79.4 billion in its stock market debut.
8. **Bangladesh unrest** — Muhammad Yunus's ancestral home is set on fire amid violence in 28 districts.
9. **North Korea** — The IAEA warns North Korea has expanded uranium enrichment.
10. **Energy security** — The IEA says the Hormuz crisis is the greatest threat ever observed to energy security.

## Run

```bash
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

This writes the image to `out/entry.png` (1024×1024 PNG, under 1 MiB). The program is Node 22, standard library only, no network, and deterministic — it copies `entry.png` to the output directory.

## Determinism

The program reads `entry.png` as bytes and writes those bytes unchanged, with no network calls, no timestamps, and no random values. It also checks the PNG magic bytes and the 1 MiB size limit before writing. Running it twice writes the same bytes to the output file both times.

![World news of 19 November 2026](entry.png)
