document.addEventListener("DOMContentLoaded", () => {
    const labelsElement = document.getElementById("cursos-labels");
    const valuesElement = document.getElementById("cursos-values");
    const chartContainer = document.querySelector("#alunosPorCursoChart");

    if (!labelsElement || !valuesElement || !chartContainer) {
        return;
    }

    const cursosLabels = JSON.parse(labelsElement.textContent);
    const cursosValues = JSON.parse(valuesElement.textContent);

    if (!Array.isArray(cursosLabels) || cursosLabels.length === 0) {
        return;
    }

    const chart = new ApexCharts(chartContainer, {
        chart: {
            type: "bar",
            height: 320,
            toolbar: { show: false },
            fontFamily: "inherit",
        },
        series: [
            {
                name: "Alunos",
                data: cursosValues,
            },
        ],
        xaxis: {
            categories: cursosLabels,
            labels: {
                style: { colors: "#6B7280", fontSize: "12px" },
            },
            axisBorder: { show: false },
            axisTicks: { show: false },
        },
        yaxis: {
            labels: {
                style: { colors: "#6B7280", fontSize: "12px" },
            },
        },
        grid: {
            borderColor: "#E5E7EB",
            strokeDashArray: 4,
            padding: { left: 12, right: 12 },
        },
        plotOptions: {
            bar: {
                borderRadius: 8,
                columnWidth: "45%",
            },
        },
        dataLabels: { enabled: false },
        colors: ["#2563EB"],
        tooltip: {
            y: {
                formatter: (value) => `${value} alunos`,
            },
        },
    });

    chart.render();
});
