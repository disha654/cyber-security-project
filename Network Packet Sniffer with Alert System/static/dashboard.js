const socket = io();
const ctx = document.getElementById('trafficChart').getContext('2d');

let totalPackets = 0;
let totalAlerts = 0;
let packetsInLastSecond = 0;

// Initialize Chart
const trafficChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Packets per Second',
            data: [],
            borderColor: '#00bcd4',
            tension: 0.4,
            fill: true,
            backgroundColor: 'rgba(0, 188, 212, 0.1)'
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: { beginAtZero: true, grid: { color: '#333' } },
            x: { grid: { display: false } }
        },
        plugins: {
            legend: { display: false }
        }
    }
});

// Update Stats from API periodically
async function updateStats() {
    const response = await fetch('/api/stats');
    const data = await response.json();
    totalPackets = data.total_packets;
    totalAlerts = data.total_alerts;
    document.getElementById('total-packets').innerText = totalPackets.toLocaleString();
    document.getElementById('total-alerts').innerText = totalAlerts.toLocaleString();
}

// Socket Events
socket.on('new_packet', (data) => {
    packetsInLastSecond++;
    totalPackets++;
    document.getElementById('total-packets').innerText = totalPackets.toLocaleString();

    // Add to table
    const table = document.getElementById('packet-table').getElementsByTagName('tbody')[0];
    const row = table.insertRow(0);
    row.innerHTML = `
        <td>${data.timestamp}</td>
        <td><span class="badge ${data.protocol.toLowerCase()}">${data.protocol}</span></td>
        <td>${data.src_ip}</td>
        <td>${data.dst_ip}</td>
        <td>${data.dst_port}</td>
        <td>${data.length}</td>
    `;
    
    if (table.rows.length > 50) table.deleteRow(50);
});

socket.on('new_alert', (data) => {
    totalAlerts++;
    document.getElementById('total-alerts').innerText = totalAlerts.toLocaleString();

    // Add to alert list
    const alertList = document.getElementById('alert-list');
    const div = document.createElement('div');
    div.className = 'alert-item';
    div.innerHTML = `
        <span class="time">${data.timestamp}</span>
        <span class="title">${data.alert_type}</span>
        <span class="desc">${data.description} (Source: ${data.src_ip})</span>
    `;
    alertList.prepend(div);
});

// Update Chart every second
setInterval(() => {
    const now = new Date().toLocaleTimeString();
    
    trafficChart.data.labels.push(now);
    trafficChart.data.datasets[0].data.push(packetsInLastSecond);
    
    if (trafficChart.data.labels.length > 20) {
        trafficChart.data.labels.shift();
        trafficChart.data.datasets[0].data.shift();
    }
    
    trafficChart.update();
    
    document.getElementById('current-pps').innerText = packetsInLastSecond + " pps";
    packetsInLastSecond = 0;
}, 1000);

// Initial stats load
updateStats();
setInterval(updateStats, 5000);
