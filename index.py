import librosa

y, sr = librosa.load("495179971-Cassin's Finch.mp3")

tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

print('Estimated tempo: {:.2f} beats per minute'.format(tempo))

beat_times = librosa.frames_to_time(beat_frames, sr=sr)

print(beat_times)