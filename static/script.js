// Get form and results div
const form = document.getElementById('upload-form');
const resultsDiv = document.getElementById('results');
const fileInput = document.getElementById('image-select');
const button = document.getElementById('browse-btn1');
const buttonDetect = document.getElementById('detect');
const fileName = document.getElementById('fileName');



// Add submit event listener to form
form.addEventListener('submit', (e) => {

  // Prevent default form submit
  e.preventDefault();

  // Get the file from the input
  const file = document.getElementById('image-select').files[0];

  // Create a FormData object
  const formData = new FormData();

  // Append file to FormData
  formData.append('image', file);
  clearImages();
  $('#loadingDiv').show();
  // POST to /detect endpoint
  fetch('/api/v1/detect', {
    method: 'POST',
    body: formData
  })
  .then(response => response.json())
  .then(imageData => {
    var imageContainer = $('#image-container');
    $('#loadingDiv').hide();
    if (imageData.error) {
      // Handle the error
      imageContainer.append($('<p>').text(imageData.error));
    }
    else if(imageData.images.length > 0) {
      // Display result data
      var desiredWidth = imageContainer.width() * 0.8;
      imageData.images.forEach(function(img) {
        var img = $('<img>').attr('src', 'data:image/png;base64,' + img);
        img.css('width', desiredWidth + 'px'); // Set the width of the image
        imageContainer.append(img);
      });
    }
    else
    {
        imageContainer.append('<p>No images found</p>');
    }
  });

});

function clearImages() {
    $('#image-container').empty();
}

button.addEventListener('click', (e) => {
 // Prevent default form submit
  e.preventDefault();
  fileInput.click();
});

// Handle file input change
fileInput.addEventListener('change', (e) => {
  fileName.value = e.target.files[0].name;
});

$('#train').click(function() {
   key = document.getElementById('fileName').value;
   $.ajax({
    url: '/api/v1/train',
    method: 'POST',
    headers: {
    'Content-Type': 'application/json'
    },
    data: JSON.stringify({
        key: key
    }),
    success: function(response) {
      console.log(response);
    },
    error: function(xhr) {
      console.log(xhr.statusText);
    }
  });

});

$('#load').click(function() {

  $.ajax({
    url: '/api/v1/load',
    method: 'POST',
    success: function(response) {
      console.log(response);
    },
    error: function(xhr) {
      console.log(xhr.statusText);
    }
  });

});