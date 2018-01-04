# RJS: Added amendments to work with refactored code 03-JAN-2018


import scipy
import numpy
import numpy as np
import scipy.signal as sps
import time

freq4 = 4 * 315.0 / 88.0
freq = 4 * 315.0 / 88.0
freq10 = 5 * 315.0 / 88.0
freq32 = 32

# RJS: standardise output for C++

def WriteFilter(name, b, a = [1.0]):
	print("std::vector<double> c_",name,"_b = {",sep="",end="")
	ct = len(b)
	for i in range(0, ct):
		# insert a new line and an indent every 4 items
		if i % 4 == 0:
			print()
			print("\t",end='')
		# print the item
		print("%.15e" % b[i], end='')
		if i < ct-1:
			print(", ", end='')
	print("\n};")

	print("std::vector<double> c_",name,"_a = {",sep="",end="")
	ct = len(a)
	for i in range(0, ct):
		# insert a new line and an indent every 4 items
		if i % 4 == 0:
			print()
			print("\t",end='')
		# print the item
		print("%.15e" % a[i], end="")
		if i < ct-1:
			print(", ", end='')
	print("\n};")
	print()
	print("Filter f_",name,"(c_",name,"_b, c_",name,"_a);",sep="")
	print()


tH = 100.0/1000000000.0 # 100nS
tL = 300.0/1000000000.0 # 300nS

n = 512 
df = 512.0/(freq) 
Fr = np.zeros(n)
Am = np.zeros(n)
Th = np.zeros(n)

f_deemp_bil_b = [2.819257458245255e-01, -4.361485083509491e-01]
f_deemp_bil_a = [1.000000000000000e+00, -1.154222762526424e+00]

w, h = sps.freqz(f_deemp_bil_b, f_deemp_bil_a)
w = w / (np.pi * 1.0)
h.imag = h.imag * 1

#fdls.doplot2(freq10,f_deemp10_b, f_deemp10_a, 1.0, f_deemp10_bil_b, f_deemp10_bil_a, 1.0)
#exit()

# RJS: put a comment on this so readers know where it came from and when
timestamp=time.gmtime()
prettytimestamp=time.strftime("%c", timestamp)
print("// Generated by filtermaker.py on",prettytimestamp)
print()
print("// Do not manually change this code; changes may be overwritten")
print()


# Write the ifdefs first
print ("#ifndef DEEMP_H")
print ("#define DEEMP_H")
print ();

Bboost = sps.firwin(33, 3.5 / (freq), window='hamming', pass_zero=False)
WriteFilter("boost", Bboost)
Bboost10 = sps.firwin(33, 3.5 / (freq10), window='hamming', pass_zero=False)
WriteFilter("boost10", Bboost10)

Ncolor = 32
Fcolor = sps.firwin(Ncolor + 1, 0.2 / (freq), window='hamming')
WriteFilter("color", Fcolor)

Nlpf = 30
lowpass_filter = sps.firwin(Nlpf + 1, 5.2 / (freq), window='hamming')
WriteFilter("lpf", lowpass_filter)

Nlpf = 30
lowpass_filter = sps.firwin(Nlpf + 1, 4.2 / (freq), window='hamming')
WriteFilter("lpf42", lowpass_filter)

# used for comb filtering
lowpass10h_filter = sps.firwin(32 + 1, 0.8 / (freq), window='hamming')
WriteFilter("lpf_comb", lowpass10h_filter)

Nlpf4 = 10
lowpass_filter4 = sps.firwin(Nlpf + 1, 5.2 / (freq4), window='hamming')
WriteFilter("lpf4", lowpass_filter4)

Nlpf10 = 30
lowpass_filter10 = sps.firwin(Nlpf + 1, 5.2 / (freq10), window='hamming')
WriteFilter("lpf10", lowpass_filter10)

Ncolor = 24
sync_filter = sps.firwin(Ncolor + 1, 0.1 / (freq), window='hamming')
WriteFilter("sync", sync_filter)

# BPF sync filter for NTSC (+/- .2mhz)
Nsyncbpf = 16 
syncbpf_filter = sps.firwin(Nsyncbpf + 1, [3.37955 / freq4, 3.77955/ freq4], window='hamming')
WriteFilter("ntscsyncbpf4", syncbpf_filter)

# Small 1mhz filter for end-of-sync det
N2sync = 16 
sync2_filter = sps.firwin(N2sync + 1, 2.0 / (freq), window='hamming')
WriteFilter("esync8", sync2_filter)

sync2_filter = sps.firwin(N2sync + 1, 2.0 / (freq4), window='hamming')
WriteFilter("esync4", sync2_filter)

sync2_filter = sps.firwin(N2sync + 1, 2.0 / (freq10), window='hamming')
WriteFilter("esync10", sync2_filter)

