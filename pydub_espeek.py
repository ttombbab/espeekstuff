import subprocess
import re
import os
from pydub import AudioSegment
from pydub.effects import normalize
import simpleaudio as sa  # For playing the processed audio

voice_names = ['english','en-scottish','english-north','english_rp' ,'english_wmids' ,
                'english-us' ,'en-westindies','default']

TEMP_WAV_FILE = "temp_speech.wav"

def speak_text(text, amplitude=100, pause_between_words=10, indicate_capital_letters=25, line_length=0,
                pitch_adjustment=50, words_per_minute=175, voice_file='default'):
    if voice_file not in voice_names:
        print('no voice name found')
        return
    # Construct the command to run espeak and save to a temporary file
    command = ['espeak', '-a', str(amplitude), '-g', str(pause_between_words), '-k', str(indicate_capital_letters),
                '-l', str(line_length), '-p', str(pitch_adjustment), '-s', str(words_per_minute), '-v', voice_file, '-w', TEMP_WAV_FILE]

    try:
        # Run the command
        process = subprocess.Popen(command, stdin=subprocess.PIPE)
        process.communicate(input=text.encode())

        if process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, command)

        # print(f"Text segment spoken successfully and saved to {TEMP_WAV_FILE}!")
    except Exception as e:
        print(f"An error occurred during espeak: {e}")

def process_and_play_audio(wav_file_path):
    """Loads a WAV file, normalizes it, and plays it."""
    try:
        audio = AudioSegment.from_wav(wav_file_path)
        normalized_audio = normalize(audio, headroom=-20.0) # Adjust headroom as needed

        # Play the normalized audio
        play_obj = sa.play_buffer(
            normalized_audio.raw_data,
            num_channels=normalized_audio.channels,
            bytes_per_sample=normalized_audio.sample_width,
            sample_rate=normalized_audio.frame_rate
        )
        play_obj.wait_done()

    except Exception as e:
        print(f"Error during pydub processing or playback: {e}")
    finally:
        # Clean up the temporary file
        if os.path.exists(wav_file_path):
            os.remove(wav_file_path)

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

        # Process and play the temporary audio file
        process_and_play_audio(TEMP_WAV_FILE)

        # Add a slightly longer pause after each sentence (optional, might need adjustment)
        import time
        time.sleep(0.1) # Reduced the pause as pydub playback might introduce some delay

# Example usage:
text_to_speak = "Hello, World! This is a test of espeak. How are you today? That's amazing!"
speak_with_cadence(text_to_speak)
