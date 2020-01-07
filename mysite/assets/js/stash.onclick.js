// CARD VIEW 1 ONCLICK
function card1Click() {
    var fileRef = folderRef.child(textFileNames[0]);
    fileRef.getDownloadURL().then(function(url) {
        var xhr = new XMLHttpRequest();
        xhr.responseType = 'text';
        xhr.open('GET', url);
        xhr.send();
        xhr.onload = function(event) {
            var textFile = xhr.response;
            $.ajax({
              url: 'http://127.0.0.1:8000/metrics/',
              type: 'POST',
              data: {'textFile': textFile},
              headers: {"X-CSRFToken":'{{ csrf_token }}'},
              success: function() {
                window.location.href = 'http://127.0.0.1:8000/metrics/';
              },
              error: function (result) {
                console.log(result);
              }
            });
        };
    }).catch(function(error) {
        alert(error.code);
    });
}

// CARD VIEW 2 ONCLICK
function card2Click() {
    var fileRef = folderRef.child(textFileNames[1]);
    fileRef.getDownloadURL().then(function(url) {
        var xhr = new XMLHttpRequest();
        xhr.responseType = 'text';
        xhr.open('GET', url);
        xhr.send();
        xhr.onload = function(event) {
            var textFile = xhr.response;
            $.ajax({
              url: 'http://127.0.0.1:8000/metrics/',
              type: 'POST',
              data: {'textFile': textFile},
              headers: {"X-CSRFToken":'{{ csrf_token }}'},
              success: function() {
                window.location.href = 'http://127.0.0.1:8000/metrics/';
              },
              error: function (result) {
                console.log(result);
              }
            });
        };
    }).catch(function(error) {
        alert(error.code);
    });
}

// CARD VIEW 3 ONCLICK
function card3Click() {
    var fileRef = folderRef.child(textFileNames[2]);
    fileRef.getDownloadURL().then(function(url) {
        var xhr = new XMLHttpRequest();
        xhr.responseType = 'text';
        xhr.open('GET', url);
        xhr.send();
        xhr.onload = function(event) {
            var textFile = xhr.response;
            $.ajax({
              url: 'http://127.0.0.1:8000/metrics/',
              type: 'POST',
              data: {'textFile': textFile},
              headers: {"X-CSRFToken":'{{ csrf_token }}'},
              success: function() {
                window.location.href = 'http://127.0.0.1:8000/metrics/';
              },
              error: function (result) {
                console.log(result);
              }
            });
        };
    }).catch(function(error) {
        alert(error.code);
    });
}

// CARD VIEW 4 ONCLICK
function card4Click() {
    var fileRef = folderRef.child(textFileNames[3]);
    fileRef.getDownloadURL().then(function(url) {
        var xhr = new XMLHttpRequest();
        xhr.responseType = 'text';
        xhr.open('GET', url);
        xhr.send();
        xhr.onload = function(event) {
            var textFile = xhr.response;
            $.ajax({
              url: 'http://127.0.0.1:8000/metrics/',
              type: 'POST',
              data: {'textFile': textFile},
              headers: {"X-CSRFToken":'{{ csrf_token }}'},
              success: function() {
                window.location.href = 'http://127.0.0.1:8000/metrics/';
              },
              error: function (result) {
                console.log(result);
              }
            });
        };
    }).catch(function(error) {
        alert(error.code);
    });
}

// CARD VIEW 5 ONCLICK
function card5Click() {
    var fileRef = folderRef.child(textFileNames[4]);
    fileRef.getDownloadURL().then(function(url) {
        var xhr = new XMLHttpRequest();
        xhr.responseType = 'text';
        xhr.open('GET', url);
        xhr.send();
        xhr.onload = function(event) {
            var textFile = xhr.response;
            $.ajax({
              url: 'http://127.0.0.1:8000/metrics/',
              type: 'POST',
              data: {'textFile': textFile},
              headers: {"X-CSRFToken":'{{ csrf_token }}'},
              success: function() {
                window.location.href = 'http://127.0.0.1:8000/metrics/';
              },
              error: function (result) {
                console.log(result);
              }
            });
        };
    }).catch(function(error) {
        alert(error.code);
    });
}

// CARD VIEW 6 ONCLICK
function card6Click() {
    var fileRef = folderRef.child(textFileNames[5]);
    fileRef.getDownloadURL().then(function(url) {
        var xhr = new XMLHttpRequest();
        xhr.responseType = 'text';
        xhr.open('GET', url);
        xhr.send();
        xhr.onload = function(event) {
            var textFile = xhr.response;
            $.ajax({
              url: 'http://127.0.0.1:8000/metrics/',
              type: 'POST',
              data: {'textFile': textFile},
              headers: {"X-CSRFToken":'{{ csrf_token }}'},
              success: function() {
                window.location.href = 'http://127.0.0.1:8000/metrics/';
              },
              error: function (result) {
                console.log(result);
              }
            });
        };
    }).catch(function(error) {
        alert(error.code);
    });
}

// CARD VIEW 7 ONCLICK
function card7Click() {
    var fileRef = folderRef.child(textFileNames[6]);
    fileRef.getDownloadURL().then(function(url) {
        var xhr = new XMLHttpRequest();
        xhr.responseType = 'text';
        xhr.open('GET', url);
        xhr.send();
        xhr.onload = function(event) {
            var textFile = xhr.response;
            $.ajax({
              url: 'http://127.0.0.1:8000/metrics/',
              type: 'POST',
              data: {'textFile': textFile},
              headers: {"X-CSRFToken":'{{ csrf_token }}'},
              success: function() {
                window.location.href = 'http://127.0.0.1:8000/metrics/';
              },
              error: function (result) {
                console.log(result);
              }
            });
        };
    }).catch(function(error) {
        alert(error.code);
    });
}

// CARD VIEW 8 ONCLICK
function card8Click() {
    var fileRef = folderRef.child(textFileNames[7]);
    fileRef.getDownloadURL().then(function(url) {
        var xhr = new XMLHttpRequest();
        xhr.responseType = 'text';
        xhr.open('GET', url);
        xhr.send();
        xhr.onload = function(event) {
            var textFile = xhr.response;
            $.ajax({
              url: 'http://127.0.0.1:8000/metrics/',
              type: 'POST',
              data: {'textFile': textFile},
              headers: {"X-CSRFToken":'{{ csrf_token }}'},
              success: function() {
                window.location.href = 'http://127.0.0.1:8000/metrics/';
              },
              error: function (result) {
                console.log(result);
              }
            });
        };
    }).catch(function(error) {
        alert(error.code);
    });
}

// CARD VIEW 9 ONCLICK
function card9lick() {
    var fileRef = folderRef.child(textFileNames[8]);
    fileRef.getDownloadURL().then(function(url) {
        var xhr = new XMLHttpRequest();
        xhr.responseType = 'text';
        xhr.open('GET', url);
        xhr.send();
        xhr.onload = function(event) {
            var textFile = xhr.response;
            $.ajax({
              url: 'http://127.0.0.1:8000/metrics/',
              type: 'POST',
              data: {'textFile': textFile},
              headers: {"X-CSRFToken":'{{ csrf_token }}'},
              success: function() {
                window.location.href = 'http://127.0.0.1:8000/metrics/';
              },
              error: function (result) {
                console.log(result);
              }
            });
        };
    }).catch(function(error) {
        alert(error.code);
    });
}
