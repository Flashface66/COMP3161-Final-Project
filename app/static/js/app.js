/* Add your Application JavaScript */
console.log('this is some JavaScript code');

function notify() {
  alert('in here I will do something');
}

// Select the dropdown element
const dropdown = document.querySelector('.dropdown');

// Select the profiledrop element
const profiledrop = document.querySelector('.profiledrop');

// Add event listener for mouseover event on dropdown element
dropdown.addEventListener('mouseover', () => {
  // Add the 'show' class to the profiledrop element
  profiledrop.classList.add('show');
});

// Add event listener for mouseout event on dropdown element
dropdown.addEventListener('mouseout', () => {
  // Remove the 'show' class from the profiledrop element
  profiledrop.classList.remove('show');
});

var dateElem = document.getElementById("date");
var today = new Date();
var options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
var formattedDate = today.toLocaleDateString('en-US', options).toUpperCase().replace(/,/g, '');
dateElem.innerText = formattedDate;


// notify();
