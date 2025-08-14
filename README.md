===========================      Ỉntroduction      ===========================

Warship is a turn-based naval strategy game where two players face off to locate 
and destroy each other’s entire fleet.

Featuring a radar system to assist in target scanning and a UDP server architecture
for fast move synchronization, the game delivers a smooth and thrilling experience. 

Each shot demands careful prediction and strategy, turning every match into
an intense battle of wits on the open seas.

===========================        Gameplay        ===========================

In Warship, each player commands a hidden fleet arranged on a grid-based map. 

Your mission is to use strategy and deduction to locate and destroy all of your opponent’s ships.

The game is played in turns:

  On each turn, you choose a coordinate to attack.

  The radar assists by scanning nearby waters, providing hint signals if it detects traces of enemy ships.

  If you score a hit, you may attack again on your next turn; if you miss, the turn passes to your opponent.

The UDP server processes all actions in real time — from sending attack coordinates, 
updating the map state, to transmitting radar signals. This ensures smooth, uninterrupted matches whether playing over a LAN or the internet.

Victory goes to the player who destroys the opponent’s entire fleet first. Each match is a 
tense battle of wits where every decision can change the tide of war.

===========================     Game run guide    ===========================

The game requires a computer from the player to run the server with the computer's own IP.

When the player starts an online match, it is required to enter the correct IP of the running server.

requires players to be on the same local network or can use RADMIN instead.

===========================     Key in game       ===========================

+ Left mouse click: fire
+ Right mouse click: rotate ship
+ Left mouse hold and move: move ship
  

