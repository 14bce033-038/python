from random import randint
from tkinter import *
from tkinter import messagebox
import functools

#GUI
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

	@classmethod
	def isInRange(self, x, y):
		if x >= 0 and x < 3 and y >= 0 and y < 3:
			return True
		return False

#Backend
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

	def __init__(self):
		self.puzzle = Tile8Puzzle()
		self.GameFrame = Tk()
		self.GameFrame.title("8Tile Puzzle!")
		self.GameFrame.geometry("240x257")
		self.createGUIBoard()
		self.updateEmptySlot()
		self.GameFrame.mainloop()

	def slideID(self, tileId):
		for tileRow in self.puzzle.board:
			for tile in tileRow:
				if tile.value == tileId:
					tile.slide(self.puzzle, self)
					return

	def createGUIBoard(self):
		for i in range(3):
			for j in range(3):
				self.gameBoard[i][j] = Button(self.GameFrame, text=self.puzzle.board[i][j].value, command= functools.partial(self.updateBoard, self.puzzle.board[i][j].value), bg="#ff8f00", height=5, width=10)
				self.gameBoard[i][j].grid(row=i, column=j)

	def updateEmptySlot(self):
		for i in range(3):
			for j in range(3):
				if self.puzzle.board[i][j].value == 0:
					self.gameBoard[i][j].configure(bg="#000000")

	def updateBoard(self, id):
		self.slideID(id)
		self.puzzle.printBoard()
		if self.puzzle.isGameOver():
			print("Hurrah! You won the game.")
			messagebox.showinfo("Win!", "You won the game!")
			self.GameFrame.destroy()

	def swapTiles(self, x, y, newX, newY):
		self.gameBoard[x][y].grid(row=newX, column=newY)
		self.gameBoard[newX][newY].grid(row=x, column=y)
		self.gameBoard[x][y], self.gameBoard[newX][newY] = self.gameBoard[newX][newY], self.gameBoard[x][y]
		
t = Tile8PuzzleBoard()
