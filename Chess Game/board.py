#Initiliazes the global variables to keep up with the states in chess
KingcastlingStateWhite = True
KingcastlingStateBlack = True
QueencastlingStateBlack = True
QueencastlingStateWhite = True
whiteUnderCheck = False
blackUnderCheck = False
whiteMoveMade = False
checkMate = False

class Board:

  #initialize the board and the pieces' position in a 2-D list
  #lowercase lettes represent the black pieces while uppercase letters represent the white pieces
  #8X8 sized list
  chessBoard = [["r", "n" ,"b", "q", "k", "b","n", "r"], 
                ["p", "p" ,"p", "p", "p", "p","p", "p"], #lowercase n = black knight, uppercase N = white knight
                [" ", " " ," ", " ", " ", " "," ", " "], #lowercase r = black rook, uppercase R = white rook
                [" ", " " ," ", " ", " ", " "," ", " "], #lowercase b = black bishop, uppercase B = white bishop
                [" ", " " ," ", " ", " ", " "," ", " "], #lowercase q = black queen, uppercase Q = white queen
                [" ", " " ," ", " ", " ", " "," ", " "], #lowercase k = black king, uppercase K = white king
                ["P", "P" ,"P", "P", "P", "P","P", "P"], #lowercase p = black pawn, uppercase P = white pawn
                ["R", "N" ,"B", "Q", "K", "B","N", "R"]]
  
  #this function is evoked by the GUI to determine the position of the piece that was selected to move              
  def determinePiece(self, move2compare):
    #get the global variables
    global KingcastlingStateBlack
    global KingcastlingStateWhite
    global QueencastlingStateWhite
    global QueencastlingStateBlack

    #variable initialization
    self.move2compare = move2compare
    Kingcolour = ""
    colour = ""

    #get the coordinates of the move that was made
    self.x1 = self.move2compare[0][0]
    self.y1 = self.move2compare[0][1]
    self.x2 = self.move2compare[0][2]
    self.y2 = self.move2compare[0][3]
    

    #get the name of the piece on that particular coordinate
    self.pieceOnBoard = self.chessBoard[self.x1][self.y1]
    
    #get all the possible moves that can be made by that particular piece
    the_possible_moves = self.possibleMoves(self.pieceOnBoard)

    #this if-else statement is required to check for castling moves
    #this following statement checks for king's movement over 1 tiles
    if (self.pieceOnBoard == "K" or self.pieceOnBoard == 'k') and (self.y2 - self.y1 == 2 or self.y2 - self.y1 == -2):

      if KingcastlingStateBlack == True or KingcastlingStateWhite == True or QueencastlingStateWhite == True or QueencastlingStateBlack == True :

        #check for white's castling state
        if self.pieceOnBoard == "K" and (QueencastlingStateWhite == True or KingcastlingStateWhite == True):
          #if the above checks are passed, the Castling function will be called by passing the necessary parameters
          if (self.x2 == 7 and self.y2 == 6) and KingcastlingStateWhite == True:
            self.Kingcolour = "White"
            self.Castling(self.Kingcolour, self.x1, self.y1, self.x2, self.y2)
          #if the above checks are passed, the Castling function will be called by passing the necessary parameters
          elif (self.x2 == 7 and self.y2 == 2) and QueencastlingStateWhite == True:
            self.Kingcolour = "White"
            self.Castling(self.Kingcolour, self.x1, self.y1, self.x2, self.y2)
         
        #checck for black's castling state
        elif self.pieceOnBoard == "k" and  (QueencastlingStateBlack == True or KingcastlingStateBlack == True):
          if (self.x2 == 0 and self.y2 == 6) and KingcastlingStateBlack == True:
            #if the above checks are passed, the Castling function will be called by passing the necessary parameters
            self.Kingcolour ="Black"
            self.Castling(self.Kingcolour, self.x1, self.y1, self.x2, self.y2)
          elif (self.x2 == 0 and self.y2 == 2) and QueencastlingStateBlack == True:
            #if the above checks are passed, the Castling function will be called by passing the necessary parameters
            self.Kingcolour ="Black"
            self.Castling(self.Kingcolour, self.x1, self.y1, self.x2, self.y2)
      else:
        pass

    #possibleOrNot() function is called to check if the proposed move is in the list of the possible moves    
    elif(self.possibleOrNot(self.move2compare, the_possible_moves)):
      #if the above check is passed, then makeMove() function will be fired to execute the move. Parameter 3 is simply given to notify that this is not a castling call.
      self.makeMove(move2compare, 3)
    else:
      pass
    
  #this function deter4mines whether the move made by the players are possible or not by comparing with all the possible moves on the board for the particular piece
  def possibleOrNot(self, proposedMove, thepossibleMoves):

    #variable initialization
    self.proposedMove = proposedMove
    self.possibleMoveslist = thepossibleMoves

    #list initialization
    proposedMove2compare = []

    #get the coordinates of the user's move
    self.x1 = self.proposedMove[0][0]
    self.y1 = self.proposedMove[0][1]
    self.x2 = self.proposedMove[0][2]
    self.y2 = self.proposedMove[0][3]

    #if the user made a move to capture the opponent's piece, then the captured piece will be recorded at the end of the string
    if self.chessBoard[self.x2][self.y2] != " ":
      proposedMove2compare.append((self.x1, self.y1, self.x2, self.y2, self.chessBoard[self.x2][self.y2]))
    else:
      proposedMove2compare.append((self.x1,self.y1,self.x2,self.y2))

    #this function will finally return the boolean value produced from the comparison of the move made by the user and the possible moves of the piece on the board
    return set(proposedMove2compare) <= set(self.possibleMoveslist)

  #this function is responsible for executing the move made by the user.
  #the function takes the move made by the user and a number representing whether it's a casting move or not
  #castling move made for the white piece is denoted by the integer "1", "2" for black and "3" for not castling move
  def makeMove(self, proposedMove, castlingState):
    #get the coordinates of the user's move
    self.x1 = proposedMove[0][0]
    self.y1 = proposedMove[0][1]
    self.x2 = proposedMove[0][2]
    self.y2 = proposedMove[0][3]

    #this statement will initialize the following variable as "White" if the move was made by the black piece player and "Black" if otherwise
    colour_to_check_opponent_threat = "White" if ord(self.chessBoard[self.x1][self.y1]) >= 97 else "Black"

    #get the global variables to update accordingly
    global whiteMoveMade
    global QueencastlingStateWhite
    global KingcastlingStateWhite
    global KingcastlingStateBlack
    global QueencastlingStateBlack
    global blackUnderCheck
    global whiteUnderCheck

    tempPiece = ""
    #get the piece that the user selected to move
    self.getChar = self.chessBoard[self.x1][self.y1]
    #if the piece moved was a king or rook, set the castling state to false. If a rook is moved, the rook will be checked first and then set the state accordingly.
    if self.getChar == "K" or self.getChar == "R":
      #if it was a rook that has been moved, the rook will be identified first
      if self.getChar == "R":
        #if it is the King's side rook, then the King's side castling state will be set to false
        if self.x1 == 7 and self.y1 == 7:
          KingcastlingStateWhite = False
        #if it is the Queen's side rook, then the Queen's side castling state will be set to false.
        elif self.x1 == 7 and self.y1 == 0:
          QueencastlingStateWhite = False
      #if it was the king that has been moved, then both of the castling state will be set to false
      if self.getChar == "K":
        QueencastlingStateWhite = False
        KingcastlingStateWhite = False
    
    elif self.getChar == "k" or self.getChar == "r":
      #if it was a rook that has been moved, the rook will be identified first
      if self.getChar == 'r':
        #if it is the Queen's side rook, then the Queen's side castling state will be set to false
        if self.x1 == 0 and self.y1 == 0:
          QueencastlingStateWhite = False
        #if it is the King's side rook, then the King's side castling state will be set to false
        elif self.x1 == 0 and self.y1 == 7:
          KingcastlingStateBlack = False
      #if it was the king that has been moved, then both of the castling state will be set to false
      if self.getChar == "k":
        QueencastlingStateBlack = False
        KingcastlingStateBlack = False
    else:
      pass

    #check if the move is made by the white piece player
    #the variable whiteMoveMade = False indicates that white piece player has yet to make a move
    if (ord(self.getChar) >= 65 and ord(self.getChar) <= 90) and whiteMoveMade == False:
      

      self.chessBoard[self.x1][self.y1] = " " #make the current tile empty
      tempPiece = self.chessBoard[self.x2][self.y2] #keep the piece of the tile the move was made to in the variable
      self.chessBoard[self.x2][self.y2] = self.getChar #make the tile where the move is made occupied with the piece that was selected to make the move
      whiteMoveMade = True #set the variable to indicate that the white piece player has made a move
      
      
      if self.CheckState("White") == True: #if the white piece player's move exposes the King, then the move will be retreated back
        self.chessBoard[self.x1][self.y1] = self.getChar
        self.chessBoard[self.x2][self.y2] = tempPiece
        whiteMoveMade = False #returns the value back to false
      else:
        #check if the pawn has made it to promotion or not
        self.Promotion_Check("White")

    #check if the move is made by the black piece player
    #the variable whiteMoveMade = False indicates that black piece player has yet to make a move
    elif (ord(self.getChar) >= 97 and ord(self.getChar) <= 122) and whiteMoveMade == True:
      
      self.chessBoard[self.x1][self.y1] = " " #make the current tile empty
      tempPiece = self.chessBoard[self.x2][self.y2] #keep the piece of the tile the move was made to in the variable
      self.chessBoard[self.x2][self.y2] = self.getChar #make the tile where the move is made occupied with the piece that was selected to make the move
      whiteMoveMade = False #set the variable to indicate that the black piece player has made a move

      if self.CheckState("Black") == True: #if the black piece player's move exposes the King, then the move will be retreated back
        
        self.chessBoard[self.x1][self.y1] = self.getChar
        self.chessBoard[self.x2][self.y2] = tempPiece
        whiteMoveMade = True
      else:
        #check if the pawn has made it to promotion or not
        self.Promotion_Check("Black")
    else:
      pass

    #if the move was a castling move, the whiteMoveMade variable will be set to false to allow the Rook to move for the second time after the King
    if castlingState == 1:
      whiteMoveMade = False
    elif castlingState == 2:
      whiteMoveMade = True
    else:
      pass
    
    #CheckState() is a function to check if the move made has "Checked" the opponent's King or not
    if colour_to_check_opponent_threat == "White":
      whiteUnderCheck = self.CheckState(colour_to_check_opponent_threat)
    elif colour_to_check_opponent_threat == "Black":
      blackUnderCheck = self.CheckState(colour_to_check_opponent_threat)
    else:
      pass
    #if the CheckState() function returns true, Check_Checkmate() is called to check if a checkmate is made or not.
    if self.CheckState("Black") == True:
      self.Check_CheckMate("Black")
    if self.CheckState("White") == True: 
      self.Check_CheckMate("White")




  #calculate all the legal moves 
  def possibleMoves(self, piece):

    self.piece = piece
    #initialize the list to store the legal moves
    movesList = []
    #iterates over all the tiles on the board
    for i in range(64):
      
      #in Python3, int have to be used to floor the value

      #check if there's a white rook at the coordinate
      if self.chessBoard[int(i/8)][i%8] == "R" and self.piece == "R":
        movesList += self.RookMove(i, "White")

      #check if there's a black rook at the coordinate
      elif self.chessBoard[int(i/8)][i%8] == 'r' and self.piece == 'r':
        movesList += self.RookMove(i, "Black")
        
      #check if there's a white knight at the coordinate  
      elif self.chessBoard[int(i/8)][i%8] == "N" and self.piece == 'N' :
        movesList += self.KnightMove(i, "White")
      
      #check if there's a black knight at the coordinate  
      elif self.chessBoard[int(i/8)][i%8] == "n" and self.piece == 'n' :
        movesList += self.KnightMove(i, "Black")

      #check if there's a white bishop at the coordinate  
      elif self.chessBoard[int(i/8)][i%8] == "B" and self.piece == 'B' :
        movesList += self.BishopMove(i, "White")

      #check if there's a black bishop at the coordinate
      elif self.chessBoard[int(i/8)][i%8] == "b" and self.piece == 'b' :
        movesList += self.BishopMove(i, "Black")

      #check if there's a white queen at the coordinate
      elif self.chessBoard[int(i/8)][i%8] == "Q" and self.piece == 'Q' :
        movesList += self.QueenMove(i, "White")

      #check if there's a black queen at the coordinate
      elif self.chessBoard[int(i/8)][i%8] == "q" and self.piece == 'q' :
        movesList += self.QueenMove(i, "Black")

      #check if there's a white king at the coordinate
      elif self.chessBoard[int(i/8)][i%8] == "K" and self.piece == 'K' :
        movesList += self.KingMove(i, "White")

      elif self.chessBoard[int(i/8)][i%8] == "k" and self.piece == 'k' :
        movesList += self.KingMove(i, "Black")

      # check if there's a white pawn at the coordinate
      elif self.chessBoard[int(i/8)][i%8] == "P" and self.piece == 'P' :
        movesList += self.WhitePawnMove(i)
        
      # check if there's a black pawn at the coordinate
      elif self.chessBoard[int(i/8)][i%8] == 'p' and self.piece == 'p' :
        movesList += self.BlackPawnMove(i)

    #returns the list of appended movement lists
    return movesList
 

  ################### MOVEMENT OF PIECES #####################################
  

  ############# BEGINNING OF PAWN'S MOVEMENTS ################# 

  #function to calculate the legal moves for white pawns
  def WhitePawnMove(self,position):

    #initialize the list to return later
    moves = []

    #initialize the variable to check if there's a piece in front of the pawn
    firstStepBlock = False

    #get the coordinates
    r = int(position / 8)
    c = position % 8

    # row 6 is white pawn's initial position
    if r == 6:
      #looping for 2 boxes ahead
      for x in range(5, 3, -1):
        #Try-Exception is used to avoid errors regarding out of bounds index when the coordinates are beyond the chess board
        try:
          #check whether the box in front is empty or not
          if self.chessBoard[x][c] == " " and firstStepBlock == False:
            #these 4 lines appends the original position and the target position
            moves.append((r,c,x,c))
            

          else:
            #if there is a piece in front, the variable will be set to true
            firstStepBlock = True

        except Exception as e:
          pass
    else:
      #Try-Exception is used to avoid errors regarding out of bounds index when the coordinates are beyond the chess board
      try:
        if self.chessBoard[r-1][c] == " ":
          #these 4 lines appends the original position and the target position
          moves.append((r,c,r-1,c))
          
      except Exception as e:
        pass
      
      
    if r-1 >= 0:
      #Try-Exception is used to avoid errors regarding out of bounds index when the coordinates are beyond the chess board
      try:
        #test whether the pawns can take any materials or not (ord function cross checks with ASCII characters for lower case characters)
        if ord(self.chessBoard[r-1][c+1]) >= 97 and ord(self.chessBoard[r-1][c+1]) <= 122:
          
          #these 4 lines appends the original position and the target position
          moves.append((r,c, r-1, c+1, self.chessBoard[r-1][c+1]))
      except Exception as e:
        pass
       
    if r-1 >= 0 and c-1 >= 0:
      try:
      #test whether the pawns can take materials or not (ord function cross checks with ASCII characters for lower case characters)
        if ord(self.chessBoard[r-1][c-1]) >= 97 and ord(self.chessBoard[r-1][c-1]) <=122:
          
          #these 4 lines appends the original position and the target position
          moves.append((r,c, r-1, c-1, self.chessBoard[r-1][c-1]))
          
      except Exception as e:
        pass
    
    #returns all the legal moves
    return moves
  ###################### END OF WHITE PAWN'S MOVEMENT ###################

  ###################### BEGINNING OF BLACK PAWN'S MOVEMENT #############
  def BlackPawnMove(self,position):

    #initialize the list to return later
    moves = []

    #initialize the variable to check if there's a piece in front of the pawn
    firstStepBlock = False

    #get the coordinates
    r = int(position / 8)
    c = position % 8

    # row 1 is black pawn's initial position
    if r == 1:
      #looping for 2 boxes ahead
      for x in range(2, 4):
        #Try-Exception is used to avoid errors regarding out of bounds index when the coordinates are beyond the chess board
        try:
          #check whether the box in front is empty or not
          if self.chessBoard[x][c] == " " and firstStepBlock == False:
            #these 4 lines appends the original position and the target position
            moves.append((r,c,x,c))
            

          else:
            #if there is a piece in front, the variable will be set to true
            firstStepBlock = True

        except Exception as e:
          pass
    else:
      #Try-Exception is used to avoid errors regarding out of bounds index when the coordinates are beyond the chess board
      try:
        if self.chessBoard[r+1][c] == " ":
          #these 4 lines appends the original position and the target position
          moves.append((r,c, r+1, c))
          
      except Exception as e:
        pass

    
    #Try-Exception is used to avoid errors regarding out of bounds index when the coordinates are beyond the chess board
    try:
      
      #test whether the pawns can take any materials or not (ord function cross checks with ASCII characters for lower case characters)
      if r+1 >= 0 and c-1 >= 0:
        if ord(self.chessBoard[r+1][c+1]) >= 65 and ord(self.chessBoard[r+1][c+1]) <= 90:
          #these 4 lines appends the original position and the target position
          moves.append((r,c, r+1, c+1, self.chessBoard[r+1][c+1]))
    except Exception as e:
      pass   

    try:
        #test whether the pawns can take materials or not (ord function cross checks with ASCII characters for lower case characters)
        if ord(self.chessBoard[r+1][c-1]) >= 65 and ord(self.chessBoard[r+1][c-1]) <=90:
          #these 4 lines appends the original position and the target position
          moves.append((r,c, r+1, c-1, self.chessBoard[r+1][c-1]))
    except Exception as e:
      pass
          
   
    
    #returns all the legal moves
    return moves

  ###################### END OF BLACK PAWN'S MOVEMENT ###################


  ###################### BEGINNING OF ROOK'S MOVEMENT #############
  def RookMove(self, position, colour):

    #set the variables according to colour of the piece
    if colour == "White":
      #these values represents the range of lowercase letters
      ordA, ordB = 97, 122

    elif colour == "Black":
      #these values represents the range of uppercase letters
      ordA, ordB = 65, 90
      
    #list initialization
    moves = []

    #coordinate of the pieces
    r = int(position / 8)
    c = position % 8
    
    #variable initialization to iterate until the end of the board
    temp = 1
    
    #this loop iterates from -1 to 1 to change the direction of the iterations ( bottom, top ,right and left)
    for j in range (-1, 2, 2):

      #initialize the variable back to 1
      temp = 1
      
      #Try-Exception is used to avoid errors regarding out of bounds index when the coordinates are beyond the chess board
      try:

        #iteration to the end of the board until there's a piece in the way
        while(self.chessBoard[r+temp*j][c] == " " and temp < 8):
          
          #if statement to make sure the value of the row does not go below 0
          if r+temp*j >= 0:
            #append the legal moves to the list
            moves.append((r,c,r+temp*j,c))
          #increase the value to iterate through the remaining boxes
          temp = temp + 1
        
        #check whether there is an enemy's piece to be captured or not
        if ord(self.chessBoard[r+temp*j][c]) >= ordA and ord(self.chessBoard[r+temp*j][c]) <= ordB:

          #if statement to make sure the value of the row does not go below 0
          if r+temp*j >= 0:
            #append the legal moves to the list
            moves.append((r,c,r+temp*j,c, self.chessBoard[r+temp*j][c]))
      
      except IndexError:
        pass

      #initialize the variable back
      temp=1

      #Try-Exception is used to avoid errors regarding out of bounds index when the coordinates are beyond the chess board
      try:
        #iteration to the end of the board until there's a piece in the way
        while(self.chessBoard[r][c+temp*j] == " " and temp < 8):

          #if statement to make sure the value of the column does not go below 0
          if c+temp*j >= 0:
            #append the legal moves to the list
            moves.append((r,c,r,c+temp*j))
          #increase the value to iterate through the remaining boxes
          temp = temp + 1

        #check whether there is an enemy's piece to be captured or not
        if ord(self.chessBoard[r][c+temp*j]) >= ordA and ord(self.chessBoard[r][c+temp*j]) <= ordB:

          #if statement to make sure the value of the column does not go below 0
          if c+temp*j >= 0:
            #append the legal moves to the list
            moves.append((r,c,r,c+temp*j,self.chessBoard[r][c+temp*j]))

      except IndexError:
        pass
    #returns all the legal moves
    return moves

   ###################### END OF ROOK'S MOVEMENT #############

   ########### BEGINNING OF KNIGHTS' MOVEMENT ########################

  def KnightMove(self, position, colour):

     #set the variables according to colour of the piece
    if colour == "White":
      #these values represents the range of lowercase letters
      ordA, ordB = 97, 122

    elif colour == "Black":
      #these values represents the range of uppercase letters
      ordA, ordB = 65, 90

    #list initialization
    moves = []

    #get the coordinate
    r = int(position / 8)
    c = position % 8
    
    #these nested loops will complete all the 8 possible route for a knight
    for j in range(-1 ,2, 2):
  
      for k in range(-1, 2, 2):
        
        #Try-Exception is used to avoid errors regarding out of bounds index when the coordinates are beyond the chess board
        try:
          #checks if the target box is empty or occupied with an enemy's piece
          if self.chessBoard[r+j][c+k*2] == " " or (ord(self.chessBoard[r+j][c+k*2]) >= ordA and ord(self.chessBoard[r+j][c+k*2]) <= ordB):

            
            #makes sure the row or column does not have a value less than 0
            if r+j >=0 and c+k*2 >= 0:
              #append the legal moves into the list
              if self.chessBoard[r+j][c+k*2] == " ":
                moves.append((r,c,r+j,c+k*2))
              else:
                moves.append((r,c,r+j,c+k*2,self.chessBoard[r+j][c+k*2]))

        except IndexError:
          pass
        
        #Try-Exception is used to avoid errors regarding out of bounds index when the coordinates are beyond the chess board
        try:
          #checks if the target box is empty or occupied with an enemy's piece
          if self.chessBoard[r+j*2][c+k] == " " or (ord(self.chessBoard[r+j*2][c+k]) >= ordA and ord(self.chessBoard[r+j*2][c+k]) <= ordB):

            #makes sure the row or column does not have a value less than 0
            if r+j*2 >= 0 and c+k >= 0:
              #append the legal moves into the list
              if self.chessBoard[r+j*2][c+k] == " ":
                moves.append((r,c,r+j*2,c+k))
              else:
                moves.append((r,c,r+j*2,c+k,self.chessBoard[r+j*2][c+k]))

        except IndexError:
          pass

    #return all the possible moves
    return moves

  ###### END OF KNIGHT'S MOVEMENT #########################################

  ###### BEGINNING OF BISHOP'S MOVEMENT ######################################
  

  def BishopMove(self, position, colour):

     #set the variables according to colour of the piece
    if colour == "White":
      #these values represents the range of lowercase letters
      ordA, ordB = 97, 122

    elif colour == "Black":
      #these values represents the range of uppercase letters
      ordA, ordB = 65, 90

    #initialize list
    moves = []

    #get the coordinate
    r = int(position / 8)
    c = position % 8
    
    #variable initialization to iterate through the diagonal line to the end
    temp = 1
    
    #these nested loops will be responsible for the movement to top, bottom, right and left by constantly changing from -1 to 1
    for j in range(-1,2,2):
      
      for k in range(-1,2,2):

        #initialize it back
        temp = 1

        #Try-Exception is used to avoid errors regarding out of bounds index when the coordinates are beyond the chess board
        try:
          #this while loop will iterate until there is no empty box to the end of the board
          while (self.chessBoard[r+temp*j][c+temp*k] == " " and temp < 8):

            #test to make sure the value of the row and column does not go below 0
            if r+temp*j >= 0 and c+temp*k >= 0:
                #append the legal moves into the list
                moves.append((r,c,r+temp*j,c+temp*k))
                
            #increase the value to iterate through the remaining boxes
            temp = temp + 1
          
          #check whether there is an enemy's piece to be captured or not
          if (ord(self.chessBoard[r+temp*j][c+temp*k]) >= ordA and ord(self.chessBoard[r+temp*j][c+temp*k]) <=ordB) and temp < 8 :
            
            #test to make sure the value of the row and column does not go below 0
            if r+temp*j >= 0 and c+temp*k >= 0:

              #append the legal moves into the list
              moves.append((r,c, r+temp*j, c+temp*k, self.chessBoard[r+temp*j][c+temp*k]))

        except IndexError:
          pass

    return moves
  ########## ENDING OF THE WHITE BISHOP'S MOVEMENT #######################

  ########## BEGINNING OF THE WHITE QUEEN'S MOVEMENT #####################
  def QueenMove(self, position, colour):

     #set the variables according to colour of the piece
    if colour == "White":
      #these values represents the range of lowercase letters
      ordA, ordB = 97, 122

    elif colour == "Black":
      #these values represents the range of uppercase letters
      ordA, ordB = 65, 90

    #initialize list
    moves = []

    #get the coordinate
    r = int(position / 8)
    c = position % 8
    
    #initialize the variable 
    temp = 1
    
    #nested loop that implements the movement of a rook and bishop
    #first loop for the horizontal and vertical iteration
    for j in range(-1,2,2):

      #initialize the variable to iterate all over again
      temp = 1
   
      #Try-Exception is used to avoid errors regarding out of bounds index when the coordinates are beyond the chess board
      try:
          
          #iterate through the boxes vertically both way
          while(self.chessBoard[r+temp*j][c] == " " and temp < 8):
            
            #makes sure that the index of the row does not go below 0
            if r+temp*j >= 0:
              #append the legal moves into the list
              moves.append((r,c,r+temp*j,c))
      
            #increase the value to iterate through the remaining boxes
            temp = temp + 1
          
          #check whether there is an enemy's piece to be captured or not
          if (ord(self.chessBoard[r+temp*j][c]) >= ordA and ord(self.chessBoard[r+temp*j][c]) <= ordB) and temp < 8:
            #makes sure that the index of the row does not go below 0
            if r+temp*j >= 0:
              #append the legal moves into the list
              moves.append((r,c,r+temp*j,c, self.chessBoard[r+temp*j][c]))

      except IndexError:
        pass     

      #initialize back the variable  
      temp = 1

      #Try-Exception is used to avoid errors regarding out of bounds index when the coordinates are beyond the chess board
      try:
        #iterate through the boxes horizontally both way
        while (self.chessBoard[r][c+temp*j] == " " and temp < 8):

          #makes sure that the index of the column does not go below 0
          if c+temp*j >= 0:
            #append the legal moves into the list
            moves.append((r,c,r,c+temp*j))

          temp = temp + 1

        if (ord(self.chessBoard[r][c+temp*j]) >= ordA and ord(self.chessBoard[r][c+temp*j]) <= ordB ) and temp < 8:

          #makes sure that the index of the column does not go below 0
          if c+temp*j  >= 0:
            #append the legal moves into the list
            moves.append((r,c,r,c+temp*j,self.chessBoard[r][c+temp*j]))
           
      except IndexError:
        pass
      
      #second loop for the diagonal iteration
      for k in range(-1,2,2):

        #initialize back the variable
        temp = 1

        #iterate through the boxes diagonally both way
        try:
          while (self.chessBoard[r+temp*j][c+temp*k] == " " and temp < 8):

            #makes sure that the index of the column and row does not go below 0
            if r+temp*j >= 0 and c+temp*k >=0 :
              #append the legal moves into the list
              moves.append((r,c, r+temp*j, c+temp*k))
            #increase the value to iterate through the remaining boxes
            temp = temp + 1

          #check whether there is an enemy's piece to be captured or not
          if (ord(self.chessBoard[r+temp*j][c+temp*k]) >= ordA and ord(self.chessBoard[r+temp*j][c+temp*k]) <= ordB) and temp < 8:

            #makes sure that the index of the column and row does not go below 0
            if r+temp*j >= 0 and c+temp*k >= 0:
              #append the legal moves into the list
              moves.append((r,c, r+temp*j, c+temp*k, self.chessBoard[r+temp*j][c+temp*k]))
        
        except IndexError:
          pass
    #returns all the legal moves
    return moves

    ################## ENDING OF THE QUEEN'S MOVEMENT ############################

    ################## BEGINNING OF THE KING'S MOVEMENT ##########################

  def KingMove(self, position, colour):

     #set the variables according to colour of the piece
    if colour == "White":
      #these values represents the range of lowercase letters
      ordA, ordB = 97, 122

    elif colour == "Black":
      #these values represents the range of uppercase letters
      ordA, ordB = 65, 90

    #initialize the list
    moves = []

    #get the coordinate
    r = int(position / 8)
    c = position % 8

    #initialize the variable 
    temp = 1
    
    #nested loop that implements the movement of a rook and bishop
    #first loop for the horizontal and vertical iteration
    for j in range(-1,2,2):

      #initialize the variable to iterate all over again
      temp = 1
   
      #Try-Exception is used to avoid errors regarding out of bounds index when the coordinates are beyond the chess board
      try:
          
          #iterate through the boxes vertically both way
          while(self.chessBoard[r+temp*j][c] == " " and temp < 2):
            
            #makes sure that the index of the row does not go below 0
            if r+temp*j >= 0:
              #append the legal moves into the list
              moves.append((r,c, r+temp*j, c))
            #increase the value to iterate through the remaining boxes
            temp = temp + 1
          
          #check whether there is an enemy's piece to be captured or not
          if (ord(self.chessBoard[r+temp*j][c]) >= ordA and ord(self.chessBoard[r+temp*j][c]) <= ordB) and temp < 2:
            #makes sure that the index of the row does not go below 0
            if r+temp*j >= 0:
              #append the legal moves into the list
              moves.append((r,c, r+temp*j,c, self.chessBoard[r+temp*j][c]))
  

      except IndexError:
        pass     

      #initialize back the variable  
      temp = 1

      #Try-Exception is used to avoid errors regarding out of bounds index when the coordinates are beyond the chess board
      try:
        #iterate through the boxes horizontally both way
        while (self.chessBoard[r][c+temp*j] == " " and temp < 2):

          #makes sure that the index of the column does not go below 0
          if c+temp*j >= 0:
            #append the legal moves into the list
            moves.append((r,c,r,c+temp*j))

          temp = temp + 1

        if (ord(self.chessBoard[r][c+temp*j]) >= ordA and ord(self.chessBoard[r][c+temp*j]) <= ordB ) and temp < 2:

          #makes sure that the index of the column does not go below 0
          if c+temp*j  >= 0:
            #append the legal moves into the list
            moves.append((r,c,r,c+temp*j, self.chessBoard[r][c+temp*j]))
            
      except IndexError:
        pass
      
      #second loop for the diagonal iteration
      for k in range(-1,2,2):

        #initialize back the variable
        temp = 1

        #iterate through the boxes diagonally both way
        try:
          while (self.chessBoard[r+temp*j][c+temp*k] == " " and temp < 2):

            #makes sure that the index of the column and row does not go below 0
            if r+temp*j >= 0 and c+temp*k >=0 :
              #append the legal moves into the list
              moves.append((r,c, r+temp*j, c+temp*k))
              
            #increase the value to iterate through the remaining boxes
            temp = temp + 1

          #check whether there is an enemy's piece to be captured or not
          if (ord(self.chessBoard[r+temp*j][c+temp*k]) >= ordA and ord(self.chessBoard[r+temp*j][c+temp*k]) <= ordB) and temp < 2:

            #makes sure that the index of the column and row does not go below 0
            if r+temp*j >= 0 and c+temp*k >= 0:
              #append the legal moves into the list
              moves.append((r,c, r+temp*j, c+temp*k, self.chessBoard[r+temp*j][c+temp*k]))
              
        
        except IndexError:
          pass
    return moves

  ################## END OF THE KING'S MOVEMENT ##########################

