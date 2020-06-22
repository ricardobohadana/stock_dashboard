// Update navbar active item
document.getElementById("query").classList.add("active");
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

// Ajax Call - CHANGE CHART RANGE
document.querySelector("select").addEventListener("change", (e) => {
  var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    },
  });
  $.ajax({
    url: query_url,
    type: "POST",
    dataType: "json",
    data: {
      range: e.target.value,
      symbol: $("h4.card-title#stock").contents().text().trim(),
    },
    success: function (json) {
      chart.updateSeries([
        {
          data: supplyData(json.labs, json.sma15, false),
          type: "line",
          name: "SMA 10",
        },
        {
          data: supplyData(json.labs, json.stock, true),
          name: "Preço",
          type: "candlestick",
        },
      ]);
      percentChart.updateSeries([
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

function updateInfos(data) {
  for (i = data.labs.length - 1; i > -1; i--) {
    let color;
    let icon;
    if (data.variance[i] > 0) {
      color = "positive-change";
      icon = "fa-arrow-up";
    } else {
      color = "negative-change";
      icon = "fa-arrow-down";
    }
    var row = `
    <tr>
      <td>${data.labs[i]}</td>
      <td><b>${data.stock[3][i].toLocaleString("pt-BR", {
        style: "currency",
        currency: "BRL",
      })}</b></td>
      <td class="${color}"><i class="fas ${icon}"></i>${data.variance[i]} %</td>
    </tr>
    `;
    $(row)
      .hide()
      .appendTo("table#dataTable.table > tbody:last-child")
      .fadeIn("slow");
  }
  $("h4.card-title#stock").append(`${data.symbol}`);
}

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

function supplyData(labs, stock, multiple) {
  let data = [];
  for (i = 0; i < labs.length; i++) {
    date = labs[i];
    if (multiple) {
      data.push({
        x: date,
        y: [stock[0][i], stock[1][i], stock[2][i], stock[3][i]],
      });
    } else {
      data.push({
        x: date,
        y: stock[i],
      });
    }
  }
  return data;
}

// Create Chart Percent objects
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

// Stock Percent Chart
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
    animations: {
      enabled: true,
      easing: "easeinout",
      speed: 800,
      animateGradually: {
        enabled: true,
        delay: 150,
      },
      dynamicAnimation: {
        enabled: true,
        speed: 350,
      },
    },
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

// Stock chart
var options = {
  series: [
    {
      data: [],
      type: "line",
      name: "EMA 10",
    },
    {
      data: [],
      name: "Preço",
      type: "candlestick",
    },
  ],
  chart: {
    type: "line",
    animations: {
      enabled: true,
      easing: "easeinout",
      speed: 800,
      animateGradually: {
        enabled: true,
        delay: 150,
      },
      dynamicAnimation: {
        enabled: true,
        speed: 350,
      },
    },
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

var chart = new ApexCharts(document.querySelector("#stockChart"), options);
chart.render();

// Ajax Call - GET INFOS
$("#query-form").submit((e) => {
  e.preventDefault();
  var loadingBar = $("div.loading-bar");
  if (loadingBar.contents()) {
    loadingBar.contents().remove();
  }
  if ($("table#dataTable.table tbody").contents() != "") {
    $("table#dataTable.table tbody").contents().remove();
  }
  if ($("h4.card-title#stock").contents() != "") {
    $("h4.card-title#stock").contents().remove();
  }
  var loading = `
  <div class="d-flex justify-content-center">
    <div class="spinner-border" role="status">
      <span class="sr-only">Loading...</span>
    </div>
  </div>`;
  var stock_symbol = $("#stock-symbol").val().toUpperCase();
  $(loading).hide().appendTo(loadingBar).fadeIn("slow");
  if (stock_symbol) {
    // Create Ajax Call
    $.ajax({
      url: query_url,
      data: {
        action: "query",
        data: stock_symbol,
      },
      dataType: "json",
      xhrFields: {
        onprogress: function (e) {
          if (e.lengthComputable) {
            console.log((e.loaded / e.total) * 100 + "%");
          }
        },
      },
      success: function (data) {
        if (data) {
          updateInfos(data);
          buildPercentChart(data.labs, data.variance);
          // creating chart
          chart.updateOptions({
            title: {
              text: data.symbol,
            },
          });
          chart.updateSeries([
            {
              data: supplyData(data.labs, data.sma15, false),
              type: "line",
              name: "EMA 10",
            },
            {
              data: supplyData(data.labs, data.stock, true),
              name: "Preço",
              type: "candlestick",
            },
          ]);
        }
        document.querySelector("div.loading-bar").style.display = "none";
      },
      error: () => {
        $("div.spinner-border").remove();
        document.querySelector(
          "div.d-flex.justify-content-center"
        ).style.display = "none";
        $("div.loading-bar").append(
          `<div class="d-flex justify-content-center">
            <h4>Desculpe, mas não foi possível completar sua consulta<h4>
          </div>`
        );
      },
    });
  } else {
    alert("All fields must have a valid value.");
  }
  $("form#query").trigger("reset");
});
