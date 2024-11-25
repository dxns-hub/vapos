# VAPOS (Vibrational and Power Optimizing Software)

A sophisticated harmonic balancing system designed for power systems and mechanical vibration applications.

## Key Features

- Adaptive frequency detection and tracking
- Application-specific harmonic processing
- Optimization-based phase adjustment
- Real-time performance monitoring
- Support for power and vibration applications

## Installation

```bash
pip install harmonic-balancer
```

## Quick Start

```python
from harmonic_balancer import EnhancedHarmonicBalancer

# Initialize balancer for power system application
balancer = EnhancedHarmonicBalancer(60, num_harmonics=5, application='power')

# Process signal
balanced_signal = balancer.balance_signal(input_signal, sample_rate)
```

## Applications

### Power Systems
- Harmonic distortion reduction
- Power quality improvement
- Grid stability enhancement

### Mechanical Vibrations
- Machine vibration control
- Resonance suppression
- Structural dynamics optimization

## Documentation

See the `docs` directory for detailed documentation and API reference.

## License

MIT License
