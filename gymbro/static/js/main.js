$(document).ready(function(){

const form = document.getElementById('register');
const first_name = document.getElementById('form_first_name');
const last_name = document.getElementById('form_last_name');
const email = document.getElementById('form_email');
const weight = document.getElementById('form_weight');
const password = document.getElementById('form_password');
const confirm_pw = document.getElementById('form_confirm')
const errorElement = document.getElementById('error')

form.addEventListener('submit', (e) => {
	let messages = []
	if (first_name.value.length < 2) {
		messages.push('First name should be at least 2 characters')
}

	if (last_name.value.length < 2) {
		messages.push('Last name should be at least 2 characters')
}

	if (password.value.length < 5) {
		messages.push('Password should be atleast 5 characters')
	}

	if (password.value != confirm_pw.value) {
		messages.push('Passords must match')
	}

	if (messages.length > 0) {
		e.preventDefault()
		errorElement.innerText = messages.join(' and ')
}
})
// The code ↓ runs the animation for sliding left and right.
const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');

signUpButton.addEventListener('click', () => {
	container.classList.add("right-panel-active");

});

signInButton.addEventListener('click', () => {
	container.classList.remove("right-panel-active");

});
});

