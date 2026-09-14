@"

# Stage B — Model Development

## Model comparison

Three classification models were compared on the validation period:

- Logistic Regression — PR-AUC: 0.4433
- Random Forest — PR-AUC: 0.4023
- Gradient Boosting — PR-AUC: 0.4465

The prevalence baseline was 0.0899.

Gradient Boosting achieved the highest PR-AUC and was selected as the strongest candidate.

## Class imbalance

Gradient Boosting was tested without adjustment, with class weighting, and with oversampling.

- Untouched — PR-AUC: 0.4465, Precision: 0.6667, Recall: 0.1864
- Class weighted — PR-AUC: 0.4452, Precision: 0.3660, Recall: 0.5642
- Oversampled — PR-AUC: 0.4432, Precision: 0.3083, Recall: 0.6524

Class weighting and oversampling increased recall but did not improve PR-AUC.

## Calibration

Probability calibration was tested using Brier score.

- Raw Brier score: 0.0642
- Calibrated Brier score: 0.0642

Calibration did not meaningfully improve the Brier score.

## Stage B conclusion

Gradient Boosting is the strongest candidate based on validation PR-AUC. The imbalance experiments show a trade-off between detecting rejected lots and avoiding false rejection. The final model decision should consider the business cost of missed rejected lots versus false rejections.
"@ | Set-Content .\docs\project3\stage_b_decisions.md
