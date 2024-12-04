document.addEventListener('DOMContentLoaded', function() {
    const startButton = document.getElementById('startDemo');
    const baseFreqInput = document.getElementById('baseFreq');
    const harmonicLevelInput = document.getElementById('harmonicLevel');

    function updatePlots() {
        fetch('/api/balance', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                baseFreq: parseFloat(baseFreqInput.value),
                harmonicLevel: parseFloat(harmonicLevelInput.value)
            }),
        })
        .then(response => response.json())
        .then(data => {
            // Update plots
            Plotly.newPlot('signalPlot', data.signals, data.layout);
            Plotly.newPlot('spectrumPlot', data.spectrum, data.spectrumLayout);
            
            // Update metrics
            document.getElementById('thdBefore').textContent = data.metrics.thdBefore;
            document.getElementById('thdAfter').textContent = data.metrics.thdAfter;
            document.getElementById('improvement').textContent = data.metrics.improvement;
        });
    }

    startButton.addEventListener('click', updatePlots);
    baseFreqInput.addEventListener('change', updatePlots);
    harmonicLevelInput.addEventListener('input', updatePlots);
});