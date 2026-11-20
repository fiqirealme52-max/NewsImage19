// World News — 19 November 2026 entry (Node 22, standard library only).
//
// What the judge receives is the PNG file entry.png sitting next to this
// program. That picture is a newspaper front page for Thursday 19 November
// 2026, drawn offline with Python/PIL by draw.py and committed to this
// repo. The visual-revision edition rebuilds the presentation from the
// top-10 research (giant serif date, three illustrated leads, seven
// illustrated medium cards, number strip, region tabs, world map with ten
// numbered pins, DATE CHECK box) while keeping the ten verified stories,
// all numbers and all dates exactly as the Detailed edition had them.
// The ALSO ON edition (2026-11-20) adds a band of 27 verified one-line
// briefs from 19 November 2026 reporting between the map and DATE CHECK
// (see README.md and also-on-sources.md; brief #8 Mongolia not used,
// #7 Denmark shown without the vote tally) and fixes the number-strip
// labels so "28" and "3rd" no longer run together. No main-story fact,
// number or date changed in either revision.
// Every story also carries a visible "CONFIRMED · outlet" tag; the outlet
// for each story was verified against live 19 November 2026 reporting and
// is recorded in README.md.
//
// This program does nothing creative: it reads entry.png as raw bytes and
// writes those exact bytes to the grader's output path, so the judge sees
// precisely the image in the repo. No network, no timestamps, no random
// values — running it twice writes identical bytes both times. The drawing
// itself is deterministic too: draw.py uses only seeded pseudo-random
// values for its print grain, so rebuilding entry.png also reproduces the
// same bytes.
//
// Run locally with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const sourcePath = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const targetPath = join(outDir, "entry.png");

const png = readFileSync(sourcePath);

// The file must really be a PNG before we hand it to the gate.
const pngMagic = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (png.length < 8 || !png.subarray(0, 8).equals(pngMagic)) {
  throw new Error(`entry.png is not a PNG file (${sourcePath})`);
}

// The gate accepts at most 1 MiB; fail loudly instead of submitting an
// oversized image. The visual-revision edition is roughly twice the size
// of the Detailed edition (richer illustrations, print grain), and the
// ALSO ON edition is larger still (about 340 KB: 27 extra briefs plus the
// print grain), so this check matters more now than it did before.
const maxBytes = 1_048_576;
if (png.length > maxBytes) {
  throw new Error(
    `entry.png is ${png.length} bytes, over the ${maxBytes} byte limit`,
  );
}

mkdirSync(outDir, { recursive: true });
writeFileSync(targetPath, png);
console.log(`wrote ${targetPath} (${png.length} bytes)`);
