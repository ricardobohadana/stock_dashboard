// Update navbar active item
document.getElementById("transactions").classList.add("active");
document.getElementById("dashboard").classList.remove("active");

// Material Select Initialization
// $(document).ready(function () {});

function editWallet(symbol) {
  if (symbol) {
    if (!isEmpty($("#transaction-title"))) {
      $("#transaction-title").contents().remove();
    }
    symbol.toString();
    $("#transaction-title").append(` ${symbol}`);
  }
}

// Check if a html tag is empty
function isEmpty(el) {
  return !$.trim(el.html());
}

// Delete wallet item
function deleteTransaction(id) {
  var action = confirm(
    "Tem certeza que deseja deletar essa transação?\n Toda a documentação e os dados serão apagados."
  );
  if (action != false) {
    $.ajax({
      url: create_url,
      data: {
        action: "delete",
        pk: id,
      },
      dataType: "json",
      success: function (data) {
        if (data.deleted) {
          $(`#transactions-${id}`).remove();
        }
      },
    });
  }
}

// Create Wallet Item
// $("form#createWallet").submit((e) => {
//   e.preventDefault();
//   var transactionOperation = $('select[name="transaction-operation"]').val();
//   var transactionStock = $('input[name="stock-transaction"]').val().trim();
//   var transactionFile = $('input[name="transaction-file"]').val().trim();
//   var transactionDate = $('input[name="transaction-date"]').val().trim();
//   if (
//     transactionDate &&
//     transactionFile &&
//     transactionStock &&
//     transactionOperation
//   ) {
//     // Create Ajax Call
//     $.ajax({
//       url: create_url,
//       method: 'post'
//       data: {
//         operation: stockInput,
//         stock: buyPriceInput,
//         date: stockAmoutInput,
//         file: stockOwner,
//       },
//       dataType: "json",
//       success: function (data) {
//         if (data) {
//           console.log("executed");
//           appendWalletToTable(data);
//           window.location.reload();
//         }
//       },
//     });
//   } else {
//     alert("All fields must have a valid value.");
//   }
//   $("form#createWallet").trigger("reset");
// });
