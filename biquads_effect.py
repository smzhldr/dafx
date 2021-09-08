import numpy as np

from audio_effect import AudioEffect


class BiquadEffect(AudioEffect):

    def __init__(self, sample_rate, cutoff_frq):
        self.b0 = 0
        self.b1 = 0
        self.b2 = 0
        self.a1 = 0
        self.a2 = 0
        self.a0 = 1

        self.x1 = 0.0
        self.x2 = 0.0
        self.y1 = 0.0
        self.y2 = 0.0

        self.w0 = 2 * np.pi * cutoff_frq / sample_rate
        # self.alpha = np.sin(self.w0) / (2 * band_width)
        # self.alpha = np.sin(self.w0) / (2 * cutoff_frq / band_width)

    def normalized(self):
        self.b0 /= self.a0
        self.b1 /= self.a0
        self.b2 /= self.a0
        self.a1 /= self.a0
        self.a2 /= self.a0

        # while self.a2 + 1 <= abs(self.a1):  # |a2| < 1, |a1| < 1 + a2
        #     self.a1 += 0.1

    def process(self, audio_data):
        rows = audio_data.shape
        input_data = audio_data.copy()
        for i in range(rows[0]):
            x0: float = input_data[i]
            y0 = self.b0 * x0 + self.b1 * self.x1 + self.b2 * self.x2 - self.a1 * self.y1 - self.a2 * self.y2
            self.y2 = self.y1
            self.y1 = y0
            self.x2 = self.x1
            self.x1 = x0
            input_data[i] = y0
        return input_data


# https://zhuanlan.zhihu.com/p/357619650
class LowPassEffect(BiquadEffect):

    def __init__(self, sample_rate, cutoff_frq, q):
        super().__init__(sample_rate, cutoff_frq)
        self.alpha = np.sin(self.w0) / (2 * q)
        self.b0 = (1 - np.cos(self.w0)) / 2
        self.b1 = 1 - np.cos(self.w0)
        self.b2 = (1 - np.cos(self.w0)) / 2
        self.a0 = 1 + self.alpha
        self.a1 = -2 * np.cos(self.w0)
        self.a2 = 1 - self.alpha
        self.normalized()


class HighPassEffect(BiquadEffect):

    def __init__(self, sample_rate, cutoff_frq, q):
        super().__init__(sample_rate, cutoff_frq)
        self.alpha = np.sin(self.w0) / (2 * q)
        self.b0 = (1 + np.cos(self.w0)) / 2
        self.b1 = -(1 + np.cos(self.w0))
        self.b2 = (1 + np.cos(self.w0)) / 2
        self.a0 = 1 + self.alpha
        self.a1 = -2 * np.cos(self.w0)
        self.a2 = 1 - self.alpha
        self.normalized()


class BandPassEffect(BiquadEffect):

    def __init__(self, sample_rate, cutoff_frq, band_width):
        super().__init__(sample_rate, cutoff_frq)
        self.alpha = np.sin(self.w0) / (2 * cutoff_frq / band_width)
        self.b0 = self.alpha
        self.b1 = 0
        self.b2 = -self.alpha
        self.a0 = 1 + self.alpha
        self.a1 = -2 * np.cos(self.w0)
        self.a2 = 1 - self.alpha
        self.normalized()


class PeakEQEffect(BiquadEffect):

    def __init__(self, sample_rate, cutoff_frq, band_width, gain):
        super().__init__(sample_rate, cutoff_frq)
        self.alpha = np.sin(self.w0) / (2 * cutoff_frq / band_width)
        self.A = np.exp(gain / 40.0 * np.log(10))
        self.b0 = 1 + self.alpha * self.A
        self.b1 = -2 * np.cos(self.w0)
        self.b2 = 1 - self.alpha * self.A
        self.a0 = 1 + self.alpha / self.A
        self.a1 = -2 * np.cos(self.w0)
        self.a2 = 1 - self.alpha / self.A
        self.normalized()
