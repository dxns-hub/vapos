# Enhanced Harmonic Balancer Documentation

## Technical Overview

The Enhanced Harmonic Balancer implements advanced signal processing techniques
for harmonic control in power systems and mechanical vibrations.

### Key Improvements

1. Adaptive Frequency Detection
   - Real-time fundamental frequency tracking
   - Drift compensation
   - Automatic frequency adjustment

2. Application-Specific Processing
   - Power Systems:
     * Focus on odd harmonics (3rd, 5th, 7th)
     * Targeted phase adjustment
     * Power quality metrics
   
   - Vibration Systems:
     * Progressive harmonic damping
     * Resonance avoidance
     * Amplitude-dependent control

3. Optimization Framework
   - Nelder-Mead optimization for Psi values
   - THD minimization
   - Real-time performance tracking

4. Performance Monitoring
   - THD tracking
   - Frequency drift monitoring
   - Phase adjustment history

## API Reference

### EnhancedHarmonicBalancer

Main class for harmonic balancing operations.

#### Methods

- `detect_base_frequency(signal_data, sample_rate)`
  Detects and tracks fundamental frequency

- `optimize_psi(signal_data, sample_rate)`
  Optimizes phase adjustment values

- `calculate_thd(signal_data, sample_rate)`
  Calculates Total Harmonic Distortion

- `balance_signal(signal_data, sample_rate)`
  Performs harmonic balancing

## Usage Examples

See the `examples` directory for detailed usage examples.
