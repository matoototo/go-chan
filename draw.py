from PIL import Image, ImageDraw

BOARD_TEXTURE = Image.open("assets/board.png")
STONE_BLACK = Image.open("assets/stone_black.png")
STONE_WHITE = Image.open("assets/stone_white.png")

BOARD_SETTINGS_9 = (8, False, 2)
BOARD_SETTINGS_13 = (12, False, 3)
BOARD_SETTINGS_19 = (18, True, 3)

def draw_loop_image(width, height, texture):
	"""Create an image of given size using an arbitrary texture.
	The texture will loop if smaller than the image size.
	
	Arguments:
	width -- The width of the resulting image
	height -- The height of the resulting image
	texture -- The texture to use
	"""
	
	board = Image.new("RGBA", (width, height), (255, 255, 255, 255))
	textureWidth, textureHeight = texture.size
	
	for x in range(0, width, textureWidth):
		for y in range(0, height, textureHeight):
			board.paste(texture, (x, y))
	
	return board

def draw_board(image, boardSettings, borderSize):
	"""Draw goban lines on the specified image.
	Returns a new copy instead of altering the original image.
	
	Arguments:
	image -- The image to draw on
	boardSettings -- A 3-tuple containing the settings for the board
	borderSize -- The size of the border around the board
	"""
	
	COLOR = (0, 0, 0, 200)
	STAR_POINT_SIZE = 2
	LABEL_BOARD_SPACING = 10
	
	(boardSize, drawExtraStarPoints, starPointOffset) = boardSettings
	newImage = image.copy()
	imageWidth, imageHeight = newImage.size
	innerWidth = imageWidth - borderSize * 2
	innerHeight = imageHeight - borderSize * 2
	draw = ImageDraw.Draw(newImage)
	stepX = innerWidth / boardSize
	stepY = innerHeight / boardSize
	
	# Draw lines and labels
	for i in range(0, boardSize + 1):
		x = borderSize + stepX * i
		label = chr(ord('A') + i)
		labelWidth, labelHeight = draw.textsize(label)
		
		draw.line([(x, borderSize), (x, innerHeight + borderSize)], fill = COLOR)
		draw.text((x - labelWidth / 2, borderSize - labelHeight - LABEL_BOARD_SPACING), label, COLOR)
		draw.text((x - labelWidth / 2, borderSize + innerHeight + LABEL_BOARD_SPACING), label, COLOR)
	
	for i in range(0, boardSize + 1):
		y = borderSize + stepY * i;
		label = str(boardSize - i + 1);
		labelWidth, labelHeight = draw.textsize(label)
		
		draw.line([(borderSize, y), (innerWidth + borderSize, y)], fill = COLOR)
		draw.text((borderSize - labelWidth - LABEL_BOARD_SPACING, y - labelHeight / 2), label, COLOR)
		draw.text((borderSize + innerWidth + LABEL_BOARD_SPACING, y - labelHeight / 2), label, COLOR)
	
	# Calculate star point positions
	centerX = boardSize / 2 * stepX + borderSize
	centerY = boardSize / 2 * stepY + borderSize
	leftX = starPointOffset * stepX + borderSize
	rightX = (boardSize - starPointOffset) * stepX + borderSize
	topY = starPointOffset * stepY + borderSize
	bottomY = (boardSize - starPointOffset) * stepY + borderSize
	
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
	
	return newImage

#board = draw_loop_image(500, 500, BOARD_TEXTURE)
#board = draw_board(board, BOARD_SETTINGS_19, 50)
#board.save("test.png")
