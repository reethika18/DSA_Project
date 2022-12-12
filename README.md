# Data Structures & Algorithms Fall 2022 Final Project : Turn based simulation of an NBA game using Object-Oriented Programming
### Team Members : 

Mathew Puthanpurackal (mputha2)

Reethika Renganathan (rr22)

Ruchi Rao (drrao2)

## Background

The National Basketball Association (NBA) is a professional basketball league in North America. This project will
enable the user to enjoy a game of basketball and concurrently discover strategies to win, thereby strengthening the
understanding of the game. We have created a basic simulation of the game, where the user will complete against an AI. 
It is a turn based game, so the user and the AI will select their moves one after the other, and the resulting gamestate
would be displayed after both of them have made a move.

![stephen-curry-ftr_1](https://user-images.githubusercontent.com/21601496/206863343-4f9ed1a0-ee32-443d-a4eb-f3ed79547663.jpeg)

## Important moves

These are the list of moves a user can choose from:
- **Move player with the ball in any direction**
- **Pass the ball to your teammate**
- **Shoot towards the basket**
- **Choose your player to move and intercept (defensive move)**

## NOTE

Please note some additional features that are significant for the game:
- **Player Attributes**  
All players have a defined attacking and defensive attribute. This means that some players are good at shooting 
the ball (attacking) but lacks defensive capabilities, and vice versa. The way we have assigned the attributes
is intuitive and easy to understand. Each player has a number attached to it when displayed (from 1 to 5).
Player with the number 1 has the highest attacking capability and lowest defensive capability. As the number increases,
the defensive capability increases and attacking capability decreases.


- **Player Movements**  
During each turn, the user can choose any player to perform the set of moves. The rest of the players in the team will
follow a default movement to make the game more realistic. By default, the rest of the players move one step
towards the ball


- **Pass interception**  
If the user decides to pass the ball to its teammate, and simultaneously the opponent decides to move and come 
between the path of the ball being passed, the ball gets intercepted by the opponent.


- **Points awarded**  
Any successful shot outside the three pointer line results in 3 points. All other successful shots are awarded 2 points.

## Shooting Function

The success of a shoot is defined by three parameters:
- **Distance of the shooting player from the basket**  
- **Shooting player's attacking attribute score**  
- **Number of opponent players close to the shooting player**  

All parameters are assigned a particular probability score and the final shoot success depends on the score which is
calculated by combining all these probabilities. 

## Artificial Intelligence
The opponent for any user is an AI. For this project, although the AI can make some smart moves, it does not learn from
its mistakes. The purpose of AI here is to make the game single-player rather than multiplayer, thereby increasing
the pace of the game (as AI can choose its move instantly).


##Time Complexity Analysis
For different functions in our program, the time complexity is slightly varying. 
The function that displays the ground to the players takes O(n^2) time.
The pass_ball_to_teammate, calculate_opp_dist, extract_three_ptr, three_ptr_region_valid, and move_remaining_players functions take O(n) time where 'n' in each case is different.
All the other functions take O(1) or constant amount of time. 


## User Guide

Clone the GitHub repo to your local IDE and run the file named 'basketball.py'. All the gamestates are displayed in the
terminal, and you can input your moves in the terminal itself. You might have to increase the size of your terminal 
to fit the gamestate being displayed. For now, we have introduced two teams - Golden State Warriors and Boston Celtics.
The user is always Golden State Warriors and the AI is Boston Celtics. Enjoy!






