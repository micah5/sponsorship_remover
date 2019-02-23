#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Author: Micah Price (98mprice@gmail.com)
    Trains network and saves trained model to ./output

    TODO: Like I mention in predict.py, we need to work on writing
    some cohesive argument flags. At the moment all the directory
    paths are pretty much hardcoded (and the same issue applies to
    certain of the model hyperparameters)
"""

import sys

from argparse import ArgumentParser

import sponsorship_remover.const
from sponsorship_remover.helper import read_data
from sponsorship_remover.rnn import create_model, create_tokenizer, preprocess_features, train, predict

def main(argv):
    parser = ArgumentParser()
    parser.add_argument('filename', help='path of file to train on', nargs='?', default='./dataset/data.csv')

    args = parser.parse_args()

    x_text, y_text = read_data(args.filename, x_colname='text', y_colname='sentiment')

    tokenizer = create_tokenizer(x_text)
    x_pad, feature_length = preprocess_features(x_text, tokenizer=tokenizer)

    model = create_model(feature_length)
    model.summary()

    train(model, x_pad, y_text, filename='./output/model.h5', validation_split=0.05)

if __name__ == '__main__':
   main(sys.argv[1:])
