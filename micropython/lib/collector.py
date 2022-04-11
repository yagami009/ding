from .peripherals import PeripheralManager
from ulab import numpy as np
import gc
import config

from micropython import schedule


class Collector:
    def __init__(self, buffer_size=256, stimulus_freqs=None, sample_freq = 256, ds_freq=64, preprocess=False, ds=False) -> None:
        if stimulus_freqs is None:
            self.stim_freqs = config.STIM_FREQS  # assign defaults

        self.base_sample_freq = sample_freq

        self.preprocessing_enabled = preprocess

        if self.preprocessing_enabled:
            self.downsampled_freq = ds_freq
        else:
            self.downsampled_freq = sample_freq

        self.downsample = ds

        self.sample_counter = 0
        self.buffer_size = buffer_size  # TODO: update this to be populated dynamically

        self.output_buffer = [0.0 for i in range(self.buffer_size)]

        self.is_setup = False
        self.is_sampling = False
        self.is_logging = False

    def setup(self, spi_params=None, adc_params=None):
        from machine import freq

        freq(config.BASE_CLK_FREQ)  # set the CPU frequency

        self._init_peripherals(spi_params, adc_params)
        gc.collect()

        print("Collector initialised with preprocessing ({0}), downsampling ({1})".format(
            self.preprocessing_enabled, self.downsample
            )
        )

        self.is_setup = True

    def run(self):
        if not self.is_setup:
            raise ValueError("Collector not setup. Call `.setup()` before running.")

        self.start_sample_timer()

    def stop(self):
        if self.is_sampling:
            self.stop_sample_timer()

        if self.is_logging:
            self.stop_logger()

    def preprocess_data(self, signal, ds=False):

        """Preprocess incoming signal before decoding algorithms.
        This involves applying a bandpass filter to isolate the target SSVEP range
        and then downsampling the signal to the Nyquist boundary.

        Returns:
            [np.ndarray]: filtered and downsampled signal
        """
        from lib.signal import sos_filter

        ds_factor = self.downsampling_factor
        signal = np.array(signal) - np.mean(signal)  # remove DC component

        # downsample filtered signal by only selecting every `ds_factor` sample
        if ds:
            return sos_filter(signal, fs=self.base_sample_freq)[::ds_factor]
        else:
            return sos_filter(signal, fs=self.base_sample_freq)

    def sample_callback(self, *args, **kwargs):
        from lib.utils import update_buffer

        self.periph_manager.adc_read_to_buff(size=1)
        self.sample_counter += 1

        # this will only be true every 1s once buffer fills
        if self.sample_counter >= self.buffer_size:
            self.periph_manager.write_led("red", 1)
            data = self._read_internal_buffer(preprocess=self.preprocessing_enabled, downsample=self.downsample)
            update_buffer(
                self.output_buffer, list(data), self.buffer_size, inplace=True
            )
            self.sample_counter = 0
            self.periph_manager.write_led("red", 0)

    def read_output_buffer(self):
        return self.output_buffer

    def start_sample_timer(self):
        from machine import Timer

        self.sample_timer = Timer(0)
        self.sample_timer.init(
            freq=self.base_sample_freq, callback=self.sample_callback
        )
        self.is_sampling = True

    def stop_sample_timer(self):
        if self.sample_timer is not None:
            self.sample_timer.deinit()
            self.is_sampling = False

    @property
    def downsampling_factor(self):
        return self.base_sample_freq // self.downsampled_freq

    def _read_internal_buffer(self, preprocess=False, downsample=False):
        data = self.periph_manager.read_adc_buffer()
        if preprocess and len(data) > 1:
            data = self.preprocess_data(data, downsample)
        return data

    def _init_peripherals(self, spi_params, adc_params):

        self.periph_manager = PeripheralManager(
            spi_params=spi_params, adc_params=adc_params
        )
        self.periph_manager.init()
