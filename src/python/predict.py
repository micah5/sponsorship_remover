#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Author: Micah Price (98mprice@gmail.com)
    Use to run a prediction on a set of strings.
    Input can be file path and the sequences will be read from there,
    otherwise it'll default to a dummy dataset with 4 tests.

    This file is just here for testing purposes, as it's been ported
    across to tensorflow.js in ./javascript/predict.js (and this is
    the version being used in the current extension).

    TODO: Need to intergrate this with the old codebase so that we
    can input a video id or channel id and scrape a training dataset
    directly from youtube itself.

    TODO: Find a tidy way to handle command line arguments. At the moment
    most of the directory paths are being hardcoded, as I had some issues
    writing cohesive flags between both this and train.py. Another option
    is to store them in ./sponsorship_remover/const.py
"""

import sys

from argparse import ArgumentParser
from youtube_transcript_api import YouTubeTranscriptApi
from keras.models import load_model

from sponsorship_remover.helper import read_data
from sponsorship_remover.rnn import predict, create_tokenizer, preprocess_features, get_feature_length

def main(argv):
    parser = ArgumentParser()
    parser.add_argument('filename', help="path of file to test on", nargs='?')

    args = parser.parse_args()

    if args.filename is not None:
        # read from file
        with open(args.filename) as fp:
            x_test = fp.readlines()
    else:
        # default to some test strings
        x_test_sponsored = [  'mecha fights giant robots youre either in or youre in and best of all you guys can get an ad free 30-day trial a verve',
                              'premium for people what does that mean well that includes offline viewing you can watch all your favorite shows on the',
                              'go without internet access and of course it also means no ads need i say more so to start your ad free 30-day trial',
                              'verve premium just go to verve co slash jacksfilms link in the description again thats verve co slash jacksfilms',
                              'for a 30-day ad free trial a verve premium oh i have a challenge for you lets create a flag for gamers subscribe',
                              'for more leaks also click right here to see the preview see i episode uh heres a clip why oh why should you go vegan to',
                              'this video was made possible by brilliant',
                              'learn something new everyday with brilliant for 20% off by being one of the first 200 to sign up at brilliant.org/wendover',
                              'so you know those short free moments during your day like when waiting for the bus or the train or for an appointment or a call? it’s hard to do anything productive during these times but brilliant tackles this in', # false neg
                              'a great way. every day their short daily problems give you the context and framework needed to solve a problem and let you tackle it on your own',
                              'they publish a huge variety of problems so once you’ve figured one out if you find it interesting you can also try their corresponding course. these are great ways to help learn a little more in a little time', # false neg
                              'thursday boots is a bootstrap startup that handcrafts boots using the highest quality materials and then sells them at', # false neg
                              'an honest price what a business model right they offer free shipping and returns and you can check them out at',
                              'thursday boots comm l tt well have that linked below',
                              'ops vast curved gaming monitor is 35 inches of gaming bliss its an ultra wide 34 40 by 1440 display with 2', # false neg
                              'millisecond response times and its got free sync it runs at a maximum 100 hertz refresh rate and its got a 2500 to 1', # false neg
                              'contrast ratio go check it out at the link in the video description for your own seamless visual experience whether', # false neg
                              'youre gaming working watching a movie or just browsing so thanks for watching guys if this video sucked you know what',
                              'to do but if it was awesome get subscribed hit that like button or check out the link to where to buy the stuff',
                              'we featured in the video description also down there is our merch store which has cool shirts like this one and our']
        x_test_not_sponsored = [  'sometimes submarines sink their systems fail and nobody can get to them before oxygen runs out. as submarines become better at masking themselves submarine tracking technology is simultaneously',
                                  'many submarine operating countries have rescue submarines that can hypothetically be used to save stranded submariners by going down latching on and shuttling sailors to the surface but in practice these have never really had much action',
                                  '24 hours after the last reading these will drift to only about 1.15 miles or 1.85 kilometers of accuracy. now this technique combined with the consultation of maps is usually fine since most of the',
                                  'and some separate systems designed for use when the main systems are compromised but vlf radio forms the bulk of communications with most submarines. but the fact that submarines spend their time underwater in stealth also makes another crucial',
                                  'providers like hp and dell you can often run into proprietary parts limited upgrade ability and configurability and',
                                  'questionable software load outs that can affect the overall experience so the popularity of machines that are',
                                  'built from retail parts by smaller system integrators like ibuypower or main gear is understandable boutique',
                                  'builders in particular dont always hit the best performance per dollar but what most of these shops offer is a high',
                                  'degree of customize ability and more transparency into the actual components youre buying now a lot of you watching',
                                  'our channel would look down on the idea of buying a pre-built computer but consider this what if a well-known and',
                                  'respected manufacturer came out offering the type of system that would be similar to what you would end up configuring for',
                                  'think is gonna be the next playable fighter in smash bros let me know in the comments below jk you already did how', # false pos
                                  'many big chungas answers so far jack um all of them all of them why why would you show me this why i was having a good',
                                  'week too crash bandicoot what hes already in the game i sweet its that egg meme that we already forgot about']
        x_test = x_test_sponsored + x_test_not_sponsored

    x_text, y_text = read_data('dataset/data.csv', x_colname='text', y_colname='sentiment')
    #print(len(x_text), len(y_text))

    tokenizer = create_tokenizer(x_text)
    x_pad, feature_length = preprocess_features(x_text, tokenizer=tokenizer)
    #print(feature_length)

    model = load_model('./output/model.h5')

    pred = predict(model, x_test, tokenizer=tokenizer, feature_length=feature_length)
    #print(pred)

    if 'x_test_sponsored' in locals():
        print('sponsored accuracy:', len(list(filter(lambda x: x < 0.5,
            pred[:len(x_test_sponsored)])))/len(x_test_sponsored))
    if 'x_test_not_sponsored' in locals():
        print('not sponsored accuracy:', len(list(filter(lambda x: x >= 0.5,
            pred[len(x_test_sponsored):])))/len(x_test_not_sponsored))

if __name__ == "__main__":
    main(sys.argv[1:])
