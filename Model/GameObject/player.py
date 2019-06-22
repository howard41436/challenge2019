import view.const	as view_const
import model.const 	as model_const	
import 	oil	as oil
from pygame.math import Vector2 as Vec
import random

class player(object):
	def __init__(self, name, index):
		self.index = index
		self.name = name
		self.bag = 0
		self.position[] = view_const.position[index]
		self.color = [ random.randint(0,255) for _ in range(3) ]
		self.price = 0


	def update_position(self, direction[]):
		if self.position[0] + direction[0] < 10 \
			or self.position[0] + direction[0] > view_const.size-10 :
			direction[0] = 0
		elif self.position[1] + direction[1] < 10 \
			or self.position[1] + direction[1] > view_const.size-10 :
			direction[1] = 0

		self.position += Vec(direction)

		for i in range(len(oils)-1, -1, -1) :
			if oils[i].pos == self.position :
				if self.bag + oils[i].weight <= model_const.bag_capacity :
					self.bag += oils[i].weight
					self.price += oils[i].price
					oils.remove(i)
	def				



