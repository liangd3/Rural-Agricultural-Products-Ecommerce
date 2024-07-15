
'use strict';

$(function() {

	$("input[type='password'][data-eye]").each(function(i) {
		var $this = $(this),
			id = 'eye-password-' + i,
			el = $('#' + id);

		$this.wrap($("<div/>", {
			style: 'position:relative',
			id: id
		}));

		$this.css({
			paddingRight: 60
		});
		$this.after($("<div/>", {
			html: 'Show',
			class: 'btn btn-success btn-sm',
			id: 'passeye-toggle-'+i,
		}).css({
				position: 'absolute',
				right: 10,
				top: ($this.outerHeight() / 2) - 12,
				padding: '2px 7px',
				fontSize: 12,
				cursor: 'pointer',
		}));

		$this.after($("<input/>", {
			type: 'hidden',
			id: 'passeye-' + i
		}));

		var invalid_feedback = $this.parent().parent().find('.invalid-feedback');

		if(invalid_feedback.length) {
			$this.after(invalid_feedback.clone());
		}

		$this.on("keyup paste", function() {
			$("#passeye-"+i).val($(this).val());
		});
		$("#passeye-toggle-"+i).on("click", function() {
			if($this.hasClass("show")) {
				$this.attr('type', 'password');
				$this.removeClass("show");
				$(this).removeClass("btn-outline-primary");
			}else{
				$this.attr('type', 'text');
				$this.val($("#passeye-"+i).val());				
				$this.addClass("show");
				$(this).addClass("btn-outline-primary");
			}
		});
	});

	$(".my-login-validation").submit(function() {
		var form = $(this);
        if (form[0].checkValidity() === false) {
          event.preventDefault();
          event.stopPropagation();
        }
		form.addClass('was-validated');
	});
});



// Controls the display and hiding of the modal
	var modal = document.getElementById("termsModal");
	var btn = document.getElementById("openTermsModal");
	var span = document.getElementsByClassName("close")[0];
	btn.onclick = function() {
		modal.style.display = "block";
	}
	span.onclick = function() {
		modal.style.display = "none";
	}
	window.onclick = function(event) {
		if (event.target == modal) {
		modal.style.display = "none";
		}
	}


// Function to validate password
function validatePassword() {
    var password = document.getElementById("password").value;
    var confirmPassword = document.getElementById("confirm_password").value;
    var pattern = /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[\W])(?!.*\s).{8,}$/;
    var errorElement = document.getElementById("passwordError");

    if (!pattern.test(password)) {
        errorElement.innerText = "Your password must contain at least one uppercase letter, one lowercase letter, one digit, one special character, and be at least 8 characters long.";
        return false;
    }
    if (password !== confirmPassword) {
        errorElement.innerText = "Passwords do not match.";
        return false;
    }
    return true;
}

// Function to check email availability
function checkEmail() {
		var email = document.getElementById("email").value;

		// Make an AJAX request to check if the email already exists
		var xhr = new XMLHttpRequest();
		xhr.open("POST", "/check_email", true);
		xhr.setRequestHeader("Content-Type", "application/json");
		xhr.onreadystatechange = function () {
			if (xhr.readyState === 4 && xhr.status === 200) {
				var response = JSON.parse(xhr.responseText);
				if (response.exists) {
					// Email already exists, display error message
					document.getElementById('check_email').innerHTML = "Email already registered!";
					document.getElementById('submitButton').disabled = true;
				} else {
					// Email is available, submit the form
					document.getElementById('check_email').innerHTML = "";
					document.getElementById('submitButton').disabled = false;
				}
			}
		};
		xhr.send(JSON.stringify({ "email": email }));
	}

