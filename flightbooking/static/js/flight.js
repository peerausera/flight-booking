// If button press
function button(elem) {
    // Create form 
    var formData = {
        flightid: elem.getAttribute("data-flight-id"),
        flight_class: elem.getAttribute("data-flightclass"),
      };
      //  Ajax post
      var token = $('[name=csrfmiddlewaretoken]').val();
      console.log('click')
      $.ajax({
        url: '/flight/createticket/',
        type: 'post',
        data:  formData,
        headers: { "X-CSRFToken": token }, 
        dataType: 'json',
        success: function  (data) {
            // If error return to index page
            if (data.error) {                           
                console.log(data.error);
                alert('เกิดข้อผิดพลาด');
                window.location.href = '/index';
            } else {
                // navigate to ticket page with ticket id           
                var strLink = "/ticket/?ticket_id=" + data.ticket_id;
                window.location.href = strLink;

            }
        },
    });
    
  }


