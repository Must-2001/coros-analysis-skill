# Evidence-backed charts

Use aligned daily panels for training duration by sport, main sleep and naps, and steps. This reveals timing without pretending to prove causation. For longer reviews use complete weekly aggregates and explain their denominators. Avoid dual axes, radar charts, combined readiness scores, diagnostic color thresholds, and decorative precision.

## Normalized input

The optional `scripts/render_review.py` consumes UTF-8 JSON, not raw MCP prose. The assistant must inspect current tool results, normalize units, deduplicate activities, exclude multisport parent/leg overlap, resolve source definitions, and document field sources first. Never parse labels heuristically without checking definitions. Do not put private source records or generated private charts into the public repository.

Top level:

- `timezone`: IANA timezone matching daily aggregate attribution.
- `start_date`, `end_date`: ISO dates, inclusive, at most 366 days.
- `language`: `en` or `zh`; Chinese requires a local CJK font.
- `synthetic`: true only for invented examples; visibly watermarked in the chart.
- `days`: one row per available local date, no duplicates. Omitted dates remain unknown.

Each daily row:

- `date`, `complete` (boolean): a partial day is shaded and excluded from summary metrics.
- `main_sleep_minutes`: actual asleep minutes, excluding awake time and naps; null if main sleep unavailable.
- `nap_minutes`: asleep minutes, not nap window duration; null if unavailable.
- `steps`: nonnegative count or null. Zero is an observation, null is unknown.
- `sleep_hrv_ms`: optional official daily HRV, not an average recalculated from raw series. The current renderer does not plot HRV; keep it for additional interpretation only.
- `training`: list of `{sport, minutes}` observations; optional `id` used for within-day duplicate validation. `[]` means confirmed no recorded activities after complete retrieval; null means unknown. Durations must use a consistent source definition.
- `sources`: a mapping from each provided metric name to its endpoint/field/date/coverage description. Training requires a source even for an empty list.

Nap-only days should have `main_sleep_minutes: null`, with observed nap minutes retained. Non-wear cannot be established from missing data alone. Coverage is metric-specific. Current script prints observed-period totals and medians only; it does not compute a historical baseline, correlations, or official scores.

## Run

Requires Python 3.10+ and Matplotlib (the summary-only mode uses the standard library). Use your environment's existing Python runtime. If needed, install Matplotlib in a virtual environment you control:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install matplotlib
.venv/bin/python skills/coros-analysis/scripts/render_review.py \
  examples/weekly-input.json --output /tmp/coros-demo.png
```

For an installed skill, resolve the renderer relative to its skill folder. For a personal review, use a private input/output directory outside this repository. An English chart remains available without a Chinese font; do not deliver broken glyphs. Keep missing points as gaps, label zeros explicitly, and never interpolate sleep gaps to make a continuous trend.

Before delivery, open the rendered file and inspect label clipping, legends, date order, gaps, and units. The normalizer and source interpretation remain the assistant's responsibility; schema validation cannot prove the underlying data is correct.
