from Stimulus import Stimulus

# Define length of stimulus in seconds and sampling rate in samples/second
length = 0.1
fs = 44100

# Initialise Stimulus object with given length and sampling rate
s = Stimulus(length, fs)

# Define frequency of tone
f = 1000

# Generate tone
s.pure_tone(f)

# Define start and stop frequency of sweep
start = 0
stop = 1000

# Generate frequency sweep
s.chirp(start,stop)

# Generate silence
s.silence()


# Generate noise and silence and add them together
fs = 44100

noise_length = 0.1
silence_length = 1


noise = Stimulus(noise_length, fs)
noise.noise()

silence = Stimulus(silence_length, fs)
silence.silence()

stim = silence + noise

# Repeat stim
repeated_stim = 3 * stim


# Plotting the stimulus waveform and spectrogram
repeated_stim.plot_waveform()
repeated_stim.plot_spectrogram()


# Saving stimulus in to wav file
repeated_stim.save_wav('filename.wav')



s.plot_stimulus_waveform()
s.plot_stimulus_spectrogram()