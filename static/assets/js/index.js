const signUpButton = document.getElementById('signUp');
/*const signInButton = document.getElementById('signIn');*/
const container = document.getElementById('container');

signUpButton.addEventListener('click', () => {
	container.classList.add("right-panel-active");
});

/*signInButton.addEventListener('click', () => {
	container.classList.remove("right-panel-active");
});


signIn = () => {
	container.classList.remove("right-panel-active");
}*/

function signIn(){
	container.classList.remove("right-panel-active");
}

function student(){
	container.classList.add("right-panel-active");
  	document.getElementById('student1').style.display = "block";
  	document.getElementById('teacher1').style.display = "none";
 }
function teacher(){
	container.classList.add("right-panel-active");
  	document.getElementById('student1').style.display = "none";
  	document.getElementById('teacher1').style.display = "block";
}