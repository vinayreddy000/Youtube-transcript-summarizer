document.addEventListener('DOMContentLoaded', function() {
  var getTabUrlButton = document.getElementById('myButton');
  var displaySummary= document.getElementById('summary');
  getTabUrlButton.addEventListener('click', function() {
    chrome.runtime.sendMessage({ message: "getURL" }, function(response) {
      fetch('http://localhost:5000/process_url', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url: response })
      })
      .then(response => response.json())
      .then(data => {
        console.log(data);
        displaySummary.textContent=data.summary;
      })
      .catch(error => {
        console.error('Error:', error);
      });
    });
  });
});
