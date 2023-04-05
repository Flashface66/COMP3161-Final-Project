/* Add your Application JavaScript */
console.log('this is some JavaScript code');

function notify() {
  alert('in here I will do something');
}

$(document).ready(function() {
  // Hide the flash message after 3 seconds
  setTimeout(function() {
    $('#my-flash-message').fadeOut();
  }, 3000);
});

// Select the dropdown element
const dropdown = document.querySelector('.dropdown');

// Select the profiledrop element
const profiledrop = document.querySelector('.profiledrop');

// Add event listener for click event on dropdown element
dropdown.addEventListener('click', () => {
  // Check if the profiledrop element has the 'show' class
  if (profiledrop.classList.contains('show')) {
    // Remove the 'show' class to hide the profiledrop element
    profiledrop.classList.remove('show');
  } else {
    // Add the 'show' class to the profiledrop element to show it
    profiledrop.classList.add('show');
  }
});


// var dateElem = document.getElementById("date");
// var today = new Date();
// var options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
// var formattedDate = today.toLocaleDateString('en-US', options).toUpperCase().replace(/,/g, '');
// dateElem.innerText = formattedDate;


// notify();
