import unittest
import numpy as np
from src.harmonic_balancer import EnhancedHarmonicBalancer

class TestEnhancedHarmonicBalancer(unittest.TestCase):

    def setUp(self):
        self.balancer = EnhancedHarmonicBalancer(base_frequency=60, num_harmonics=5, application='power')

    def test_initialization(self):
        self.assertEqual(self.balancer.base_frequency, 60)
        self.assertEqual(self.balancer.num_harmonics, 5)
        self.assertEqual(self.balancer.application, 'power')
        self.assertEqual(len(self.balancer.psi), 5)

    def test_detect_base_frequency(self):
        t = np.linspace(0, 1, 1000)
        signal = np.sin(2 * np.pi * 60 * t)
        detected_freq = self.balancer.detect_base_frequency(signal, sample_rate=1000)
        self.assertAlmostEqual(detected_freq, 60, delta=1)

    def test_calculate_thd(self):
        t = np.linspace(0, 1, 1000)
        signal = np.sin(2 * np.pi * 60 * t) + 0.1 * np.sin(2 * np.pi * 120 * t)
        thd = self.balancer.calculate_thd(signal, sample_rate=1000)
        self.assertGreater(thd, 0)
        self.assertLess(thd, 1)

    def test_balance_signal(self):
        t = np.linspace(0, 1, 1000)
        signal = np.sin(2 * np.pi * 60 * t) + 0.5 * np.sin(2 * np.pi * 120 * t)
        balanced = self.balancer.balance_signal(signal, sample_rate=1000)
        self.assertEqual(len(balanced), len(signal))
        self.assertNotEqual(np.sum(np.abs(balanced - signal)), 0)

    def test_power_specific_processing(self):
        t = np.linspace(0, 1, 1000)
        signal = np.sin(2 * np.pi * 60 * t) + 0.5 * np.sin(2 * np.pi * 180 * t)
        processed = self.balancer.power_specific_processing(signal, sample_rate=1000)
        self.assertEqual(len(processed), len(signal))

        # Test if harmonics are reduced
        fft_original = np.fft.fft(signal)
        fft_processed = np.fft.fft(processed)
        self.assertLess(np.abs(fft_processed[180]), np.abs(fft_original[180]))

    def test_combined_approach(self):
        t = np.linspace(0, 1, 1000)
        signal = np.sin(2 * np.pi * 60 * t) + 0.5 * np.sin(2 * np.pi * 120 * t) + 0.3 * np.sin(2 * np.pi * 180 * t)
        processed = self.balancer.power_specific_processing(signal, sample_rate=1000)

        # Check if the signal is changed
        self.assertFalse(np.array_equal(signal, processed))

        # Check if harmonics are reduced
        fft_original = np.fft.fft(signal)
        fft_processed = np.fft.fft(processed)
        self.assertLess(np.abs(fft_processed[120]), np.abs(fft_original[120]))
        self.assertLess(np.abs(fft_processed[180]), np.abs(fft_original[180]))

        # Check if THD is improved
        thd_original = self.balancer.calculate_thd(signal, 1000)
        thd_processed = self.balancer.calculate_thd(processed, 1000)
        self.assertLess(thd_processed, thd_original)

if __name__ == '__main__':
    unittest.main()