sync2_filter = sps.firwin(N2sync + 1, 2.0 / (freq32), window='hamming')
WriteFilter("esync32", sync2_filter)

# PAL sync filter
Ndsync = 32 
dsync_filter = sps.firwin(Ndsync + 1, 2.0 / (freq), window='hamming')
WriteFilter("psync8", dsync_filter)

Ndsync = 32 
dsync_filter = sps.firwin(Ndsync + 1, 2.0 / (freq4), window='hamming')
WriteFilter("psync4", dsync_filter)

Ndsync = 32 
dsync_filter = sps.firwin(Ndsync + 1, 2.0 / (freq10), window='hamming')
WriteFilter("psync10", dsync_filter)

# used in ntsc to determine sync level
Ndsync = 32 
dsync_filter = sps.firwin(Ndsync + 1, 0.1 / (freq), window='hamming')
WriteFilter("dsync", dsync_filter)

Ndsync = 20 
dsync_filter4 = sps.firwin(Ndsync + 1, 0.1 / (freq4), window='hamming')
WriteFilter("dsync4", dsync_filter4)

Ndsync = 32 
dsync_filter10 = sps.firwin(Ndsync + 1, 0.1 / (freq10), window='hamming')
WriteFilter("dsync10", dsync_filter10)

Ndsync = 32 
dsync_filter32 = sps.firwin(Ndsync + 1, 0.1 / (freq32), window='hamming')
WriteFilter("dsync32", dsync_filter32)

Nsync = 20
sync_filter4 = sps.firwin(Nsync + 1, 0.1 / (freq4), window='hamming')
WriteFilter("sync4", sync_filter4)

Nsync = 32
sync_filter10 = sps.firwin(Nsync + 1, 0.1 / (freq10), window='hamming')
WriteFilter("sync10", sync_filter10)

Nnr = 24
hp_nr_filter = sps.firwin(Nnr + 1, 1.80 / (freq / 2.0), window='hamming', pass_zero=False)
WriteFilter("nr", hp_nr_filter)
hp_nr28_filter = sps.firwin(Nnr + 1, [2.60 / (freq / 2.0), 2.9 / (freq / 2.0)], window='hamming', pass_zero=False)
WriteFilter("nr28", hp_nr28_filter)

Nnr = 24
hp_nr_filter = sps.firwin(Nnr + 1, 1.80 / (freq / 2.0), window='hamming', pass_zero=True)
WriteFilter("lp18", hp_nr_filter)

Nnrc = 24
Nnrc = 16
hp_nrc_filter = sps.firwin(Nnrc + 1, 0.4 / (freq / 2.0), window='hamming', pass_zero=False)
WriteFilter("nrc", hp_nrc_filter)

Ncolorlp = 8 
colorwlpi_filter = sps.firwin(Ncolorlp + 1, [1.3 / (freq4 / 1)], window='hamming')
colorwlpq_filter = sps.firwin(Ncolorlp + 1, [0.6 / (freq4 / 1)], window='hamming')

#Ncolorlp = 16
#colorwlpi_filter = sps.firwin(Ncolorlp + 1, [1.6 / (freq4 / 2)], window='hamming')
#colorwlpq_filter = sps.firwin(Ncolorlp + 1, [0.55 / (freq4 / 2)], window='hamming')

#WriteFilter("colorlpi", colorwlpi_filter)
#WriteFilter("colorlpq", colorwlpq_filter)

i_filter_b, i_filter_a = sps.butter(1, (1.3/(freq4/2)), 'low')
q_filter_b, q_filter_a = sps.butter(3, (0.6/(freq4/2)), 'low')
WriteFilter("colorlpi", i_filter_b, i_filter_a)
WriteFilter("colorlpq", q_filter_b, q_filter_a)
print("const int f_colorlpi_offset = 2;")
print("const int f_colorlpq_offset = 14;")

Ncolorbp4 = 8
colorbp4_filter = sps.firwin(Ncolorbp4 + 1, [3.4006 / (freq / 2), 3.7585 / (freq / 2)], window='hamming', pass_zero=False)
WriteFilter("colorbp4", colorbp4_filter)

Ncolorbp8 = 16
colorbp8_filter = sps.firwin(Ncolorbp8 + 1, [3.4006 / (freq), 3.7585 / (freq)], window='hamming', pass_zero=False)
WriteFilter("colorbp8", colorbp8_filter)

#audioin_filter = sps.firwin(65, 3.15 / (freq), window='hamming')
#WriteFilter("audioin", audioin_filter)

audioin_filter_b, audioin_filter_a = sps.butter(8, 3.3 / freq)
WriteFilter("audioin", audioin_filter_b, audioin_filter_a)

