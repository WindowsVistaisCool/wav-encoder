from waveformEncoder import AudioWaveformDecoder

try:
    decodedMessage = AudioWaveformDecoder("output.wav").decode(verbose=True)
    print("Decoded Message: \n\n" + str(decodedMessage))
except FileNotFoundError:
    print("No audio file found. Please run encode.py first.")