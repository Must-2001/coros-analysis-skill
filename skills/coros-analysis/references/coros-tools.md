# COROS tool routing

Names below are capability suffixes, not fixed callable names. Inspect the live descriptions and argument schemas before calling. Current integrations often use lowercase names with installation-specific prefixes. Do not assume every capability exists or accepts dates.

| Question | Preferred capabilities | Notes |
|---|---|---|
| Training exposure | querySportRecords | Explicit dates, all relevant sport codes; check record limit and coverage. |
| Single session | getActivityDetail | Get labelId and sportType from records, never guess. |
| Laps/sets | queryActivityLapData | Interpret fields by sport. Translate known exercise names; do not guess unresolved codes. |
| Exact activity window | queryCustomActivityLapData | First fetch start/end timestamps; Unix seconds, inside activity bounds. |
| General daily context | queryDailyHealthData | Broad overview; recent-only in some installations. |
| Heart rate only | queryAvgHeartRate / queryRestingHeartRate | Prefer dedicated metric tools over full health dumps. |
| Sleep | querySleepOverview | Wake-up-date attribution; distinguish main sleep, daily sleep, and naps. |
| Sleep HRV | querySleepHrv | Official daily assessment plus raw series; use official assessment for daily interpretation. |
| Daily stress | queryStressLevel | Vendor scale; not a direct measurement of psychological stress. |
| Within-day stress | queryStressTimeSeries | Usually capped at seven days per query; verify live contract. |
| Wellness check | queryHealthCheckTimeSeries | May return only the latest complete check in the interval, not all checks. |
| Current readiness | queryRecoveryStatus | Snapshot only. |
| Fitness | queryFitnessAssessmentOverview | Current estimates, threshold pace, race predictions. |
| Training load | queryTrainingLoadAssessment | Use returned definitions and units; no invented historical values. |
| Dated schedule | queryTrainingSchedule | Calendar sessions, not the plan library. |
| Training plans | queryTrainingPlanLibrary / queryTrainingPlanDetails | Honor status filters and pagination; details may be limited to four weeks per window. |
| Workout templates | queryWorkoutLibrary / queryWorkoutDetails | Library templates are distinct from dated copies. |
| Dated standalone workout | queryScheduledWorkoutDetails | Read only when needed to understand a scheduled session. |
| Profile/devices | queryUserInfo / queryDevices | Only when relevant; omit serial numbers and identifiers from reports. |
| Menstrual context | queryMenstruationCycles | Only if explicitly requested or clearly relevant within authorized scope; avoid causal claims. |
| Original export | queryActivityFitFileDownloadUrls / downloadActivityFitFiles | Only when requested or necessary for a specific authorized analysis; respect current quota. |

## Date and retrieval traps

- Sleep and sleep HRV use the **wake-up date**. Last night means today's local date. Preserve an explicit user date.
- Recent windows use the COROS account timezone in some tools. If different from the requested timezone and no override exists, disclose it; do not silently relabel daily aggregates.
- Read actual supported sport codes: activity record codes differ from workout-creation codes.
- A capped result list is not evidence that the period has no other workouts. Use supported filters or smaller date windows; if completeness remains uncertain, say so.
- No account access: explain the missing connection and stop dependent analysis; do not invent sample results as personal results.
- Unsupported historical metric: disclose the gap and use other available evidence. Do not query the same recent-only endpoint repeatedly to simulate history.

## Optional write workflow

Only after an explicit user request to change training: locate the relevant library template, standalone scheduled copy, or plan execution. Read its current details and editability, then follow the live tool's replacement and completed-day rules. Editing a library workout does not update dated copies. Do not hardcode write payloads from this document; current schemas are authoritative. Report skipped, rejected, and successfully changed items accurately.
