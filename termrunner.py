########################
#!/usr/bin/env python  #
#                      #
#  TuX Runner ver.1.1  #
########################
import random, ttyLinux, time, os
from util import *

class Player :
	def setDirection (self, ch) : pass

	def move (self) :
		global inPlay, you, players
		spot = getSpot(self.row,self.col)
		lspot = getSpot(self.row,self.col-1)
		rspot = getSpot(self.row,self.col+1)
  
		horz,vert = self.dir
		writeScreen(self.row,self.col,spot)
		if   spot == '_' : self.col += horz  # by left/right arself.row
		elif spot == '^' : self.row -= vert  # left/right
		elif spot == '/' : self.col += horz  # by left/right arself.row
		elif spot == '\\' : self.col += horz  # by left/right arself.row
		elif spot == 'I' : self.row += vert  # left/right
		elif spot == ')' : self.row += vert  # left/right
		elif spot == '(' : self.row += vert  # left/right  
		elif spot == '|' : self.row -= vert  # by up/down arrow
		elif spot == ' ' : self.row += 1     # always fall in air
		elif spot == 'i' : self.row -= vert  # left/right
		# Ok to walk horizontally past a ladder or obstacle
		if   lspot == '_' and horz == -1 : self.col -= 1
		elif rspot == '_' and horz ==  1 : self.col += 1
		writeScreen(self.row,self.col,self.face)
		if self.row > 23 :
			if self.face == '8' : inPlay = 0
			else : players.remove(self)

class You(Player) :
	def __init__ (self, Row=1, Col=10, Face='8') :
		self.row = Row; self.col = Col; self.face=Face
		self.dir = (0,0); self.score=0

	def setDirection (self, ch) :
		here = getSpot(self.row,self.col)
		if here == '.' :
			self.score += 10
			setSpot(self.row,self.col,"_")
			writeScreen(self.row,self.col,"_")   # update the screen
                if here == '<' :
                        setSpot(self.row,self.col," ")
		        writeScreen (24,0,'NooOOoo!!! You took my SECRET!!! ')
			time.sleep(4)
			writeScreen (24,0,'    It was my best secret, and now you stold it!! ')
 			time.sleep(4)
			writeScreen (24,0,'    I say FLOOR BE GONE! ( Bye bye! )                        ')
			time.sleep(3)
                        writeScreen(self.row,self.col,"_")   # update the screen

		if ch == '\033[A' : self.dir=( 0, 1)  # up
		if ch == '\033[B' : self.dir=( 0,-1)  # down
		if ch == '\033[C' : self.dir=( 1, 0)  # right
		if ch == '\033[D' : self.dir=(-1, 0)  # left
		if ch == 'a' : burn(self.row, self.col-1)
		if ch == 's' : burn(self.row, self.col+1)

class Robot(Player) :
	def __init__ (self, Row=1, Col=12, Face='@') :
		self.row = Row; self.col = Col; self.face=Face
		self.hisLadder = 0
		self.dir = (0,0)

	def move (self) :
		global clock
		if clock%2 == 0 : Player.move(self)

	def setDirection (self, ch) :
		global inPlay, you
		# did we tag him?
		if you.row == self.row and you.col == self.col : inPlay=0
		# same level. run toward you
		if self.row == you.row :
			if self.col > you.col : self.dir=(-1,0) # left
			if self.col < you.col : self.dir=( 1,0) # right
		else :
			me = getSpot(self.row,self.col)  # where am I
			if me == "|" : # on a ladder
				if self.row > you.row : self.dir=(0, 1) # up
				if self.row < you.row : self.dir=(0,-1) # down
	
def burn (row,col) :
	"Burn a hole in the catwalk at row,col"
	setSpot(row,col," ")       # set the board
	writeScreen(row,col," ")   # update the screen

def main ():
	setBoard(4)
	try :
		ttyLinux.setSpecial()
		playGame()
	finally : ttyLinux.setNormal()

