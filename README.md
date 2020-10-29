# NBA Player Recommender

This is a software that will recommend NBA players to a specific team based solely on empirical data. This software is not to be served as the absolute truth. Instead, it will serve as a supporting tool for teams to determine the best player for their team. 


## How to use
Visit the [website](https://agkee.github.io/nba-player-recommender/) and input your team of interest and the number of players you want to be recommended. 

Example) Boston Celtics, 10

## Algorithm
### 1. Find the ideal player of the input team.
- The leagues average on certain stats and the specific teams certain stats average is used to determine the ideal player.

### 2. Find players to recommend based on the ideal player
- Finds players from the league that are most similar to this ideal player, the players to recommend.   
