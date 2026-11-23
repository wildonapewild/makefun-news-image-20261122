# THE MERIDIAN LINE — Final 4 (@wildonaped) · NI22 Wave 7

One-page newspaper for Sunday 22 November 2026: 15 cards + 21 briefs = 36
stories, 7 regions. Lead trio Ukraine → COP31 → Iran; indigo / cream;
Layout A (three leads in a row, then 12 minis 4×3).

## Build

- `compose.py` — PIL renderer (W=3900; fonts x1.45 vs G6, structure x~1.3).
  Renders `variant_A.png` (matrix layout A, matrix palette), `variant_B.png`
  (alternate layout B, same palette), `variant_C.png` (layout A, ochre accent).
  Duel in `duel.md`: winner **A (35/40)**.
- `ni22v7-finish.sh final4 A` — fits winner to `entry.png` (1024×1024),
  runs margin check with `--fresh ni22-fresh-g7.txt`, writes `preview-300.png`.
- `main.py` — stdlib-only copy-only carrier with the 1024×1024 dimension gate.

## Gates (verified)

- entry.png 1024×1024, 219.268 bytes, sha256
  `f534c12a6a580a58319115b2d72fe40177162b7671197d19374c2fb9a75be68e`
- margin check 13/13 (fresh G7 pool)
- render aspect 0,908 (3900×4293)
- main.py 2× run byte-identical (see verification below)

## Verify

```
MAKEFUN_OUTPUT_DIR=/tmp/ni22v7-verify-final4 python3 main.py
```

Izin Brian (chat utama, 23 Nov 2026): "Ya — bangun G7, bedah Top 1 dulu".
