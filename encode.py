from waveformEncoder import AudioWaveformEncoder

encoder = AudioWaveformEncoder(pauseGeneration=True)

message = input("Enter a message to encode: ")

data = encoder.runScrambleMethod(message)

print(f"Encoded Binary Data: {data}")

wav = encoder.generateAudioWaveform(data)
encoder.sendWaveformToFile("output.wav", wav)