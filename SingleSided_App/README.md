# Side Aware Swiss Software (SASS)

## A tournament manager app designed for Netrunner tournaments

This app is meant to be an interactive application for tournament managers to seamlessly run single sided (or double sided if they're feeling perverse) locally on their machine.

This is an early version, so many features will be missing. Most importantly hand re-pairings, double sided, and top cuts are not implemented at all, but are on the list of features. Additionally the tournament import/export is very basic, and is not an easily parsable log of what occurred. Eventually I want to make the export [Always Be Running](https://alwaysberunning.net/) compatible.

## Submit Feature Request/Bug Reports Here (if you don't have a GitHub account already)
[https://gitreports.com/issue/Chemscribbler/Netrunner](https://gitreports.com/issue/Chemscribbler/Netrunner)

## Some current known limitations:
- Resizing does not work the way it should (High Priority Fix)
- If you mark the Bye player as winning the match, no error is thrown
- If you name a player 'Bye' you get weird results
- No ability to load
- No ability to modify round results between pairings
- Dropping a player take a while to show in rankings
- Corp and Runner IDs are not up to date (except for a Core 1.0 tournament)

## Some future plans (in rough order):
- Automatically determine rounds & support cut
- Make a pipeline for ABR uploading
- Double sided Swiss support
- Dynamically adjust score factor (see explaination below)
- Get some Netrunnerdb integration to get updated ID choices
- Ability to load/import tournaments


If you have feature requests, it's probably best to make an issue. But you can also contact me on [Stimslack](https://www.google.com/url?q=https%3A%2F%2Fstimslackinvite.herokuapp.com%2F&sa=D&sntz=1&usg=AFQjCNGcS166Mr8z-H0l4RcoGM43C_dc5w) as Ysengrin.

## How the pairing algorithm works
At a high level, what this algorithm is finding the minimum weight graph where each player is a node, and each edge is the desirability of a given pairing. The weight on the edge is affected by the difference in the player's scores (ranking) and also the difference in the amount of games they've played with each side. The closer a pair's ranks are to each other the lower the score. Similarly if the players have no side bias (or opposite side bias) the cost of pairing them is 0. But if they have the same side bias, the cost increases (decreasing the likelyhood that they will get paired).

## What is Score Factor?

Score factor affects how many prestige up/down the algorithm will look to avoid having someone play an additional game with the side they have played more. Another player in the same level will be prefered, though some configurations will have pair up/downs to minimize the overall parity.
