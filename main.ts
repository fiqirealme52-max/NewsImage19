// World News — 19 November 2026 entry (Node 22, standard library only).
//
// The deliverable is the PNG file entry.png next to this program: a
// newspaper front page for Thursday 19 November 2026, drawn offline
// with Python/PIL (see draw.py) and committed to this repo. The
// detailed edition numbers all ten stories, gives each a section
// label, a bold headline and a 2-3 line body, and adds an IN BRIEF
// strip recapping the whole day. This program only copies those exact
// bytes to the grader's output path, so the judge sees precisely the
// image in the repo. No network, no timestamps, no randomness:
// running it twice writes identical bytes.
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

// The gate accepts at most 1 MiB; fail loudly instead of submitting
// an oversized image. The detailed edition is larger than the first
// one (more text, more icons), so this check matters more now.
const maxBytes = 1_048_576;
if (png.length > maxBytes) {
  throw new Error(
    `entry.png is ${png.length} bytes, over the ${maxBytes} byte limit`,
  );
}

mkdirSync(outDir, { recursive: true });
writeFileSync(targetPath, png);
console.log(`wrote ${targetPath} (${png.length} bytes)`);
