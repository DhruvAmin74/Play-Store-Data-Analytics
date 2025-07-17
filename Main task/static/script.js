document.addEventListener('DOMContentLoaded', function () {
    // Get current IST time
    function getISTTime() {
        const now = new Date();
        const ISTOffset = 330; // IST is UTC+5:30
        return new Date(now.getTime() + (ISTOffset + now.getTimezoneOffset()) * 60000);
    }

    // Time check for Choropleth (6 PM - 8 PM IST)
    function isChoroplethTime() {
        const istTime = getISTTime();
        const hour = istTime.getHours();
        return hour >= 18 && hour < 20;
    }

    // Time check for Timeseries (6 PM - 9 PM IST)
    function isTimeseriesTime() {
        const istTime = getISTTime();
        const hour = istTime.getHours();
        return hour >= 18 && hour < 21;
    }

    function toggleGraphs() {
        const choroplethSection = document.getElementById('choropleth');
        const choroplethMessage = document.getElementById('choropleth-msg');

        const timeseriesSection = document.getElementById('timeseries');
        const timeseriesMessage = document.getElementById('timeseries-msg');

        // Handle Choropleth
        if (isChoroplethTime()) {
            choroplethSection.style.display = 'block';
            choroplethMessage.style.display = 'none';
        } else {
            choroplethSection.style.display = 'none';
            choroplethMessage.style.display = 'block';
        }

        // Handle Timeseries
        if (isTimeseriesTime()) {
            timeseriesSection.style.display = 'block';
            timeseriesMessage.style.display = 'none';
        } else {
            timeseriesSection.style.display = 'none';
            timeseriesMessage.style.display = 'block';
        }
    }

    toggleGraphs();
    setInterval(toggleGraphs, 60000);
});
