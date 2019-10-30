function find_player() {

    var team = document.getElementById("team").value;
    var limit = document.getElementById("playerNumber").value;
    
    var result = "Players: " + team + "<br>" + "show this many teams: " + limit;




    document.getElementById("players").innerHTML = result;
}