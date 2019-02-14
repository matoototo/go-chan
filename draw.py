from PIL import Image, ImageDraw, ImageFont

BOARD_TEXTURE = Image.open("assets/board.png")
STONE_BLACK_TEXTURE = Image.open("assets/stone_black.png")
STONE_WHITE_TEXTURE = Image.open("assets/stone_white.png")

BOARD_SETTINGS_9 = (9, False, 2)
BOARD_SETTINGS_13 = (13, False, 3)
BOARD_SETTINGS_19 = (19, True, 3)

class VisualBoard:
	"""Contains data for the visual representation of a Go board."""
	
	def __init__(self, width, height, borderSize, settings, boardTexture, stoneBlackTexture, stoneWhiteTexture):
		"""Instantiates a new board from the given data.
		
		Arguments:
		width -- The board width
		height -- The board height
		borderSize -- The size of the border around the board
		settings -- A 3-tuple containing information about the board settings
		boardTexture -- The base texture to use for the board
		stoneBlackTexture -- The texture to use for black stones
		stoneWhiteTexture -- The texture to use for white stones
		"""
		
		self.width = width
		self.height = height
		self.innerWidth = width - borderSize * 2
		self.innerHeight = height - borderSize * 2
		self.borderSize = borderSize
		self.settings = settings
		self.baseImage = Image.new("RGBA", (width, height), (255, 255, 255, 255))
		
		(boardSize, _, _) = self.settings
		stoneWidth = int(self.innerWidth / boardSize)
		stoneHeight = int(self.innerWidth / boardSize)
		
		self.stoneBlackTexture = stoneBlackTexture.resize((stoneWidth, stoneHeight), Image.BICUBIC)
		self.stoneWhiteTexture = stoneWhiteTexture.resize((stoneWidth, stoneHeight), Image.BICUBIC)
		
		self.__draw_board_texture(boardTexture)
		self.__draw_board()
	
	def __draw_board_texture(self, texture):
		"""Draws a texture on the internal image.
		If the texture is smaller than the image it loops.
		"""
		
		textureWidth, textureHeight = texture.size
		
		for x in range(0, self.width, textureWidth):
			for y in range(0, self.height, textureHeight):
				self.baseImage.paste(texture, (x, y))
	
	def __draw_board(self):
		"""Draw goban lines, labels and star points on the internal image."""
		
		COLOR = (0, 0, 0, 200)
		LINE_WIDTH = 2
		STAR_POINT_SIZE = 4
		FONT_SIZE = 18
		
		(boardSize, drawExtraStarPoints, starPointOffset) = self.settings
		boardSize -= 1
		stepX = self.innerWidth / boardSize
		stepY = self.innerHeight / boardSize
		labelBoardSpacing = self.borderSize / 3
		draw = ImageDraw.Draw(self.baseImage)
		font = ImageFont.truetype("assets/font_fifteentwenty.otf", FONT_SIZE)
		
		# Draw lines and labels
		for i in range(0, boardSize + 1):
			x = self.borderSize + stepX * i
			label = chr(ord('A') + i)
			labelWidth, labelHeight = draw.textsize(label, font)
			
			draw.line([(x, self.borderSize), (x, self.innerHeight + self.borderSize)], COLOR, LINE_WIDTH)
			draw.text((x - labelWidth / 2, self.borderSize - labelHeight - labelBoardSpacing), label, COLOR, font)
			draw.text((x - labelWidth / 2, self.borderSize + self.innerHeight + labelBoardSpacing), label, COLOR, font)
		
		for i in range(0, boardSize + 1):
			y = self.borderSize + stepY * i
			label = str(boardSize - i + 1)
			labelWidth, labelHeight = draw.textsize(label, font)
			
			draw.line([(self.borderSize, y), (self.innerWidth + self.borderSize, y)], COLOR, LINE_WIDTH)
			draw.text((self.borderSize - labelWidth - labelBoardSpacing, y - labelHeight / 2), label, COLOR, font)
			draw.text((self.borderSize + self.innerWidth + labelBoardSpacing, y - labelHeight / 2), label, COLOR, font)
		
		# Calculate star point positions
		centerX = boardSize / 2 * stepX + self.borderSize
		centerY = boardSize / 2 * stepY + self.borderSize
		leftX = starPointOffset * stepX + self.borderSize
		rightX = (boardSize - starPointOffset) * stepX + self.borderSize
		topY = starPointOffset * stepY + self.borderSize
		bottomY = (boardSize - starPointOffset) * stepY + self.borderSize
		
		# Draw star points
		draw.ellipse([(centerX - STAR_POINT_SIZE, centerY - STAR_POINT_SIZE), (centerX + STAR_POINT_SIZE, centerY + STAR_POINT_SIZE)], COLOR)
		draw.ellipse([(leftX - STAR_POINT_SIZE, topY - STAR_POINT_SIZE), (leftX + STAR_POINT_SIZE, topY + STAR_POINT_SIZE)], COLOR)
		draw.ellipse([(rightX - STAR_POINT_SIZE, topY - STAR_POINT_SIZE), (rightX + STAR_POINT_SIZE, topY + STAR_POINT_SIZE)], COLOR)
		draw.ellipse([(leftX - STAR_POINT_SIZE, bottomY - STAR_POINT_SIZE), (leftX + STAR_POINT_SIZE, bottomY + STAR_POINT_SIZE)], COLOR)
		draw.ellipse([(rightX - STAR_POINT_SIZE, bottomY - STAR_POINT_SIZE), (rightX + STAR_POINT_SIZE, bottomY + STAR_POINT_SIZE)], COLOR)
		
		if drawExtraStarPoints:
			draw.ellipse([(centerX - STAR_POINT_SIZE, topY - STAR_POINT_SIZE), (centerX + STAR_POINT_SIZE, topY + STAR_POINT_SIZE)], COLOR)
			draw.ellipse([(leftX - STAR_POINT_SIZE, centerY - STAR_POINT_SIZE), (leftX + STAR_POINT_SIZE, centerY + STAR_POINT_SIZE)], COLOR)
			draw.ellipse([(centerX - STAR_POINT_SIZE, bottomY - STAR_POINT_SIZE), (centerX + STAR_POINT_SIZE, bottomY + STAR_POINT_SIZE)], COLOR)
			draw.ellipse([(rightX - STAR_POINT_SIZE, centerY - STAR_POINT_SIZE), (rightX + STAR_POINT_SIZE, centerY + STAR_POINT_SIZE)], COLOR)
	
	def generate_image(self, stones):
		"""Generates a visual representation of a Go game.
		The dimensions of the passed array have to match the board size.
		
		Arguments:
		stones -- A 2D-array of values either 0 (no stone), 1 (black stone) or 2 (white stone)
		"""
		
		(boardSize, _, _) = self.settings
		boardSize -= 1
		newImage = self.baseImage.copy()
		stepX = self.innerWidth / boardSize
		stepY = self.innerHeight / boardSize
		
		for y, row in enumerate(stones):
			for x, stone in enumerate(row):
				posX = int(self.borderSize + x * stepX)
				posY = int(self.borderSize + y * stepY)
				image = None
				
				if stone == 1:
					image = self.stoneBlackTexture
				elif stone == 2:
					image = self.stoneWhiteTexture
				else:
					image = Image.new("RGBA", (1, 1))
				
				imageWidth, imageHeight = image.size
				
				newImage.paste(image, (int(posX - imageWidth / 2), int(posY - imageHeight / 2)), image)
		
		return newImage

#board = VisualBoard(750, 750, 75, BOARD_SETTINGS_19, BOARD_TEXTURE, STONE_BLACK_TEXTURE, STONE_WHITE_TEXTURE)
#stones = [
#	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#	[0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#	[0, 0, 0, 0, 0, 0, 1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#	[0, 0, 0, 0, 0, 0, 1, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#	[0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
#	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
#	[0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#]
#board.generate_image(stones).save("test.png")
