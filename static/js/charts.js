// Chart.js Visualizations for Model Evaluation & Engagement Dashboards

document.addEventListener('DOMContentLoaded', function () {
  // 1. Model Evaluation Comparison Bar Chart
  const modelCompCanvas = document.getElementById('modelComparisonChart');
  if (modelCompCanvas && window.Chart) {
    new Chart(modelCompCanvas, {
      type: 'bar',
      data: {
        labels: ['Random Forest', 'XGBoost', 'CRNN (Attention)', 'CNN + Conformer', 'YOLOv12 CV'],
        datasets: [
          {
            label: 'Accuracy (%)',
            data: [83.4, 86.8, 91.5, 93.7, 89.2],
            backgroundColor: 'rgba(79, 70, 229, 0.85)',
            borderColor: '#4f46e5',
            borderRadius: 6
          },
          {
            label: 'F1-Score (%)',
            data: [82.9, 86.3, 91.2, 93.4, 88.8],
            backgroundColor: 'rgba(6, 182, 212, 0.85)',
            borderColor: '#06b6d4',
            borderRadius: 6
          },
          {
            label: 'Precision (%)',
            data: [82.8, 86.2, 91.1, 93.4, 88.7],
            backgroundColor: 'rgba(139, 92, 246, 0.85)',
            borderColor: '#8b5cf6',
            borderRadius: 6
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { labels: { color: '#cbd5e1' } },
          tooltip: { mode: 'index', intersect: false }
        },
        scales: {
          y: {
            min: 70,
            max: 100,
            grid: { color: 'rgba(148, 163, 184, 0.1)' },
            ticks: { color: '#94a3b8' }
          },
          x: {
            grid: { display: false },
            ticks: { color: '#cbd5e1' }
          }
        }
      }
    });
  }

  // 2. Training vs Validation Learning Curves (Conformer & CRNN)
  const learningCurvesCanvas = document.getElementById('learningCurvesChart');
  if (learningCurvesCanvas && window.Chart) {
    new Chart(learningCurvesCanvas, {
      type: 'line',
      data: {
        labels: ['Ep 1', 'Ep 5', 'Ep 10', 'Ep 15', 'Ep 20', 'Ep 25', 'Ep 30'],
        datasets: [
          {
            label: 'CNN+Conformer Train Acc',
            data: [62.4, 78.5, 86.2, 90.1, 93.4, 95.2, 96.8],
            borderColor: '#22c55e',
            backgroundColor: 'transparent',
            tension: 0.3,
            borderWidth: 2.5
          },
          {
            label: 'CNN+Conformer Val Acc',
            data: [59.8, 75.1, 84.0, 88.5, 91.7, 93.0, 93.7],
            borderColor: '#06b6d4',
            backgroundColor: 'transparent',
            borderDash: [5, 5],
            tension: 0.3,
            borderWidth: 2.5
          },
          {
            label: 'CRNN with Attention Val Acc',
            data: [57.2, 72.8, 81.5, 86.4, 89.2, 90.8, 91.5],
            borderColor: '#f59e0b',
            backgroundColor: 'transparent',
            tension: 0.3,
            borderWidth: 2
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { labels: { color: '#cbd5e1' } }
        },
        scales: {
          y: {
            min: 50,
            max: 100,
            grid: { color: 'rgba(148, 163, 184, 0.1)' },
            ticks: { color: '#94a3b8' }
          },
          x: {
            grid: { color: 'rgba(148, 163, 184, 0.05)' },
            ticks: { color: '#cbd5e1' }
          }
        }
      }
    });
  }

  // 3. Prediction Probability Distribution Chart (if present on prediction page)
  const probDoughnutCanvas = document.getElementById('predictionProbChart');
  if (probDoughnutCanvas && window.Chart && window.PREDICTION_DATA) {
    const dataObj = window.PREDICTION_DATA;
    const emotions = ['angry', 'happy', 'relax', 'rock', 'romantic', 'sad', 'surprise'];
    const values = emotions.map(e => dataObj[e] || 0);
    const colors = ['#ef4444', '#22c55e', '#06b6d4', '#f59e0b', '#ec4899', '#6366f1', '#8b5cf6'];

    new Chart(probDoughnutCanvas, {
      type: 'doughnut',
      data: {
        labels: emotions.map(e => e.toUpperCase()),
        datasets: [{
          data: values,
          backgroundColor: colors,
          borderColor: '#0f172a',
          borderWidth: 2
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'bottom', labels: { color: '#cbd5e1', font: { size: 11 } } }
        },
        cutout: '65%'
      }
    });
  }
});
