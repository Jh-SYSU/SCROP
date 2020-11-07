#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, unicode_literals
import argparse
from rdkit import Chem
import pandas as pd
import onmt.opts

def canonicalize_smiles(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is not None:
        return Chem.MolToSmiles(mol, isomericSmiles=True)
    else:
        return ''

def get_rank(row, base, max_rank):
    for i in range(1, max_rank+1):
        if row['target'] == row['{}{}'.format(base, i)]:
            return i
    return 0

def main(opt):
    with open(opt.targets, 'r') as f:
        targets = [''.join(line.strip().split(' ')) for line in f.readlines()]

    targets = targets[:]
    predictions = [[] for i in range(opt.beam_size)]


    # predictions of Original
    beam = pd.DataFrame(targets)
    beam.columns = ['target']
    total = len(beam)

    with open(opt.original_predictions, 'r') as f:
        # lines = f.readlines()
        # lines = [''.join(x.strip().split()[1:]) for x in lines]
        # print(lines[1])
        for i, line in enumerate(f.readlines()):
            # if i ==800*10:
            #     break
            predictions[i % opt.beam_size].append(''.join(line.strip().split(' ')))
            
    
    for i, preds in enumerate(predictions):
        beam['prediction_{}'.format(i + 1)] = preds
        beam['canonical_prediction_{}'.format(i + 1)] = beam['prediction_{}'.format(i + 1)].apply(
            lambda x: canonicalize_smiles(x))

    beam['rank'] = beam.apply(lambda row: get_rank(row, 'canonical_prediction_', opt.beam_size), axis=1)


    # predictions of Self Syntax_Corrector
    beamsys = pd.DataFrame(targets)
    beamsys.columns = ['target']
    with open(opt.selfCorrected_predictions, 'r') as f:
        # lines = f.readlines()
        # lines = [''.join(x.strip().split()[1:]) for x in lines]
        # print(lines[1])
        for i, line in enumerate(f.readlines()):
            # if i ==800*10:
            #     break
            predictions[i % opt.beam_size].append(''.join(line.strip().split(' ')))
            
    
    for i, preds in enumerate(predictions):
        beamsys['prediction_{}'.format(i + 1)] = preds
        beamsys['canonical_prediction_{}'.format(i + 1)] = beamsys['prediction_{}'.format(i + 1)].apply(
            lambda x: canonicalize_smiles(x))

    beamsys['rank'] = beamsys.apply(lambda row: get_rank(row, 'canonical_prediction_', opt.beam_size), axis=1)
    # test_df.to_csv('surprise.csv')
    # correct = 0
    # invalid_smiles = 0
    # for i in range(1, opt.beam_size+1):
    #     correct += (test_df['rank'] == i).sum()
    #     invalid_smiles += (test_df['canonical_prediction_{}'.format(i)] == '').sum()
    #     if opt.invalid_smiles:
    #         print('Top-{}: {:.1f}% || Invalid SMILES {:.2f}%'.format(i, correct/total*100,
    #                                                                  invalid_smiles/(total*i)*100))
    #     else:
    #         print('Top-{}: {:.1f}%'.format(i, correct / total * 100))


    for i in range(len(beam['rank'])):
        for j in range(1,opt.beam_size+1):
            if beam['canonical_prediction_{}'.format(j)][i]=='-1':    #beam['canonical_prediction_{}'.format(j)][i] == '':
                beam['canonical_prediction_{}'.format(j)][i] = beamsys['canonical_prediction_{}'.format(j)][i]
#             beam['canonical_prediction_{}'.format(j)][i] = beamsys['canonical_prediction_{}'.format(j)][i]

    beam_intergrate = beam
    beam_intergrate['rank'] = beam_intergrate.apply(lambda row: get_rank(row, 'canonical_prediction_', 10), axis=1)
    correct = 0
    invalid_smiles= 0
    total = 5004
    for i in range(1, opt.beam_size+1):
        correct += (beam_intergrate['rank'] == i).sum()
        invalid_smiles += (beam['canonical_prediction_{}'.format(i)] == '-1').sum()
        if opt.invalid_smiles:
            print('Top-{}: {:.1f}% || Invalid SMILES {:.2f}%'.format(i, correct/total*100,
                                                                 invalid_smiles/(total*i)*100))
        else:
            print('Top-{}: {:.1f}%'.format(i, correct / total * 100))



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='score_predictions.py',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    onmt.opts.add_md_help_argument(parser)

    parser.add_argument('-beam_size', type=int, default=10,
                       help='Beam size')
    parser.add_argument('-invalid_smiles', action="store_true",
                       help='Show %% of invalid SMILES')
    parser.add_argument('-original_predictions', type=str, 
                       help="Path to file containing the predictions")
    parser.add_argument('-selfCorrected_predictions', type=str,
                       help="Path to file containing the predictions")
    parser.add_argument('-targets', type=str, default="data/MIT_mixed_augm_clusterSplit/tgt-valid-RX",
                       help="Path to file containing targets")

    opt = parser.parse_args()
    main(opt)
