var symbols = JSON.parse(document.getElementById("symbols").textContent);
function appendStocktoCard(stock) {
  let date = new Date(stock.updated);
  let hr = date.getHours();
  let min = date.getMinutes();
  let day = date.getDay();
  let mth = date.getMonth();
  let fulldate = `${day} de ${son[mth]} às ${hr}:${min}`;
  $(`a#${stock.pk}`).contents().remove();
  let percent_div;
  let var_div;
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
  $(`a#${stock.pk}`).append(`
      ${percent_div}
        <div class="">
          <h4 class="center"><b>${stock.symbol}</b></h4>
        </div>
        <div class="card-content ${stock.pk}">
          <div class="row">
            <div class="col s12 l6 center-align">
              <span class="">Preço: <b>R$${stock.price}</b></span>
            </div> 
            <div class="col s12 l6 center-align">
              ${var_div}
            </div>
            <div class="col s12 l12 center-align">
              <span><span class="">Atualização: </span><span class=""><b>${fulldate}</b></span></span>
            </div>
          </div>
        </div>
      </div>
    `);
}

function updateStocksAJAX(i, lengthoaded) {
  $.ajax({
    url: home_url,
    data: {
      stock_symbol: symbols[i],
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
document.addEventListener("DOMContentLoaded", function () {
  for (i = 0; i < symbols.length; i++) {
    updateStocksAJAX(i, symbols.length);
  }
});

son = {
  1: "Janeiro",
  2: "Fevereiro",
  3: "Março",
  4: "Abril",
  5: "Maio",
  6: "Junho",
  7: "Julho",
  8: "Agosto",
  9: "Setembro",
  10: "Outubro",
  11: "Novembro",
  12: "Dezembro",
};
