from waveformEncoder import AudioWaveformEncoder

encoder = AudioWaveformEncoder(pauseGeneration=True)

while True:
    message = input("Enter a message to encode: ")
    if message != "": break
    print("The message cannot be empty!")

data = encoder.runScrambleMethod(message)

print(f"Encoded Binary Data: {data}")

wav = encoder.generateAudioWaveform(data)
encoder.sendWaveformToFile("output.wav", wav)