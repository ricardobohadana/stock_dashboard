document.getElementById("dashboard").classList.remove("active");
document.getElementById("stocks-summary").classList.add("active");

document.addEventListener("DOMContentLoaded", ajaxStockLoader());

function ajaxStockLoader() {
  $.ajax({
    url: sum_stocks_url,
    method: "GET",
    data: {},
    dataType: "json",
    success: (response) => {
      if (response) {
        appendStocks(response);
      }
    },
  });
}

function appendStocks(stocks) {
  $("#loading").remove();
  for (i = 0; i < stocks.length; i++) {
    let price = stocks[i].price.toLocaleString("en-US", {
      style: "currency",
      currency: "BRL",
    });
    let colorClass = stocks[i].change_percent > 0 ? "success" : "danger";
    let stockColor = "secondary";
    if (stocks[i].is_etf) {
      stockColor = "warning";
    }
    console.log(stocks[i].is_fund);
    console.log(stocks[i].is_etf);

    if (stocks[i].is_fund) {
      stockColor = "default";
    }

    let myData = `
    <div class="col-xl-3 col-lg-4 col-md-6 col-sm-12 mt-4">
      <div class="card mt-1">
        <div class="">
          <span class="${stockColor}-color z-depth-2 px-4 py-2 ml-3 mt-n3 rounded text-white">${stocks[i].symbol}</span>
          <div class="float-right text-right p-3">
            <p class="text-uppercase text-muted mb-1"><small>PREÇO</small></p>
            <h4 class="font-weight-bold mb-0">${price}<span class=" ml-3 badge-pill badge badge-${colorClass}">${stocks[i].change_percent}%</span></h4>
          </div>
        </div>
        <div class="card-body pt-0">
          <div class="progress md-progress">
            <div class="progress-bar bg-${colorClass}" role="progressbar" style="width: 100%" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100"></div>
          </div>
        </div>
      </div>
    </div>
    `;
    $(myData).appendTo("#stocks-info-row");
  }
}
