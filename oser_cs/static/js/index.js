// $(function() {
//   var div = document.querySelector('#content');
//   $.ajax({
//     dataType: 'json',
//     url: 'http://localhost:8000/api/users/',
//     success: function(data) {
//       div.textContent = JSON.stringify(data);
//     }
//   });
// });

// from https://docs.djangoproject.com/en/1.8/ref/csrf/#ajax
// use for POST requests
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) == (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

div = document.querySelector('#content');
url = '/api/users/';

fetch(url).then((resp) => resp.json()).then(function(data) {
  console.log("Data is ok");
  div.textContent = JSON.stringify(data);
}).catch(function(error) {
  console.log("parsing failed", error);
});
