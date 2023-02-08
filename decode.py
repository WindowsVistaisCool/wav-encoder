from waveformEncoder import AudioWaveformDecoder

decodedMessage = AudioWaveformDecoder("output.wav").decode(verbose=True)
print("Decoded Message: \n\n" + str(decodedMessage))