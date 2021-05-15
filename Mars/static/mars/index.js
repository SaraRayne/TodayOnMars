// Javascript for forums page (named index as it was the first one created)
document.addEventListener('DOMContentLoaded', function() {

  // Add onclick for dropdown button
  document.querySelector('#dropbtn').addEventListener('click', () => dropdown());

  // Add onclick for create a post, show form and hide button (default is hidden)
  document.querySelector('#createPost-button').addEventListener('click', function(event) {
    button = event.target;
    document.querySelector('#createPost-button').style.display = 'none';
    form = document.querySelector('#createPost-form');
    form.style.display = 'block';
  });

  // Grab form and button for creating a new thread
  var thread_form = document.getElementById('createPost-form');
  var thread_button = document.getElementById('createPost-button');

  // Checks for click anywhere on page other than thread form and button
  document.addEventListener('click', function(event) {
    var form = thread_form.contains(event.target);
    var button = thread_button.contains(event.target);
    // Hides form and shows button if user clicks outside of form
    if (!form && !button) {
        thread_form.style.display = 'none';
        thread_button.style.display = 'block';
    }
  });

});

// dropdown function adapted from https://www.w3schools.com/howto/howto_js_dropdown.asp
// When the user clicks on the button,
// toggle between hiding and showing the dropdown content
function dropdown() {
  document.getElementById("myDropdown").classList.toggle("show");
}

// Close the dropdown menu if the user clicks outside of it
window.addEventListener('click', function(event) {
  if (!event.target.matches('#dropbtn')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
})