leftbp_filter = sps.firwin(33, [2.2/(freq/4), 2.4/(freq/4)], window='hamming', pass_zero=False)
WriteFilter("leftbp", leftbp_filter)
rightbp_filter = sps.firwin(33, [2.7/(freq/4), 2.9/(freq/4)], window='hamming', pass_zero=False)
WriteFilter("rightbp", rightbp_filter)

# decoded audio LP first stage:  2x fsc sample rate 

audiolp_filter_b, audiolp_filter_a = sps.butter(8, .10 / (freq / 4))
WriteFilter("audiolp", audiolp_filter_b, audiolp_filter_a)

# decoded audio LP second stage:  2x/20 fsc sample rate 

audiolp_filter_b, audiolp_filter_a = sps.butter(8, .024 / (freq / 4 / 20))
WriteFilter("audiolp20", audiolp_filter_b, audiolp_filter_a)

a500_48k_b, a500_48k_a = sps.butter(4, 500.0/24000.0, btype='highpass')
#a500_48k_b = sps.firwin(17, 500.0/24000.0, pass_zero=False)
#a500_48k_a = [1.0]
WriteFilter("a500_48k", a500_48k_b, a500_48k_a)

#a500_44k_b, a500_44k_a = sps.butter(8, 500.0/22050.0) 
a500_44k_b = sps.firwin(17, 500.0/22050.0, pass_zero=False) 
a500_44k_a = [1.0]
WriteFilter("a500_44k", a500_44k_b, a500_44k_a)

a40h_48k_b, a40h_48k_a = sps.butter(4, 40.0/24000.0, btype='highpass')
#a40h_48k_b = sps.firwin(17, 40.0/24000.0, pass_zero=False) 
#a40h_48k_a = [1.0]
WriteFilter("a40h_48k", a40h_48k_b, a40h_48k_a)

# from http://tlfabian.blogspot.com/2013/01/implementing-hilbert-90-degree-shift.html
hilbert_filter = np.fft.fftshift(
    np.fft.ifft([0]+[1]*13+[0]*13)
)
WriteFilter("hilbertr", hilbert_filter.real)
WriteFilter("hilberti", hilbert_filter.imag)

# PAL sync 3.75mhz pilot burst filter 
freq_pal4fsc = 4 * 4.43361875
Npilot = 16
#pilot_filter = sps.firwin(Npilot + 1, [3.7 / (freq_pal4fsc / 2), 3.8 / (freq_pal4fsc / 2)], window='hamming', pass_zero=False)
pilot_filter = sps.firwin(Npilot + 1, [3.74 / 7.5, 3.76 / 7.5], window='hamming', pass_zero=False)
WriteFilter("pilot", pilot_filter)

# fm deemphasis (75us)
table = [[.000, 0], [.1, -.01], [.5, -.23], [1, -.87], [2, -2.76], [3, -4.77], [4, -6.58], [5, -8.16], [6, -9.54], [7, -10.75], [8, -11.82], [9, -12.78], [10, -13.66], [11, -14.45], [12, -15.18], [13, -15.86], [14, -16.49], [15, -17.07], [16, -17.62], [17, -18.14], [18, -18.63], [19, -19.09], [20, -19.53], [24, -20]]

Fr = np.empty([len(table)])
Am = np.empty([len(table)])
for i in range(0, len(table)):
	Fr[i] = (table[i][0] / 24.0)
	Am[i] = (np.exp(table[i][1] / 9.0))

Bfmdeemp = sps.firwin2(33, Fr, Am)
WriteFilter("fmdeemp", Bfmdeemp)

# bandpass filter for smoothing out EFM audio, fsc=8
efm_filter_bf = sps.firwin(49, [.05/freq, 1.10/freq], pass_zero=False)
efm_filter_af = [1.0]
WriteFilter("efm8", efm_filter_bf, efm_filter_af)

# Used to determine sync status - feed it a 1 when level < 12000 (fsc8) or IRE -10 or so (fsc4) 
f_syncid_b, f_syncid_a = sps.butter(3, 0.002)
WriteFilter("syncid8", f_syncid_b, f_syncid_a)

f_syncid_b, f_syncid_a = sps.butter(3, 0.004)
WriteFilter("syncid4", f_syncid_b, f_syncid_a)

f_syncid_b, f_syncid_a = sps.butter(3, 0.0018)
WriteFilter("syncid32", f_syncid_b, f_syncid_a)

f_syncid_b, f_syncid_a = sps.butter(3, 0.0016)
WriteFilter("syncid10", f_syncid_b, f_syncid_a)

print("const int syncid4_offset = 165;")
print("const int syncid8_offset = 320;")
print("const int syncid32_offset = 360;")
print("const int syncid10_offset = 400;")


linelen_filter_b = sps.firwin(17, 0.1)
WriteFilter("linelen", linelen_filter_b, [1.0])

print("#endif")
