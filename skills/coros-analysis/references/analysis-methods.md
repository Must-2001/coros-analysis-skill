# Analysis methods

## Coverage first

State exact local dates, source, observation counts, and unavailable inputs. Count coverage separately for each metric; a day with steps may still lack sleep or HRV. Do not treat absence as rest, zero stress, or zero heart rate. A missing workout list can reflect a connection failure or a result cap. Do not infer non-wear as fact without evidence.

For a default seven-day review, compare against the preceding 28 non-overlapping calendar days. Use matching weekdays or weekly-normalized totals where appropriate. A seven-day total should not be directly compared to a 28-day total. Describe shorter available baselines and limited confidence rather than applying a universal minimum-day rule. Long-term reviews use comparable complete weeks; label partial boundary weeks.

For metric summaries report valid day count and denominator. Use a median for skewed daily observations when useful; do not call it the official device baseline. Calculate percentage changes only with a valid, nonzero denominator; otherwise use absolute differences. Round to the precision justified by the source. No imputation by default.

## Sleep source reconciliation

Prefer `querySleepOverview` for sleep duration and scope. Some daily-health summaries label the main sleep **period including awake time** as “Total”; that is not interchangeable with main sleep **asleep** or daily sleep including naps. Reconcile the same date's explicit asleep/period/awake fields before interpreting a difference. Never subtract awake twice or average these different definitions together. Keep a field-level source ledger when combining endpoints.

A nap-only day has observed nap sleep but unknown main sleep, not a confirmed extremely short night. Preserve the recorded nap total, flag incomplete main-sleep coverage, and omit it from main-sleep medians. Likewise, unavailable score sentinels (such as -1, or 0 alongside an explicit unavailable-detail message) are missing assessments, not bad sleep scores. Judge missingness from field meaning and source messages, not a universal rule that every zero is missing.

A completed long event in the comparison period can dominate a four-week average. Show weekly totals or the largest sessions alongside the average; do not assume every week was typical or infer a race from distance alone. Avoid conclusions about post-event recovery unless subsequent signals and subjective feedback support them.

## Units and records

- Normalize durations to seconds for arithmetic, then display readable hours/minutes.
- Normalize distance to meters; distinguish km, m, and miles in input/output.
- Pace is time per distance: smaller is faster. Swimming commonly uses time per 100 m, running time per km, cycling speed or power. If a returned label seems inconsistent, verify against distance, timer duration, moving duration, and source detail before reporting it. Do not silently “correct” an uncertain value.
- Aggregate running pace as total matching duration / total matching distance when appropriate, not an unweighted average of pace strings. Do not mix elapsed and moving time. State the denominator used.
- Distinguish sessions from sport legs in multisport data; avoid counting both an overall event and its legs twice.
- Deduplicate repeated records by source activity identifier. Never publish those identifiers as useful report content.

## Training and performance

Summarize frequency, duration, sport-specific distance, elevation where available, and official load metrics. Keep heart-rate/pace/power zone systems distinct. Derive zone time only when the source supplies adequate zone or time-series data; mean heart rate cannot reconstruct it.

For mixed sports, duration is useful exposure context, but equal duration does not imply equal physiological or musculoskeletal load. Preserve sport-specific views. Strength sessions need sets/repetitions/load and context where available; low average heart rate does not prove low training demand. Hiking may warrant duration/elevation and subsequent recovery review rather than running pace comparisons. Never infer a specific muscle injury or fatigue level from wearable load alone.

Performance comparison requires comparable sport, terrain, conditions, duration, and intensity. Lower heart rate on one slower or cooler run does not establish improved fitness. Describe confounders that are actually relevant; do not invent temperature, travel, illness, or alcohol data. Vendor VO2max and race predictions are estimates, not measured outcomes or promises. Do not fabricate HR zones, lactate thresholds, FTP, acute:chronic risk cutoffs, or historical scores.

## Recovery and daily life

Use official daily sleep HRV assessments and provided normal ranges. Raw HRV samples support within-night descriptions, not a replacement daily assessment. Check sleep duration, timing/regularity, resting heart rate, and recent exposure together. Sleep stage estimates are device estimates; do not diagnose sleep disorders from them.

Keep main sleep, naps, and total daily sleep separate; inspect source definitions before summing. Do not double-count naps already included in total daily sleep. Recovery percentage is an algorithmic snapshot, not medical clearance or proof the athlete feels ready.

Steps and activity minutes provide context about movement, not complete energy expenditure or motivation. Distinguish active calories, exercise calories, and total calories as returned. Do not calculate energy deficit or prescribe food intake from an ambiguous calorie field. Device stress scores do not identify a psychological cause.

## Evidence and recommendations

For each important observation provide its period, values, comparator, and material missingness. Separate observation (“sleep was shorter on four measured nights”) from hypothesis (“this may have contributed to how the week felt”). A handful of observations is descriptive, not proof of a relationship. Even longer associations have confounders; do not claim causality from correlation or seek many correlations until something looks significant.

Prioritize changes that matter to the user's question. Offer a small number of feasible options tied to goals and constraints, with conditions when subjective fatigue or symptoms are unknown. Do not automatically prescribe a hard session because recovery is high, or cancel training because one HRV value is low. Do not invent precise training intensities when the necessary context is absent.

For medical interpretation, abnormal symptoms, or diagnosis requests, follow the assistant's medical guidance requirements and use appropriate current authoritative sources. The ordinary training review is not a substitute for clinical assessment.
