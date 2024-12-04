from flask import Flask, render_template, request, jsonify
from src.harmonic_balancer import EnhancedHarmonicBalancer
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/balance', methods=['POST'])
def balance():
    data = request.json
    base_freq = data['baseFreq']
    harmonic_level = data['harmonicLevel']
    
    # Generate a sample signal
    t = np.linspace(0, 1, 1000)
    signal = np.sin(2 * np.pi * base_freq * t) + (harmonic_level / 100) * np.sin(2 * np.pi * 2 * base_freq * t)
    
    # Process the signal
    balancer = EnhancedHarmonicBalancer(base_freq, num_harmonics=5, application='power')
    balanced_signal = balancer.balance_signal(signal, sample_rate=1000)
    
    # Calculate THD before and after
    thd_before = balancer.calculate_thd(signal, 1000)
    thd_after = balancer.calculate_thd(balanced_signal, 1000)
    
    # Prepare data for plotting
    return jsonify({
        'signals': [
            {'x': t.tolist(), 'y': signal.tolist(), 'type': 'scatter', 'name': 'Original'},
            {'x': t.tolist(), 'y': balanced_signal.tolist(), 'type': 'scatter', 'name': 'Balanced'}
        ],
        'layout': {'title': 'Signal Comparison'},
        'spectrum': [
            {'x': np.fft.fftfreq(1000, 1/1000)[:500].tolist(), 'y': np.abs(np.fft.fft(signal))[:500].tolist(), 'type': 'scatter', 'name': 'Original Spectrum'},
            {'x': np.fft.fftfreq(1000, 1/1000)[:500].tolist(), 'y': np.abs(np.fft.fft(balanced_signal))[:500].tolist(), 'type': 'scatter', 'name': 'Balanced Spectrum'}
        ],
        'spectrumLayout': {'title': 'Frequency Spectrum'},
        'metrics': {
            'thdBefore': f"{thd_before:.2%}",
            'thdAfter': f"{thd_after:.2%}",
            'improvement': f"{(thd_before - thd_after) / thd_before:.2%}"
        }
    })

if __name__ == '__main__':
    app.run(debug=True)