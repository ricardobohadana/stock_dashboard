// pegando as variáveis do views.py get_historicalData()
var variance = JSON.parse(document.getElementById("variance").textContent);
var labs = JSON.parse(document.getElementById("labs").textContent);
var stock = JSON.parse(document.getElementById("stock").textContent);
var sma15 = JSON.parse(document.getElementById("sma15").textContent);
var sma30 = JSON.parse(document.getElementById("sma30").textContent);
var sma60 = JSON.parse(document.getElementById("sma60").textContent);
var symbol = JSON.parse(document.getElementById("symbol").textContent);
var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
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
      return `<div class="card">Média: ${mean}</div>`;
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
  ],
};

$.ajaxSetup({
  beforeSend: function (xhr, settings) {
    xhr.setRequestHeader("X-CSRFToken", csrftoken);
  },
});

document.querySelector("select").addEventListener("change", (e) => {
  $.ajax({
    url: detailed_url,
    type: "POST",
    data: { value: e.target.value },
    success: function (json) {
      chart.updateSeries([
        {
          data: supplyData(json.labs, json.sma15, false),
          type: "line",
          name: "SMA 14",
        },
        {
          data: supplyData(json.labs, json.stock, true),
          name: "Preço",
          type: "candlestick",
        },
      ]);
      chart2.updateSeries([
        {
          name: "Variação Positiva",
          data: splitVariance(json.variance)[0],
        },
        {
          name: "Variação Negativa",
          data: splitVariance(json.variance)[1],
        },
      ]);
    },
    fail: function (data) {
      console.log("FAIL");
    },
  });
});

// Create Chart Percent objects

function splitVariance(labs, variance) {
  let date0 = new Date(labs[0]).toDateString().substring(4, 10);
  var positive = [
    {
      x: date0,
      y: null,
    },
  ];
  var negative = [
    {
      x: date0,
      y: null,
    },
  ];
  for (var i = 1; i < variance.length; i++) {
    let date = new Date(labs[i]).toDateString().substring(4, 10);
    if (variance[i] > 0) {
      positive.push({
        x: date,
        y: variance[i],
      });
      negative.push({
        x: date,
        y: null,
      });
    } else {
      negative.push({
        x: date,
        y: variance[i],
      });
      positive.push({
        x: date,
        y: null,
      });
    }
  }
  return [positive, negative];
}

function supplyData(labs, stock, multiple) {
  let data = [];
  for (i = 0; i < labs.length; i++) {
    date = new Date(labs[i]);
    if (multiple) {
      data.push({
        x: date.toDateString().substring(4, 10),
        y: [stock[0][i], stock[1][i], stock[2][i], stock[3][i]],
      });
    } else {
      data.push({
        x: date.toDateString().substring(4, 10),
        y: stock[i],
      });
    }
  }
  return data;
}

var options = {
  series: [
    {
      data: supplyData(labs, sma15, false),
      type: "line",
      name: "SMA 14",
    },
    {
      data: supplyData(labs, stock, true),
      name: "Preço",
      type: "candlestick",
    },
  ],
  chart: {
    type: "line",
  },
  title: {
    text: symbol,
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

var chart = new ApexCharts(document.querySelector("#stockChart"), options);
chart.render();

var options2 = {
  series: [
    {
      name: "Variação Positiva",
      data: splitVariance(labs, variance)[0],
    },
    {
      name: "Variação Negativa",
      data: splitVariance(labs, variance)[1],
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
      text: "Variação",
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
    text: "Variação por dia",
  },
  responsive: default_responsive,
};

var chart2 = new ApexCharts(
  document.querySelector("#stockChartpercent"),
  options2
);
chart2.render();
