# Test report — news-image-20261119

Entry: **THE WORLD TODAY — Thursday 19 November 2026** (35 stories, 6 continents, one day).
Built 20 Nov 2026 by the composition agent. Nothing submitted to make.fun.

## Results (name / PASS-FAIL / evidence / issues / fixes)

### entry.png size + dimensions
- **PASS** — 255,077 bytes (24.3% of the 1 MiB limit), 1024×1024 RGB.
- Evidence: `python3 compose.py` printed `entry.png: 255,077 bytes (OK <=1MiB)` (fix round, 20 Nov 2026);
  IHDR check read width 1024, height 1024.
- Issues: none. Fixes: none.

### entry.png sha256
- **PASS** — `4b646ca4d2deca2aa89462d504be9c722c48f80d7fdf1e78a9dd6f3172e75c41`
- Evidence: `sha256sum entry.png` (source) and the main.py output below
  return the identical digest. (Pre-fix-round digest was
  `cb7f5b29b9af314c118e82f4a2630a293f63254bc1a0318c553a679299537e37`;
  it changed because index lines 21 and 28 changed.)

### main.py byte-identical reproduction
- **PASS** — main.py run into a fresh dir (`/tmp/mf-fix1`) with
  `MAKEFUN_OUTPUT_DIR` set; output `cmp`-identical to `repo/entry.png`,
  same sha256 `4b646ca4…72e75c41`, same size 255,077 bytes.
- Issues: none. Fixes: none.

### compose.py warnings (clipping / shrink floors / index overflow)
- **PASS** — `compose.py` printed `no warnings` (fix round, 20 Nov 2026):
  no headline/sub clipped, no shrink floor hit, no index line too wide,
  no index row past its box. The two changed index lines (21, 28) fit on
  one line each.
- Evidence: compose run output, 20 Nov 2026 (pre-fix-round run also
  printed `no warnings`).