######################################## END OF PIECES' MOVEMENT ##########################################



######################## THREAD DETECTION AND CASTLING ##################################################

  #function to perform castling  
  def Castling(self, colour, x1, y1, x2, y2):

    #variable initialization
    KingMove = []
    RookMove = []
    castlingAbility = True
    
    #check to see if the castling move was made by white piece player
    #x1 = 7 and y1 = 4 indicates that the King is in the initial position
    if colour == "White" and x1 == 7 and y1 == 4:
      #x2 = 7 and y2 = 6 indicates that the King is moved to the right side 2 tiles (King's side castling)
      if x2 == 7 and y2 == 6:
        #check if there exists a rook at the right end and the tiles between are empty
        if self.chessBoard[7][7] == "R" and self.chessBoard[7][5] == " " and self.chessBoard[7][6] == " ":
          #initialize these sets to check if they are attacked
          setA = [7,5]
          setB = [7,6]
          #Check_Opponent_Threat() is a function that detects all the threats that are made by a certain player
          for every_set in self.Check_Opponent_Threat("White", "Threat"):
            #if there exists a threat on the tiles that are about to be passed by the King, the castlingAbility variable will be set to false to deny the castling move
            if setA == every_set:
              castlingAbility = False
            if setB == every_set:
              castlingAbility = False
          #if there exists no threat on the selected tiles, the castling move can proceed
          if castlingAbility == True:
            #calling the makeMove function with parameter 1 to denote the white's castling move
            #calling the makeMove function for the second time with parameter 3 to denote the end of castling move
            KingMove.append((x1,y1,x2,y2))
            RookMove.append((7,7,7,5))
            self.makeMove(KingMove, 1)
            self.makeMove(RookMove, 3)
         
          
        else:
          pass
      #x2 = 7 and y2 = 2 indicates that the King is moved to the left side 2 tiles (Quuen's side castling)
      elif x2 == 7 and y2 == 2:
        #check if there exists a rook at the left end and the tiles between are empty
        if self.chessBoard[7][0] == "R" and self.chessBoard[7][1] == " " and self.chessBoard[7][2] == " " and self.chessBoard[7][3] == " ":
          #initialize these sets to check if they are attacked
          setA = [7,2]
          setB = [7,3]

          #Check_Opponent_Threat() is a function that detects all the threats that are made by a certain player
          for every_set in self.Check_Opponent_Threat("White", "Threat"):
            #if there exists a threat on the tiles that are about to be passed by the King, the castlingAbility variable will be set to false to deny the castling move
            if setA == every_set:
              castlingAbility = False
           
            if setB == every_set:
              castlingAbility = False
              
            

          if castlingAbility == True:
            #calling the makeMove function with parameter 1 to denote the white's castling move
            #calling the makeMove function for the second time with parameter 3 to denote the end of castling move
            KingMove.append((x1,y1,x2,y2))
            RookMove.append((7,0,7,3))
            self.makeMove(KingMove, 1)
            self.makeMove(RookMove, 3)
        else:
          pass
    #check to see if the castling move was made by black piece player
    elif colour == "Black" and x1 == 0 and y1 == 4:
      #x2 = 0 and y2 = 6 indicates that the King is moved to the right side 2 tiles (King's side castling)
      if x2 == 0 and y2 == 6:
        #check if there exists a rook at the right end and the tiles between are empty
        if self.chessBoard[0][7] == "r" and self.chessBoard[0][6] == " " and self.chessBoard[0][5] == " ":
          #initialize these sets to check if they are attacked
          setA = [0,6]
          setB = [0,5]

          #Check_Opponent_Threat() is a function that detects all the threats that are made by a certain player
          for every_set in self.Check_Opponent_Threat("Black", "Threat"):
            #if there exists a threat on the tiles that are about to be passed by the King, the castlingAbility variable will be set to false to deny the castling move
            if setA == every_set:
              castlingAbility = False
           
            if setB == every_set:
              castlingAbility = False

          if castlingAbility == True:
            #calling the makeMove function with parameter 2 to denote the black's castling move
            #calling the makeMove function for the second time with parameter 3 to denote the end of castling move
            KingMove.append((x1,y1,x2,y2))
            RookMove.append((0,7,0,5))
            self.makeMove(KingMove, 2)
            self.makeMove(RookMove, 3)

        else:
          pass
      #x2 = 0 and y2 = 2 indicates that the King is moved to the left side 2 tiles (Queen's side castling)
      elif x2 == 0 and y2 == 2:
        #check if there exists a rook at the right end and the tiles between are empty
        if self.chessBoard[0][0] == "r" and self.chessBoard[0][1] == " " and self.chessBoard[0][2] == " " and self.chessBoard[0][3] == " ":
          #initialize these sets to check if they are attacked
          setA = [0,2]
          setB = [0,3]
          #Check_Opponent_Threat() is a function that detects all the threats that are made by a certain player
          for every_set in self.Check_Opponent_Threat("Black", "Threat"):
            #if there exists a threat on the tiles that are about to be passed by the King, the castlingAbility variable will be set to false to deny the castling move
            if setA == every_set:
              castlingAbility = False
           
            if setB == every_set:
              castlingAbility = False

          if castlingAbility == True:
            #calling the makeMove function with parameter 2 to denote the black's castling move
            #calling the makeMove function for the second time with parameter 3 to denote the end of castling move
            KingMove.append((x1,y1,x2,y2))
            RookMove.append((0,0,0,3))
            self.makeMove(KingMove, 2)
            self.makeMove(RookMove, 3)
          
        else:
          pass

  #this function is to check a particular player's threat to the other player
  #this function is can also be used to return all the possible moves that can be made by a player, thus the paremeter desire is used accordingly
  #note that this function is not the same as the possibleMoves() function as possiblMoves() function can only be passed with one single character at one time (Means can only calculate the possible moves of one particular piece)
  def Check_Opponent_Threat(self, colour, desire):
    #create a list of pieces for black and white players
    mylists_for_black = ["p","r","n","b","q","k"]
    mylists_for_white = ["P","R","N","B","Q","K"]
    all_the_possible_moves = []
    threats = []

    
    #if the parameter was passed in with "White" colour, then the possible moves for black will be generated and vice versa
    if colour == "White":
      #iterate through all the 6 pieces
      for i in range(6):
        all_the_possible_moves += self.possibleMoves(mylists_for_black[i])

    elif colour == "Black":
      #iterate through all the 6 pieces
      for i in range(6):
        all_the_possible_moves += self.possibleMoves(mylists_for_white[i])  
    else:
      pass  
    #if the desire was only to calculate the possible moves, then the function shall return the possible moves immediately
    if desire == "PossibleMovesOnly":
      # print(all_the_possible_moves)
      return all_the_possible_moves

    else:
    #this loop returns just the last 2 values of the coordinate, 3 if there's a piece that can be captured
      for k in range(len(all_the_possible_moves)):
        #variable initialization is made here so that it will be emptied everytime a loop of k is made
        temp=[]
        temp1 = []
        for j in range(2, len(all_the_possible_moves[k])):

          temp.append(all_the_possible_moves[k][j])

          if j == len(all_the_possible_moves[k]) - 1:
            temp1.append((temp))
            threats += temp1

      #returns the list of the threats
      return threats

  #this function is used to check whether a player is in Check or not
  def CheckState(self,colour):

    #initialize the variables
    check_state = False
    colour_to_check = ""
    setA = []

    #set the King's character according to the colour
    if colour == "White":
      setA = ["K"]
      colour_to_check = "White"
    elif colour == "Black":
      setA = ["k"]
      colour_to_check = "Black"

    #get the threats of the opponent player
    threat = self.Check_Opponent_Threat(colour_to_check, "Threat")
    #check if there exists a "K" or 'k' in the threats
    for each in threat:
      #comparison
      if set(setA) <= set(each):
        check_state = True
      
    #returns the boolean value of the check_state
    return check_state

  #this function is to check whether a player has been checkmated or not
  #this is the function that fires when a player is in check
  def Check_CheckMate(self, colour):

    if colour == "White":
      #by giving the parameter "PossibleMovesOnly" to the Check_Opponent_Threat() function, the function will return only the possible moves, not the threats.
      allPossibleMoves = self.Check_Opponent_Threat("Black", "PossibleMovesOnly")
      #initialize counter
      counter = 0
      
      #iterate through all the possible moves
      for each_possible_move in allPossibleMoves:

        #get the coordinates of the possible moves
        x1 = each_possible_move[0]
        y1 = each_possible_move[1]
        x2 = each_possible_move[2]
        y2 = each_possible_move[3]


        self.character = self.chessBoard[x1][y1] #get the piece 
        self.chessBoard[x1][y1] = " " #empty the current tile
        tempPiece = self.chessBoard[x2][y2] #get the piece in the tile that the move has been made to
        self.chessBoard[x2][y2] = self.character #replace the tile that the move was made to with the piece that the move was made
    
        #for every move of white that ends in check, the counter will be increased by 1
        if self.CheckState("White") == True:
          counter = counter + 1
        #undo back the move
        self.chessBoard[x1][y1] = self.character
        self.chessBoard[x2][y2] = tempPiece

      #if every single move of white ends in Check, that denotes Checkmate!
      if counter == len(allPossibleMoves):
        print("Checkmate")

    #Checkmate test for black
    elif colour == "Black":
      #by giving the parameter "PossibleMovesOnly" to the Check_Opponent_Threat() function, the function will return only the possible moves, not the threats.
      allPossibleMoves = self.Check_Opponent_Threat("White", "PossibleMovesOnly")
      #initialize counter
      counter = 0
      
      #iterate through all the possible moves
      for each_possible_move in allPossibleMoves:
        #get the coordinates of the possible moves
        x1 = each_possible_move[0]
        y1 = each_possible_move[1]
        x2 = each_possible_move[2]
        y2 = each_possible_move[3]



        self.character = self.chessBoard[x1][y1]#get the piece 
        self.chessBoard[x1][y1] = " " #empty the current tile
        tempPiece = self.chessBoard[x2][y2] #get the piece in the tile that the move has been made to
        self.chessBoard[x2][y2] = self.character #replace the tile that the move was made to with the piece that the move was made
        
        #if every single move of black ends in Check, that denotes Checkmate!
        if self.CheckState("Black") == True:
          counter = counter + 1
        #undo back the move
        self.chessBoard[x1][y1] = self.character
        self.chessBoard[x2][y2] = tempPiece

      #if every single move of black ends in Check, that denotes Checkmate!
      if counter == len(allPossibleMoves):
        print("Checkmate")


  #this function is used to check if there's a pawn that has reached the final rank
  def Promotion_Check(self, colour):
    
    #if the check is performed for the white piece player, then the row that should be checked is row 0
    if colour == "White":
      row = 0

    #if the check is performed for the white piece player, then the row that should be checked is row 7
    if colour == "Black":
      row = 7

    #this iterates through all the column in that particular row
    for i in range(8):
      #check if there is a pawn on that particular row
      if self.chessBoard[row][i] == "P":
        #if there exists a white pawn in the final rank, the Promotion_Pick() function will be called by passing three parameters. The colour of the piece, the row and the column the piece is located.
        self.Promotion_Pick("White", row, i)
      elif self.chessBoard[row][i] == 'p':
        #if there exists a black pawn in the final rank, the Promotion_Pick() function will be called by passing three parameters. The colour of the piece, the row and the column the piece is located.
        self.Promotion_Pick("Black", row, i)
  

  #this function is called when there is a promotion move available for any of the two players
  def Promotion_Pick(self, colour, row, column):
    #initiliaze the variable
    promotionpiece=""

    #these 2 lines is to prompt the players for their desired promotion piece
    print("What would you like your pawn to be promoted to? Default is Queen")
    promotionpiece = input()

    #for players that play the white pieces 
    if colour=="White":
      
      if promotionpiece == "Rook":
        #replaces the pawn's position with a Rook
        self.chessBoard[row][column] = "R"
      elif promotionpiece == "Queen":
        #replaces the pawn's position with a Queen
        self.chessBoard[row][column] = "Q"
      elif promotionpiece == "Knight":
        #replaces the pawn's position with a Knight
        self.chessBoard[row][column] = "N"
      elif promotionpiece == "Bishop":
        #replaces the pawn's position with a Bishop
        self.chessBoard[row][column] = "B"
      else:
        #if the user did not enter anything, or entered something else other than the 4 words above, a Queen will be automatically given
        self.chessBoard[row][column] = "Q"

    #for players that play the black pieces
    if colour=="Black":
      if promotionpiece == "Rook":
        #replaces the pawn's position with a Rook
        self.chessBoard[row][column] = "r"
      elif promotionpiece == "Queen":
        #replaces the pawn's position with a Queen
        self.chessBoard[row][column] = "q"
      elif promotionpiece == "Knight":
        #replaces the pawn's position with a Knight
        self.chessBoard[row][column] = "n"
      elif promotionpiece == "Bishop":
        #replaces the pawn's position with a Bishop
        self.chessBoard[row][column] = "b"
      else:
        #if the user did not enter anything, or entered something else other than the 4 words above, a Queen will be automatically given
        self.chessBoard[row][column] = "q"

        