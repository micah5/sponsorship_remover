# Sponsorship Remover Prototype

This is the codebase for sponsorship remover/blocker.

## Usage

### Training

```bash
python src/python/train.py
```

### Prediction

#### Python
```bash
python src/python/predict.py
```

#### Javascript
```bash
node src/javascript/predict.js
```

To try the extension, go to `chrome://extensions/` and load the unpacked directory `./src/javascript/extension/chrome`.
You can see how it works [here](https://youtu.be/stkBeRPUHqQ).

## Directory Guide
```
root/
├── dataset/
│   └── data.csv : CSV file of sponsored (0) and non-sponsored (1) sequences
├── output/
│   ├── model.h5 : Keras model
│   ├── js/
│   │   └── ...  : Tensorflow.js model
│   └── misc
│       └── word_index.json : Dictionary mapping unique words to token
└── src/
    ├── python/
    │   ├── predict.py : Runs a prediction on a trained model stored in output/
    │   ├── train.py : Trains a model and saves in output/
    │   ├── sponsorship_remover/
    │   │   └── ... : Internal functions used by predict.py & train.py
    │   └── transcript_server
    │       └── ... : Simple flask web server that wraps YouTubeTranscriptApi
    └── javascript/
        ├── predict.py : Javascript implementation of predict.py using tf.js
        └── extension/
            └── chrome/
                ├── manifest.json : Metadata for chrome extension
                ├── popup.html : HTML template (with Vue.js) for extension popout
                ├── js
                │   └── content.js : Deployed within browser, contains code to handle predictions
                │   └── popup.js : Logic for popup.html
                │   └── libs
                │       └── ... : Deployed dependencies
                └── style
                    └── ... : Misc style files including CSS for popup.html
```
