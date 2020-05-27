// Update navbar active item
document.getElementById("forex").classList.add("active");
document.getElementById("dashboard").classList.remove("active");

// API KEY
var apikey = "JLXK7AOR79EQNKJ5";
// EXECUTING FUNCTION
// chart_data = getDolarData(apikey);

addEventListener("DOMContentLoaded", (e) => {
  $.ajax({
    url:
      "https://www.alphavantage.co/query?function=FX_DAILY&from_symbol=USD&to_symbol=BRL&apikey=demo" +
      apikey,
    type: "GET",
    // data: { value: e.target.value },
    success: function (data) {
      let obj = data["Time Series FX (Daily)"];
      var array_labels = [];
      var array_dataset = [];
      for (arg in obj) {
        array_labels.push(arg.toString());
        array_dataset.push(parseFloat(obj[arg]["4. close"]));
      }
      createChartvalues(array_labels.reverse(), array_dataset.reverse());
      createrowData(array_labels, array_dataset);
    },
    fail: function (data) {
      console.log("FAIL");
    },
  });
});

function createChartvalues(label, dataset) {
  // CREATING CHART
  var ctx = document.getElementById("forexChart").getContext("2d");
  var chart = new Chart(ctx, {
    // The type of chart we want to create
    type: "line",

    // The data for our dataset
    data: {
      labels: label,
      datasets: [
        {
          label: "BRL - USD",
          borderColor: "rgb(187,93,10)",
          backgroundColor: "rgb(187,93,10)",
          pointBackgroundColor: "rgb(187,93,10)",
          pointHoverRadius: 5,
          data: dataset,
          fill: false,
        },
      ],
    },

    // Configuration options go here
    options: {
      responsive: true,
      maintainAspectRatio: false,
    },
  });
}
function createChartpercent(label, dataset) {
  var positive = [null];
  var negative = [null];
  for (var i = 1; i < dataset.length; i++) {
    if (dataset[i] > 0) {
      positive.push(dataset[i]);
      negative.push(null);
    } else {
      positive.push(null);
      negative.push(dataset[i]);
    }
  }
  // CREATING CHART
  var ctx = document.getElementById("forexChartpercent").getContext("2d");
  var chart = new Chart(ctx, {
    // The type of chart we want to create
    type: "bar",

    // The data for our dataset
    data: {
      labels: label,
      datasets: [
        {
          label: "BRL - USD neg",
          borderColor: "rgb(235,57,57)",
          backgroundColor: "rgb(235,57,57)",
          pointBackgroundColor: "rgb(235,57,57)",
          pointHoverRadius: 5,
          data: negative,
          fill: false,
        },
        {
          label: "BRL - USD pos",
          borderColor: "rgb(0,153,0)",
          backgroundColor: "rgb(0,153,0)",
          pointBackgroundColor: "rgb(0,153,0)",
          pointHoverRadius: 5,
          data: positive,
          fill: false,
        },
      ],
    },

    // Configuration options go here
    options: {
      responsive: true,
      maintainAspectRatio: false,
    },
  });
}

function createrowData(labels, dataset) {
  var total_profit = ["Sem Informação"];

  for (var i = 1; i < dataset.length; i++) {
    var prof = Math.round((dataset[i] / dataset[i - 1] - 1) * 10000) / 100;

    total_profit.push(prof);
  }
  for (var i = dataset.length - 1; i > -1; i--) {
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
  total_profit[0] = null;
  createChartpercent(labels, total_profit);
}