### Legibility check at full size (1024×1024, checklist D.5)
- **PASS** — entry.png inspected at full size:
  - Masthead, date "THURSDAY 19 NOVEMBER 2026", count line and judge line
    ("Every story below happened, or was first reported, on 19 November
    2026.") all legible.
  - Lead headline fits one line; lead sub fits one line.
  - All 10 tile headlines legible (2-line wraps on #2, #6, #8, #9, #10,
    #11); all tile subs on one line, no clipping.
  - All 11 map pins visible and numbered; The Hague (#2) / Frankfurt
    (#9) nudged apart and distinct; #5 (Xavier) and #3 (Auckland) at the
    map edges are fully visible.
  - All 24 index lines (12–35) on one line each, legible, no overflow.
  - Sources line fits one line.
- Issues: none. Fixes: none.

### Illustration review at full size (checklist D.5 + C.4)
- **PASS with fixes** — all 11 vignettes reviewed at full size on a
  contact sheet before composing; 3 redrawn for judge-tied reasons:
  - #4 Anthropic: first version sparse (small screen/rocket, dead navy
    space). Redrawn larger (Nasdaq screen, rocket with visible flame,
    candlesticks, second tower, coins low). Re-checked: flame now visible
    above the ground line.
  - #8 COP31: first version's draft papers read as a thin brown bar.
    Redrawn as two large lined sheets on a table with a leaf sprig.
    Re-checked: sheets now read as papers.
  - #10 Lula: sun overlapped the Congress dome and the decree paper was
    tiny. Sun moved top-left; decree paper enlarged with a red seal.
    Re-checked: Congress + flag + decree all read clearly.
  - The other 8 passed first review: #1 trilateral (3 flags + Kylin
    Villa pavilion + Shenzhen skyline), #2 ICJ (Peace Palace + scales),
    #3 GTA VI (neon Vice City skyline + moon + palms), #5 Xavier
    (cyclone spiral + island shelter), #6 Akvan (spiral + boat + coast),
    #7 Tokyo (Fuji + Tokyo Tower + India/Japan flags), #9 UniCredit
    (Frankfurt towers + joining arch + converging arrows + coins),
    #11 Mrima Hill (red-earth terraces + crystals + acacia + Kenyan flag).
- Approach: PIL vector illustrations (`vignettes.py`, flat editorial
  style, text-free by design). The media image-generation tool is capped
  at 4 images per response, so a mixed generated/PIL set would have been
  stylistically inconsistent across 11 slots; a single consistent PIL set
  was chosen instead, as the task allows.
- Remaining weakness: tile images are small (242×64), so fine detail in
  #5/#6 spirals and #8 papers is only just visible at tile size — the
  same constraint as the accepted 20261118 entry, and the full-size
  review confirms each tile's subject is identifiable.

### Figure fidelity (research-notes.md Pass 2)
- **PASS** — spot-checked against research-notes.md: GTA uses ~19.1M /
  ~$1.84B (not 15.88M/$1.54B); Anthropic uses $111.50 first trade /
  $97.17 close (no "~$1.08T"); UniCredit uses $1.4T (not $1.43T);
  McBride leads with 248 votes; #18 framed "UNCONFIRMED claim";
  #31 framed as the NCoS response; #32 as day 3; #30 as the 19 Nov
  police reveal + charges.
- No dropped figure was reintroduced.

### Secrets check
- **PASS** — grep for api keys / passwords / private keys / tokens across
  `*.py` and `*.md` in the repo returned nothing (exit 1, no matches).
  No wallet addresses, seeds or credentials in any file.

## Fix round — audit-pass2.md findings (20 Nov 2026, fix agent; did NOT build or audit this entry)

### #21 FAIL — story REPLACED (D.11), not reframed
- **PASS** — Old #21 (Argentina condemns Princess Anne's Falklands visit) removed entirely: the Foreign Ministry statement was issued Tue 17 Nov; 19 Nov items are republications. Replacement #21: **Argentina logs record October trade surplus** — INDEC released October trade data Thu 19 Nov (exports $10.06B, +26.4% y/y, new monthly record; imports $6.67B; surplus $3.39B). South America stays at 3 stories (#10, #21, #22); total stays 35; all 6 continents covered.
- Evidence: Reuters via TradingView publ. 2026-11-19T19:07:20Z ("the government's statistics office said on Thursday"); Trading Economics release calendar lists the Oct Balance of Trade release 19 Nov 19:00; Caputo X post 19 Nov 16:21. Republication-trap check: earliest publication of the $3.39B/$10.06B October figures is 19 Nov; the similar $2.98B/$10.04B figures are September's (published 19–20 Oct), a different month.
- Issues: none. Fixes: compose.py index line 21, research-notes.md #21 section + continent counts + dropped list, README.md index line 21. No other story, illustration, layout, or text touched.

### #28 WEAK — count fixed
- **PASS** — Index line 28 changed from "40+ partners" to "nearly 40 leaders" (AP wording, per audit). Story itself unchanged.
- Evidence: compose.py line 28 + research-notes.md #28 section + README.md line 28 all updated; grep confirms no "40+" remains outside the fix-round documentation notes.
- Issues: none. Fixes: as above.

### Candidates considered and rejected (fix round)
- **Lula criticises markets over "speculation" (Reuters, 19 Nov 14:52 UTC)** — genuine 19 Nov story, but a second Lula story when #10 is already Lula; rejected for duplication.
- **Milei bids farewell to Pope Leo XIV (Al Jazeera, publ. 19 Nov 17:48Z)** — rejected: the farewell's date could not be cleanly anchored (source URL path dated 12 Nov; Pope's visit spanned several days); not pursued further once the INDEC release verified.
- **Paraguay's Santiago Peña "jailed / moved to military prison" (Breitbart list, 19 Nov)** — rejected: Peña is Paraguay's sitting president; the claim is implausible/unverified and no credible corroboration was found.
- **Ecuadorian fishermen sue Trump administration over alleged drone strike (Netasgard, 19 Nov 01:29)** — rejected: low-credibility aggregator, filing date and facts not independently verifiable.
- **OpenAI/Aleph ChatGPT Ads in 44 countries (GlobeNewswire, 19 Nov 14:00 GMT)** — genuine 19 Nov, kept as fallback only; not needed once the Argentina trade release verified (and it would have dropped South America to 2 stories).

## Files
- `entry.png` — 255,077 bytes, sha256
  `4b646ca4d2deca2aa89462d504be9c722c48f80d7fdf1e78a9dd6f3172e75c41`
- `main.py` — stdlib-only copy-pattern entrypoint (same as 20261118)
- `compose.py` — layout-D composer (adapted from 20261118)
- `vignettes.py` + `candidates/01–11` — the 11 illustrations
- `layouts/layout-d.png`, `layouts/layout-d-300.png`
- `ne_110m_land.geojson`, `README.md`, `LICENSE`, `research-notes.md`
