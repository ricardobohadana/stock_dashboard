// Update navbar active item
document.getElementById("wallet").classList.add("active");
document.getElementById("dashboard").classList.remove("active");

createrowTotal("Todos");
// Create row Total at the load of the page
// window.onload = () => {
//   var tableSearch = document.querySelector(".search-input");
//   tableSearch.addEventListener("input", (e) => {
//     console.log(String(e.target.value));
//     createrowTotal(String(e.target.value));
//   });
// };
// Initialize select filter
// $("select.selectpicker").selectpicker();

// Append created item to wallet table
function appendWalletToTable(wallet) {
  var percent =
    Math.round((wallet.money_amount / wallet.investment - 1) * 10000) / 100;
  var color = "negative-change";
  if (percent > 0) {
    color = "positive-change";
  }
  $("#walletTable > tbody:last-child").append(`
		<tr id="wallet-${wallet.pk}">
			<td class="stock-owner">${wallet.owner}</td>
			<td class="stock-symbol">${wallet.stocksymbol}</td>
			<td class="stock-amount">${wallet.stock_amount}</td>
			<td class="stock-investment">R$ ${wallet.investment}</td>
			<td class="stock-price">R$ ${wallet.stock_price}</td>
			<td class="stock-money-amount">R$ ${wallet.money_amount}</td>
			<td class="stock-change-percent ${color}">${percent} %</td>
			<td><button data-toggle="modal" onClick="editWallet('${wallet.stocksymbol}')" class="btn btn-primary" href="#modal1">EDITAR</button></td>
			<td><button onClick="deleteWallet('${wallet.pk}')" class="waves-effect waves-light btn">LIQUIDAR</button></td>
		</tr>
	`);
}

// Update wallet row
$("form#updateWallet").submit((e) => {
  e.preventDefault();
  var stock_symbol = $("#stock-title").contents().text().trim();
  var stock_amount = $('input[name="stock_amount_update"]').val().trim();
  var buy_price = $('input[name="buy_price_update"]').val().trim();
  if (stock_amount && buy_price) {
    // Create Ajax Call
    $.ajax({
      url: update_url,
      data: {
        stock_symbol: stock_symbol,
        stock_amount: stock_amount,
        buy_price: buy_price,
      },
      dataType: "json",
      success: function (data) {
        if (data) {
        }
      },
    });
  } else {
    alert("All fields must have a valid value.");
  }
  $("form#updateWallet").trigger("reset");
  $("#modal1").modal("hide");
  $(".modal-backdrop").hide();
  window.location.reload();
  return false;
});

function editWallet(symbol) {
  if (symbol) {
    if (!isEmpty($("#stock-title"))) {
      $("#stock-title").contents().remove();
    }
    symbol.toString();
    $("#stock-title").append(` ${symbol}`);
  }
}

// Check if a html tag is empty
function isEmpty(el) {
  return !$.trim(el.html());
}

// Delete wallet item
function deleteWallet(id) {
  var action = confirm("Tem certeza que deseja liquidar essa ação?");
  if (action != false) {
    $.ajax({
      url: delete_url,
      data: {
        pk: id,
      },
      dataType: "json",
      success: function (data) {
        if (data.deleted) {
          $("#wallet-" + id).remove();
          createrowTotal("Todos");
        }
      },
    });
  }
}

// Total row
function createrowTotal(owner) {
  var total_row = document.getElementById("wallet-table-total");
  var color = "negative-change";

  if (total_row) {
    total_row.remove();
  }
  var table = document.getElementById("walletTable");
  var total_amount = 0;
  var total_investment = 0;
  var total_money_amount = 0;
  for (var i = 1, row; (row = table.rows[i]); i++) {
    let amount = parseInt(row.cells[2].textContent);
    let investment = toFloat(row.cells[3].textContent);
    let money_amount = toFloat(row.cells[5].textContent);
    total_amount += amount;
    total_investment += investment;
    total_money_amount += money_amount;
  }
  var total_profit =
    Math.round((total_money_amount / total_investment - 1) * 10000) / 100;
  if (total_profit > 0) {
    color = "positive-change";
  }
  total_investment = (
    Math.round(100 * total_investment) / 100
  ).toLocaleString("en-US", { style: "currency", currency: "BRL" });
  total_money_amount = (
    Math.round(100 * total_money_amount) / 100
  ).toLocaleString("en-US", { style: "currency", currency: "BRL" });
  $("#walletTable > tbody:last-child").append(`
		<tr id="wallet-table-total">
			<td class="stock-symbol"><strong>${owner}<strong></td>
			<td class="stock-symbol"><b>TOTAL</b></td>
			<td class="stock-amount"><b>${total_amount}</b></td>
			<td class="stock-investment"><b>${total_investment}</b></td>
			<td class="stock-price"><b>-</b></td>
			<td class="stock-money-amount"><b>${total_money_amount}</b></td>
			<td class="stock-change-percent ${color}"><b>${total_profit}%</b></td>
		</tr>
	`);
}

// Create Wallet Item Django Ajax Call
$("form#createWallet").submit((e) => {
  e.preventDefault();
  var stockInput = $('select[name="stockObject"]').val().trim();
  var buyPriceInput = $('input[name="buy_price"]').val().trim();
  var stockAmoutInput = $('input[name="stock_amount"]').val().trim();
  var stockOwner = $('select[name="owner"]').val().trim();
  if (stockInput && buyPriceInput && stockAmoutInput && stockOwner) {
    // Create Ajax Call
    $.ajax({
      url: create_url,
      data: {
        stock: stockInput,
        buy_price: buyPriceInput,
        stock_amount: stockAmoutInput,
        owner: stockOwner,
      },
      dataType: "json",
      success: function (data) {
        if (data) {
          console.log("executed");
          appendWalletToTable(data);
          createrowTotal("Todos");
          window.location.reload();
        }
      },
    });
  } else {
    alert("All fields must have a valid value.");
  }
  $("form#createWallet").trigger("reset");
});

function toFloat(num) {
  const cleanStr = String(num).replace(/[^0-9.,]/g, "");
  let dotPos = cleanStr.indexOf(".");
  let commaPos = cleanStr.indexOf(",");

  if (dotPos < 0) dotPos = 0;

  if (commaPos < 0) commaPos = 0;

  const dotSplit = cleanStr.split(".");
  const commaSplit = cleanStr.split(",");

  const isDecimalDot =
    dotPos &&
    ((commaPos && dotPos > commaPos) ||
      (!commaPos && dotSplit[dotSplit.length - 1].length === 2));

  const isDecimalComma =
    commaPos &&
    ((dotPos && dotPos < commaPos) ||
      (!dotPos && commaSplit[commaSplit.length - 1].length === 2));

  let integerPart = cleanStr;
  let decimalPart = "0";
  if (isDecimalComma) {
    integerPart = commaSplit[0];
    decimalPart = commaSplit[1];
  }
  if (isDecimalDot) {
    integerPart = dotSplit[0];
    decimalPart = dotSplit[1];
  }

  return parseFloat(
    `${integerPart.replace(/[^0-9]/g, "")}.${decimalPart.replace(
      /[^0-9]/g,
      ""
    )}`
  );
}
