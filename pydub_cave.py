from pydub import AudioSegment

import numpy as np

def add_cave_ambience(speech_wav, output_wav):
    speech = AudioSegment.from_wav(speech_wav)

    # Add echo to simulate cave
    #cave_echo = echo(speech, delays=[200, 400, 600], decays=50)
    
    #audio = AudioSegment.from_wav(input_wav_path)
    cave_echo = speech.overlay(speech.fade_in(50).fade_out(100) * 10, position=1)
    # Load cave background sound (replace with your file)
    try:
        cave_sound = AudioSegment.from_mp3("/home/ttombbab/pydub_espeek/Spirits_in_a_cave.mp3")
        # Ensure the background sound is at least as long as the speech
        if len(cave_sound) < len(cave_echo):
            repetitions = int(np.ceil(len(cave_echo) / len(cave_sound)))
            cave_sound = cave_sound * repetitions
        cave_sound = cave_sound[:len(cave_echo)] # Trim to the length of the speech

        # Overlay the speech with the background sound at a lower volume
        combined = cave_echo.overlay(cave_sound - 20) # Reduce background volume by 20 dB

        combined.export(output_wav, format="wav")
        print(f"Cave ambience added to {output_wav}")

    except FileNotFoundError:
        print("Error: cave_background.wav not found. Only echo added.")
        cave_echo.export(output_wav, format="wav")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
speech_file = "/home/ttombbab/pydub_espeek/final_output.wav" # Your recorded speech file
output_file = "/home/ttombbab/pydub_espeek/cave_speech.wav"
add_cave_ambience(speech_file, output_file)
