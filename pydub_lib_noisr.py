import librosa
import noisereduce as nr
import soundfile as sf

def reduce_noise(input_wav_path, output_wav_path):
    """Reduces noise from the audio file."""
    try:
        y, sr = librosa.load(input_wav_path)
        reduced_noise = nr.reduce_noise(y=y, sr=sr)
        sf.write(output_wav_path, reduced_noise, sr)
        print(f"Noise reduced and saved to {output_wav_path}")
    except Exception as e:
        print(f"Error during noise reduction: {e}")

# Example usage
input_file = "/home/ttombbab/pydub_espeek/cadence.wav"
output_file = "/home/ttombbab/pydub_espeek/noise_reduced_speech.wav"
reduce_noise(input_file, output_file)
