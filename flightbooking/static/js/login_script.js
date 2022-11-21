$(document).ready(function () {
	const signUpButton = document.getElementById('signUp');
	const signInButton = document.getElementById('signIn');
	const container = document.getElementById('container');
	signUpButton.addEventListener('click', () => {
		container.classList.add("right-panel-active");
	});

	signInButton.addEventListener('click', () => {
		container.classList.remove("right-panel-active");
	});
	$(function() {
		$('#birthday').datepicker();
	  });
	
	// var dateForm = function () {
		
	// };

	$('#btnsignup').click(function () {
		var formData = {
			username: $("#username").val(),
			password: $("#password").val(),
			firstname: $("#firstname").val(),
			lastname: $("#lastname").val(),
			birthday: $("#birthday").val(),
			phonenumber: $("#phonenumber").val(),
		  };

		var username = $('#username').val().trim();
		if (username == '') {
			alert('กรุณาระบุชื่อ');
			$('#username').focus();
			return false;
		}
		var password = $('#password').val().trim();
		if (password == '') {
			alert('กรุณาระบุรหัสผ่าน');
			$('#password').focus();
			return false;
		}
		var firstname = $('#firstname').val().trim();
		if (firstname == '') {
			alert('กรุณาระบุชื่อจริง');
			$('#firstname').focus();
			return false;
		}
		var birthday = $('#birthday').val().trim();
		if (birthday == '') {
			alert('กรุณาระบุวันเกิด');
			$('#birthday').focus();
			return false;
		}
		var token = $('[name=csrfmiddlewaretoken]').val();
		console.log(formData)
		$.ajax({
			url: '/login/signup/',
			type: 'post',
			data:  formData,
			headers: { "X-CSRFToken": token },
			dataType: 'json',
			success: function  (data) {
				if (data.error) {                           
					console.log(data.error);
					alert('สร้างบัญชีล้มเหลว');
				} else {            
					var username = $('#username').val().trim();
					var strLink = "/flight/?username=" + username;
					window.location.href = strLink;

				}
			},
		});

	});

	$('#btnlogin').click(function () {
			
		var user = $('#user').val().trim();
		if (user == '') {
			alert('กรุณาระบุชื่อผู้ใช้');
			$('#user').focus();
			return false;
		}
		var password = $('#pwd').val().trim();
		if (password == '') {
			alert('กรุณาระบุรหัสผ่าน');
			$('#pwd').focus();
			return false;
		}
		
		$.ajax({
			url: '/login/user/' + user,
			type: 'get',
			dataType: 'json',
			success: function  (data) {
				var database_password = new String(data.customer[0].password);
				var pass = database_password.replace(/ /g,'');
				var pwd = new String($('#pwd').val());
				
				if (data.error) {                           
					alert('ชื่อผู้ใช้ไม่ถูกต้อง');
				} 
				else if (pwd != pass){
					alert('รหัสผ่านไม่ถูกต้อง');
				} else {            
					var strLink = "/flight/?username=" + user;
					window.location.href = strLink;
				}
			},
		});

	});

});
