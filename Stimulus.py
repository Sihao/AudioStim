import numpy as np
import scipy.io.wavfile as io
import scipy.signal as sig
import matplotlib.pyplot as plt

class Stimulus():
    """Object which generates an auditory stimulus using scipy functions and stores it"""

    def __init__(self, length, fs):
        """Constructor"""

        # Length of desired stimulus in seconds
        self.length = length

        # Sampling frequency fs of stimulus in Hz
        self.fs = fs

        # Number of samples for length at sampling frequency fs
        self.num_samples = self._calc_num_samples()

        # Array of time points
        self.time_points = np.linspace(0, self.length, self.num_samples)

        # Actual stimulus data
        self.data = []



    def pure_tone(self, f):
        """Generate pure tone at specified frequency of length specified in object (at specified sampling frequency)"""

        t = np.arange(self.num_samples)
        self.data = np.sin(2 * np.pi * f * t / self.fs)

    def noise(self):
        """Generate white noise"""
        self.data = 2 * np.random.random(size = self.num_samples) - 1

    def chirp(self, f0, f1, method = 'linear'):
        """
        Generate frequency sweeped cosine

        f0: frequency at time 0 (Hz)
        f1: frequency at end (Hz)
        method: method to sweep across frequencies; 'linear', 'quadratic', 'logarithmic' or 'hyperbolic'
        """

        self.data = sig.chirp(t = self.time_points, f0 = f0, f1 = f1, t1 = self.length, method = method)

    def silence(self):
        """Generate silence (zeroes)"""

        self.data = np.zeros(self.num_samples)

    def taper(self,start_pct,end_pct):
        """
        Tapers the power across all frequencies at the start and end of stimulus

        start_pct: percentage of the full stimulus to taper at the start of the stimulus (0-1)
        end_pct: percentage of the full stimulus to taper at the end of the stimulus (0-1)
        """

        assert start_pct < 1 and start_pct > 0, "start_pct must be between 0 and 1"
        assert end_pct < 1 and end_pct > 0, "end_pct must be between 0 and 1"
        assert start_pct+end_pct < 1, "Sum of start_pct and end_pct can not exceed 1"

    def plot_waveform(self):
        """Plot the waveform of the generated stimulus"""

        fig = plt.figure()
        plt.plot(self.time_points, self.data)

        plt.ylabel('Amplitude')
        plt.xlabel('Time [sec]')

        fig.show()

    def plot_spectrogram(self):
        """Plot the spectrogram of the generated stimulus"""

        f, t, Sxx = sig.spectrogram(self.data, self.fs)

        fig = plt.figure()
        plt.pcolormesh(t, f, Sxx)
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time [sec]')
        fig.show()

    def save_wav(self, filename, bit_depth='16'):
        """Saves the stimulus stored in self.data into a .wav file

           filename: path to save wav file to
           bit_depth: either '16' or '32', sets the bit depth of the output wavfile

        """
        if bit_depth is '16':
            max = np.iinfo(np.int16).max

            io.write(filename, self.fs, (self.data*max).astype(np.int16))
        elif bit_depth is '32':
            max = np.iinfo(np.int32).max

            io.write(filename, self.fs, (self.data*max).astype(np.int32))
        else:
            io.write(filename, self.fs, self.data)

    def __add__(self, other):
        assert self.fs == other.fs, "Sampling frequencies must be equal"

        result_length = self.length + other.length
        result = Stimulus(result_length, self.fs)
        result.data = np.append(self.data, other.data)

        return(result)

    def __rmul__(self, other):
        assert isinstance(other, int), "Multiplication is only possible with scalars"

        result_length = other * self.length

        result = Stimulus(result_length, self.fs)

        for i in range(other):
            result.data = np.append(result.data, self.data)

        return result

    def _calc_num_samples(self):
        """Calculate number of samples needed to have stim of specified length at specified sampling frequency"""

        return np.int32(np.floor(self.length * self.fs))