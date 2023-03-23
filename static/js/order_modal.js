
var currid = "";

function showmodal(id) {
  $.ajax({
    type: "GET",
    url: `https://dashboard.pureseed.in/api/users/order/${id}/`,
    xhrFields: {
      withCredentials: true
    },
    dataType: "json",
    success: function (data) {
      // Create table headers
      var table = "<table>";
      // Get user info
      var user = data.user;
      var name = user.first_name + " " + user.last_name;
      var phone = data.shippingAddress.phone_number;
      var email = user.email;
      // Get order info
      var orderId = data.custom_order_id;
      var orderItems = data.orderItems;
      var price = data.totalPrice;
      var deliveryPrice = data.shippingPrice;      
      currid = id;
      $("#ostatus").val(data.status);
      // Create table rows
      var row = "<tr><td>Name:</td><td> " + name + "</td></tr><tr><td>Phone: </td><td> " +
        phone + "</td></tr><tr><td>Email: </td><td> " + email + "</td></tr><tr><td>OrderId: </td><td> " + orderId + "</td></tr><b>";
      for (var i = 0; i < orderItems.length; i++) {
        row += "<b> <tr class='data'><td>" + orderItems[i].name + " </td><td>  Rs. " + orderItems[i].price + "</td></tr> </b>";
      }
      row += "</td></tr><tr><td>Delivery Price: </td><td> Rs. " + deliveryPrice + "</td></tr><tr><td>Total Price: </td><td> Rs. " + price + "</td></tr>";

      // Add rows to table
      table += row + "</table><br>";
      // Display table in modal

      $("#order-modal-body").html(table);
      $("#order-modal").modal("show");
    }
  });
}

function submitform(){
  if ($("#ostatus").val != "dispatched"){
    $.ajax({
      type: "POST",
      url: 'https://dashboard.pureseed.in/api/edit_order_status/',
      headers: {
        "X-CSRFToken": jQuery("[name=csrfmiddlewaretoken]").val(),
      },
      data: {
        "csrfmiddlewaretoken": $("[name=csrfmiddlewaretoken]").val(),
        "new_status": $('#ostatus').val(),
        "order_id": currid
      },
      dataType: "json",
      success: function (data) {
        $('#form2').submit();
        //console.log(data)
      }
    });
  }

  else {
    $.ajax({
      type: "POST",
      url: 'https://dashboard.pureseed.in/api/edit_order_status/',
      headers: {
        "X-CSRFToken": jQuery("[name=csrfmiddlewaretoken]").val(),
      },
      data: {
        "csrfmiddlewaretoken": $("[name=csrfmiddlewaretoken]").val(),
        "new_status": $('#ostatus').val(),
        "courier-info": $("courier-data").val(),
        "order_id": currid
      },
      dataType: "json",
      success: function (data) {
       $('#form2').submit();
       //console.log(data)
      }
    });
  }
}
