# Stage C — Threshold and Decision Analysis

## Purpose

Stage C converts the model's probability output into an operational ACCEPT/REJECT decision.

The final test period remains untouched. Threshold selection is based only on the validation period.

## Threshold results

| Threshold | Precision | Recall |
|---:|---:|---:|
| 0.10 | 0.2883 | 0.6585 |
| 0.15 | 0.3447 | 0.5772 |
| 0.20 | 0.3996 | 0.5014 |
| 0.25 | 0.4305 | 0.4363 |
| 0.30 | 0.4714 | 0.3577 |
| 0.35 | 0.5576 | 0.3279 |
| 0.40 | 0.5868 | 0.2656 |
| 0.45 | 0.6462 | 0.2276 |
| 0.50 | 0.6602 | 0.1843 |

## Decision

A threshold of **0.20** is selected for the final evaluation.

At this threshold, the validation results were:

- Precision: 0.3996
- Recall: 0.5014
- PR-AUC: 0.4388

The threshold was selected because the project prioritizes detecting rejected cocoa while still controlling unnecessary false rejections. Lower thresholds provide more recall but substantially reduce precision, while higher thresholds miss more genuinely rejected lots.

The threshold is now fixed and will not be changed using the final test results.

## Important evaluation rule

The final test period must remain untouched until Stage D. No threshold tuning will be performed using final-test results.
