# COROS Analysis Skill

[English](README.md) | [简体中文](README.zh-CN.md)

An open-source AI skill for understanding training, recovery, sleep, and everyday activity together, using your own COROS data through the official COROS MCP.

**Better questions. Traceable observations. Practical next steps.**

This is a set of instructions for a compatible AI assistant, not a standalone app or a new physiological prediction model. An independent community project; not affiliated with or endorsed by COROS.

## What it does

- **Weekly review:** compare training, sleep, recovery, and daily activity against your recent history.
- **Daily check-in:** review available readiness signals alongside your scheduled workout and personal context.
- **Long-term trends:** examine consistency and comparable performance across weeks or months.
- **Activity deep dive:** inspect laps, terrain, intensity, and the days around a session.
- **Focused questions:** explore patterns such as short sleep followed by harder training, without confusing association with causation.

Running, cycling, swimming, hiking, strength, and other recorded activities are considered in context. It does not treat running mileage as the measure of every sport.

## Requirements

1. An AI assistant that supports skills and MCP tools (such as Codex).
2. Your COROS account connected through the official COROS integration.
3. Available synced records. Some metrics depend on device, settings, wear time, and activity type.

The skill cannot authenticate to COROS for you. It discovers tools by capability instead of relying on installation-specific tool prefixes.

Official setup: [COROS MCP repository](https://github.com/coroslab/COROS-MCP) · [COROS MCP updates](https://www.coros.com/stories/coros-metrics/c/mcp-testing)

## Install in Codex

Clone this repository, then copy only `skills/coros-analysis` into your personal skills folder:

```bash
git clone https://github.com/Must-2001/coros-analysis-skill.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R coros-analysis-skill/skills/coros-analysis "${CODEX_HOME:-$HOME/.codex}/skills/"
```

If a folder named `coros-analysis` already exists, review or back it up before copying. Start a new conversation after installation if your assistant has not refreshed its skill list. Other assistants may use different skill locations; point them to the same `SKILL.md`.

## Try it

```text
Use $coros-analysis to review my last complete week. Compare it with
my recent baseline, explain the three most meaningful changes, and
suggest practical adjustments. Reply in English.
```

```text
用 $coros-analysis 综合复盘我最近一个完整周的训练、睡眠和日常活动。
跟我自己的历史比较，指出最重要的变化、证据和下周的调整建议。
```

Other questions:

- “How did I recover after my last long hike?”
- “Compare these two runs, accounting for terrain and intensity.”
- “I have 40 minutes today and slept poorly. Review my planned session.”
- “过去八周，我的训练连续性和恢复有什么变化？”

## How analysis works

The default weekly review uses seven complete local calendar days and the preceding 28 days as context. It checks coverage, keeps missing data separate from zero, and asks for deeper records only when useful. Historical API support varies; an incomplete baseline is disclosed rather than invented.

Every report separates **observations**, **possible explanations**, and **actions**. Official COROS assessments remain distinct from the assistant's interpretation. No proprietary readiness score, diagnosis, injury prediction, or guaranteed race result is generated.

See [analysis methods](skills/coros-analysis/references/analysis-methods.md), [tool routing](skills/coros-analysis/references/coros-tools.md), and a [fully fictional bilingual example](examples/weekly-review.md).

## Privacy and control

Analysis is read-only by default. Connecting data does not authorize changes to workouts or plans. Saving or changing training requires a separate explicit request and the appropriate tool workflow. This repository contains no athlete records, credentials, GPS tracks, or device identifiers. Reports stay in the conversation unless you request an export. Never add personal exports to a public contribution.

For concerning symptoms or medical questions, this skill cannot provide a diagnosis; seek appropriate professional assessment. Recovery percentages are not medical clearance.

## Contributing

Report routing errors, unit problems, missing-data failures, or examples of unsupported conclusions. Use synthetic or anonymized minimal examples; remove timestamps, coordinates, IDs, and other identifying details as needed. Behavioral acceptance cases are in [evals/scenarios.md](evals/scenarios.md). They are a manual review checklist, not a claim of clinical validation.

## License

[MIT](LICENSE). COROS trademarks belong to their respective owners.
