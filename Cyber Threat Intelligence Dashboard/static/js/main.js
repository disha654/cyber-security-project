document.addEventListener('DOMContentLoaded', () => {
    const lookupForm = document.getElementById('lookup-form');
    const resultsDiv = document.getElementById('results');
    const loadingDiv = document.getElementById('loading');

    if (lookupForm) {
        lookupForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const target = document.getElementById('target').value;
            
            // UI States
            loadingDiv.classList.remove('hidden');
            resultsDiv.classList.add('hidden');
            resultsDiv.innerHTML = '';

            try {
                const formData = new FormData();
                formData.append('target', target);

                const response = await fetch('/lookup', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();
                loadingDiv.classList.add('hidden');
                
                if (data.error) {
                    resultsDiv.innerHTML = `<p class="error">Error: ${data.error}</p>`;
                } else {
                    renderResults(data);
                }
                resultsDiv.classList.remove('hidden');
            } catch (err) {
                loadingDiv.classList.add('hidden');
                resultsDiv.innerHTML = `<p class="error">Failed to fetch data. Check server console.</p>`;
                resultsDiv.classList.remove('hidden');
            }
        });
    }

    function renderResults(data) {
        const vt = data.results.VirusTotal || {};
        const abuse = data.results.AbuseIPDB || {};

        let html = `<h3>Analysis for ${data.target} (${data.type})</h3>`;

        // VirusTotal Section
        html += `<div class="api-result">
            <h4>VirusTotal</h4>
            ${vt.error ? `<p class="text-danger">${vt.error}</p>` : `
                <p>Reputation: ${vt.reputation}</p>
                <div class="stats-grid">
                    <span class="risk-high">Malicious: ${vt.malicious_count}</span>
                    <span class="risk-low">Harmless: ${vt.harmless_count}</span>
                    <span>Suspicious: ${vt.suspicious_count}</span>
                </div>
                <p>Country: ${vt.country} | ASN: ${vt.asn} (${vt.as_owner})</p>
            `}
        </div>`;

        // AbuseIPDB Section
        if (data.type === 'IP') {
            html += `<div class="api-result">
                <h4>AbuseIPDB</h4>
                ${abuse.error ? `<p class="text-danger">${abuse.error}</p>` : `
                    <p>Abuse Confidence Score: <strong>${abuse.abuse_confidence_score}%</strong></p>
                    <p>Total Reports: ${abuse.total_reports}</p>
                    <p>Usage Type: ${abuse.usage_type}</p>
                    <p>Domain: ${abuse.domain}</p>
                `}
            </div>`;
        }

        resultsDiv.innerHTML = html;
    }

    // Initialize Charts
    if (window.metricsData && window.metricsData.type_counts && Object.keys(window.metricsData.type_counts).length > 0) {
        const ctx = document.getElementById('typeChart').getContext('2d');
        const typeCounts = window.metricsData.type_counts;
        
        const labels = Object.keys(typeCounts);
        const values = Object.values(typeCounts);
        
        document.getElementById('total-lookups').textContent = values.reduce((a, b) => a + b, 0);

        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: values,
                    backgroundColor: ['#1f6feb', '#8957e5', '#3fb950'],
                    borderColor: '#161b22',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { color: '#c9d1d9' }
                    }
                }
            }
        });
    } else if (document.getElementById('typeChart')) {
        document.getElementById('typeChart').parentElement.innerHTML = '<p style="text-align: center; color: var(--text-secondary);">No data yet. Perform a lookup to see metrics.</p>';
    }
});
