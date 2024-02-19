import time
import librosa
import numpy as np
from panns_inference import AudioTagging

at = AudioTagging(checkpoint_path=None, device='cpu')

def embed_audio(audio_filepath):
  y, _ = librosa.load(path=audio_filepath, sr=32000, mono=True)

  audio = y[None, :]

  start_time = time.time()

  try:
    _, embeddings = at.inference(audio)
    embeddings = embeddings/np.linalg.norm(embeddings)
    embeddings = embeddings.tolist()[0]
    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"Time taken by my_function: {elapsed_time:.6f} seconds")

    return embeddings
  except Exception as e:
    print(f"Failed to embed: {str(e)}")
    return
  