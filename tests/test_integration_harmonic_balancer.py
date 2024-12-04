import unittest
import numpy as np
from src.harmonic_balancer import EnhancedHarmonicBalancer
import time

class TestEnhancedHarmonicBalancerIntegration(unittest.TestCase):

    def setUp(self):
        self.balancer = EnhancedHarmonicBalancer(base_frequency=60, num_harmonics=5, application='power')

    def generate_signal(self, duration, sample_rate, base_freq, harmonics):
        t = np.linspace(0, duration, int(duration * sample_rate))
        signal = np.zeros_like(t)
        for i, amplitude in enumerate(harmonics):
            signal += amplitude * np.sin(2 * np.pi * base_freq * (i + 1) * t)
        return signal

    def test_complex_signal_balancing(self):
        # Generate a complex signal with multiple harmonics
        signal = self.generate_signal(duration=1, sample_rate=1000, base_freq=60, 
                                      harmonics=[1, 0.5, 0.3, 0.2, 0.1])
        
        balanced = self.balancer.balance_signal(signal, sample_rate=1000)
        
        # Check if THD is improved
        original_thd = self.balancer.calculate_thd(signal, 1000)
        balanced_thd = self.balancer.calculate_thd(balanced, 1000)
        self.assertLess(balanced_thd, original_thd)

    def test_frequency_drift_adaptation(self):
        # Generate a signal with drifting frequency
        t = np.linspace(0, 1, 1000)
        drifting_freq = 60 + 2 * np.sin(2 * np.pi * 0.5 * t)  # Frequency drifts between 58 and 62 Hz
        signal = np.sin(2 * np.pi * drifting_freq * t)
    
        initial_frequency = self.balancer.base_frequency
        balanced = self.balancer.balance_signal(signal, sample_rate=1000)
    
        # Check if the balancer detected any frequency change
        self.assertNotEqual(self.balancer.base_frequency, initial_frequency)
        self.assertNotEqual(self.balancer.base_frequency, 60)

    def test_noise_robustness(self):
        # Generate a signal with added noise
        signal = self.generate_signal(duration=1, sample_rate=1000, base_freq=60, 
                                      harmonics=[1, 0.5, 0.3])
        noise = np.random.normal(0, 0.1, signal.shape)
        noisy_signal = signal + noise
        
        balanced = self.balancer.balance_signal(noisy_signal, sample_rate=1000)
        
        # Check if the balancer still improves THD despite noise
        original_thd = self.balancer.calculate_thd(noisy_signal, 1000)
        balanced_thd = self.balancer.calculate_thd(balanced, 1000)
        self.assertLess(balanced_thd, original_thd)

    def test_performance_scaling(self):
        durations = [0.1, 1, 10, 100]  # Logarithmic scale
        execution_times = []
    
        for duration in durations:
            signal = self.generate_signal(duration=duration, sample_rate=1000, base_freq=60, 
                                          harmonics=[1, 0.5, 0.3, 0.2, 0.1])
            
            # Run the balance_signal method multiple times and take the average
            num_runs = 5
            total_time = 0
            for _ in range(num_runs):
                start_time = time.time()
                self.balancer.balance_signal(signal, sample_rate=1000)
                end_time = time.time()
                total_time += end_time - start_time
            
            average_time = total_time / num_runs
            execution_times.append(average_time)
    
        # Print execution times for debugging
        for duration, exec_time in zip(durations, execution_times):
            print(f"Duration: {duration}s, Execution time: {exec_time:.6f}s")
    
        # Check if there's a general increasing trend
        # We'll allow for small fluctuations by checking if at least 2 out of 3 transitions show an increase
        increases = sum(execution_times[i] < execution_times[i+1] for i in range(len(execution_times)-1))
        self.assertGreaterEqual(increases, 2, "Execution time should generally increase with signal duration")
    
        # Check if the execution time for the longest duration is significantly larger than for the shortest
        self.assertGreater(execution_times[-1], execution_times[0] * 1.5, 
                           "Execution time for the longest duration should be at least 1.5 times that of the shortest duration")

    def test_edge_case_very_low_frequency(self):
        signal = self.generate_signal(duration=10, sample_rate=1000, base_freq=1, 
                                      harmonics=[1, 0.5, 0.3])
        
        balanced = self.balancer.balance_signal(signal, sample_rate=1000)
        
        # Check if the balancer can handle very low frequencies
        self.assertIsNotNone(balanced)
        self.assertEqual(len(balanced), len(signal))

    def test_edge_case_very_high_frequency(self):
        signal = self.generate_signal(duration=0.1, sample_rate=100000, base_freq=10000, 
                                      harmonics=[1, 0.5, 0.3])
        
        balanced = self.balancer.balance_signal(signal, sample_rate=100000)
        
        # Check if the balancer can handle very high frequencies
        self.assertIsNotNone(balanced)
        self.assertEqual(len(balanced), len(signal))

    def test_application_specific_processing(self):
        signal = self.generate_signal(duration=1, sample_rate=1000, base_freq=60, 
                                      harmonics=[1, 0, 0.3, 0, 0.1])  # Only odd harmonics for power systems
        
        # Test power application
        self.balancer.application = 'power'
        power_balanced = self.balancer.balance_signal(signal, sample_rate=1000)
        
        # Test vibration application
        self.balancer = EnhancedHarmonicBalancer(base_frequency=60, num_harmonics=5, application='vibration')
        vibration_balanced = self.balancer.balance_signal(signal, sample_rate=1000)
        
        # Check if the results are different for different applications
        self.assertFalse(np.array_equal(power_balanced, vibration_balanced))

if __name__ == '__main__':
    unittest.main()