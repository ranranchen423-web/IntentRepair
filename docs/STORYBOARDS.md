# A2 illustrated interaction storyboard plan

These are reproducible scenarios. For final report, add screenshots captured from the running app (not fake screenshots) after following each sequence.

## 1. Normal use — clear prompt

| Frame | User action | System response / feedback |
|---|---|---|
| 1 | Opens IntentRepair | Input interface and examples are visible. |
| 2 | Enters `Suggest a quiet one-day hiking trip near Birmingham` | Browser submits text. |
| 3 | Waits for response | Rule engine extracts `Hiking` and `Birmingham`; no ambiguity flag. |
| 4 | Reads output | Illustrative nature-walk plan shown, with sample-data disclaimer. |
| 5 | May continue | Input remains available and refinement control is visible. |

## 2. Misunderstanding and repair — vague prompt

| Frame | User action | System response / feedback |
|---|---|---|
| 1 | Enters `Suggest a day trip` | Request has no clear activity. |
| 2 | Reads response | System illustrates a city trip assumption, marked explicitly. |
| 3 | Notices mismatch with intended hiking | Visible warning and `Refine your request` button offer a recovery path. |
| 4 | Clicks refinement and selects `Hiking` | Editable activity control shows selection. |
| 5 | Clicks `Update recommendation` | New response reflects hiking, with success feedback. |

## 3. Additional constraint refinement

| Frame | User action | System response / feedback |
|---|---|---|
| 1 | From a hiking response, selects refinement | The menu opens. |
| 2 | Selects `Low` budget and `Nearby` distance | Selected choices visibly change. |
| 3 | Clicks update | Server validates and merges preferences. |
| 4 | Reads new output | Refreshed answer lists selected budget and distance. |

