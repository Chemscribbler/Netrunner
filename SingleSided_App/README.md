# Side Aware Swiss Software (SASS)

## A tournament manager app designed for Netrunner tournaments

This app is meant to be an interactive application for tournament managers to seamlessly run single sided (or double sided if they're feeling perverse) locally on their machine.

This is an early version, so many features will be missing. Most importantly hand re-pairings, double sided, and top cuts are not implemented at all, but are on the list of features. Additionally the tournament import/export is very basic, and is not an easily parsable log of what occurred. Eventually I want to make the export [Always Be Running](https://alwaysberunning.net/) compatible.

## Some current known limitations:
- If you mark the Bye player as winning the match, no error is thrown
- If you name a player 'Bye' you get weird results
- No ability to load
- No ability to modify round results between pairings
- Dropping a player take a while to show in rankings
- Corp and Runner IDs are not up to date (except for a Core 1.0 tournament)

## Some future plans:
- Make a pipeline for ABR uploading
- Get some Netrunnerdb integration to get updated ID choices
- Ability to load/import tournaments
- Double sided Swiss support

If you have feature requests, it's probably best to make an issue. But you can also contact me on [Stimslack](https://www.google.com/url?q=https%3A%2F%2Fstimslackinvite.herokuapp.com%2F&sa=D&sntz=1&usg=AFQjCNGcS166Mr8z-H0l4RcoGM43C_dc5w) as Ysengrin.