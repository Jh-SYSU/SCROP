#!/usr/bin/env bash

original_dataset=USPTO-50K   # USPTO-50K for Self-Corrected Retrosynthetic Reaction Predictor
dataset=MIT_Syntax_Corrector # self-corrected retrosynthesis
original_model=${original_dataset}_model_average.pt
model=${dataset}_model_average.pt

# translate the training-validation set 
python translate.py -model experiments/models/${original_model} \
                    -src data/${original_dataset}/src-train-val.txt \
                    -output experiments/results/predictions_${model}_on_${original_dataset}_beam10_train_val.txt \
                    -batch_size 64 -replace_unk -max_length 200 -beam_size 10 -n_best 10


# obtain the noSC preditions
python translate.py -model experiments/models/${original_model} \
                    -src data/${original_dataset}/src-test.txt \
                    -output experiments/results/predictions_${original_model}_on_${original_dataset}_beam10_test.txt \
                    -batch_size 64 -replace_unk -max_length 200 -beam_size 10 -n_best 10


# process the syntax corrector dataset and train the SC system
python preprocess.py -train_src data/${dataset}/experiments/results/predictions_${original_model}_on_${original_dataset}_beam10_test.txt \
                     -train_tgt data/${dataset}/tgt-train-val-beam10.txt \
                     -valid_src data/${dataset}/src-val.txt \
                     -valid_tgt data/${dataset}/tgt-val.txt \
                     -save_data data/${dataset}/${dataset} \
                     -src_seq_length 1000 -tgt_seq_length 1000 \
                     -src_vocab_size 1000 -tgt_vocab_size 1000 -share_vocab


python  train.py -data data/${dataset}/${dataset} \
                 -save_model experiments/checkpoints/${dataset}/${dataset}_model_self_corrected \
                 -seed 42 -gpu_ranks 0 -save_checkpoint_steps 20000 -keep_checkpoint 20 \
                 -train_steps 200000 -param_init 0  -param_init_glorot -max_generator_batches 32 \
                 -batch_size 4096 -batch_type tokens -normalization tokens -max_grad_norm 0  -accum_count 4 \
                 -optim adam -adam_beta1 0.9 -adam_beta2 0.998 -decay_method noam -warmup_steps 8000  \
                 -learning_rate 2 -label_smoothing 0.0 -report_every 10000 \
                 -layers 4 -rnn_size 256 -word_vec_size 256 -encoder_type transformer -decoder_type transformer \
                 -dropout 0.1 -position_encoding -share_embeddings \
                 -global_attention general -global_attention_function softmax -self_attn_type scaled-dot \
                 -heads 8 -transformer_ff 2048

# obtain the corrected preditions, strip null rows if needed
python translate.py -model experiments/checkpoints/${dataset}/${dataset}_model_self_corrected \
                    -src experiments/results/predictions_${original_model}_on_${original_dataset}_beam10_test.txt \
                    -output experiments/results/predictions_${model}_on_${dataset}_beam10_self_corrected_test.txt \
                    -batch_size 64 -replace_unk -max_length 200 -beam_size 10 -n_best 10


# combine two csv-file to obtain the final results (SCROP preditions)
python score_predictions_self_corrected.py -targets data/${dataset}/tgt-test.txt -beam_size 10 -invalid_smiles \
                    -original_predictions experiments/results/predictions_${original_model}_on_${original_dataset}_beam10_test.txt \
                    -selfCorrected_predictions experiments/results/predictions_${model}_on_${dataset}_beam10_self_corrected_test.txt