from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import ShortTermFeatures
from pydub import AudioSegment
import matplotlib.pyplot as plt

mp3_file = "audios/parecidos/XC11503.mp3"
audio = AudioSegment.from_mp3(mp3_file)
wav_file = "audios/parecidos/XC11503.wav"
audio.export(wav_file, format="wav")

[Fs, x] = audioBasicIO.read_audio_file(wav_file)
F, f_names = ShortTermFeatures.feature_extraction(x, Fs, 0.050*Fs, 0.025*Fs)
plt.subplot(2,1,1); plt.plot(F[0,:]); plt.xlabel('Frame no'); plt.ylabel(f_names[0]) 
plt.subplot(2,1,2); plt.plot(F[1,:]); plt.xlabel('Frame no'); plt.ylabel(f_names[1])
plt.savefig(f'./output/parecidos/XC11503.png', bbox_inches='tight', pad_inches=0.0)