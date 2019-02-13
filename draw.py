from PIL import Image

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

#b = create_board(500, 500, boardTexture)
#b.save("test.png")
