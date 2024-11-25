import numpy as np
from scipy.optimize import minimize
from typing import Dict, List, Tuple, Optional
import logging

class EnhancedHarmonicBalancer:
    """
    Advanced harmonic balancing system for power and vibration applications.
    
    This class implements an enhanced version of the harmonic balancer that uses
    adaptive frequency detection, optimization-based Psi adjustment, and 
    application-specific processing for power systems and mechanical vibrations.
    
    Attributes:
        base_frequency (float): The fundamental frequency of the system
        num_harmonics (int): Number of harmonics to consider
        application (str): Type of application ('power' or 'vibration')
        psi (np.ndarray): Phase adjustment values for each harmonic
        frequencies (np.ndarray): Array of harmonic frequencies
        history (dict): Historical performance metrics
        
    Example:
        >>> balancer = EnhancedHarmonicBalancer(60, num_harmonics=5, application='power')
        >>> balanced_signal = balancer.balance_signal(input_signal, sample_rate)
    """
    
    def __init__(self, base_frequency: float, num_harmonics: int = 5, 
                 application: str = 'power') -> None:
        """
        Initialize the harmonic balancer.
        
        Args:
            base_frequency: Fundamental frequency of the system
            num_harmonics: Number of harmonics to consider
            application: Type of application ('power' or 'vibration')
        """
        self.base_frequency = base_frequency
        self.num_harmonics = num_harmonics
        self.golden_ratio = (1 + np.sqrt(5)) / 2
        self.psi = np.random.uniform(0, 2*np.pi, num_harmonics)
        self.frequencies = np.array([base_frequency * (i + 1) for i in range(num_harmonics)])
        self.application = application
        self.learning_rate = 0.01
        self.history = {'thd': [], 'psi': [], 'frequency_drift': []}
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def detect_base_frequency(self, signal_data: np.ndarray, 
                            sample_rate: float) -> float:
        """
        Detect the fundamental frequency in the signal.
        
        Uses FFT-based analysis to identify the dominant frequency component
        and updates the internal frequency tracking if drift is detected.
        
        Args:
            signal_data: Input time series data
            sample_rate: Sampling rate of the signal
            
        Returns:
            float: Detected fundamental frequency
        """
        spectrum = np.abs(np.fft.fft(signal_data))
        freqs = np.fft.fftfreq(len(signal_data), 1/sample_rate)
        positive_freqs = freqs[:len(freqs)//2]
        positive_spectrum = spectrum[:len(spectrum)//2]
        
        main_freq_idx = np.argmax(positive_spectrum)
        detected_freq = np.abs(positive_freqs[main_freq_idx])
        
        if np.abs(detected_freq - self.base_frequency) > 0.5:
            self.logger.info(f"Frequency drift detected: {detected_freq - self.base_frequency:.2f} Hz")
            self.base_frequency = detected_freq
            self.frequencies = np.array([detected_freq * (i + 1) for i in range(self.num_harmonics)])
            
        return detected_freq
    
    def optimize_psi(self, signal_data: np.ndarray, 
                    sample_rate: float) -> float:
        """
        Optimize Psi values to minimize Total Harmonic Distortion.
        
        Uses Nelder-Mead optimization to find optimal phase adjustments.
        
        Args:
            signal_data: Input time series data
            sample_rate: Sampling rate of the signal
            
        Returns:
            float: Final THD value after optimization
        """
        def objective(psi_values):
            self.psi = psi_values
            balanced = self.balance_signal(signal_data, sample_rate)
            return self.calculate_thd(balanced, sample_rate)
        
        result = minimize(objective, self.psi, method='Nelder-Mead')
        self.psi = result.x
        return result.fun
    
    def calculate_thd(self, signal_data: np.ndarray, 
                     sample_rate: float) -> float:
        """
        Calculate Total Harmonic Distortion of the signal.
        
        Args:
            signal_data: Input time series data
            sample_rate: Sampling rate of the signal
            
        Returns:
            float: THD value
        """
        spectrum = np.abs(np.fft.fft(signal_data))
        freqs = np.fft.fftfreq(len(signal_data), 1/sample_rate)
        
        fundamental_idx = np.argmax(spectrum[:len(spectrum)//2])
        harmonics = spectrum[fundamental_idx*2:fundamental_idx*5]
        
        thd = np.sqrt(np.sum(harmonics**2)) / spectrum[fundamental_idx]
        return thd
    
    def balance_signal(self, signal_data: np.ndarray, 
                      sample_rate: float) -> np.ndarray:
        """
        Apply harmonic balancing to the input signal.
        
        Implements application-specific processing for power systems
        and mechanical vibrations.
        
        Args:
            signal_data: Input time series data
            sample_rate: Sampling rate of the signal
            
        Returns:
            np.ndarray: Balanced signal
        """
        detected_freq = self.detect_base_frequency(signal_data, sample_rate)
        
        freq_domain = np.fft.fft(signal_data)
        freqs = np.fft.fftfreq(len(signal_data), 1/sample_rate)
        
        if self.application == 'power':
            # Focus on odd harmonics for power systems
            for i, freq in enumerate(self.frequencies):
                if i % 2 == 0:  # Odd harmonics
                    mask = (np.abs(freqs) >= freq-1) & (np.abs(freqs) <= freq+1)
                    freq_domain[mask] *= np.exp(1j * self.psi[i])
                    
        elif self.application == 'vibration':
            # Consider all harmonics with progressive damping
            for i, freq in enumerate(self.frequencies):
                mask = (np.abs(freqs) >= freq-2) & (np.abs(freqs) <= freq+2)
                damping = 1 / (i + 1)
                freq_domain[mask] *= np.exp(1j * self.psi[i]) * damping
        
        balanced = np.real(np.fft.ifft(freq_domain))
        
        # Update history
        self.history['thd'].append(self.calculate_thd(balanced, sample_rate))
        self.history['psi'].append(self.psi.copy())
        self.history['frequency_drift'].append(detected_freq - self.base_frequency)
        
        return balanced
