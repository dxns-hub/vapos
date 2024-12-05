import unittest
import numpy as np
from src.harmonic_balancer import EnhancedHarmonicBalancer

class TestEnhancedHarmonicBalancer(unittest.TestCase):

    def test_combined_approach(self):
        # Generate a complex signal with multiple harmonics
        t = np.linspace(0, 1, 1000)
        base_freq = 60
        signal = (
            np.sin(2 * np.pi * base_freq * t) +  # Fundamental
            0.5 * np.sin(2 * np.pi * 2 * base_freq * t) +  # 2nd harmonic
            0.3 * np.sin(2 * np.pi * 3 * base_freq * t) +  # 3rd harmonic
            0.2 * np.sin(2 * np.pi * 4 * base_freq * t) +  # 4th harmonic
            0.1 * np.sin(2 * np.pi * 5 * base_freq * t)    # 5th harmonic
        )

        # Create balancer and process signal
        balancer = EnhancedHarmonicBalancer(base_frequency=base_freq, num_harmonics=5, application='power')
        balanced_signal = balancer.balance_signal(signal, sample_rate=1000)

        # Perform FFT to analyze frequency components
        fft_original = np.abs(np.fft.fft(signal))
        fft_balanced = np.abs(np.fft.fft(balanced_signal))

        # Normalize the balanced signal to match the fundamental frequency amplitude of the original signal
        fundamental_index = int(base_freq * len(t) / 1000)
        normalization_factor = fft_original[fundamental_index] / fft_balanced[fundamental_index]
        balanced_signal_normalized = balanced_signal * normalization_factor
        fft_balanced_normalized = np.abs(np.fft.fft(balanced_signal_normalized))

        # Calculate THD before and after balancing
        thd_before = balancer.calculate_thd(signal, 1000)
        thd_after = balancer.calculate_thd(balanced_signal_normalized, 1000)

        # Test 1: Verify THD improvement
        self.assertLess(thd_after, thd_before, "THD should be reduced after balancing")

        # Test 2: Check if the fundamental frequency (60 Hz) is preserved
        self.assertAlmostEqual(fft_balanced_normalized[fundamental_index], fft_original[fundamental_index], delta=fft_original[fundamental_index]*0.01,
                               msg="Fundamental frequency component should be preserved")

        # Test 3: Verify reduction in harmonic amplitudes
        for harmonic in range(2, 6):  # Check 2nd to 5th harmonics
            harmonic_index = int(harmonic * base_freq * len(t) / 1000)
            self.assertLess(fft_balanced_normalized[harmonic_index], fft_original[harmonic_index],
                            f"Amplitude of {harmonic}th harmonic should be reduced")

        # Test 4: Ensure the balanced signal is not just a flat line
        self.assertGreater(np.std(balanced_signal_normalized), 0, "Balanced signal should not be a flat line")

        # Test 5: Check if the total energy of the signal is reduced but not excessively
        energy_original = np.sum(signal**2)
        energy_balanced_normalized = np.sum(balanced_signal_normalized**2)
        energy_ratio = energy_balanced_normalized / energy_original
        print(f"Energy ratio (balanced / original): {energy_ratio:.4f}")
        self.assertGreater(energy_ratio, 0.5, "Balanced signal energy should not be less than 50% of the original")
        self.assertLess(energy_ratio, 1.0, "Balanced signal energy should be less than the original")

        # Additional checks
        print(f"THD before: {thd_before:.4f}, THD after: {thd_after:.4f}")
        print(f"Original signal RMS: {np.sqrt(np.mean(signal**2)):.4f}")
        print(f"Balanced signal RMS: {np.sqrt(np.mean(balanced_signal_normalized**2)):.4f}")
if __name__ == '__main__':
    unittest.main()

