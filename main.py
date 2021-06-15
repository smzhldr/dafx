import wave

import numpy as np
import pylab as plt


def main() -> None:
    wave_file = wave.open('mono_s16_48k.wav', 'rb')
    params = wave_file.getparams()
    channels, sample_width, sample_rate, num_frames = params[:4]

    str_data = wave_file.readframes(num_frames)
    wave_file.close()

    wave_data = np.frombuffer(str_data, dtype=np.short) / 32768

    fft_size = 1024
    start = 0
    freq = np.linspace(0, int(sample_rate), int(fft_size))
    c = np.fft.fft(wave_data[start:start + (fft_size - 1)])



    plt.subplot(212)
    plt.plot(freq[start:round(fft_size - 1)], abs(c[:round(len(c))]), 'r')
    plt.title('Freq')
    plt.xlabel("Freq/Hz")
    plt.show()

    # time = np.arange(0, num_frames) / sample_rate
    # plt.figure()
    # plt.subplot(211)
    # plt.plot(time, wave_data)
    # plt.xlabel("time/s")
    # plt.title('Wave')


if __name__ == "__main__":
    main()
