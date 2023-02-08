import typing
import struct
import wave
import numpy as np
from scipy.fft import *
from scipy.io import wavfile

class AudioWaveformEncoder:
    def __init__(
        self,
        *,
        message: str = None,
        fileName: str = None,
        pauseGeneration: bool = False
    ) -> None:
        if not fileName and not pauseGeneration: raise ValueError("fileName must be provided if waitGeneration is False")

        self.rate: typing.Final = 44100
        self.message = message
        self.hasMessage = bool(self.message)
        self.scrambleMethod = self._directBinaryScramble

        if message and not pauseGeneration: self.fullGenerate(fileName, message)

    def fullGenerate(self, fileName: str, message: str = None) -> None:
        self.runScrambleMethod(message if message else self.message)
        waveform = self.generateAudioWaveform(self.binaryData)
        self.sendWaveformToFile(fileName, waveform)

    def runScrambleMethod(self, message: str) -> bytes:
        self.binaryData = self.scrambleMethod(message)
        return self.binaryData

    def generateAudioWaveform(self, binaryData: bytes) -> bytes:
        audioMap: typing.Final = {
            '0': b''.join(self._generateSineWave(36, 0.25)),
            '1': b''.join(self._generateSineWave(196, 0.25)),
            ' ': b''.join(self._generateSineWave(0, 0.5))
        }
        return b''.join([audioMap[i] for i in list(binaryData.decode('ascii'))])

    def sendWaveformToFile(self, fileName: str, waveform: bytes) -> None:
        output = wave.open(fileName,'w')
        output.setparams((2, 2, self.rate, 0, 'NONE', 'not compressed'))
        output.writeframes(waveform)
        output.close()

    def _generateSineWave(self, freq: int, dur: float) -> typing.List[bytes]:
        x_values = (2*np.pi*freq/self.rate) * np.arange(self.rate*dur)
        wave = (32767 * np.sin(x_values)).astype(int) # 32767 is short integer max value
    
        return map(lambda v: struct.pack('h', v), wave)

    def _directBinaryScramble(self, message: str) -> bytes:
        return ' '.join(format(ord(i), 'b').zfill(8) for i in message).encode("ascii")

class AudioWaveformDecoder:
    def __init__(self, fileName: str) -> None:
        self.fileName = fileName

    def decode(self, *, verbose = False) -> str:
        sr, data = wavfile.read(self.fileName)
        if data.ndim > 1: data = data[:, 0]

        bitrate = 250 / 2
        length = len(data)/(sr/8)
        collectedData = []
        bitCollection = [] # 8 bits make a byte
        continueOnSpace = False
        for i in range(0, int(length)):
            if continueOnSpace:
                continueOnSpace = False
                continue

            freq = self.getFrequencySegment(data, sr, i*bitrate, (i*bitrate) + bitrate)
            if freq == 0:
                if len(bitCollection) > 0:
                    collectedData.append(''.join(bitCollection).encode('ascii'))
                    if verbose: print(bitCollection)
                    bitCollection = []
                    continueOnSpace = True
            elif freq < 100:
                bitCollection.append('0')
            elif freq > 100:
                bitCollection.append('1')
        collectedData.append(''.join(bitCollection).encode('ascii')) # file does not end with space, so append the last bit collection
        asciiDecimal = [int(i, 2) for i in collectedData]
        decodedMessage = ''.join([chr(i) for i in asciiDecimal])

        if verbose:
            print("\nSample Rate: " + str(sr))
            print("Data Length: " + str(length))
            print("Bitrate: " + str(bitrate))
            print("\nCollected Data: " + str(collectedData))
            print("\nASCII Decimal: " + str(asciiDecimal), end="\n")

        return decodedMessage

    def getFrequencySegment(self, data, sr: int, start_time: int, end_time: int) -> int:
        dataToRead = data[int(start_time * sr / 1000) : int(end_time * sr / 1000) + 1]
        if len(dataToRead) == 0: return 0

        N = len(dataToRead)
        yf = rfft(dataToRead)
        xf = rfftfreq(N, 1 / sr)

        idx = np.argmax(np.abs(yf))
        freq = xf[idx]
        return freq

if __name__ == '__main__':
    print("Run the encode.py or decode.py file instead.")