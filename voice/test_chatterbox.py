import os
# Ensure HF_HOME is set for the voice directory
os.environ['HF_HOME'] = os.path.join(os.getcwd(), "cache")
os.environ['HF_HUB_CACHE'] = os.path.join(os.getcwd(), "cache")
os.environ['HF_TOKEN'] = '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' 

import torchaudio as ta
import torch
import librosa
import numpy as np

# Patch librosa.load to use torchaudio, bypassing numba compilation issues
original_load = librosa.load
def patched_load(path, sr=None, mono=True, offset=0.0, duration=None, dtype=None, res_type='soxr_hq'):
    try:
        wav, original_sr = ta.load(path)
        if mono and wav.shape[0] > 1:
            wav = torch.mean(wav, dim=0, keepdim=True)
        if sr is not None and sr != original_sr:
            resampler = ta.transforms.Resample(orig_freq=original_sr, new_freq=sr)
            wav = resampler(wav)
        out_wav = wav.squeeze().numpy()
        if dtype is not None:
            out_wav = out_wav.astype(dtype)
        else:
            out_wav = out_wav.astype(np.float32)
        return out_wav, sr if sr else original_sr
    except Exception as e:
        print(f"Fallback to librosa load failed: {e}")
        return original_load(path, sr=sr, mono=mono, offset=offset, duration=duration, dtype=dtype, res_type=res_type)

librosa.load = patched_load

from chatterbox.tts_turbo import ChatterboxTurboTTS

# Load the Turbo model
model = ChatterboxTurboTTS.from_pretrained(device="cpu")

# Generate with Paralinguistic Tags
text = "Oh, that's hilarious! [chuckle] Um anyway, we do have a new model in store. AI integration with ChatGPT and all that jazz. Would you like me to get some prices for you?"
# Generate audio (requires a reference clip for voice cloning)
try:
    import numpy as np
    import soundfile as sf
    dummy_audio = np.random.randn(6 * 18000).astype(np.float32)
    # sf.write('media/dummy_6s.wav', dummy_audio, 18000)
    wav = model.generate(text, audio_prompt_path="media/rayeed.wav")
    print(f"Audio generated successfully. Shape: {wav.shape}")
    ta.save("test-turbo-output.wav", wav, model.sr)    
    print("Audio saved to test-turbo-output.wav")
except Exception as e:
    import traceback
    traceback.print_exc()
    print("Error during generation:", e)
    print("Ensure enough space is available and retry.")