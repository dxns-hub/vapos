import numpy as np
import matplotlib.pyplot as plt
from harmonic_balancer import EnhancedHarmonicBalancer

# Generate test signal
def generate_power_signal(t, frequency_drift=0):
    f = 60 + frequency_drift
    return (np.sin(2*np.pi*f*t) +
            0.15*np.sin(2*np.pi*3*f*t) +
            0.1*np.sin(2*np.pi*5*f*t) +
            0.05*np.sin(2*np.pi*7*f*t) +
            0.02*np.random.randn(len(t)))

# Test the balancer
sample_rate = 1000
t = np.linspace(0, 5, 5000)
signal = generate_power_signal(t, frequency_drift=0.5)

balancer = EnhancedHarmonicBalancer(60, application='power')
balanced = balancer.balance_signal(signal, sample_rate)

# Plot results
plt.figure(figsize=(12, 6))
plt.plot(t[:500], signal[:500], label='Original')
plt.plot(t[:500], balanced[:500], label='Balanced')
plt.title('Harmonic Balancing Example')
plt.legend()
plt.grid(True)
plt.show()
