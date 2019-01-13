import requests
import json
import string
import datetime
import math
import sys
import getopt
import re
from argparse import ArgumentParser

import numpy as np
import pandas as pd
from youtube_transcript_api import YouTubeTranscriptApi

from sklearn.feature_extraction.text import CountVectorizer
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential, load_model
from keras.layers import Dense, Embedding, LSTM, SpatialDropout1D
from sklearn.model_selection import train_test_split
from keras.utils.np_utils import to_categorical

def pretty_date(seconds):
    return str(datetime.timedelta(seconds=math.ceil(seconds)))

def preprocess(transcript):
    lines = []
    times = [{
        'start': 0.0
    }]
    buf = ''
    count = 0
    duration = 0
    for i in range(len(transcript)):
        obj = transcript[i]
        buf += obj['text'] + ' '
        if count == 3:
            lines.append(buf)
            times[-1]['duration'] = duration
            duration = 0
            if i + 1 < len(transcript):
                times.append({
                    'start': transcript[i+1]['start']
                })
            else:
                times.append({
                    'start': transcript[i]['start']
                })
            buf = ''
            count = 0
        count += 1
        duration += obj['duration']
    return lines, times

def print_results(sentiments, lines, times, verbose=False):
    if verbose:
        for i in range(len(sentiments)):
            sentiment = sentiments[i]
            if np.argmax(sentiment) == 0:
                print("sponsor %s -> %s\n------------------------------------\n" % (pretty_date(times[i]['start']),
                    pretty_date(times[i]['start'] + times[i]['duration'])), lines[i], '\n')
            elif np.argmax(sentiment) == 1:
                print("normal %s -> %s\n------------------------------------\n" % (pretty_date(times[i]['start']),
                    pretty_date(times[i]['start'] + times[i]['duration'])), lines[i], '\n')
    else:
        sponsor_times = []
        for i in range(len(sentiments)):
            sentiment = sentiments[i]
            if np.argmax(sentiment) == 0:
                sponsor_times.append({
                    'start': pretty_date(times[i]['start']),
                    'end': pretty_date(times[i]['start'] + times[i]['duration'])
                })
        print(math.ceil((len(sponsor_times) / len(sentiments)) * 100))
        print(sponsor_times)

def predict(id, tokenizer, model, verbose=False):
    if verbose:
        print('predicting %s... (verbose output)' % id)
    else:
        print('predicting %s...' % id)
    transcript = YouTubeTranscriptApi.get_transcript(id)
    lines, times = preprocess(transcript)

    twt = []
    for line in lines:
        twt.append(line)
    twt = tokenizer.texts_to_sequences(twt)
    twt = pad_sequences(twt, maxlen=3821, dtype='int32', value=0)
    sentiments = model.predict(twt, batch_size=1, verbose=2)
    print_results(sentiments, lines, times, verbose)
    return sentiments

def predict_channel(channel_id, tokenizer, model, verbose=False):
    if verbose:
        print('predicting from channel %s... (verbose output)' % channel_id)
    else:
        print('predicting from channel %s...' % channel_id)

    search_response = requests.request("GET", "https://www.googleapis.com/youtube/v3/search", params = {
        "part": "snippet",
        "channelId": channel_id,
        "key": "",
        "maxResults": "10",
        "order": "date"
        })

    search_items = json.loads(search_response.text)['items']
    videos = []
    simple_plots = []
    for item in search_items:
        search_id = item['id']
        try:
            sentiments = predict(search_id['videoId'], tokenizer, model, verbose)
            simple_plot = []
            for i in range(len(sentiments)):
                sentiment = sentiments[i]
                if np.argmax(sentiment) == 0:
                    simple_plot.append(0)
                elif np.argmax(sentiment) == 1:
                    simple_plot.append(1)
            print(simple_plot)
            simple_plots.append(simple_plot)
        except Exception:
            pass
    print(simple_plots)
    np.save('output/%s.npy' % channel_id, np.array(simple_plots))

def main(argv):
    parser = ArgumentParser()
    parser.add_argument("-i", "--id", dest="id", help="video id")
    parser.add_argument("-c", "--channel", dest="channel", help="channel id")
    parser.add_argument("-v", "--verbose", action='store_true', dest="verbose", default=False)

    args = parser.parse_args()

    # preparation
    data = pd.read_csv('data.csv')
    data = data[['text','sentiment']]

    data['text'] = data['text'].apply(lambda x: x.lower())
    data['text'] = data['text'].apply((lambda x: re.sub('[^a-zA-z0-9\s]','',x)))

    max_fatures = 2000
    tokenizer = Tokenizer(num_words=max_fatures, split=' ')
    tokenizer.fit_on_texts(data['text'].values)

    model = load_model('model.h5')

    # prediction
    if args.channel is not None:
        predict_channel(args.channel, tokenizer, model, args.verbose)
    else:
        predict(args.id, tokenizer, model, args.verbose)

if __name__ == "__main__":
   main(sys.argv[1:])
