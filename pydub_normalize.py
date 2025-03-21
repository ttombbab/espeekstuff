from pydub import AudioSegment
from pydub.effects import normalize

def normalize_audio(input_wav_path, output_wav_path, target_level=-20.0):
    """Normalizes the audio to a target RMS level (in dBFS)."""
    try:
        audio = AudioSegment.from_wav(input_wav_path)
        normalized_audio = normalize(audio, headroom=target_level)
        normalized_audio.export(output_wav_path, format="wav")
        print(f"Audio normalized and saved to {output_wav_path}")
    except Exception as e:
        print(f"Error during normalization: {e}")

# Example usage
input_file = "/home/ttombbab/pydub_espeek/echoed_speech.wav"
output_file = "/home/ttombbab/pydub_espeek/normalized_speech.wav"
normalize_audio(input_file, output_file)
