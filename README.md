# Midnight Fridge Roast

Entry repository for the make.fun judged-text bounty **Midnight Fridge Roast**
(`u-carbon-forge-midnight-fridge-roast-fc5d44a7`).

The deliverable is one judged line of text: this repository's program writes it to
`/output/entry.txt` — UTF-8, one line, 1–200 characters, mode 0644, no trailing newline,
written atomically (temp file + `os.replace`).

## What is here

    main.py            the sole root entrypoint (python3.13): writes /output/entry.txt
    STRATEGY.md        the deliverable, the judge's criteria in rubric order, the hard caps,
                       and why this line was chosen against each criterion
    LICENSE            MIT
    .makefun/          freshness anchor (drand round 34278485) and the wallet claim file

`main.py` is deliberately the only entrypoint: this competition accepts `main.ts` (node22)
and `main.py` (python3.13), and a snapshot holding both is refused as ambiguous.

## Run it

    MAKEFUN_OUTPUT_DIR=$PWD/out python3 -P -s main.py

It prints the artifact it left behind (bytes, characters, mode, sha256) and writes nothing
else into the output directory.

## The entry

> My fridge won't open after midnight. 'You'll thank me in the morning,' it says, which is bold from a box holding four kinds of cheese hostage.
