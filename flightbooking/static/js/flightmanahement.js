$(document).ready(function () {
    $("#txt_BoardingDate").datepicker({
        dateFormat: 'dd/mm/yy'
    });

    $('#btn_BoardingDate').click(function () {
        $('#txt_BoardingDate').datepicker('show');
    });


    $('#btn_BoardingTime').click(function () {
        $('#txt_BoardingTime').timepicker({
            minuteStep: 1,
            showMeridian: false,
            snapToStep: true
        });
    });


    $('#btnNew').click(function () {
        reset_form();
    });

    $('#btnSave').click(function () {
        var flight_id = $('#txt_Flight_ID').val().trim();
        if (flight_id == '') {
            alert('กรุณาระบุ Flight ID');
            $('#txt_Flight_ID').focus();
            return false;
        }
        var gate = $('#txt_Gate').val().trim();
        if (gate == '') {
            alert('กรุณาระบุ Gate');
            $('#txt_Gate').focus();
            return false;
        }
        var departure = $('#txt_Departure').val().trim();
        if (departure == '') {
            alert('กรุณาระบุ Departure');
            $('#txt_Departure').focus();
            return false;
        }
        var boarding_date = $('#txt_BoardingDate').val().trim();
        if (boarding_date == '') {
            alert('กรุณาระบุ Boarding Date');
            $('#txt_BoardingDate').focus();
            return false;
        }
        var boarding_time = $('#txt_BoardingTime').val().trim();
        if (boarding_time == '') {
            alert('กรุณาระบุ Boarding time');
            $('#txt_BoardingTime').focus();
            return false;
        }
        var token = $('[name=csrfmiddlewaretoken]').val();

        $.ajax({
            url: '/FlightManagement/save/',
            type: 'post',
            data: $('#form_flight').serialize(),
            headers: { "X-CSRFToken": token },
            dataType: 'json',
            success: function (data) {
                if (data.error) {
                    console.log(data.error);
                    alert('การบันทึกล้มเหลว');
                } else {
                    console.log(data)
                    // $('#txt_Flight_ID').val(data.flight.flight_id)
                    // alert('บันทึกสำเร็จ');
                }
            },
        });
    });
});



function reset_form() {
    $('#txt_Flight_ID').val('');
    $('#txt_Gate').val('');
    $('#txt_Departure').val('');
    $('#txt_Destination').val('');
    $('#txt_BoardingDate').val('');
    $('#txt_BoardingTime').val('');
}