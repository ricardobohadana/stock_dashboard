var symbols = JSON.parse(document.getElementById("symbols").textContent);
son = [
  "Janeiro",
  "Fevereiro",
  "Março",
  "Abril",
  "Maio",
  "Junho",
  "Julho",
  "Agosto",
  "Setembro",
  "Outubro",
  "Novembro",
  "Dezembro",
];

function appendStocktoCard(stock) {
  let date = new Date(stock.updated);
  $(`div#${stock.pk}`).contents().remove();
  let percent_div;
  let var_div;
  let stock_fav;
  if (stock.favorite) {
    stock_fav = `<div data-id="${stock.pk}" onclick="ajaxFavUpdater(this)" class="right"><i id="favid-${stock.pk}" class="fas fa-star fa-xs btn-flat yellow-text"></i></div>`;
  } else {
    stock_fav = `<div data-id="${stock.pk}" onclick="ajaxFavUpdater(this)" class="right"><i id="favid-${stock.pk}" class="far  fa-star fa-xs btn-flat yellow-text"></i></div>`;
  }
  if (stock.change_percent > 0) {
    percent_div = `<div id="removable" class="card green hoverable">`;
    var_div = `<span class=""> Variação: <span class="green "> <b>${stock.change_percent}%</b> <i class="fas fa-long-arrow-alt-up"></i></span></span>`;
  } else if (stock.change_percent < 0) {
    percent_div = `<div id="removable" class="card red hoverable">`;
    var_div = `<span class=""> Variação: <span class="red "> <b>${stock.change_percent}%</b> <i class="fas fa-long-arrow-alt-down"></i></span></span>`;
  } else {
    percent_div = `<div id="removable" class="card amber accent-4 hoverable">`;
    var_div = `<span class=""> Variação: <span class="amber accent-4 "> <b>${stock.change_percent}%</b> <i class="fas fa-minus"></i></span></span>`;
  }
  $(`div#${stock.pk}`).append(`
      ${percent_div}
        <div class="">
          <h4 class="center"><b>${stock.symbol}</b>${stock_fav}</h4>
        </div>
        <a class="grey-text text-darken-4" href="/detailedstock/${stock.pk}">
          <div class="card-content ${stock.pk}">
            <div class="row">
              <div class="col s12 l6 center-align">
                <span class="">Preço: <b>R$${stock.price}</b></span>
              </div> 
              <div class="col s12 l6 center-align">
                ${var_div}
              </div>
              <div class="col s12 l12 center-align">
                <span><span class="">Atualização: </span><span class=""><b>${date.toString()}</b></span></span>
              </div>
            </div>
          </div>
        </a>
      </div>
    `);
}

function ajaxStockUpdater(i) {
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
      }
    },
  });
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
  $.when(ajaxStockWrapper()).then(ajaxFeaturedStocks);
  document.getElementById("updateButton").addEventListener("click", () => {
    $.when(ajaxStockWrapper).then(ajaxFeaturedStocks);
  });
});

function ajaxStockWrapper() {
  for (i = 0; i < symbols.length; i++) {
    ajaxStockUpdater(i);
  }
}

function ajaxFeaturedStocks(iterator) {
  $.ajax({
    url: home_url,
    data: {
      action: "update_features",
      data: "",
    },
    dataType: "json",
    success: (response) => {
      if (response) {
        ajaxFeaturedStocksWrapper(
          response.highrel,
          response.highabs,
          response.lowrel,
          response.lowabs
        );
      }
    },
  });
}

function ajaxFeaturedStocksWrapper(highrel, highabs, lowrel, lowabs) {
  if (!isEmpty($("#relative-high tbody"))) {
    $("#relative-high tbody").contents().remove();
  }
  if (!isEmpty($("#absolute-high tbody"))) {
    $("#absolute-high tbody").contents().remove();
  }
  if (!isEmpty($("#absolute-low tbody"))) {
    $("#absolute-low tbody").contents().remove();
  }
  if (!isEmpty($("#relative-low tbody"))) {
    $("#relative-low tbody").contents().remove();
  }
  for (i = 1; i < 6; i++) {
    appendFeaturedStocks(highrel, highabs, lowrel, lowabs, i);
  }
}
function isEmpty(el) {
  return !$.trim(el.html());
}

function appendFeaturedStocks(highrel, highabs, lowrel, lowabs, iterator) {
  let colorH;
  let colorN;
  if (iterator % 2 == 0) {
    colorH = `green darken-4`;
    colorN = `red darken-4  `;
  } else {
    colorN = `red darken-2`;
    colorH = `#2e7d32 green darken-2`;
  }
  $("#relative-high > tbody:last-child").append(`
    <tr class="${colorH}">
      <td>${highrel[i - 1].symbol}</td>
      <td>R$ ${highrel[i - 1].price}</td>
      <td>${highrel[i - 1].change_percent}%</td>
    </tr>
  `);

  $("#absolute-high > tbody:last-child").append(`
  <tr class="${colorH}">
    <td>${highabs[i - 1].symbol}</td>
    <td>R$ ${highabs[i - 1].price}</td>
    <td>R$ ${highabs[i - 1].price_change}</td>
  </tr>
  `);

  $("#relative-low > tbody:last-child").append(`
    <tr class="${colorN}">
      <td>${lowrel[i - 1].symbol}</td>
      <td>R$ ${lowrel[i - 1].price}</td>
      <td>${lowrel[i - 1].change_percent}%</td>
    </tr>
  `);

  $("#absolute-low > tbody:last-child").append(`
  <tr class="${colorN}">
    <td>${lowabs[i - 1].symbol}</td>
    <td>R$ ${lowabs[i - 1].price}</td>
    <td>R$ ${lowabs[i - 1].price_change}</td>
  </tr>
  `);
}
