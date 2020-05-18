var index = 0;
var player = document.getElementById('player');
function goThroughSongs(test) {
        document.getElementById("player").src = "https://open.spotify.com/embed/track/"+ test[index];
        index = (index + 1) % test.length ;
};


function printIndex(){
    console.log(index);
}

function displayPlaylistName(){
    console.log(sessionStorage.getItem('username'))
    if (/create/.test(window.location.href) == true) {
        document.getElementById("display-playlist-name").innerHTML = sessionStorage.getItem('playlist_name');
    }
}
