// RUNNING ANIMATION
baguetteBox.run('.cards-gallery', { animation: 'slideIn'});

// SETTING UP FIREBASE CREDENTIALS
var firebaseConfig = {
    apiKey: "AIzaSyDhJD_AENniovRoVttwWmwaKwlpKuHyVck",
    authDomain: "whatsapp-27255.firebaseapp.com",
    databaseURL: "https://whatsapp-27255.firebaseio.com",
    projectId: "whatsapp-27255",
    storageBucket: "whatsapp-27255.appspot.com",
    messagingSenderId: "998524713961",
    appId: "1:998524713961:web:dedfaf0cc4d5710d65e978",
    measurementId: "G-T5B7QLDPKN"
};

// CONFIGURE REFERENCES
firebase.initializeApp(firebaseConfig);
var storageRef = firebase.storage().ref();

// COOKIE GETTER HELPER TO RETRIEVE CURRENT USER'S DISPLAY NAME
function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

// HELPER : COOKIE SETTER TO PASS ON fileContentsList
function setCookie(name,value,days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days*24*60*60*1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "")  + expires + "; path=/";
    alert("COOKIE SET : " + document.cookie);
}

// GET CURRENT USER'S NAME VIA COOKIE
var currentUserName = getCookie('currentUserName');

// SETUP CLOUD DIRECTORY TO PULL FROM
var folderRef = storageRef.child(currentUserName);
var fileList = [];

// CREATE A LIST OF TRUNCATED FILENAMES
var textFileNames = []; // ["... with ABC.txt", "... with XYZ.txt"];

// PULL ALL FILES BELONGING TO THE USER
folderRef.listAll().then(function (res) {
    res.items.forEach(function (itemRef) {
        fileList.push(itemRef);
    });

<!--			// DEBUG AND CHECK IF FILES ARE THERE-->
<!--			alert(fileList.join("\n"));-->

    // POPULATE THE LISTVIEW
    var historyListView = document.getElementById('historyListView');
    for (var i = 1; i < 10; i++) {

        // RENDER CARD
        if (i < fileList.length + 1) {

            // GET COMPONENT
            var fileNameID = 'name' + i;  // name1, name2, ...
            var fileDateID = 'date' + i;  // date1, date2, ...
            var fileName = document.getElementById(fileNameID);
            var fileDate = document.getElementById(fileDateID);

            // SET COMPONENT NAME
            var regExp = /WhatsApp Chat with .*.txt$/g;
            var match = regExp.exec(fileList[i-1]);
            var newName = match[0].substring(0, match[0].length - 4);
            fileName.innerHTML = newName;

            // ADD FILENAME TO LIST FOR ACCESSING FIREBASE STORAGE
            var newNameWithExtension = newName + '.txt';
            textFileNames.push(newNameWithExtension);
        }
        // REMOVE CARD
        else {
            var cardID = 'card' + i;
            var fileCard = document.getElementById(cardID);
            fileCard.style.display = "none";
        }
    }
    }).catch(function (error) {
        alert(error.message);
    });


// CARD VIEW 1 ONCLICK
function card1Click() {
<!--			alert("Card 1");-->
    var fileRef = folderRef.child(textFileNames[0]);
    fileRef.getDownloadURL().then(function(url) {
        var xhr = new XMLHttpRequest();
        xhr.responseType = 'text';
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
        xhr.open('GET', url);
        xhr.send();
    }).catch(function(error) {
        alert(error.code);
    });
}

// CARD VIEW 2 ONCLICK
function card2Click() {
    alert("Card 2");
}

// CARD VIEW 3 ONCLICK
function card3Click() {
    alert("Card 3");
}

// CARD VIEW 4 ONCLICK
function card4Click() {
    alert("Card 4");
}

// CARD VIEW 5 ONCLICK
function card5Click() {
    alert("Card 5");
}

// CARD VIEW 6 ONCLICK
function card6Click() {
    alert("Card 6");
}

// CARD VIEW 7 ONCLICK
function card7Click() {
    alert("Card 7");
}

// CARD VIEW 8 ONCLICK
function card8Click() {
    alert("Card 8");
}

// CARD VIEW 9 ONCLICK
function card9lick() {
    alert("Card 9");
}
