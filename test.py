from app import text_summarizer

text_summarizer.summarize_text(input_file='app/file/input.txt', output_file="app/file/output.txt", \
  compression_rate=0.3, number_of_clusters=2, algorithm_num=2, distance_num=1)