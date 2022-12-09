
let country = '';

$('#1').click(function () {
    console.log('button 1 click')
    country = 'Tokyo';
    console.log(country)
    $("#audio1")[0].play();       
});

$('#2').click(function () {
    console.log('button 2 click')
    country = 'Beijing'; 
    console.log(country)
    $("#audio2")[0].play();      
});

$('#3').click(function () {
    console.log('button 3 click')
    country = 'Seoul';    
    console.log(country)  
    $("#audio3")[0].play();       
});

$('#4').click(function () {
    console.log('button 4 click')
    country = 'Singapore';  
    console.log(country)    
    $("#audio4")[0].play();       
});

$('#5').click(function () {
    console.log('button 5 click')
    country = 'Maldives';   
    console.log(country)    
    $("#audio5")[0].play();      
});
$('#6').click(function () {
    console.log('button 6 click')
    country = 'London';
    console.log(country)       
    $("#audio6")[0].play();      
});
$('#7').click(function () {
    console.log('button 7 click')
    country = 'New York'; 
    console.log(country)      
    $("#audio7")[0].play();      
});
$('#8').click(function () {
    console.log('button 8 click')
    country = 'Los Angeles'; 
    console.log(country)      
    $("#audio8")[0].play();      
});
$('#9').click(function () {
    console.log('button 9 click')
    country = 'Hanoi';   
    console.log(country)    
    $("#audio9")[0].play();      
});

$('#btn-submit').click(function () {
    var formData = {
        destination: country,
        date:  $("#date").val(),
        
      };
    if (country == '') {
        $("#audio11")[0].play();      
        return false;
    }
    var date = $('#date').val().trim();
    if (date == '') {
        $("#audio10")[0].play();      
        $('#date').focus();
        return false;
    }
    console.log(formData)                  
    var token = $('[name=csrfmiddlewaretoken]').val();
            $.ajax({
                url:  '/voice/search/',
                type:  'post',
                data: formData,
                headers: { "X-CSRFToken": token },
                dataType:  'json',
            });   
        
});

