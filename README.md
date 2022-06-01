# Recognising Ukranian words with EEG recordings
___
## Overview
This repo contains dataset of EEG recordings and Jupyter Notebook with code for its filtering and using for training model that is able to recognise Ukrainian words imagined while making EEG recordings.
___
## Dataset

The dataset consists of 20 samples x 5 seconds, each word was imagined once during this period.
Selected words:
  - "перемога" - (victory)emotionally positive word
  - "поразка" - (defeat)emotionally negative word
  - "таємниця" - (mystery)neither positive nor negative, but still emotional word
  - "слово" - (word)absolutely neutral word
___
## Data processing
Firstly, data is manually filtered and applied with band-pass filter from 0.5 Hz to 40 Hz.
Then, we apply 1DCNN-LSTM model in order to recognise Ukranian words from 