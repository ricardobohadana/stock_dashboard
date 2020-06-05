document.getElementById("ibovespa").classList.add("active");
document.getElementById("dashboard").classList.remove("active");

var ibov = JSON.parse(document.getElementById("ibov").textContent);
const default_responsive = [
  {
    breakpoint: 1000,
    options: {
      chart: {
        height: 400,
      },
      yaxis: {
        show: false,
      },
      xaxis: {
        labels: {
          show: false,
        },
      },
    },
  },
];

const default_tooltip = {
  shared: true,
  custom: [
    function ({ seriesIndex, dataPointIndex, w }) {
      var mean = w.globals.series[seriesIndex][dataPointIndex].toLocaleString(
        "pt-BR",
        {
          style: "currency",
          currency: "BRL",
        }
      );
      return `<div class="card">Média Simples: ${mean}</div>`;
    },
    function ({ seriesIndex, dataPointIndex, w }) {
      var o = w.globals.seriesCandleO[seriesIndex][
        dataPointIndex
      ].toLocaleString("pt-BR", {
        style: "currency",
        currency: "BRL",
      });
      var h = w.globals.seriesCandleH[seriesIndex][
        dataPointIndex
      ].toLocaleString("pt-BR", {
        style: "currency",
        currency: "BRL",
      });
      var l = w.globals.seriesCandleL[seriesIndex][
        dataPointIndex
      ].toLocaleString("pt-BR", {
        style: "currency",
        currency: "BRL",
      });
      var c = w.globals.seriesCandleC[seriesIndex][
        dataPointIndex
      ].toLocaleString("pt-BR", {
        style: "currency",
        currency: "BRL",
      });
      return `
      <div class="card">
        <div class="card-body text-center ">
          <span><strong>Close: ${c}</strong></span></br>
          <span>Open: ${o}</span></br>
          <span>High: ${h}</span></br>
          <span>Low: ${l}</span>
        </div>
      </div>
      `;
    },
    function ({ seriesIndex, dataPointIndex, w }) {
      var mean = w.globals.series[seriesIndex][dataPointIndex].toLocaleString(
        "pt-BR",
        {
          style: "currency",
          currency: "BRL",
        }
      );
      return `<div class="card">Média Exponencial: ${mean}</div>`;
    },
  ],
};

//On change - CHART RANGE
document.querySelector("select").addEventListener("change", (e) => {
  $.ajax({
    url: ibov_url,
    type: "GET",
    data: { value: e.target.value },
    success: function (json) {
      stockChart.updateSeries([
        {
          data: supplyDataIbov(json)[1],
          type: "line",
          name: "SMA 14",
        },
        {
          data: supplyDataIbov(json)[0],
          name: "Preço",
          type: "candlestick",
        },
        {
          data: supplyDataIbov(json)[2],
          type: "line",
          name: "EWMA",
        },
      ]);
      percentChart.updateSeries([
        {
          name: "Variação Positiva",
          data: splitVariance(json.Variance)[0],
        },
        {
          name: "Variação Negativa",
          data: splitVariance(json.Variance)[1],
        },
      ]);
    },
    fail: function (data) {
      console.log("FAIL");
    },
  });
});

document.addEventListener("DOMContentLoaded", () => {
  for (i = ibov.Close.length - 1; i > -1; i--) {
    let percentClass = "positive";
    let iconClass = "up";
    if (ibov.Variance[i] < 0) {
      percentClass = "negative";
      iconClass = "down";
    }
    let price = ibov.Close[i].toLocaleString("pt-BR", {
      style: "currency",
      currency: "BRL",
    });
    let date = new Date(ibov.labs[i]).toDateString().substring(4, 15);
    let data = `
    <tr>
      <td>${date}</td>
      <td class="">${price}</td>
      <td class="${percentClass}-change">${ibov.Variance[i]}% <i class="fas fa-arrow-${iconClass}"></i></td>
    </tr>
    `;
    $(data).hide().appendTo("table#dataTable > tbody:last-child").fadeIn(1500);
  }
  buildPercentChart(ibov.labs, ibov.Variance);
});

// Percent Chart
function buildPercentChart(labs, variance) {
  let arr = [[], []];
  for (i = 0; i < variance.length; i++) {
    if (variance[i] > 0) {
      arr[0].push({
        x: labs[i],
        y: variance[i],
      });
      arr[1].push({
        x: labs[i],
        y: null,
      });
    } else {
      arr[1].push({
        x: labs[i],
        y: variance[i],
      });
      arr[0].push({
        x: labs[i],
        y: null,
      });
    }
  }
  percentChart.updateSeries([{ data: arr[0] }, { data: arr[1] }]);
}

function splitVariance(variance) {
  var positive = [null];
  var negative = [null];
  for (var i = 1; i < variance.length; i++) {
    if (variance[i] > 0) {
      positive.push(variance[i]);
      negative.push(null);
    } else {
      positive.push(null);
      negative.push(variance[i]);
    }
  }
  return [positive, negative];
}

var optionsPercent = {
  series: [
    {
      name: "Variação Positiva",
      data: [],
    },
    {
      name: "Variação Negativa",
      data: [],
    },
  ],
  chart: {
    type: "bar",
    height: 440,
    stacked: true,
  },
  colors: ["#00B746", "#EF403C"],
  plotOptions: {
    bar: {
      horizontal: false,
      barHeight: "80%",
    },
  },
  dataLabels: {
    enabled: false,
  },
  stroke: {
    width: 1,
    colors: ["#fff"],
  },

  grid: {
    xaxis: {
      lines: {
        show: false,
      },
    },
  },
  yaxis: {
    // min: -20,
    // max: 20,
    title: {
      text: "Variação (%)",
    },
  },
  tooltip: {
    shared: false,
    x: {
      formatter: function (val) {
        return val;
      },
    },
    y: {
      formatter: function (val) {
        return Math.abs(val) + "%";
      },
    },
  },
  title: {
    text: "Resumo de desempenho",
  },
  responsive: default_responsive,
};

var percentChart = new ApexCharts(
  document.querySelector("#stockChartpercent"),
  optionsPercent
);
percentChart.render();

//Main Stock Chart
function supplyDataIbov(ibov) {
  let mainData = [];
  let smaData = [];
  let ewmaData = [];
  for (i = 0; i < ibov.labs.length; i++) {
    date = new Date(ibov.labs[i]).toDateString().substring(4, 10);
    mainData.push({
      x: date,
      y: [ibov.Open[i], ibov.High[i], ibov.Low[i], ibov.Close[i]],
    });
    smaData.push({
      x: date,
      y: ibov.sma10[i],
    });
    ewmaData.push({
      x: date,
      y: ibov.ewma[i],
    });
  }
  return [mainData, smaData, ewmaData];
}

var mainOptions = {
  series: [
    {
      data: supplyDataIbov(ibov)[1],
      type: "line",
      name: "SMA 14",
    },
    {
      data: supplyDataIbov(ibov)[0],
      name: "Preço",
      type: "candlestick",
    },
    {
      data: supplyDataIbov(ibov)[2],
      type: "line",
      name: "EWMA",
    },
  ],
  chart: {
    type: "line",
  },
  title: {
    text: "",
    align: "left",
  },
  stroke: {
    width: [3, 1],
  },
  yaxis: {
    tooltip: {
      enabled: true,
    },
  },
  tooltip: default_tooltip,
  responsive: default_responsive,
};

var stockChart = new ApexCharts(
  document.querySelector("#stockChart"),
  mainOptions
);
stockChart.render();
