// Update navbar active item
document.getElementById("forex").classList.add("active");
document.getElementById("dashboard").classList.remove("active");

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

// API KEY
var apikey = "JLXK7AOR79EQNKJ5";
// EXECUTING FUNCTION
// chart_data = getDolarData(apikey);

addEventListener("DOMContentLoaded", (e) => {
  $.ajax({
    url:
      "https://www.alphavantage.co/query?function=FX_DAILY&from_symbol=USD&to_symbol=BRL&apikey=" +
      apikey,
    type: "GET",
    // data: { value: e.target.value },
    success: function (data) {
      let obj = data["Time Series FX (Daily)"];
      var array_labels = [];
      var array_dataset = [];
      for (arg in obj) {
        let data = arg.toString();
        array_labels.push(data);
        array_dataset.push(parseFloat(obj[arg]["4. close"]));
      }
      // createChartvalues(array_labels.reverse(), array_dataset.reverse());
      supplyDataForex(array_labels, array_dataset);
      buildPercentChart(array_labels, array_dataset);
      createrowData(array_labels, array_dataset);
    },
    fail: function (data) {
      console.log("FAIL");
    },
  });
});

function createrowData(labels, dataset) {
  var total_profit = [];

  for (var i = 0; i < dataset.length - 1; i++) {
    var prof = Math.round((dataset[i] / dataset[i + 1] - 1) * 10000) / 100;

    total_profit.push(prof);
  }
  total_profit[total_profit.length] = "Sem Informação";

  for (var i = 0; i < dataset.length; i++) {
    let iconClass;
    let changeClass;
    if (total_profit[i] > 0) {
      iconClass = "fas fa-arrow-up";
      changeClass = "positive-change";
    } else {
      iconClass = "fas fa-arrow-down";
      changeClass = "negative-change";
    }
    $("#dataTable > tbody:last-child").append(`
        <tr id="wallet-table-total">
          <td scope="col"><b>${labels[i]}</b></td>
          <td scope="row"><b>R$ ${dataset[i]}</b></td>
          <td scope="row"><span class="${changeClass}"><i class="${iconClass}"></i> <b>${total_profit[i]}%</b></span></td>
        </tr>
      `);
  }
}

function supplyDataForex(labs, data) {
  var newData = [];
  for (i = labs.length - 1; i > -1; i--) {
    newData.push({
      x: labs[i],
      y: data[i],
    });
  }
  forexChart.updateSeries([{ data: newData }]);
}

var options = {
  series: [
    {
      name: "USD - BRL",
      data: [],
    },
  ],
  chart: {
    type: "area",
    stacked: false,
    height: 350,
    zoom: {
      type: "x",
      enabled: true,
      autoScaleYaxis: true,
    },
    toolbar: {
      autoSelected: "zoom",
    },
  },
  dataLabels: {
    enabled: false,
  },
  markers: {
    size: 0,
  },
  title: {
    text: "Stock Price Movement",
    align: "left",
  },
  fill: {
    type: "gradient",
    gradient: {
      shadeIntensity: 1,
      inverseColors: false,
      opacityFrom: 0.5,
      opacityTo: 0,
    },
  },
  responsive: default_responsive,
};

var forexChart = new ApexCharts(document.querySelector("#forexChart"), options);
forexChart.render();

// Percent Chart
function buildPercentChart(labs, dataset) {
  var variance = [];

  for (var i = 0; i < dataset.length - 1; i++) {
    var prof = Math.round((dataset[i] / dataset[i + 1] - 1) * 10000) / 100;

    variance.push(prof);
  }
  variance[variance.length] = null;
  let arr = [[], []];
  for (i = variance.length - 1; i > -1; i--) {
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
  responsive: [
    {
      breakpoint: 800,
      options: {
        legend: {
          position: "top",
        },
        chart: {
          height: 700,
        },
        yaxis: {
          show: false,
        },
        xaxis: {
          labels: {
            show: false,
          },
        },
        plotOptions: {
          bar: {
            horizontal: true,
          },
        },
      },
    },
  ],
};

var percentChart = new ApexCharts(
  document.querySelector("#forexChartpercent"),
  optionsPercent
);
percentChart.render();
