var index = 0;
var currSong;
var player = document.getElementById('player');
function goThroughSongs(song) {
        document.getElementById("player").src = "https://open.spotify.com/embed/track/"+ song[index];
        currSong = {"song_id": song[index]}
        index = (index + 1) % song.length ;
};


function printIndex(){
    console.log(index);
}


$(function() {
    $('button#add').on('click', function() {
        event.preventDefault();
        $.ajax({
            type: 'POST',
            contentType: 'application/json',
            url: '/create',
            dataType : 'json',
            data : JSON.stringify(currSong),
        });      
    });
  });
  
