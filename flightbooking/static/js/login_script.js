$(document).ready(function () {
	var disabled_person = $('#disabled').val(); 					// Get disabled data 
	const signUpButton = document.getElementById('signUp');
	const signInButton = document.getElementById('signIn');
	const container = document.getElementById('container');

	// change too sign-up view 
	signUpButton.addEventListener('click', () => {
		container.classList.add("right-panel-active");
		if (disabled_person == 'true'){
			$("#audio1")[0].play(); 
		}
		
	});

	// change too sign-in view 
	signInButton.addEventListener('click', () => {
		container.classList.remove("right-panel-active");
	});

	// If press signup button
	$('#btnsignup').click(function () {
		// Create form
		var formData = {
			username: $("#username").val(),
			password: $("#password").val(),
			passport: $("#passport").val(),
			firstname: $("#firstname").val(),
			lastname: $("#lastname").val(),
			birthday: $("#birthday").val(),
			phonenumber: $("#phonenumber").val(),
			disabled: disabled_person,
		  };
		
		// Check if username is blank
		var username = $('#username').val().trim();
		if (username == '') {
			alert('กรุณาระบุชื่อ');
			$('#username').focus();
			return false;
		}
		// Check if password is blank
		var password = $('#password').val().trim();
		if (password == '') {
			alert('กรุณาระบุรหัสผ่าน');
			$('#password').focus();
			return false;
		}
		// Check if passport is blank
		var passport = $('#passport').val().trim();
		if (passport == '') {
			alert('กรุณาระบุหมายเลขพาสปอร์ต');
			$('#passport').focus();
			return false;
		}
		// Check if firstname is blank
		var firstname = $('#firstname').val().trim();
		if (firstname == '') {
			alert('กรุณาระบุชื่อจริง');
			$('#firstname').focus();
			return false;
		}
		// Check if birthday is blank
		var birthday = $('#birthday').val().trim();
		if (birthday == '') {
			alert('กรุณาระบุวันเกิด');
			$('#birthday').focus();
			return false;
		}

		// Ajax post
		var token = $('[name=csrfmiddlewaretoken]').val();
		console.log(formData)
		$.ajax({
			url: '/login/signup/',
			type: 'post',
			data:  formData,
			headers: { "X-CSRFToken": token },
			dataType: 'json',
			success: function  (data) {
				// If error
				if (data.error) {                           
					console.log(data.error);
					alert('สร้างบัญชีล้มเหลว');
				} else {
					//navigate to flight page with username            
					var username = $('#username').val().trim();
					var strLink = "/flight/?username=" + username; 
					window.location.href = strLink;

				}
			},
		});

	});

	// If press signin button
	$('#btnlogin').click(function () {

		// Check if username is blank
		var user = $('#user').val().trim();
		if (user == '') {
			alert('กรุณาระบุชื่อผู้ใช้');
			$('#user').focus();
			return false;
		}
		// Check if password is blank
		var password = $('#pwd').val().trim();
		if (password == '') {
			alert('กรุณาระบุรหัสผ่าน');
			$('#pwd').focus();
			return false;
		}
		// Ajax get username and password from database
		$.ajax({
			url: '/login/user/' + user,
			type: 'get',
			dataType: 'json',
			success: function  (data) {
				var database_password = new String(data.customer[0].password); 			// Get password from database
				var pass = database_password.replace(/ /g,'');							// Delete bank space 
				var pwd = new String($('#pwd').val());									// Get password from ui
				
				if (data.error) {                           
					alert('ชื่อผู้ใช้ไม่ถูกต้อง');
				} 
				else if (pwd != pass){
					alert('รหัสผ่านไม่ถูกต้อง');
				} else {
					//navigate to flight page with username                   
					var strLink = "/flight/?username=" + user;
					window.location.href = strLink
				}
			},
		});

	});

});



