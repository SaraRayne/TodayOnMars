// Javascript for thread page
document.addEventListener('DOMContentLoaded', function() {

  // Add onclick for create a reply, show form and hide button (default is hidden)
  document.querySelector('#reply-button').addEventListener('click', function(event) {
    console.log("clicked");
    button = event.target;
    document.querySelector('#reply-button').style.display = 'none';
    form = document.querySelector('#reply-form');
    form.style.display = 'block';
  });

  // Grab form and button for creating a reply
  var reply_form = document.getElementById('reply-form');
  var reply_button = document.getElementById('reply-button');

  // Checks for click anywhere on page other than reply form and button
  document.addEventListener('click', function(event) {
    var form = reply_form.contains(event.target);
    var button = reply_button.contains(event.target);
    // Hides form and shows button if user clicks outside of form
    if (!form && !button) {
        reply_form.style.display = 'none';
        reply_button.style.display = 'block';
    }
  });

});
