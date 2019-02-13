from PIL import Image, ImageDraw

boardTexture = Image.open("assets/board.png");
stoneBlack = Image.open("assets/stone_black.png");
stoneWhite = Image.open("assets/stone_white.png");

def loop_image(width, height, texture):
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
			board.paste(boardTexture, (x, y))
	
	return board

def draw_board(image, boardSize, drawExtraStarPoints = True):
	"""Draw goban lines on the specified image.
	Returns a new copy instead of altering the original image.
	
	Arguments:
	image -- The image to draw on
	boardSize -- The size of the board (9, 13, or 19)
	"""
	
	COLOR = (0, 0, 0, 200)
	STAR_POINT_SIZE = 3
	
	boardSize -= 1
	newImage = image.copy()
	imageWidth, imageHeight = newImage.size
	draw = ImageDraw.Draw(newImage)
	stepX = imageWidth / boardSize
	stepY = imageHeight / boardSize
	
	for i in range(1, boardSize):
		x = stepX * i;
		
		draw.line([(x, 0), (x, imageHeight)], fill = COLOR)
	
	for i in range(1, boardSize):
		y = stepY * i;
		
		draw.line([(0, y), (imageWidth, y)], fill = COLOR)
	
	centerX = boardSize / 2 * stepX
	centerY = boardSize / 2 * stepY
	leftHalfX = 3 * stepX
	rightHalfX = (boardSize - 3) * stepX
	topHalfY = 3 * stepY
	bottomHalfY = (boardSize - 3) * stepY
	
	draw.ellipse([(centerX - STAR_POINT_SIZE, centerY - STAR_POINT_SIZE), (centerX + STAR_POINT_SIZE, centerY + STAR_POINT_SIZE)], fill = COLOR)
	draw.ellipse([(leftHalfX - STAR_POINT_SIZE, topHalfY - STAR_POINT_SIZE), (leftHalfX + STAR_POINT_SIZE, topHalfY + STAR_POINT_SIZE)], fill = COLOR)
	draw.ellipse([(rightHalfX - STAR_POINT_SIZE, topHalfY - STAR_POINT_SIZE), (rightHalfX + STAR_POINT_SIZE, topHalfY + STAR_POINT_SIZE)], fill = COLOR)
	draw.ellipse([(leftHalfX - STAR_POINT_SIZE, bottomHalfY - STAR_POINT_SIZE), (leftHalfX + STAR_POINT_SIZE, bottomHalfY + STAR_POINT_SIZE)], fill = COLOR)
	draw.ellipse([(rightHalfX - STAR_POINT_SIZE, bottomHalfY - STAR_POINT_SIZE), (rightHalfX + STAR_POINT_SIZE, bottomHalfY + STAR_POINT_SIZE)], fill = COLOR)
	
	if drawExtraStarPoints:
		draw.ellipse([(centerX - STAR_POINT_SIZE, topHalfY - STAR_POINT_SIZE), (centerX + STAR_POINT_SIZE, topHalfY + STAR_POINT_SIZE)], fill = COLOR)
		draw.ellipse([(leftHalfX - STAR_POINT_SIZE, centerY - STAR_POINT_SIZE), (leftHalfX + STAR_POINT_SIZE, centerY + STAR_POINT_SIZE)], fill = COLOR)
		draw.ellipse([(centerX - STAR_POINT_SIZE, bottomHalfY - STAR_POINT_SIZE), (centerX + STAR_POINT_SIZE, bottomHalfY + STAR_POINT_SIZE)], fill = COLOR)
		draw.ellipse([(rightHalfX - STAR_POINT_SIZE, centerY - STAR_POINT_SIZE), (rightHalfX + STAR_POINT_SIZE, centerY + STAR_POINT_SIZE)], fill = COLOR)
	
	return newImage

#board = loop_image(500, 500, boardTexture);
#board = draw_board(board, 19)
#board.save("test.png")
