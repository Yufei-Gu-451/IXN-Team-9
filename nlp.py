from app import speech_to_text
from app import text_summarizer

#speech_to_text.speech_to_text(inputfile="app/audio/aboutSpeechSdk.wav", outputfile="app/file/temp_result.txt")

text_summarizer.summarize_text(input_file='app/file/temp_input.txt', 
            output_file='app/file/temp_output.txt', compression_rate=0.25, number_of_clusters=4, algorithm_num=1)