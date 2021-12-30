import os
import speech_to_text
import file

test_file = "test/testfile.txt"
test_audio = "audiofiles/aboutSpeechSdk.wav"

false_audio = "test/testfile.txt"
false_audio2 = "audiofiles/x.wav"
false_audio3 = "audiofile/aboutSpeechSdk.wav"

false_file = "test/testfile.tx"
false_file2 = "test/testfile2.txt"
false_file2 = "tes/testfile2.txt"

class TestSpeechToText(object):
    # Set up method executed before all test methods in the class
    def setup_class(self):
        print("\n\nTestSpeechToText Class : Test begins\n")
        # Create a temporal test file
        open(test_file, 'w')

    # Tear down method executed after all test methods in the class
    def teardown_class(self):
        print("\nTestSpeechToText Class : Test ends\n\n")
        # Delete the temporal test file
        os.remove(test_file)

    # Test normal transcribe result
    def test_transcribe(self):
        speech_to_text.speech_to_text(inputfile=test_audio, outputfile=test_file)

        file_content = file.read_file(test_file)

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
    def test_false_audio(self):
        try:
            speech_to_text.speech_to_text(inputfile=false_audio, outputfile=test_file)
        except Exception as e:
            assert str(e) == 'speech_to_text: audio file error : %s test/testfile.txt'