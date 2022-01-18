from PIL import ImageColor

add_alpha = lambda x : (x[0],x[1],x[2],0)

square_bright = add_alpha(ImageColor.getrgb("#f0d9b5"))
square_dark = add_alpha(ImageColor.getrgb("#b58863"))
last_move_square_dark = add_alpha(ImageColor.getrgb("#aba23b"))
last_move_square_bright = add_alpha(ImageColor.getrgb("#cdd26b"))
capturing_square_bright = add_alpha(ImageColor.getrgb("#829769"))
capturing_square_dark = add_alpha(ImageColor.getrgb("#84794e"))
circle_color = add_alpha(ImageColor.getrgb("#718a53"))
background_promotion = (125,125,125,0)
red = (255,125,125,0)
