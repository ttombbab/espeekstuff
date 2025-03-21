import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt

def analyze_frequency_spectrum(input_wav_path):
    """Analyzes and plots the frequency spectrum of the audio."""
    try:
        y, sr = librosa.load(input_wav_path)
        fft = np.fft.fft(y)
        magnitude_spectrum = np.abs(fft)
        frequency = np.linspace(0, sr, len(magnitude_spectrum))

        plt.figure(figsize=(12, 4))
        plt.plot(frequency[:len(frequency)//2], magnitude_spectrum[:len(magnitude_spectrum)//2]) # Plot up to Nyquist frequency
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Magnitude")
        plt.title("Frequency Spectrum")
        plt.grid(True)
        plt.show()
    except Exception as e:
        print(f"Error analyzing spectrum: {e}")

# Example usage
input_file = "/home/ttombbab/pydub_espeek/cadence.wav"
analyze_frequency_spectrum(input_file)
