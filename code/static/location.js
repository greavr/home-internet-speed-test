function getLocation() {
  var x = document.getElementById("geo-location");
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition);
  } else {
    x.innerHTML = "<b>Geolocation is not supported by this browser.</b>";
  }
}

function showPosition(position) {
  var x = document.getElementById("geo-location");
  x.innerHTML = "<b>Latitude: </b>" + position.coords.latitude +
  "<br><b>Longitude: </b>" + position.coords.longitude;
}