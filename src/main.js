
function find_player() {

    var team = document.getElementById("team").value;
    var limit = document.getElementById("playerNumber").value;
    
    // loadJson("https://17jn058fdh.execute-api.us-east-1.amazonaws.com/test", gotData)

    var result = "It will take some time... maybe 30 seconds... <br> <br> Appreciate your patience.";

    document.getElementById("players").innerHTML = result; 

    // testUrl = "https://cors-anywhere.herokuapp.com/https://17jn058fdh.execute-api.us-east-1.amazonaws.com/test/"
    testUrl = "https://cors-anywhere.herokuapp.com/https://17jn058fdh.execute-api.us-east-1.amazonaws.com/test2/"
    // testUrl = "https://17jn058fdh.execute-api.us-east-1.amazonaws.com/noproxy/"
    
    testUrl += "?" + "Team=" + team + "&Limit=" + limit.toString()
    var url = new URL(testUrl);
    console.log(testUrl)
    // var url = new URL("https://17jn058fdh.execute-api.us-east-1.amazonaws.com/test");
    // var Url = "http://api.ipinfodb.com/v3/ip-city/?key=9d64fcfdfacc213c7ddf4ef911okjjhh97b55e4696be3532bf8302hhhhc09ebad06b&format=json&ip=" + x;
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    xhr.send(JSON.stringify({ "Team": team, "Limit": limit }));

    // xhr.send();
    xhr.onreadystatechange = processRequest;
    function processRequest(e) {
        if (xhr.readyState == 4 && xhr.status == 200) {
            // alert(xhr.responseText);
            response = JSON.parse(xhr.responseText);
            
            team = response.Team;
            players = response.Players;
            text = "<br>";

            for (var i = 0; i < players.length; i++) {
                var split = players[i].split(" ");
                imglink = "https://nba-players.herokuapp.com/players/" + split[1] + "/" + split[0];
                var xml = new XMLHttpRequest();
                xml.open('GET', imglink, false);
                xml.send();
                var res = xml.responseText;

                if(res.startsWith("Sorry")) {
                    text += (i + 1).toString() + ". " + players[i] + "    (No image Available) <br>";
                }else{
                    text += (i + 1).toString() + ". " + players[i] + "<img src=" + imglink + " alt=" + players[i] + "> <br>";
                }
                // }
                // var n = str.startsWith("Hello");
                // console.log(xml);
                // console.log(xml.responseType);
                // xhr.onreadystatechange = processPlayer;
                // text += (i + 1).toString() + ". <img src= " + imglink + " alt=" + players[i] + "> " + players[i] + "<br>";
                // console.log(imglink); 
            }
            document.getElementById("players").innerHTML = "Team is: " + team + "<br>" + "Players are: " + text;
        }
    }
    //     ,params = { Team: team, Limit: limit }
    // Object.keys(params).forEach(key => url.searchParams.append(key, params[key]))
    // fetch(url).then(/* … */)


    // document.getElementById("players").innerHTML = result;
}