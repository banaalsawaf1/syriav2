class ProjectChartFactory {
    static createChart(type, data, containerId) {
        switch(type) {
            case 'cost':
                return this.createCostChart(data, containerId);
            case 'area':
                return this.createAreaChart(data, containerId);
            case 'duration':
                return this.createDurationChart(data, containerId);
            default:
                return null;
        }
    }
    
    static createCostChart(costData, containerId) {
        return new Chart(document.getElementById(containerId), {
            type: 'pie',
            data: {
                labels: ['الميزانية', 'المصروف'],
                datasets: [{
                    data: [costData, costData * 0.3],
                    backgroundColor: ['#2b6b42', '#3a8a57'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                        rtl: true
                    }
                }
            }
        });
    }
    
    static createAreaChart(areaData, containerId) {
        var trace = {
            x: ['المساحة'],
            y: [areaData],
            type: 'bar',
            marker: {
                color: '#2b6b42'
            }
        };
        
        var layout = {
            title: 'المساحة بالمتر المربع',
            font: {
                family: 'Cairo'
            }
        };
        
        return Plotly.newPlot(containerId, [trace], layout);
    }
    
    static createDurationChart(durationData, containerId) {
        
    }
}