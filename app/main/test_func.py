import os
import speech_to_text
import file

test_file = "FILE/testfile.txt"
wrong_file = "FILE/testfile.tx"
test_audio = "AUDIO/aboutSpeechSdk.wav"

class TestSpeechToText(object):
    # Set up method executed before all test methods in the class
    def setup_class(self):
        print("\n\nTestSpeechToText Class : Test begins\n")
        # Create a temporal test file
        open(test_file, 'w')
        open(wrong_file, 'w')

    # Tear down method executed after all test methods in the class
    def teardown_class(self):
        print("\nTestSpeechToText Class : Test ends\n\n")
        # Delete the temporal test file
        os.remove(test_file)
        os.remove(wrong_file)

    # Test normal transcribe result
    def test_transcribe(self):
        speech_to_text.speech_to_text(inputfile=test_audio, outputfile=test_file)

        file_content = file.read_txt_file(test_file)

        answer = ["The Speech SDK exposes many features from the speech service, but not all of them.\n",
                    "The capabilities of the speech SDK are often associated with scenarios.\n",
                    "The Speech SDK is ideal for both real time and non real time scenarios using local devices files, " +
                    "Azure blob storage and even input and output streams.\n",
                    "When a scenario is not achievable with the speech SDK, look for a rest API alternative " +
                    "speech to text, also known as speech recognition, transcribes audio streams to text that " +
                    "your applications, tools, or devices can consume or display.\n",
                    "Use speech to text with language understanding Lewis to derive user intents " + \
                    "from transcribed speech and act on voice commands. Use speech translation to translate speech input "
                    "to a different language with a single call. For more information, see speech to text basics.\n"]

        assert len(file_content) == len(answer)

        for i in range(len(file_content)):
            assert answer[i] == file_content[i]

    # Test wrong audio with wrong file type
    def test_audio_filetype(self):
        try:
            speech_to_text.speech_to_text(inputfile='FILE/testfile.txt', outputfile=test_file)
        except Exception as e:
            assert str(e) == 'speech_to_text: audio file type error: FILE/testfile.txt should be of type wav'

    def test_not_exist_audio(self):
        try:
            speech_to_text.speech_to_text(inputfile="AUDIO/x.wav", outputfile=test_file)
        except Exception as e:
            assert str(e) == 'speech_to_text: audio file not exists: AUDIO/x.wav'

    def test_not_exist_dir(self):
        try:
            speech_to_text.speech_to_text(inputfile="AUDIO/aboutSpeechSdk.wav", outputfile=test_file)
        except Exception as e:
            assert str(e) == 'speech_to_text: audio file not exists: AUDIO/aboutSpeechSdk.wav'

    def test_file_filetype(self):
        try:
            speech_to_text.speech_to_text(inputfile=test_audio, outputfile=wrong_file)
        except Exception as e:
            assert str(e) == 'speech_to_text: output file type error: FILE/testfile.tx should be of type txt'

    def test_not_exist_file(self):
        try:
            speech_to_text.speech_to_text(inputfile=test_audio, outputfile="FILE/testfile2.txt")
        except Exception as e:
            assert str(e) == 'speech_to_text: output file not exists: FILE/testfile2.txt'


class TestFile(object):
    # Set up method executed before all test methods in the class
    def setup_class(self):
        print("\n\nTestFile Class : Test begins\n")
        # Create a temporal test file
        open(test_file, 'w')
        open(wrong_file, 'w')

    # Tear down method executed after all test methods in the class
    def teardown_class(self):
        print("\nTestFile Class : Test ends\n\n")
        # Delete the temporal test file
        os.remove(test_file)
        os.remove(wrong_file)

    def test_write_to_file_single_line(self):
        file.write_txt_file(output_file_name=test_file, text='test string', append=False)
        
        file_content = file.read_txt_file(filename=test_file)
        file_string = ''
        for line in file_content:
            file_string += line

        assert file_string == 'test string'

    def test_write_to_file_multiple_lines(self):
        file.write_txt_file(output_file_name=test_file, text='test line1\ntest line2\n', append=False)
        
        file_content = file.read_txt_file(filename=test_file)
        file_string = ''
        for line in file_content:
            file_string += line

        assert file_string == 'test line1\ntest line2\n'

    def test_write_to_wrong_file(self):
        try:
            file.write_txt_file(output_file_name=wrong_file, text='test line1\ntest line2\n', append=False)
        except Exception as e:
            assert e == ''