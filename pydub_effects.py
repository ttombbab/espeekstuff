from pydub import AudioSegment

import numpy as np

def add_forest_ambience(speech_wav, output_wav):
    speech = AudioSegment.from_wav(speech_wav)

    # Add a subtle echo to suggest open space (optional)
    forest_echo = speech.overlay(speech.fade_in(50).fade_out(100) * 5, position=5)

    # Load forest background sound (replace with your file)
    try:
        forest_sound = AudioSegment.from_mp3("/home/ttombbab/pydub_espeek/garden_of_eden.mp3")
        # Ensure the background sound is at least as long as the speech
        if len(forest_sound) < len(forest_echo):
            repetitions = int(np.ceil(len(forest_echo) / len(forest_sound)))
            forest_sound = forest_sound * repetitions
        forest_sound = forest_sound[:len(forest_echo)]

        # Overlay the speech with the background sound at a lower volume
        combined = forest_echo.overlay(forest_sound - 15) # Reduce background volume by 15 dB

        combined.export(output_wav, format="wav")
        print(f"Forest ambience added to {output_wav}")

    except FileNotFoundError:
        print("Error: forest_background.wav not found. Only subtle echo added.")
        forest_echo.export(output_wav, format="wav")
    except Exception as e:
        print(f"An error occurred: {e}")

def add_building_ambience(speech_wav, output_wav):
    speech = AudioSegment.from_wav(speech_wav)

    # Add a shorter echo for a building interior
    building_echo = speech.overlay(speech.fade_in(50).fade_out(100) * 20, position=1)

    # Load building background sound (replace with your file - e.g., wind or distant traffic)
    try:
        building_sound = AudioSegment.from_mp3("/home/ttombbab/pydub_espeek/Footsteps_in_a_large.mp3")
        # Ensure the background sound is at least as long as the speech
        if len(building_sound) < len(building_echo):
            repetitions = int(np.ceil(len(building_echo) / len(building_sound)))
            building_sound = building_sound * repetitions
        building_sound = building_sound[:len(building_echo)]

        # Overlay the speech with the background sound at a lower volume
        combined = building_echo.overlay(building_sound - 20) # Reduce background volume by 20 dB

        combined.export(output_wav, format="wav")
        print(f"Building ambience added to {output_wav}")

    except FileNotFoundError:
        print("Error: building_background.wav not found. Only shorter echo added.")
        building_echo.export(output_wav, format="wav")
    except Exception as e:
        print(f"An error occurred: {e}")

def add_underwater_ambience(speech_wav, output_wav):
    speech = AudioSegment.from_wav(speech_wav)

    # Load underwater background sound (replace with your file)
    try:
        underwater_sound = AudioSegment.from_mp3("/home/ttombbab/pydub_espeek/Being_underwater.mp3")
        # Ensure the background sound is at least as long as the speech
        if len(underwater_sound) < len(speech):
            repetitions = int(np.ceil(len(speech) / len(underwater_sound)))
            underwater_sound = underwater_sound * repetitions
        underwater_sound = underwater_sound[:len(speech)]

        # Overlay the speech with the background sound at a moderate volume
        combined = speech.overlay(underwater_sound - 10) # Reduce background volume by 10 dB

        # **Simulating Muffling (Limited in pydub):**
        # pydub doesn't have built-in advanced filtering like low-pass.
        # A very basic way to simulate muffling is to reduce high frequencies slightly
        # by making the audio a bit quieter overall.
        muffled_speech = combined - 3 # Reduce overall volume slightly

        muffled_speech.export(output_wav, format="wav")
        print(f"Underwater ambience added to {output_wav}")

    except FileNotFoundError:
        print("Error: underwater_background.wav not found. No ambience added.")
        speech.export(output_wav, format="wav")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
speech_file = "/home/ttombbab/pydub_espeek/final_output.wav" # Your recorded speech file

# Forest
forest_output = "/home/ttombbab/pydub_espeek/forest_speech.wav"
add_forest_ambience(speech_file, forest_output)

# Building
building_output = "/home/ttombbab/pydub_espeek/building_speech.wav"
add_building_ambience(speech_file, building_output)

# Underwater
underwater_output = "/home/ttombbab/pydub_espeek/underwater_speech.wav"
add_underwater_ambience(speech_file, underwater_output)
