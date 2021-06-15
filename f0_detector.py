

# base_frequency_index = 0
#     last_av_amplitude = 0
#     for index in range(1, len(c)):
#         avg_amplitude = 0
#         i = index
#         count = 0
#         while i < len(c):
#             avg_amplitude += abs(c[i])
#             i *= 2
#             count += 1
#         avg_amplitude = avg_amplitude / count
#         if avg_amplitude > last_av_amplitude:
#             last_av_amplitude = avg_amplitude
#             base_frequency_index = index
#
#     print("base frequency index %d value %f" % (base_frequency_index,freq[base_frequency_index]))