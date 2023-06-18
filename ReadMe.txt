The Game of Nim

The game can be played at Stanford's Code in Place IDE at: https://codeinplace.stanford.edu/cip3/share/gTgw06Ei5o3ohsAB7JUe

If you want to run this code you need to use Stanford's Code in Place IDE since graphics.py, one of the libraries used (based on tkinter), is not fully available. An older version of the library can be found at https://cs106a.stanford.edu/graphics.zip but the code will not work appropriately.

The program only uses the canvas to communicate and can receive input from the mouse or the keyboard. Contains 45 variations, without including other versions when the number of stones it's different than 20 (from 1 up to 9999).

Options:

1. Play with a friend or against the computer (choose if you want to play first or second).

2. Play the standard game or change one or more rules:

- Number of stones in the game.

- The player who takes the last stone is the winner or the loser

- Maximum number of stones removed per turn (2 or 3)

- When the pile is divisible by 3 the player can or cannot go again.

*Code and CIP2023*
I started the game for the console extension on week 3 of CIP23 and continued working on it developing more extensions, fixing bugs and applying the new skills and knowledge from the weekly lessons and section.

However I reached an endpoint on the last week about lists and dictionaries because I wanted to avoid using global variables keeping in mind Chris' suggestion on his lesson and other comments of TAs in the general forum and I couldn't figure it out how to do it so I wrote a message asking for help to Derek, my section leader, and he told me that object oriented programming could help me with my issue. Even if that part wasn't part of Code in Place he explained me some general concepts about it and sent me very useful resources to learn and apply it. With that new knowledge I was able to optimize my code and make it more clear.

In this program I was able to apply everything I learned with CIP including decomposition, control flow, functions, parameters, lists and dictionaries. The only thing new in the code is the use of a few classes I created but I was only able to do it thanks to the concepts learned at CIP.