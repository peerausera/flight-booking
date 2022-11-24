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
});



function reset_form() {
    $('#txt_Flight_ID').val('');
    $('#txt_Gate').val('');
    $('#txt_Departure').val('');
    $('#txt_Destination').val('');
    $('#txt_BoardingDate').val('');
    $('#txt_BoardingTime').val('');
}