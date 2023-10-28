Welcome to Hindi Dataset's documentation!
=========================================

Overview:
---------

   This project aims to create a system that can retrieve YouTube videos based on a user query and convert them into audio files that are suitable for speech recognition. The system consists of the following steps:

   - The system takes a user query as input and uses the request module in urllib library to get the video IDs of the relevant videos for the query.
   - The system downloads the videos with Hindi audio and Hindi transcript and converts them into audio files using a video-to-audio conversion library(pytube).
   - The system filters out the video IDs that do not have Hindi audio and Hindi transcript by using the YouTube Transcript API and a language detection library(whisper).
   - The system preprocesses the audio files for speech recognition by applying segmentation based on transcript using pydub library, vocals extraction using spleeter library and resampling(set frame rate, sample width, number of channels).

   The output of the system is a set of preprocessed audio files that can be used as input for a speech recognition model. The system can be useful for applications such as speech-to-text transcription, voice search, voice assistant, and voice analysis.

.. toctree::
   :maxdepth: 2

   user/install
   user/Quickstart
   user/yt_audio_collector

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
