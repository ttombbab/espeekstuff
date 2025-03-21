import subprocess
import re
import os
import librosa
import noisereduce as nr
import soundfile as sf
from pydub import AudioSegment  # Import AudioSegment

voice_names = ['english','en-scottish','english-north','english_rp' ,'english_wmids' ,
                'english-us' ,'en-westindies','default']

TEMP_ESPEAK_WAV = "temp_espeak.wav"
TEMP_PROCESSED_WAV = "temp_processed.wav"
FINAL_OUTPUT_WAV = "final_output.wav"  # Name of the final recorded file

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

def process_audio_with_noise_reduction(input_wav_path, output_wav_path):
    """Loads a WAV file and reduces noise, saving the result."""
    try:
        y, sr = librosa.load(input_wav_path)
        reduced_noise = nr.reduce_noise(y=y, sr=sr)
        sf.write(output_wav_path, reduced_noise, sr)
        return output_wav_path
    except Exception as e:
        print(f"Error during noise reduction: {e}")
        return None

def speak_with_cadence(full_text, base_amplitude=80, base_pause=8, base_pitch=50, base_speed=160, voice='english_rp'):
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!)\s', full_text)
    combined_audio = AudioSegment.empty()  # Initialize an empty AudioSegment

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

        # Process audio with noise reduction
        processed_file = process_audio_with_noise_reduction(TEMP_ESPEAK_WAV, TEMP_PROCESSED_WAV)

        if processed_file:
            try:
                sentence_audio = AudioSegment.from_wav(processed_file)
                combined_audio += sentence_audio
            except Exception as e:
                print(f"Error loading processed audio segment: {e}")

        # Clean up temporary files
        if os.path.exists(TEMP_ESPEAK_WAV):
            os.remove(TEMP_ESPEAK_WAV)
        if os.path.exists(TEMP_PROCESSED_WAV):
            os.remove(TEMP_PROCESSED_WAV)

        # Add a slightly longer pause after each sentence in the combined audio
        if i < len(sentences) - 1:
            combined_audio += AudioSegment.silent(duration=200) # Add a 200ms silence

        import time
        time.sleep(0.05) # Small delay to avoid potential issues

    # Save the combined audio to a single WAV file
    combined_audio.export(FINAL_OUTPUT_WAV, format="wav")
    print(f"Entire output recorded to {FINAL_OUTPUT_WAV}")

# Example usage:
# text_to_speak = """The Flynn Tower, an isolated research facility perched on the edge of reality, hums with latent energy. You, Dr. Aris Thorne, are monitoring anomalous readings when a shimmering drone materializes. It pulses with an otherworldly light, a cryptic message flashing across its surface: "Convergence Imminent."
            
# What do you do?"""
text_to_speak = """As you approach, the drone projects a holographic interface, revealing a network of interconnected portals and glimpses of an underwater city, the bioluminescent metropolis of Aquatica. The message also whispers: "The Veil thins. The Watchers awaken."
            
What will you focus on?"""
speak_with_cadence(text_to_speak,voice='english_rp',base_speed=150)
#speak_with_cadence(text_to_speak,voice='en-westindies',base_speed=170, base_pitch=150)
