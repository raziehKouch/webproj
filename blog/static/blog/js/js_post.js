
function myFunction(id) {
  var x = document.getElementById(id);
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}

function share() {

  var copyGfGText = document.getElementById("url");
  copyGfGText.select();
  document.execCommand("copy");

}
function commentshare() {

  var copyGfGText = document.getElementById("url2");
  copyGfGText.select();
  document.execCommand("copy");

}

