from random import randint
from tkinter import *
from tkinter import messagebox
import functools

class Tile:
	value = 0
	xCoord = 0
	yCoord = 0
	X = [0, -1, 1, 0]
	Y = [-1, 0, 0, 1]

	def __init__(self, value, xCoord, yCoord):
		self.value = value
		self.xCoord = xCoord
		self.yCoord = yCoord

	def slide(self, tile8Puzzle, Tile8PuzzleBoard):
		for i in range(4):
			newY = self.yCoord+self.Y[i]
			newX = self.xCoord+self.X[i]
			if self.isInRange(newX, newY) and tile8Puzzle.board[newX][newY].value == 0:
				tile8Puzzle.board[newX][newY].value, self.value = self.value, tile8Puzzle.board[newX][newY].value
				print(str(self.xCoord) +" "+ str(self.yCoord) +" "+ str(newX) +" "+ str(newY))
				Tile8PuzzleBoard.swapTiles(self.xCoord, self.yCoord, newX, newY)
				return
		messagebox.showinfo("Invalid move", "Only neighbouring tiles of 0 can be moved!")
		
	@classmethod
	def isInRange(self, x, y):
		if x >= 0 and x < 3 and y >= 0 and y < 3:
			return True
		return False

class Tile8Puzzle:
	"""8TileBoard"""
	board = [[0 for x in range(3)] for y in range(3)]
	solution = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
	def __init__(self):
		self.createRandomBoard()

	@classmethod
	def createRandomBoard(self):
		tile = randint(0, 8)
		hash = [0 for x in range(10)]
		for i in range(3):
			for j in range(3):
				while hash[tile] == 1:
					tile = randint(0, 8)
				self.board[i][j] = Tile(tile, i, j)
				hash[tile] = 1

	def printBoard(self):
		for i in range(3):
			for tile in self.board[i]:
				print(tile.value, end=" ")
			print()

	def isGameOver(self):
		for i in range(3):
			for j in range(3):
				if self.board[i][j] != self.solution[i][j]:
					return False;
		return True


class Tile8PuzzleBoard:
	gameBoard = [[0 for x in range(3)] for y in range(3)]
	puzzle = 0
	GameFrame = 0
	steps = 0

	def __init__(self):
		self.puzzle = Tile8Puzzle()
		self.GameFrame = Tk()
		self.GameFrame.title("8Tile Puzzle!")
		self.GameFrame.geometry("240x257")
		self.createGUIBoard()
		self.GameFrame.mainloop()

	def slideID(self, tileId):
		if(tileId == 0):
			messagebox.showinfo("Invalid Step", "You can't move this tile!")
			return
			
		for tileRow in self.puzzle.board:
			for tile in tileRow:
				if tile.value == tileId:
					tile.slide(self.puzzle, self)
					return

	def createGUIBoard(self):
		for i in range(3):
			for j in range(3):
				self.gameBoard[i][j] = Button(self.GameFrame, text=self.puzzle.board[i][j].value, command= functools.partial(self.updateBoard, self.puzzle.board[i][j].value), height=5, width=10)
				self.gameBoard[i][j].grid(row=i, column=j)

	def updateBoard(self, id):
		self.steps = self.steps + 1
		self.slideID(id)
		self.puzzle.printBoard()
		if self.puzzle.isGameOver():
			messagebox.askquestion("Won!", "You won the game with" + str(steps) + " steps!\ndo you wanna play again?")
			self.GameFrame.destroy()
			if 'yes':
				Tile8PuzzleBoard()

	def swapTiles(self, x, y, newX, newY):
		self.gameBoard[x][y].grid(row=newX, column=newY)
		self.gameBoard[newX][newY].grid(row=x, column=y)
		self.gameBoard[x][y], self.gameBoard[newX][newY] = self.gameBoard[newX][newY], self.gameBoard[x][y]
	
Tile8PuzzleBoard()
