import speech_to_text
import text_summarizer
import new_summarizer

#speech_to_text.speech_to_text(inputfile="AUDIO/aboutSpeechSdk.wav", 
#                outputfile="FILE/temp_result.txt")

#text_summarizer.summarize_text(input_file='FILE/temp_input.txt', 
#            output_file='FILE/temp_output.txt', compression_rate=0.3, number_of_clusters=4)

new_summarizer.summarize_text(input_file='FILE/temp_input.txt', 
            output_file='FILE/temp_output.txt', compression_rate=0.3, number_of_clusters=4)