
function myFunction(id) {
  var x = document.getElementById(id);
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}

function Copy(){
 var textArea = document.createElement("textarea");
  textArea.value = text;
  textArea.style.position="fixed";  //avoid scrolling to bottom
  document.body.appendChild(textArea);
  textArea.focus();
  textArea.select();

      var text = document.createElement("textarea");
                text.innerHTML = window.location.href;
//                alert(text.innerHTML)
                Copied = text.createTextRange();
                Copied.select();
                Copied.setSelectionRange(0, 99999)
                Copied.execCommand("Copy");
                alert("copied",window.location.href )
}