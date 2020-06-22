document.getElementById("transactions").classList.add("active");
document.getElementById("dashboard").classList.remove("active");

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
