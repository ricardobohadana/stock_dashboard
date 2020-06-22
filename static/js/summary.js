//django variables
var apikey = "JLXK7AOR79EQNKJ5";
var stocks_all = JSON.parse(document.getElementById("stocks_all").textContent);
var amount_etf = JSON.parse(document.getElementById("amount_etf").textContent);
var amount_fund = JSON.parse(
  document.getElementById("amount_fund").textContent
);
var amount_stock = JSON.parse(
  document.getElementById("amount_stock").textContent
);
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
// sidenav events
$(document).ready(function () {
  document
    .getElementsByClassName("fa-bars")[0]
    .addEventListener("click", openSideNav);

  document
    .getElementsByClassName("fa-times")[0]
    .addEventListener("click", openSideNav);
});

// sidenav
function openSideNav() {
  // console.log("clicked");
  topnav = document.getElementsByClassName("navbar")[0];
  body = document.getElementsByTagName("body")[0];
  sidenav = document.getElementsByClassName("sidebar-fixed")[0];
  if (sidenav.style.left === "-270px") {
    sidenav.style.left = "0px";
    topnav.classList.add("ml-270");
    body.classList.add("ml-270");
  } else {
    sidenav.style.left = "-270px";
    topnav.classList.remove("ml-270");
    body.classList.remove("ml-270");
  }
}

const donutData = () => {
  let arrSeries = [];
  let arrLabels = [];
  for (i = 0; i < stocks_all.length; i++) {
    arrSeries.push(stocks_all[i][2]);
    arrLabels.push(stocks_all[i][1]);
  }
  return [arrSeries, arrLabels];
};

// donut chart - todas as ações
optionsDonut = {
  chart: {
    type: "donut",
    height: 420,
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
  // title: {
  //   text: "Participação de cada ",
  // },
  plotOptions: {
    pie: {
      donut: {
        labels: {
          show: true,
          name: {
            show: true,
            fontFamily: "Oswald",
          },
          value: {
            show: true,
            fontFamily: "Oswald",
            formatter: function (val) {
              let amount = parseFloat(val).toLocaleString("en-US", {
                style: "currency",
                currency: "BRL",
              });
              console.log(amount);
              return `${amount}`;
            },
          },
        },
      },
    },
  },
  legend: {
    show: true,
    position: "bottom",
  },
  colors: [
    "#2E93fA",
    "#66DA26",
    "#546E7A",
    "#E91E63",
    "#FF9800",
    "#00B746",
    "#EF403C",
    "#3D3D3D",
  ],
  dataLabels: {
    enabled: true,
    formatter: function (val) {
      return Math.round(val * 100, 2) / 100 + "%";
    },
  },
  series: donutData()[0],
  labels: donutData()[1],
  responsive: default_responsive,
};
var donutChart = new ApexCharts(
  document.querySelector("#donut-chart"),
  optionsDonut
);
donutChart.render();

// donut chart - etf, acoes, fii
optionsDonutDiv = {
  chart: {
    type: "donut",
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
  // title: {
  //   text: "Participação de cada ",
  // },
  plotOptions: {
    pie: {
      donut: {
        labels: {
          show: true,
          name: {
            show: true,
            fontFamily: "Oswald",
          },
          value: {
            show: true,
            fontFamily: "Oswald",
            formatter: function (val) {
              let amount = parseFloat(val).toLocaleString("en-US", {
                style: "currency",
                currency: "BRL",
              });
              console.log(amount);
              return `${amount}`;
            },
          },
        },
      },
    },
  },
  legend: {
    show: true,
    position: "bottom",
  },
  colors: [
    "#2E93fA",
    "#66DA26",
    "#546E7A",
    "#E91E63",
    "#FF9800",
    "#00B746",
    "#EF403C",
    "#3D3D3D",
  ],
  dataLabels: {
    enabled: true,
    formatter: function (val) {
      return Math.round(val * 100, 2) / 100 + "%";
    },
  },
  series: [amount_etf, amount_stock, amount_fund],
  labels: ["ETF", "Ações", "Fundos Imobiliários"],
  responsive: default_responsive,
};
var donutChartDiv = new ApexCharts(
  document.querySelector("#donut-chart-divisao"),
  optionsDonutDiv
);
donutChartDiv.render();
