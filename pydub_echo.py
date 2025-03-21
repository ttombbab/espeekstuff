from pydub import AudioSegment

def add_simple_echo(input_wav_path, output_wav_path, delay=10, decay=1):
    """Adds a simple echo effect."""
    try:
        audio = AudioSegment.from_wav(input_wav_path)
        echo = audio.overlay(audio.fade_in(50).fade_out(100) * decay, position=delay)
        echo.export(output_wav_path, format="wav")
        print(f"Simple echo added and saved to {output_wav_path}")
    except Exception as e:
        print(f"Error adding echo: {e}")

# Example usage
input_file = "/home/ttombbab/pydub_espeek/final_output.wav"
output_file = "/home/ttombbab/pydub_espeek/echoed_speech.wav"
add_simple_echo(input_file, output_file)
