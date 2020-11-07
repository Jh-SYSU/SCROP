
#!/usr/bin/env bash

dataset=USPTO-50K
model=${dataset}_model_average.pt

python score_predictions.py -targets data/${dataset}/tgt-test.txt -beam_size 10 -invalid_smiles \
                    -predictions experiments/results/predictions_${model}_on_${dataset}_beam10.txt