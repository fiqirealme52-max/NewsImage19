// News-image entry for 19 November 2026 (Node 22, standard library only).
// The entry is the PNG file entry.png next to this program: a newspaper
// front page summing up Thursday 19 November 2026, drawn once, offline,
// with Python/PIL and committed to this repo. This program's only job is
// to place an exact copy of that image at the grader's output path, so
// the judge sees exactly the bytes in this repo. It never touches the
// network and never changes the image, so repeated runs are byte-identical.
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

// Sanity check: the file really is a PNG before we hand it to the gate.
const pngMagic = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (png.length < 8 || !png.subarray(0, 8).equals(pngMagic)) {
  throw new Error(`entry.png is not a PNG file (${sourcePath})`);
}

// The gate accepts at most 1 MiB; fail loudly here instead of silently
// submitting an oversized image.
const maxBytes = 1_048_576;
if (png.length > maxBytes) {
  throw new Error(`entry.png is ${png.length} bytes, over the ${maxBytes} byte limit`);
}

mkdirSync(outDir, { recursive: true });
writeFileSync(targetPath, png);
console.log(`wrote ${targetPath} (${png.length} bytes)`);
