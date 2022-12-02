function button(elem) {
    var formData = {
        flightid: elem.getAttribute("data-flight-id"),
        flight_class: elem.getAttribute("data-flightclass"),
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


