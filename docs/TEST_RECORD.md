# A2 test record

**Environment:** Python 3 standard-library engine, local demo app.

| Test | Input | Expected | Observed | Result |
|---|---|---|---|---|
| T1 clear request | `Suggest a quiet one-day hiking trip near Birmingham` | Hiking intent, no ambiguity warning | Rule engine identifies Hiking / Birmingham | PASS |
| T2 vague request | `Suggest a day trip` | Flag missing activity and mark city result as assumed | Ambiguity flag true; assumed answer | PASS |
| T3 user repairs T2 | Activity = Hiking; budget = Low | Updated hiking recommendation, selected preference visible | Corrected intent and recommendation | PASS |
| T4 multiple activities | `hiking or museum?` | Do not force a single activity | Ambiguity flag true | PASS |
| T5 invalid correction | Activity = Skydiving | Reject with validation error | ValueError | PASS |
| T6 empty prompt | blank spaces | Reject | ValueError | PASS |
| T7 no refinement selection | `{}` | Reject | ValueError | PASS |
| T8 city-specific request | `I want a city tour` | City sightseeing | City sightseeing | PASS |

Run with `python -m unittest discover -s tests -v` for independently reproducible automated evidence. These tests confirm deterministic rules only; **they do not show that novice users find the interface usable**.

## Suggested manual UI checks before submission

- Open the app on a laptop and phone-sized browser; observe layout.
- Verify typing, submit via button and Enter, selection feedback, correction button visibility and reset.
- Capture actual screenshots for the three storyboard examples and link them in the final report.
