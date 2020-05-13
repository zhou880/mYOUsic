
var index = 0;
var player = document.getElementById('player');
function goThroughSongs(test) {
        document.getElementById("player").src = "https://open.spotify.com/embed/track/"+ test[index];
        index = (index + 1) % test.length ;
};

function printIndex(){
    console.log(index);
}

function printCreate(){
    var name = document.getElementById('playlist-name').value;
    console.log(name);
}