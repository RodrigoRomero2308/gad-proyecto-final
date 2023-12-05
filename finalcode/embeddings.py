import librosa


def embed_audio(audio_filepath):
  y, sr = librosa.load(audio_filepath)

  mfccs = librosa.feature.mfcc(y=y, sr=sr)

  return mfccs