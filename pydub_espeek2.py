import subprocess
import re
import os
import librosa
import noisereduce as nr
import soundfile as sf
from playsound import playsound  # Install with: pip install playsound

voice_names = ['english','en-scottish','english-north','english_rp' ,'english_wmids' ,
                'english-us' ,'en-westindies','default']

TEMP_ESPEAK_WAV = "temp_espeak.wav"
TEMP_PROCESSED_WAV = "temp_processed.wav"

def speak_text(text, amplitude=100, pause_between_words=10, indicate_capital_letters=25, line_length=0,
                pitch_adjustment=50, words_per_minute=175, voice_file='default'):
    if voice_file not in voice_names:
        print('no voice name found')
        return
    # Construct the command to run espeak and save to a temporary file
    command = ['espeak', '-a', str(amplitude), '-g', str(pause_between_words), '-k', str(indicate_capital_letters),
                '-l', str(line_length), '-p', str(pitch_adjustment), '-s', str(words_per_minute), '-v', voice_file, '-w', TEMP_ESPEAK_WAV]

    try:
        # Run the command
        process = subprocess.Popen(command, stdin=subprocess.PIPE)
        process.communicate(input=text.encode())

        if process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, command)

        # print(f"Text segment spoken successfully and saved to {TEMP_ESPEAK_WAV}!")
    except Exception as e:
        print(f"An error occurred during espeak: {e}")

def process_and_play_with_noise_reduction(input_wav_path, output_wav_path):
    """Loads a WAV file, reduces noise, saves it, and plays it."""
    try:
        y, sr = librosa.load(input_wav_path)
        reduced_noise = nr.reduce_noise(y=y, sr=sr)
        sf.write(output_wav_path, reduced_noise, sr)
        playsound(output_wav_path)
    except Exception as e:
        print(f"Error during noise reduction or playback: {e}")
    finally:
        # Clean up the temporary files
        if os.path.exists(input_wav_path):
            os.remove(input_wav_path)
        if os.path.exists(output_wav_path):
            os.remove(output_wav_path)

def speak_with_cadence(full_text, base_amplitude=80, base_pause=8, base_pitch=50, base_speed=160, voice='english_rp'):
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!)\s', full_text)
    for i, sentence in enumerate(sentences):
        amplitude = base_amplitude
        pause = base_pause
        pitch = base_pitch
        speed = base_speed

        if sentence.endswith('?'):
            pitch = min(99, base_pitch + 20)  # Increase pitch for questions
        elif sentence.endswith('!'):
            amplitude = min(200, base_amplitude + 20) # Increase amplitude for emphasis

        # Slightly vary parameters for consecutive sentences
        if i % 2 == 0:
            speed = base_speed + 10
            pause = base_pause + 2
        else:
            speed = base_speed - 10
            pause = base_pause - 2

        speak_text(sentence.strip(), amplitude=amplitude, pause_between_words=pause,
                   indicate_capital_letters=15, pitch_adjustment=pitch, words_per_minute=speed, voice_file=voice)

        # Process and play the temporary audio file with noise reduction
        process_and_play_with_noise_reduction(TEMP_ESPEAK_WAV, TEMP_PROCESSED_WAV)

        # Add a slightly longer pause after each sentence (optional, might need adjustment)
        #import time
        #time.sleep(0.1) # Reduced the pause as playback might introduce some delay

# Example usage:
text_to_speak = "Hello, World! This is a test of espeak. How are you today? That's amazing!"
speak_with_cadence(text_to_speak,voice='en-westindies')
