// (function() {
//     var scrt_var = "Quagmire";
//     var strLink = "/ticket/?username=" + scrt_var;
//     document.getElementById("btn-select").setAttribute("href",strLink);
// })();
function button() {
    var formData = {
        flightid: $("#flightid").val(),
        flight_class: $("#flightclass").val(),
      };
      var token = $('[name=csrfmiddlewaretoken]').val();
      console.log('click')
      $.ajax({
        url: '/flight/createticket/',
        type: 'post',
        data:  formData,
        headers: { "X-CSRFToken": token },
        dataType: 'json',
        success: function  (data) {
            if (data.error) {                           
                console.log(data.error);
                alert('เกิดข้อผิดพลาด');
                window.location.href = '/index';
            } else {            
                var strLink = "/ticket/?ticket_id=" + data.ticket_id;
                window.location.href = strLink;

            }
        },
    });
  }
// $(document).ready(function () {
// 	$('#btn-select').click(function () {
		

// 	});

// });