def playGame() :
	os.system("clear")
	print" "
	print" _______                       ______                                    "
	print"|_     _|.-----.----.--------.|   __ \.--.--.-----.-----.-----.----.     "
	print"   |   |  |  -__|   _|        ||      <|  |  |     |     |  -__|   _|    "
	print"   |___|  |_____|__| |__|__|__||___|__||_____|__|__|__|__|_____|__|      "
	print"                                          __                             "
	print"                     ?                  _/--\_                           "                    
	print"                   ' _  '                |--|                            "     
	print"                    ( )                  |--|                            "
	print"                    _;_                  |--|      /|                    "
	print"                   / | \                 |--|     / |                    "
	print"                   \ |  \     ___________|--|____/  |    .       .       "
	print"   .      .         `|\  `   |--|__|__|__|__|__|_o  |      .    .        "
	print"     \__/            | \     |--|                 o |       \__/         "
	print"     (oo)           /  /     |--|                - o|       (oo)         "
	print"    //||\\\         /_ /_     |--|                0 |       //||\\\      "
	print" .:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:. "  
	print"========================================================================="
	print"              -> By Daniel.J aka *hexabit* 2009 <- "
	print"========================================================================="
        print" "
	print"                      Starting up...                               "
	print" "
	time.sleep(4)
	global clock, inPlay, you, players
	you = You()
	writeBoard ()
	players = [you]
	clock = 0
	inPlay = 1
	while inPlay :
		if you.score == 180:
			print"   --->  -->  WELL DONE! Level 1 completed!  <---  <---"
			time.sleep(2)
			os.system("clear")
			print" "
			print" <------------> <--------------> <------------->"
			print" "
			print"   LEVEL 2 .... Construction site :-)"
			print" "
			print" <------------> <--------------> <------------->" 
			time.sleep(4)
			setBoard(0)
			playGame2()
	
		clock += 1
		if clock > 60 and len(players) < 3 :
			players.append(Robot(Col=int(random.random()*40+5)))
		#time.sleep(.1)
                #time.sleep(.1)
		keys = ttyLinux.readLookAhead()
		for player in players :
			player.setDirection(keys)
			player.move()
		writeScreen (40,0,'>>> The owner of the house says (but wait! he is DEAD right ?!?) Dont touch my secret!  ')
	writeScreen (20,0,'')
	os.system("clear")
	print"Sorry you died!! Try again and again!!"
	print"                                                                        "
        print"                      _                                              "
        print"                     ( ) /                                             "
        print"                    \ | /           ||                                    "
        print"                     \|/        ----||----                                         "
        print"   .      . ______    |         ----||----                                        "
        print"     \__/  (hehehe)   |             ||  *            *                        "
        print"     (oo)  /''''''   / \            ||   GAME OVER                             "
        print"    //||\\\         \/   \/          || *           *                             "
        print" .:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:. "
	print"=========================================================================="
	print" Your points: ", you.score 
	print"=========================================================================="
	time.sleep(1)
	playGame()




def playGame2() :
	global clock, inPlay, you, players
	you = You()
	writeBoard ()
	players = [you]
	clock = 0
	inPlay = 1
	while inPlay :
		if you.score == 60:
			print"  WELL DONE! Now lets got to level 3 ......"
			time.sleep(2)
			os.system("clear")
			print" "
			print" THE SEA OF HEARTBREAK !!  -->  "
			time.sleep(3)
			setBoard(5)
			playGame5() ## <-- Change that to playGame3() later on :=)
		clock += 1
		if clock > 40 and len(players) < 3 :
			players.append(Robot(Col=int(random.random()*40+5)))
		time.sleep(.1)
		keys = ttyLinux.readLookAhead()
		for player in players :
			player.setDirection(keys)
			player.move()
		writeScreen (20,0,'<< Robots are humans too!! >..<        ')
	writeScreen (20,0,'')
	
def playGame3() :
	global clock, inPlay, you, players
	you = You()
	writeBoard ()
	players = [you]
	clock = 0
	inPlay = 1
	while inPlay :
		if you.score == 60:
			print"  WELL DONE! Now lets got to level 3 ......"
			time.sleep(2)
			os.system("clear")
			print" "
			print" m/0-0\m  Lets go!!! -->  "
			time.sleep(3)
			setBoard(4)
			playGame4() ## <-- Change that to playGame3() later on :=)
		clock += 1
		if clock > 40 and len(players) < 3 :
			players.append(Robot(Col=int(random.random()*40+5)))
		time.sleep(.1)
		keys = ttyLinux.readLookAhead()
		for player in players :
			player.setDirection(keys)
			player.move()
		writeScreen (20,0,'<< Robots are humans too!! >..<        ')
	writeScreen (20,0,'')
	
def playGame5() :
        global clock, inPlay, you, players
        you = You()
        writeBoard ()
        players = [you]
        clock = 0
        inPlay = 1
        while inPlay :
                if you.score == 120:
                        print"  WELL DONE! ***Near faaar! Where eeeeeverrr you aareee!!  *********"
                        time.sleep(2)
                        os.system("clear")
                        print" "
                        print" m/0-0\m  Lets go!!! -->  "
                        time.sleep(3)
                        setBoard(3)
                        playGame3() ## <-- Change that to playGame3() later on :=)
                clock += 1
                if clock > 40 and len(players) < 3 :
                        players.append(Robot(Col=int(random.random()*40+5)))
                time.sleep(.1)
                keys = ttyLinux.readLookAhead()
                for player in players :
                        player.setDirection(keys)
                        player.move()
                writeScreen (45,0,'Ghost says: ^Do not try to escape before you have collect all coins! ^')
        writeScreen (20,0,'')

	

if __name__ == "__main__" : main()
