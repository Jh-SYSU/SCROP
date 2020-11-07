# Self-Corrected Retrosynthetic Reaction Predictor

This is the code for the "Predicting Retrosynthetic Reaction using Self-Corrected Transformer Neural Networks" paper
found on [Journal of Chemical Information and Modeling](https://pubs.acs.org/doi/abs/10.1021/acs.jcim.9b00949)

To implement our models we were based on [OpenNMT-py (v0.4.1)](http://opennmt.net/OpenNMT-py/).

## Install requirements

Create a new conda environment:

```bash
conda create -n SCRP_transformer python=3.5
source activate SCRP_transformer
conda install rdkit -c rdkit
conda install future six tqdm pandas
```

The code was tested for pytorch 0.4.1, to install it go on [Pytorch](https://pytorch.org/get-started/locally/).
Select the right operating system and CUDA version and run the command, e.g.:

```bash
conda install pytorch=0.4.1 torchvision -c pytorch
```
Then,
```bash
pip install torchtext==0.3.1
pip install -e . 
```


## Pre-processing 

In the experiments we use an open-source datasets (and train/valid/test splits).

* [**USPTO-50K** dataset](https://github.com/pandegroup/reaction_prediction_seq2seq) data/USPTO-50K
* [**USPTO-50K-cluster** dataset]() 
* [**Jin’s USPTO dataset**](https://github.com/sysu-yanglab/Self-Corrected-Retrosynthetic-Reaction-Predictor/blob/master/data/Jin's_USPTO_dataset.zip)

The tokenized datasets can be found on the `data/` folder. 


For Input file generation, we the [preprocess.sh](https://github.com/sysu-yanglab/Self-Corrected-Retrosynthetic-Reaction-Predictor/blob/master/preprocess.sh) script:

We use a shared vocabulary. The `vocab_size` and `seq_length` are chosen to include the whole datasets.


## Training

The data has already been preprocessed for training the Self-Corrected Retrosynthetic Reaction Predictor


Model training can be started by running the [training.sh](https://github.com/sysu-yanglab/Self-Corrected-Retrosynthetic-Reaction-Predictor/blob/master/training.sh) script


To achieve the best results with single models, we average the last 10 checkpoints.

## Testing

To generate the predictions use the `translate.py` script:

### greedy search

Model testing of greedy search can be started by running the [testing_greedy_search.sh](https://github.com/sysu-yanglab/Self-Corrected-Retrosynthetic-Reaction-Predictor/blob/master/testing_greedy_search.sh) script


### beam search

Model testing of greedy search can be started by running the [testing_beam_search.sh](https://github.com/sysu-yanglab/Self-Corrected-Retrosynthetic-Reaction-Predictor/blob/master/testing_beam_search.sh) script


# Evaluate predictions

Run the the [score_predictions.sh](https://github.com/sysu-yanglab/Self-Corrected-Retrosynthetic-Reaction-Predictor/blob/master/score_predictions.sh) script to get the top-10 accuracy.

# Molecular syntax corrector

1. use a fully trained model to generate the top ten candidate precursors given a set of target compounds in the training set and validation set.
2. construct a training library that consists of a set of input-output pairs, where the inputs are predicted invalid reactants, and the outputs are the ground truth reactants.
3. get the top-1 candidate produced by the syntax corrector and replace the original invalid smiles.
* run the the [self_corrected.sh](https://github.com/sysu-yanglab/Self-Corrected-Retrosynthetic-Reaction-Predictor/blob/master/self_corrected.sh) script to get the top-10 accuracy of the syntax corrector.


## Citation

If you find this work useful in your research, please consider citing the paper:
"Predicting Retrosynthetic Reaction using Self-Corrected Transformer Neural Networks".
