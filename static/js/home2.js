//
var positiveStocks = 0;
var negativeStocks = 0;
var symbols = JSON.parse(document.getElementById("symbols").textContent);
var favorites = JSON.parse(document.getElementById("favorites").textContent);
var stocks_json = JSON.parse(
  document.getElementById("stocks_json").textContent
);

function appendStocktoCard(stock) {
  let price = stock.price.toLocaleString("pt-BR", {
    style: "currency",
    currency: "BRL",
  });
  var favIcon = "fa-star";
  let cpClass;
  let iconClass;
  if (stock.change_percent > 0) {
    cpClass = "positive-change";
    iconClass = "fa-arrow-up";
  } else {
    cpClass = "negative-change";
    iconClass = "fa-arrow-down";
  }
  if (!stock.favorite) {
    var data = `
    <tr>
      <td ><a onclick="ajaxFavUpdater(this)"  role="button" data-id="${stock.pk}">
      <i class="far ${favIcon}" id="favid-${stock.pk}"></i>
      </a></td>
      <td>
      ${stock.symbol}
      </td>
      <td>
        ${price}
      </td>
      <td>
      <span class="${cpClass}"> <i class="fas ${iconClass}"></i> ${stock.change_percent} %</span>
      </td>
      <td class="d-flex justify-content-end" style="width: fit-content;">
      <a class="btn-sm btn" href="/detailedstock/${stock.pk}"><i class="fas fa-chart-area"></i></a>
      <a class="btn-sm btn" href="/removestock/${stock.pk}"><i class="fas fa-times"></i></a>
      </td>
    </tr>
    `;
    $(data)
      .hide()
      .appendTo("table.table.favorites > tbody:last-child")
      .fadeIn("slow");
  } else {
    var data = `
    <div class="col-lg-3 mb-2">
    <div class="card">
      <div class="card-header">
        <div class="d-flex justify-content-between">
          <div class="card-title"><h4>${stock.symbol}</h4></div>
          <div class="card-title"><h4>${price}</h4></div>
        </div>
        <div class="d-flex justify-content-between">
          <div>
            <p>Variação</p>
          </div>
          <div>
            <p class="${cpClass}">
              <i class="fas ${iconClass}"></i> ${stock.change_percent}%
            </p>
          </div>
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
          <a href="/detailedstock/${stock.pk}" class="btn"><i class="fas fa-chart-area"></i></a>
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

function ajaxStockUpdater(i, positiveVar, negativeVar) {
  $.ajax({
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
        appendStocktoChart(response, positiveVar, negativeVar);
      }
    },
  });
}

function splitVariance(stock, positiveVar, negativeVar) {
  if (stock.change_percent > 0) {
    positiveVar.push(stock.change_percent);
    negativeVar.push(null);
  } else {
    negativeVar.push(stock.change_percent);
    positiveVar.push(null);
  }
}

function appendStocktoChart(stock, positiveVar, negativeVar) {
  splitVariance(stock, positiveVar, negativeVar);
  let len = positiveVar.length - 1;
  if (positiveVar[len]) {
    chart.data.datasets[0].data[0] = chart.data.datasets[0].data[0] + 1;
  } else {
    chart.data.datasets[0].data[1] = chart.data.datasets[0].data[1] + 1;
  }
  chart.update();
  chart2.data.datasets[0].data = positiveVar;
  chart2.data.datasets[1].data = negativeVar;
  chart2.update();
}
var ctx = document.getElementById("stockChartPie").getContext("2d");
var chart = new Chart(ctx, {
  // The type of chart we want to create
  type: "pie",

  // The data for our dataset
  data: {
    labels: ["Ações crescendo", "Ações caindo"],
    datasets: [
      {
        // borderColor: ["rgb(0,153,0)", "rgb(235,57,57)"],
        backgroundColor: ["rgb(0,153,0)", "rgb(235,57,57)"],
        data: [0, 0],
      },
    ],
  },
  options: {},
});
var ctx2 = document.getElementById("stockChartpercent").getContext("2d");
var chart2 = new Chart(ctx2, {
  // The type of chart we want to create
  type: "bar",

  // The data for our dataset
  data: {
    labels: symbols,
    datasets: [
      {
        label: "Variação positiva",
        borderColor: "rgb(0,153,0)",
        backgroundColor: "rgb(0,153,0)",
        pointBackgroundColor: "rgb(0,153,0)",
        pointHoverRadius: 5,
        data: [],
        fill: false,
      },
      {
        label: "Variação negativa",
        borderColor: "rgb(235,57,57)",
        backgroundColor: "rgb(235,57,57)",
        pointBackgroundColor: "rgb(235,57,57)",
        pointHoverRadius: 5,
        data: [],
        fill: false,
      },
    ],
    options: {
      responsive: true,
      maintainAspectRatio: false,
    },
  },

  // Configuration options go here
  options: {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      xAxes: [
        {
          scaleLabel: {
            display: true,
            labelString: "Ações",
            fontColor: "black",
          },
        },
      ],
      yAxes: [
        {
          scaleLabel: {
            display: true,
            labelString: "Porcentagem de Variação",
            fontColor: "black",
          },
        },
      ],
    },
  },
});

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
  var positiveVar = [];
  var negativeVar = [];
  for (i = 0; i < symbols.length; i++) {
    ajaxStockUpdater(i, positiveVar, negativeVar);
  }
}

// function ajaxFeaturedStocks(iterator) {
//   $.ajax({
//     url: home_url,
//     data: {
//       action: "update_features",
//       data: "",
//     },
//     dataType: "json",
//     success: (response) => {
//       if (response) {
//         ajaxFeaturedStocksWrapper(
//           response.highrel,
//           response.highabs,
//           response.lowrel,
//           response.lowabs
//         );
//       }
//     },
//   });
// }

// function ajaxFeaturedStocksWrapper(highrel, highabs, lowrel, lowabs) {
//   if (!isEmpty($("#relative-high tbody"))) {
//     $("#relative-high tbody").contents().remove();
//   }
//   if (!isEmpty($("#absolute-high tbody"))) {
//     $("#absolute-high tbody").contents().remove();
//   }
//   if (!isEmpty($("#absolute-low tbody"))) {
//     $("#absolute-low tbody").contents().remove();
//   }
//   if (!isEmpty($("#relative-low tbody"))) {
//     $("#relative-low tbody").contents().remove();
//   }
//   for (i = 1; i < 6; i++) {
//     appendFeaturedStocks(highrel, highabs, lowrel, lowabs, i);
//   }
// }
// function isEmpty(el) {
//   return !$.trim(el.html());
// }

// function appendFeaturedStocks(highrel, highabs, lowrel, lowabs, iterator) {
//   let colorH;
//   let colorN;
//   if (iterator % 2 == 0) {
//     colorH = `green darken-4`;
//     colorN = `red darken-4  `;
//   } else {
//     colorN = `red darken-2`;
//     colorH = `#2e7d32 green darken-2`;
//   }
//   $("#relative-high > tbody:last-child").append(`
//     <tr class="${colorH}">
//       <td>${highrel[i - 1].symbol}</td>
//       <td>R$ ${highrel[i - 1].price}</td>
//       <td>${highrel[i - 1].change_percent}%</td>
//     </tr>
//   `);

//   $("#absolute-high > tbody:last-child").append(`
//   <tr class="${colorH}">
//     <td>${highabs[i - 1].symbol}</td>
//     <td>R$ ${highabs[i - 1].price}</td>
//     <td>R$ ${highabs[i - 1].price_change}</td>
//   </tr>
//   `);

//   $("#relative-low > tbody:last-child").append(`
//     <tr class="${colorN}">
//       <td>${lowrel[i - 1].symbol}</td>
//       <td>R$ ${lowrel[i - 1].price}</td>
//       <td>${lowrel[i - 1].change_percent}%</td>
//     </tr>
//   `);

//   $("#absolute-low > tbody:last-child").append(`
//   <tr class="${colorN}">
//     <td>${lowabs[i - 1].symbol}</td>
//     <td>R$ ${lowabs[i - 1].price}</td>
//     <td>R$ ${lowabs[i - 1].price_change}</td>
//   </tr>
//   `);
// }
