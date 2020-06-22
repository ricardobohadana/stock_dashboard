var landingPage = document.querySelector(".landing-page");
var default_responsive = [
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
setTimeout(function () {
  landingPage.style.display = "none";
}, 3500);

var symbols = JSON.parse(document.getElementById("symbols").textContent);
var favorites = JSON.parse(document.getElementById("favorites").textContent);
function appendStocktoCard(stock) {
  let price = stock.price.toLocaleString("pt-BR", {
    style: "currency",
    currency: "BRL",
  });
  var favIcon = "fa-star";
  let cpClass;
  let iconClass;
  let priceChange = ((stock.change_percent / 100) * stock.price).toLocaleString(
    "pt-BR",
    {
      style: "currency",
      currency: "BRL",
    }
  );

  if (stock.change_percent > 0) {
    cpClass = "badge-success";
  } else {
    cpClass = "badge-danger";
  }
  if (!stock.favorite) {
    var data = `
    <div class="list-group-item list-group-item-action waves-effect d-flex justify-content-between">
      <a onclick="mx-1 ajaxFavUpdater(this)"  role="button" data-id="${stock.pk}">
        <i class="far ${favIcon}" id="favid-${stock.pk}"></i>
      </a>
      <a class="mx-1 text-dark" href="/detailedstock/${stock.pk}">${stock.symbol}</a>
      <span class="mx-1 text-dark">${price}</span>      
      <span class="mx-1 badge badge-pill ${cpClass}">${stock.change_percent} %</span>
      
      <a class="mx-1 btn-sm btn-link" href="/removestock/${stock.pk}"><i class="fas fa-times"></i></a>
      
    </div>
    `;
    $(data).hide().appendTo(".stock-list").fadeIn("slow");
  } else {
    var data = `
    <div class="col-xl-3 col-lg-4 mb-2">
    <div class="card">
      <div class="card-header">
        <div class="d-flex justify-content-between">
          <div class="card-title"><h4>${stock.symbol}</h4></div>
          <div class="card-title d-flex"><h4>${price}<span class="badge badge-pill ml-2 ${cpClass}">${stock.change_percent} %</span></h4></div>
        </div>
        <div class="d-flex justify-content-between">
          <div>
            <p>Média (14)</p>
          </div>
          <div>
            <p class="">
              ${stock.SMA_14}
            </p>
          </div>
        </div>
        <div class="d-flex justify-content-between">
          <div>
            <p>Média (30)</p>
          </div>
          <div>
            <p class="">
              ${stock.SMA_30}
            </p>
          </div>
        </div>
        <div class="d-flex justify-content-between">
          <div>
          <a href="/detailedstock/${stock.pk}" role="button" class="btn-link"><i class="fas fa-chart-area"></i></a>
          </div>
          <div>
            <a onclick="ajaxFavUpdater(this)" role="button" data-id="${stock.pk}">
              <i class="fas ${favIcon}" id="favid-${stock.pk}"></i>
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
    `;
    $(data).hide().appendTo("#favs-row").fadeIn("slow");
  }
}

function ajaxFavUpdater(e) {
  // Get CSRFTOKEN for 'POST' requests and set it up with all ajax calls
  let csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
  let id = e.getAttribute("data-id");
  $.ajax({
    url: home_url,
    method: "GET",
    data: {
      action: "update_favorites",
      data: id,
    },
    dataType: "json",
    success: (response) => {
      if (response) {
        if (response.fav) {
          console.log("Favoritado");
          $(`#favid-${id}`).removeClass("far");
          $(`#favid-${id}`).addClass("fas");
        } else {
          $(`#favid-${id}`).addClass("far");
          $(`#favid-${id}`).removeClass("fas");
          console.log("Desfavoritado");
        }
      }
    },
  });
}
document.addEventListener("DOMContentLoaded", function () {
  ajaxStockWrapper();
});

function ajaxStockWrapper() {
  var labs = [];
  var variance = [];
  var status = [];
  for (i = 0; i < symbols.length; i++) {
    ajaxStockUpdater(i, labs, variance, status);
  }
  $.when.apply(null, status).done(() => {
    console.log("Building percent chart");
    buildPercentChart(labs, variance);
  });
}

function ajaxStockUpdater(i, labs, variance, status) {
  var request = $.ajax({
    url: home_url,
    data: {
      action: "update_stocks",
      data: symbols[i],
    },
    xhrFields: {
      onprogress: function (e) {
        if (e.lengthComputable) {
          console.log((e.loaded / e.total) * 100 + "%");
        }
      },
    },
    dataType: "json",
    success: (response) => {
      if (response) {
        appendStocktoCard(response);
        appendStocktoChart(response);
        variance.push(response.change_percent);
        labs.push(response.symbol);
      }
    },
  });
  status.push(request);
}

// Pie Chart
function appendStocktoChart(stock) {
  let arr = pieChart.w.globals.series;
  if (stock.change_percent > 0) {
    arr[0] = arr[0] + 1;
  } else {
    arr[1] = arr[1] + 1;
  }
  pieChart.updateSeries(arr);
}

var optionsPie = {
  series: [0, 0],
  chart: {
    width: 350,
    type: "pie",
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
  labels: ["Ativos subindo", "Ativos caindo"],
  colors: ["#00B746", "#EF403C"],
  stroke: {
    width: 4,
  },
  dataLabels: {
    enabled: false,
  },
  legend: {
    position: "bottom",
  },
  responsive: [
    {
      breakpoint: 480,
      options: {
        chart: {
          width: 300,
        },
        legend: {
          position: "bottom",
        },
      },
    },
  ],
};

var pieChart = new ApexCharts(
  document.querySelector("#stockChartPie"),
  optionsPie
);
pieChart.render();

// Variation Chart

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
