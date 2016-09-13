[![No Maintenance Intended](http://unmaintained.tech/badge.svg)](http://unmaintained.tech/)

Jeopardy Clone
===============
This is a simple jeapordy game,no values, no scoring, just the clues and answers. 


What is this?
-------------

A simple jeopardy board generator/viewer. This project was design mostly for my own use learning trivia and having fun with my family.

The downloader and parser were modified from whymarrh's [Jeopardy Parser]:https://github.com/whymarrh/jeopardy-parser fixing a few errors I ran into and simplifying the database structure as I did not need all the information captured by the scraper.


  [Jeopardy!]:http://www.jeopardy.com/
  [J! Archive]:http://j-archive.com/
  [Original Jeopardy Parser]:https://github.com/whymarrh/jeopardy-parser

Quick start
-----------
Create jclues.db 
```bash
python main_app.py
```
First Download and Parse Files Creating a jclues.db file of ~48mb

After this you can start a new game

You will be greeted with a jeapordy game board listing the categories and clues. Click on a clue to view the answer.

TODO
----------------------------
Provide Simple GUI for Download and Parsing Scripts

Provide a simple editor for teachers/custom clues 

Possibly:

Create raspberry pi version with 3 buttons for players, score keeping, daily doubles,timed clues, etc...

Will require a 4th player to play judge

License
-------

This software is released under the MIT License. See the [LICENSE.md](LICENSE.md) file for more information.
