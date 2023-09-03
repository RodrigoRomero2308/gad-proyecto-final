from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import ShortTermFeatures
from pyAudioAnalysis import audioVisualization
from pydub import AudioSegment
import matplotlib.pyplot as plt
import os

folder = 'parecidos'

audioFiles = [f"audios/{folder}/{file}" for file in os.listdir("audios/parecidos") if file.endswith(".mp3")]

wavFiles = []

for audioFile in audioFiles:
    newFilename = audioFile.replace(".mp3", ".wav")
    wavFiles.append(newFilename)
    if (not os.path.exists(newFilename)):
      audio = AudioSegment.from_mp3(audioFile)
      audio.export(newFilename, format="wav")

dataByAudioFile = []

for wav in wavFiles:
  print(f'Extracting features from {wav}')
  [Fs, x] = audioBasicIO.read_audio_file(wav)
  print(Fs)
  print(x.__len__())
  F = None
  f_names = None
  try:
    F, f_names = ShortTermFeatures.feature_extraction(x, Fs, 0.050*Fs, 0.025*Fs)
  except ValueError:
    # Si falla tratamos de pasar la señal a mono (error: ValueError: cannot reshape array of size XXXX into shape (XX,XX))
    x = audioBasicIO.stereo_to_mono(x)
    F, f_names = ShortTermFeatures.feature_extraction(x, Fs, 0.050*Fs, 0.025*Fs)
  print(f'Finished extrcting features from {wav}')
  dataByAudioFile.append([wav, F, f_names])
    
index = 1
fileAmount = dataByAudioFile.__len__()
featureName = ''
for file in dataByAudioFile:
   print(f'Processing {file[0]}')
   featureName = file[2][0]
   plt.subplot(fileAmount, 1, index); plt.plot(file[1][0,:]); plt.xlabel(file[0]); plt.ylabel(file[2][0])
   index += 1

plt.savefig(f'./output/{folder}/{featureName}.png')