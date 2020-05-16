
var index = 0;
var player = document.getElementById('player');
function goThroughSongs(test) {
        document.getElementById("player").src = "https://open.spotify.com/embed/track/"+ test[index];
        index = (index + 1) % test.length ;
};

function printIndex(){
    console.log(index);
}

function getPlaylistName(){
    name = document.getElementById('playlist-name').value;
}
function displayPlaylistName(){
    if (/create/.test(window.location.href) == true) {
        document.getElementById("display-playlist-name").innerHTML = name;
    }
}