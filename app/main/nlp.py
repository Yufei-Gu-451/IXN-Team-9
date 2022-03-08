import speech_to_text
import text_summarizer

speech_to_text.speech_to_text(inputfile="audio/aboutSpeechSdk.wav", 
                outputfile="file/temp_result.txt")

text_summarizer.summarize_text(input_file='file/temp_input.txt', 
            output_file='file/temp_output.txt', compression_rate=0.3, number_of_clusters=4)