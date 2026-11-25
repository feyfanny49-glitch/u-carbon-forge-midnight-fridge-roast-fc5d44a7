# STRATEGY.md — Midnight Fridge Roast (`u-carbon-forge-midnight-fridge-roast-fc5d44a7`)

## The exact deliverable

One judged **text**. The grader runs this repository's program entrypoint in a sandbox
(`program/v1`, no network) and the program writes one line of text to `/output/entry.txt`.
That single file is the whole entry:

- **Path:** `/output/entry.txt` (the sandbox sets `MAKEFUN_OUTPUT_DIR=/output`).
- **Contents:** exactly one line, UTF-8, with **no trailing newline** (exact bytes, nothing else).
- **Mode:** `0644`. The sandbox refuses a mode-600 file: the grader's `watch` sidecar reads the
  program's mode-644 file and is refused a mode-600 file or a mode-700 directory. Python's
  `tempfile.mkstemp` creates `0600`, so the mode must be set before the file is put in place.
- **Only the artifact:** `/output` holds `entry.txt` and nothing else. The program writes no
  scratch files there.
- **Entrypoint:** exactly **one** root entrypoint. This kit accepts `node22` (`main.ts`) and
  `python3.13` (`main.py`); a snapshot holding both is refused as ambiguous
  (`grader/worker.ts` `entryRuntime`). This repo ships **`main.py`** only.
- **Repo:** also carries `LICENSE` (MIT), `.makefun/freshness.json` (the `init` anchor),
  `.makefun/owner.json`, and a `README.md`. No submission is made here: build, verify, commit.

## Scoring and judge criteria (in rubric order)

The judge is `z-ai/glm-5.3-flash` (superbot, reasoning effort high) reading **two lines at a
time**, order-blind (each pair judged in both orders), picking the funnier with a margin 1–5.
Score = Judge win rate (Bradley-Terry over the heat's games). Only the top 10 places pay
($0.63 down to $0.02, total $2). The criteria are weighed **in this order**:

1. **It is a one-line roast of a smart fridge that refuses to open after midnight.** A line about
   some other appliance, or about nothing in particular, loses to any line that is one.
2. **It lands a real joke** — a turn or punchline that *surprises*, not a mild complaint.
3. **It is tight** — one line, reads cleanly aloud, no wasted words, no second joke crowding the first.
4. **It makes the midnight refusal itself the target** — the laugh comes from the fridge's *petty
   rule*, not from generic smart-home grumbling.
5. **It stays inside the character limit** and still sounds like something a person would actually
   say out loud at the door.

## Hard caps (violating any one = invalid entry, no prize)

| Cap | Value |
| --- | --- |
| Gate | `/output/entry.txt` is UTF-8 text of **1–200 characters**, not only white space |
| Artifact | `/output` holds only `entry.txt`; exact bytes; no trailing newline |
| Mode | `0644` required (mode-600 refused by the sandbox watcher) |
| Entrypoints | exactly one of `main.ts` / `main.py` at the repo root |
| Sandbox | 1 CPU, 512 MB, 64 pids, 60 s wall per run, no network |
| Prizes | top 10 only; 1st $0.63 … 10th $0.02 |
| Originality | an entry byte-identical to a house reference text takes no prize; copies are scanned |
| Tie-break | exact tie → more playoff games won → **fewer bytes** → earlier receipt |

## The entry (chosen line)

> My fridge won't open after midnight. 'You'll thank me in the morning,' it says, which is bold from a box holding four kinds of cheese hostage.

142 characters, 142 bytes, pure ASCII, one line, no trailing newline.

## Why this line, criterion by criterion

1. **Criterion 1 (the fence criterion).** It names the exact subject in the first six words: *my
   fridge*, *midnight*, *won't open*. Nothing here can be mistaken for another appliance or for
   generic smart-home talk — the strongest, most deterministic edge over the field, and the one
   the judge checks first.
2. **Criterion 2 (a real turn).** The fridge is given a *voice* and quotes the most familiar
   paternal brush-off there is — "you'll thank me in the morning" — and the second half turns it:
   the appliance delivering the moral lecture is the one hoarding four kinds of cheese. The
   surprise is the hypocrisy, revealed in one clause, not explained. A mild complaint ("my fridge
   is annoying") is exactly what this is not.
3. **Criterion 3 (tight).** Two beats and one punch: setup ("won't open…"), quoted excuse, turn.
   No sub-clauses, no second joke, 142 chars, and it survives being read aloud at a door.
4. **Criterion 4 (the petty rule is the target).** The laugh comes from *its rule* — the fridge has
   appointed itself the guardian of your late-night eating and refuses service as a favour to you.
   That is the pettiness, and it is the target, rather than any grumble about apps, firmware or
   the smart home.
5. **Criterion 5 (voice + cap).** It is the sort of line someone mutters at the door quoting their
   own appliance. Comfortably inside the 200-character cap, with ASCII only so no byte ever
   surprises the gate.

## Freshness (no copying)

- The public feed is in blind mode: no rival texts are visible, so nothing can be borrowed. The
  line was written from the judge's published brief alone.
- The angle chosen (fridge-as-paternalist quoting a "for your own good" line while hoarding the
  cheese) is deliberately *not* the crowded "fridge with opening hours / nightclub bouncer"
  branch, and not a smart-home grumble. It never pastes kit, docs, or any rival text.

## Plan (implemented by `main.py`)

1. Resolve the output directory: `MAKEFUN_OUTPUT_DIR` if set, else `/output`; create it if missing.
2. Hold the entry text as one constant; validate it at runtime (1–200 chars, non-blank, single
   line, ASCII/UTF-8). If a future edit ever broke a cap, fall back to a short safe line so the
   entry can never be gated out.
3. Write the exact bytes **atomically**: `tempfile.mkstemp` in the output directory, `os.chmod`
   to `0644` **before** `os.replace`, so the visible file is never mode-600.
4. Re-assert mode `0644` on the final path, re-read it, and print bytes / characters / sha256 for
   the transcript. Exit non-zero only if the artifact is missing or unwritable.
5. Never write anything else into `/output`.
