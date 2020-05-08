// pegando as variáveis do views.py get_historicalData()
var labs = JSON.parse(document.getElementById("labs").textContent);
var stock = JSON.parse(document.getElementById("stock").textContent);
var sma15 = JSON.parse(document.getElementById("sma15").textContent);
var sma30 = JSON.parse(document.getElementById("sma30").textContent);
var sma60 = JSON.parse(document.getElementById("sma60").textContent);
var symbol = JSON.parse(document.getElementById("symbol").textContent);

var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();

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
      chart.data.labels = json.labs;
      chart.data.datasets[3].data = json.stock;
      chart.data.datasets[0].data = json.sma15;
      chart.data.datasets[1].data = json.sma30;
      chart.data.datasets[2].data = json.sma60;
      chart.update();
    },
    fail: function (data) {
      console.log("FAIL");
    },
  });
});

// Inicializando o elemnto <select>
document.addEventListener("DOMContentLoaded", function () {
  var elemens = document.querySelectorAll("select");
  var instances = M.FormSelect.init(elemens);
});

// criando o gráfico
var ctx = document.getElementById("stockChart").getContext("2d");
var chart = new Chart(ctx, {
  // The type of chart we want to create
  type: "line",

  // The data for our dataset
  data: {
    labels: labs,
    datasets: [
      {
        label: "SMA 14 days",
        borderColor: "rgb(187,93,10)",
        backgroundColor: "rgb(187,93,10)",
        pointBackgroundColor: "rgb(187,93,10)",
        pointHoverRadius: 5,
        data: sma15,
        fill: false,
      },
      {
        label: "SMA 30 days",
        borderColor: "rgb(228, 203, 116)",
        backgroundColor: "rgb(228, 203, 116)",
        pointBackgroundColor: "rgb(228, 203, 116)",
        data: sma30,
        fill: false,
      },
      {
        label: "SMA 7 days",
        borderColor: "rgb(143, 249, 236)",
        backgroundColor: "rgb(143, 249, 236)",
        pointBackgroundColor: "rgb(143, 249, 236)",
        data: sma60,
        fill: false,
      },
      {
        label: symbol,
        backgroundColor: "rgb(162,162,162)",
        borderColor: "rgb(51, 51, 51)",
        pointBackgroundColor: "rgb(162,162,162)",
        data: stock,
      },
    ],
  },

  // Configuration options go here
  options: {},
});
