#!/usr/bin/python
from PIL import Image, ImageDraw
import argparse

colors = [
	(52, 51, 97, 255),
	(138, 49, 72, 255),
	(84, 123, 56, 255),
	(157, 126, 60, 255)
]

def nthdir(n):
	if n==0:
		return 1
	while (n%2 == 0):
		n = n/2
	return 2 - (n%4)

class Line(object):
	norm = 0
	def __init__(self, dir, color):
		self.dir = dir%4
		self.x = 0
		self.y = 0
		self.color = color
	def set_pos(self, nx, ny):
		self.x = nx
		self.y = ny
	def turn(self, angle):
		self.dir += angle
		self.dir %= 4
	def draw(self, draw, scale):
		if self.dir % 2 == 0:
			newx = self.x
			newy = self.y + (self.dir - 1)*scale
		else:
			newx = self.x + (2 - self.dir)*scale
			newy = self.y
		draw.line((self.x,self.y, newx,newy), fill=self.color)
		self.x = newx
		self.y = newy
		Line.norm = max(self.x, self.y, Line.norm)

def gen_lines(size, nlines=4):
	lines = []
	for i in range(0,nlines):
		l = Line(i, colors[i%len(colors)])
		l.set_pos(size/2, size/2)
		lines.append(l)
	return lines

def blank_image(size):
	return Image.new("RGBA", (size, size), (255,255,255,0))

def fill_image(img, lines, pattern_size, fill=False, scale=2):
	n = 0
	draw = ImageDraw.Draw(img)
	Line.norm = 0
	while Line.norm < pattern_size or (fill and Line.norm < pattern_size*2):
		angle = nthdir(n)
		n = n + 1
		for line in lines:
			line.turn(angle)
			line.draw(draw, scale)
	return img

def go(size, fill=False, scale=2, nlines=4):
	im = blank_image(size)
	lines = gen_lines(size, nlines=nlines)
	return fill_image(im, lines, size, fill, scale)

if __name__ == "__main__":
	# We want to generate a single image
	parser = argparse.ArgumentParser(description="The dragon curve generator.")
	parser.add_argument("size", type=int, help="size of the generated image")
	parser.add_argument("-f", "--fill", action="store_true", help="fills in the image instead of stopping at the edges", default=False)
	parser.add_argument("-s", "--scale", type=int, help="change the size of the pattern", default=2)
	parser.add_argument("-o", "--output", help="output file")
	args = parser.parse_args()

	res = go(args.size, fill=args.fill, scale=args.scale)
	if args.output != None:
		res.save(args.output)
	else:
		res.show()