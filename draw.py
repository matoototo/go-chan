from PIL import Image, ImageDraw

BOARD_TEXTURE = Image.open("assets/board.png")
STONE_BLACK_TEXTURE = Image.open("assets/stone_black.png")
STONE_WHITE_TEXTURE = Image.open("assets/stone_white.png")

BOARD_SETTINGS_9 = (8, False, 2)
BOARD_SETTINGS_13 = (12, False, 3)
BOARD_SETTINGS_19 = (18, True, 3)

class VisualBoard:
	"""Contains data for the visual representation of a go board."""
	
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
		self.borderSize = borderSize
		self.settings = settings
		self.stoneBlackTexture = stoneBlackTexture
		self.stoneWhiteTexture = stoneWhiteTexture
		self.baseImage = Image.new("RGBA", (width, height), (255, 255, 255, 255))
		
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
		"""Draw goban lines, labels and star points on the internal image.
		"""
		
		COLOR = (0, 0, 0, 200)
		STAR_POINT_SIZE = 2
		LABEL_BOARD_SPACING = 10
		
		(boardSize, drawExtraStarPoints, starPointOffset) = self.settings
		imageWidth, imageHeight = self.baseImage.size
		innerWidth = imageWidth - self.borderSize * 2
		innerHeight = imageHeight - self.borderSize * 2
		draw = ImageDraw.Draw(self.baseImage)
		stepX = innerWidth / boardSize
		stepY = innerHeight / boardSize
		
		# Draw lines and labels
		for i in range(0, boardSize + 1):
			x = self.borderSize + stepX * i
			label = chr(ord('A') + i)
			labelWidth, labelHeight = draw.textsize(label)
			
			draw.line([(x, self.borderSize), (x, innerHeight + self.borderSize)], fill = COLOR)
			draw.text((x - labelWidth / 2, self.borderSize - labelHeight - LABEL_BOARD_SPACING), label, COLOR)
			draw.text((x - labelWidth / 2, self.borderSize + innerHeight + LABEL_BOARD_SPACING), label, COLOR)
		
		for i in range(0, boardSize + 1):
			y = self.borderSize + stepY * i
			label = str(boardSize - i + 1)
			labelWidth, labelHeight = draw.textsize(label)
			
			draw.line([(self.borderSize, y), (innerWidth + self.borderSize, y)], fill = COLOR)
			draw.text((self.borderSize - labelWidth - LABEL_BOARD_SPACING, y - labelHeight / 2), label, COLOR)
			draw.text((self.borderSize + innerWidth + LABEL_BOARD_SPACING, y - labelHeight / 2), label, COLOR)
		
		# Calculate star point positions
		centerX = boardSize / 2 * stepX + self.borderSize
		centerY = boardSize / 2 * stepY + self.borderSize
		leftX = starPointOffset * stepX + self.borderSize
		rightX = (boardSize - starPointOffset) * stepX + self.borderSize
		topY = starPointOffset * stepY + self.borderSize
		bottomY = (boardSize - starPointOffset) * stepY + self.borderSize
		
		# Draw star points
		draw.ellipse([(centerX - STAR_POINT_SIZE, centerY - STAR_POINT_SIZE), (centerX + STAR_POINT_SIZE, centerY + STAR_POINT_SIZE)], fill = COLOR)
		draw.ellipse([(leftX - STAR_POINT_SIZE, topY - STAR_POINT_SIZE), (leftX + STAR_POINT_SIZE, topY + STAR_POINT_SIZE)], fill = COLOR)
		draw.ellipse([(rightX - STAR_POINT_SIZE, topY - STAR_POINT_SIZE), (rightX + STAR_POINT_SIZE, topY + STAR_POINT_SIZE)], fill = COLOR)
		draw.ellipse([(leftX - STAR_POINT_SIZE, bottomY - STAR_POINT_SIZE), (leftX + STAR_POINT_SIZE, bottomY + STAR_POINT_SIZE)], fill = COLOR)
		draw.ellipse([(rightX - STAR_POINT_SIZE, bottomY - STAR_POINT_SIZE), (rightX + STAR_POINT_SIZE, bottomY + STAR_POINT_SIZE)], fill = COLOR)
		
		if drawExtraStarPoints:
			draw.ellipse([(centerX - STAR_POINT_SIZE, topY - STAR_POINT_SIZE), (centerX + STAR_POINT_SIZE, topY + STAR_POINT_SIZE)], fill = COLOR)
			draw.ellipse([(leftX - STAR_POINT_SIZE, centerY - STAR_POINT_SIZE), (leftX + STAR_POINT_SIZE, centerY + STAR_POINT_SIZE)], fill = COLOR)
			draw.ellipse([(centerX - STAR_POINT_SIZE, bottomY - STAR_POINT_SIZE), (centerX + STAR_POINT_SIZE, bottomY + STAR_POINT_SIZE)], fill = COLOR)
			draw.ellipse([(rightX - STAR_POINT_SIZE, centerY - STAR_POINT_SIZE), (rightX + STAR_POINT_SIZE, centerY + STAR_POINT_SIZE)], fill = COLOR)

#board = VisualBoard(500, 500, 50, BOARD_SETTINGS_19, BOARD_TEXTURE, STONE_BLACK_TEXTURE, STONE_WHITE_TEXTURE)
#board.baseImage.save("test.png")
