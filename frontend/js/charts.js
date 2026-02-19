/* ============================================
   Chart.js Configuration & Additional Charts
   ============================================ */

class ChartManager {
    constructor() {
        this.initializeAllCharts();
    }

    initializeAllCharts() {
        this.initCategoryChart();
        this.initYearChart();
        this.initReadinessChart();
    }

    initCategoryChart() {
        const ctx = document.getElementById('categoryChart');
        if (!ctx) return;

        new Chart(ctx, {
            type: 'radar',
            data: {
                labels: ['Internships', 'Certifications', 'Hackathons', 'Publications', 'Workshops', 'Projects'],
                datasets: [{
                    label: 'Department Performance',
                    data: [85, 90, 75, 60, 88, 92],
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    borderWidth: 2,
                    pointBackgroundColor: '#667eea',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    }
                },
                scales: {
                    r: {
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        });
    }

    initYearChart() {
        const ctx = document.getElementById('yearChart');
        if (!ctx) return;

        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['1st Year', '2nd Year', '3rd Year', '4th Year'],
                datasets: [{
                    label: 'Student Count',
                    data: [450, 420, 380, 350],
                    backgroundColor: '#667eea',
                    borderColor: '#667eea',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: true
                    }
                }
            }
        });
    }

    initReadinessChart() {
        const ctx = document.getElementById('readinessChart');
        if (!ctx) return;

        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Ready', 'Developing', 'Not Ready'],
                datasets: [{
                    data: [65, 25, 10],
                    backgroundColor: ['#10b981', '#f59e0b', '#ef4444'],
                    borderColor: '#fff',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }
}

// Initialize charts when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    if (typeof Chart !== 'undefined') {
        new ChartManager();
    }
});
