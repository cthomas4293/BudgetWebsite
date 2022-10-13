'use strict';

const ctx = document.getElementById('balanceChart').getContext('2d');
const balanceChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Yellow', 'Green'],
        datasets: [{
            label: '# of Votes',
            data: [19, 3],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

const ctx2 = document.getElementById('expenseChart').getContext('2d');
const expenseChart = new Chart(ctx2, {
    type: 'bar',
    data: {
        labels: ['Red', 'Blue'],
        datasets: [{
            label: 'Expenses',
            data: [12, 19],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
            ],
            borderWidth: 1
        }]
    },
    options: {
        indexAxis: 'y',
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

const ctx3 = document.getElementById('incomeChart').getContext('2d');
const incomeChart = new Chart(ctx3, {
    type: 'bar',
    data: {
        labels: ['Red', 'Blue'],
        datasets: [{
            label: 'Income',
            data: [3, 5],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
            ],
            borderWidth: 1
        }]
    },
    options: {
        indexAxis: 'y',
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});