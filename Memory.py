import random #to shuffle cards and randomize first player
ROWS_DIM=6
COLS_DIM=7
NUM_PLAYERS=2

#blueprint for each card
class Card:
    def __init__(self,r,c,v):
        self.c=c #column attribute per card
        self.r=r #row attribute per card
        self.v=v #value attribute per card
        self.row=0
        self.col=0
        self.owner=5 # attaches card color to the player who won the two cards. Later assigned '0' if player color is Red or '1' if player color is Blue
        self.flipped=False #Indicates 'flipped mode' of card. Switched to true if card is flipped
        self.img=loadImage(str(self.v)+'.png')  #image attribute of each card
        self.card_back=loadImage('cardBack.png') #card back attribute of each card
    
    def display(self): #displays card back when called  
        image(self.card_back,5+self.c*105,5+self.r*105) 
            
    def displayPokemon(self,row,col): #displays card value when called
        self.col=col
        self.row=row
        image(self.img,5+self.col*105,self.row*105)

#blueprint for overall set of cards (Cards Deck )   
class Deck:
    def __init__(self,numRows,numCols):
        self.numRows = numRows #row dimensions
        self.numCols = numCols #column dimensions
        self.board = [] #card deck
        self.pause=0 #2 second pausing functionality
        self.match=False #Indicates whether card has been matched or not
            
    def createBoard(self):
        self.font=loadFont('data/memorygame.vlw')
           
        card_list=[] #temporary list to shuffle card values to create board shuffling effect
        for num in range((self.numRows*self.numCols)//2):
            card_list.append(num)
            card_list.append(num)                            
        
        random.shuffle(card_list) #shuffling functionality
        
        #create card 'board'
        cnt=0        
        for r in range(self.numRows):
            for c in range(self.numCols):
                self.board.append(Card(r,c,str(card_list[cnt]))) #add cards 
                cnt+=1
                
    #enables access to card by row and column value
    def getCard (self,r,c): 
        for card in self.board:
            if card.r == r and card.c == c:
                return card
    
    #enables access to card by value
    def getCardByValue (self,v):
        for card in self.board:
            if card.v == v:
                return card    
    
    #main card set display functionality
    def display(self):     
          
        if self.pause>0: #temporaily pauses game to enbale players view selected cards
            self.pause-=1
            return
        background(0)
        
        for card in self.board:
            if card.flipped==True: #helps highlight card and maintain card highlight if 'flipped' remains true               
                if g1.turn==0: #if player turn is playerRed
                    #highlight card border
                    stroke(200,0,0)
                    strokeWeight(7)
                    rect(2+card.c*105,2+card.r*105,101,101)
                if g1.turn==1: #if player turn is playerBlue
                    #highlight card border
                    stroke(0,0,200)
                    strokeWeight(7)
                    rect(2+card.c*105,2+card.r*105,101,101)
                    
                if card.owner==0: #if owner of card is playerRed
                    #highlight card border
                    stroke(200,0,0)
                    strokeWeight(7)
                    rect(2+card.c*105,2+card.r*105,101,101)
                    
                if card.owner==1: #if owner of card is playerRed
                    #highlight card border
                    stroke(0,0,200)
                    strokeWeight(7)
                    rect(2+card.c*105,2+card.r*105,101,101)
                                            
                strokeWeight(7)
                #rect(2+card.c*105,2+card.r*105,101,101)
                noFill()
                card.displayPokemon(card.r,card.c) #display Pokemon card
                
            else: #if card is not in 'flipped' stage, display card back
                card.display()
        
        #SIDE DISPLAYS ON RIGHT-HAND SIDE OF GAME
        fill(255)
        stroke(204,102,0)
        strokeWeight(9)
        rect(COLS_DIM*105+50,20,300,49) 
        textFont(self.font,32)
        textSize(32)
        fill(0)
        text('MEMORY GAME',COLS_DIM*106+70,55) #print('Memory Game')
        
        fill(255)
        stroke(204,102,0)
        strokeWeight(9)
        rect(COLS_DIM*105+50,90,300,49) 
        textFont(self.font,32)
        textSize(32)
        fill(255,0,0)
        text('Player Red: '+str(int(g1.playerRed)),COLS_DIM*106+70,125) #print playerRed score
        
        fill(255)
        stroke(204,102,0)
        strokeWeight(9)
        rect(COLS_DIM*105+50,160,300,49) 
        textFont(self.font,32)
        textSize(32)
        fill(0,0,255)
        text('Player Blue: '+str(int(g1.playerBlue)),COLS_DIM*106+70,195) #print playerBlue score
        
        if len(g1.plays)>=ROWS_DIM*COLS_DIM:
            fill(255)
            stroke(204,102,0)
            strokeWeight(9)
            rect(COLS_DIM*105+50,230,300,49) 
            textFont(self.font,32)
            textSize(32)
            fill(0)
            if int(g1.playerRed)>int(g1.playerBlue): #announce winner
                text('Player Red Wins',COLS_DIM*106+70,265)
            elif int(g1.playerRed)<int(g1.playerBlue): #announce winner
                text('Player Blue Wins',COLS_DIM*106+70,265)
            else:
                text('Draw!',COLS_DIM*106+70,265)
                
                
        noFill()
     
    def flip_card(self,r,c): #flip and show card when called
        for card in self.board:
            if card.r == r and card.c == c:
                card.displayPokemon(r,c)
                card.flipped=True
    
    def un_flip_card_by_value(self,v): #enable unflipping of card using card value
        for card in self.board:
            if card.v==v:
                # card.displayPokemon(card.r,card.c)
                card.flipped=False
        
    def un_flip(self,r,c): #enable unflipping of card using card row and column value
        for card in self.board:
            if card.r == r and card.c == c:
                card.flipped=False    
                          
d1=Deck(ROWS_DIM,COLS_DIM) #create object from Deck class

class Game:
    def __init__(self):
        self.checklist=[] #list to check if card values are the same
        self.plays=[] #stores cards that have been matched to ensure they remain on screen
        self.numplayers=NUM_PLAYERS
        self.turn=random.randint(0,self.numplayers-1)
        self.r=0
        self.c=0
        self.v=0
        self.obj=0
        self.matched=False #changed to True if two selected cards match
        self.playerRed=0.0 #player Red score
        self.playerBlue=0.0 #player Blue score
        self.rows=[] #checks if same card is not selected twice and counted as a match
        self.cols=[] #checks if same card is not selected twice and counted as a match
    
    #Card Match Checker and Main Game Manager Upon Clicking
    def checker(self,r,c,value,obj):    
        
        self.r=r #row of card clicked
        self.r=c #column of card clicked
        self.v=value #value of clicked card
        self.obj=obj #card object
        if len(self.checklist)!=2: #if two cards have not been clicked yet, add card value to checklist
            self.checklist.append(value)
            self.rows.append(r)
            self.cols.append(c)
                       
        if len(self.checklist)==2: #if two cards have been clicked, analyze cards
               
            #if card values are the same and cards do not exist at the same position ,ie. potential winning of the two cards    
            if self.checklist[0]==self.checklist[1] and (((self.rows[0]==self.rows[1] and self.cols[0]!=self.cols[1]) or (self.rows[0]!=self.rows[1] and self.cols[0]==self.cols[1])) or (self.rows[0]!=self.rows[1] and self.cols[0]!=self.cols[1])):
                #record that the card has been matched
                self.plays.append(self.checklist[0])
                self.plays.append(self.checklist[1])
                for card in d1.board:
                    if card.v in self.checklist:
                        if self.turn==0: #if current player is playerRed
                            card.owner=0 #make owner of card playerRed
                            self.playerRed+=0.5 #increase playerRed score
                        if self.turn==1:
                            card.owner=1
                            self.playerBlue+=0.5 #increase playerBlue score
                self.checklist=[] #empty checklist and wait for next two cards that are clicked
                self.rows=[] #empty rows list and wait for next two cards that are clicked
                self.cols=[] #empty cols list and wait for next two cards that are clicked
                self.matched=True  #verify that cards were matched                    
                
                for card in d1.board:
                    if card.v in self.plays:
                        card.flipped=True #keep matched cards flipped up
                               
            else:
                d1.display()
                d1.pause=60*2 #pauses game for two seconds to enable users temporarily see selected cards
               
                for card in d1.board:
                    if card.v not in self.plays: #if card is not a matched card, unflip it back
                        d1.un_flip_card_by_value(card.v)
                        card.flipped=False #unflip card back
                        card.owner=4
                self.checklist=[] #empty checker check list
                self.rows=[] #empty rows list and wait for next two cards that are clicked
                self.cols=[] #empty cols list and wait for next two cards that are clicked
                #alternate between players only if player didnt get cards to match
                self.turn=(self.turn+1)%self.numplayers 
                        
g1=Game()  #start game functionality

def setup():
    size(COLS_DIM*105+5+400,ROWS_DIM*105+5+80)
    background(0) #set black background    
    d1.createBoard()
    
def draw():
    d1.display()

def mouseClicked():
    if d1.pause>0:
        return
    #put width and height within normal column and row range
    c=mouseX//105 
    r=mouseY//105
    
    #whenever mouse is clicked, if card is at that location, flip it up
    d1.flip_card(r,c)
    for card in d1.board:
        if card.r == r and card.c == c:      
            g1.checker(r,c,card.v,card)#send card data for evaluation in checker method
            
    