document.addEventListener('DOMContentLoaded', function() {
    const dataElem = document.getElementById('dashboard-data');
    if (!dataElem) return;

    let dashboardData;
    try {
        dashboardData = JSON.parse(dataElem.textContent);
    } catch (e) {
        console.error('Ошибка парсинга данных дэшборда:', e);
        return;
    }

    // Линейный график
    const lineCtx = document.getElementById('lineChart').getContext('2d');
    new Chart(lineCtx, {
        type: 'line',
        data: {
            labels: dashboardData.days,
            datasets: [{
                label: 'Количество аукционов',
                data: dashboardData.auctionsCounts,
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                fill: true,
                tension: 0.2,
                pointRadius: 4,
                pointHoverRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: {
                        font: { size: 14 }
                    }
                }
            },
            layout: {
                padding: 10
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Дата'
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Количество'
                    }
                }
            }
        }
    });

    // Круговая диаграмма с добавлением данных для "На изменении"
    const pieCtx = document.getElementById('pieChart').getContext('2d');
    new Chart(pieCtx, {
        type: 'pie',
        data: {
            labels: [
                'Подтвержденные', 
                'Ожидающие', 
                'Отклонённые', 
                'Завершённые', 
                'На изменении'
            ],
            datasets: [{
                data: [
                    dashboardData.statusData.approved,
                    dashboardData.statusData.pending,
                    dashboardData.statusData.rejected,
                    dashboardData.statusData.completed,
                    dashboardData.statusData.change_requested
                ],
                backgroundColor: [
                    'rgba(26, 255, 0, 0.7)',       // Подтвержденные
                    'rgba(255, 206, 86, 0.7)',       // Ожидающие
                    'rgba(255, 99, 132, 0.7)',       // Отклонённые
                    'rgba(75, 192, 192, 0.7)',       // Завершённые
                    'rgba(255, 159, 64, 0.7)'        // На изменении (желтый/оранжевый)
                ],
                borderColor: [
                    'rgb(26, 255, 0)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            aspectRatio: 1.5,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        font: { size: 14 }
                    }
                }
            },
            layout: {
                padding: 20
            }
        }
    });
});
