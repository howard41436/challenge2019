import view.const	as view_const
import model.const 	as model_const

from pygame.math import Vector2 as Vec
import random

class player(object):
	def __init__(self, name, index):
		self.index = index
		self.name = name
		self.bag = 0
		self.position = Vec(view_const.position[index])
		self.color = [ random.randint(0,255) for _ in range(3) ]
		self.price = 0


	def update_position(self, direction, oils, bases):
		if self.position[0] + direction[0] < 10 \
			or self.position[0] + direction[0] > view_const.size-10:
			direction[0] = 0
		elif self.position[1] + direction[1] < 10 \
			or self.position[1] + direction[1] > view_const.size-10:
			direction[1] = 0

		self.position += Vec(direction)

		for i in reverse(range(len(oils)):
			if oils[i].pos == self.position:
				if self.bag + oils[i].weight <= model_const.bag_capacity:
					self.bag += oils[i].weight
					self.price += oils[i].price
					oils.remove(i)

		for i in reverse(range(len(bases))):
			if self.position[0] <= bases[i].center + bases[i].length/2 \
				and self.position[0] >= bases[i].center - bases[i].length/2 \
				or self.position[1] <= bases[i].center + bases[i].length/2 \
				and self.position[1] <= bases[i].center - bases[i].length/2:
				put_oil(self.price)
				self.price = 0
		collide = []
		total = 0
		for player in players:
			if self is player:
				pass
			if Vec.magnitude(player.position - self.position) <= 1e-9:
				collide.append(player.index)
			for index in collide:
				total += 









