import wave
import numpy as np
import pylab as plt

from biquads_effect import *


def main() -> None:
    wave_file = wave.open('mixue_48k.wav', 'rb')
    params = wave_file.getparams()
    channels, bit_depth, sample_rate, num_frames = params[:4]

    str_data = wave_file.readframes(num_frames)
    wave_file.close()

    audio_data = np.frombuffer(str_data, dtype=np.short)
    audio_data = np.asarray(audio_data / 32768.0, dtype=float)

    # butter_worth = LowPassEffect(sample_rate, cutoff_frq=500, q=0.707)
    # butter_worth = HighPassEffect(sample_rate, cutoff_frq=8000, q=0.707)
    # butter_worth = BandPassEffect(sample_rate, cutoff_frq=3000, band_width=1000)
    butter_worth = PeakEQEffect(sample_rate, cutoff_frq=300, band_width=200, gain=-10)
    audio_data = butter_worth.process(audio_data)

    audio_data = np.asarray(audio_data * 32768.0, dtype=np.short)

    out_wave_file = wave.open('output.wav', 'wb')
    out_wave_file.setnchannels(channels)
    out_wave_file.setsampwidth(bit_depth)
    out_wave_file.setframerate(sample_rate)
    out_wave_file.writeframes(audio_data.tobytes())
    out_wave_file.close()


if __name__ == "__main__":
    main()
