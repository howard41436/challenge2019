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
	def pick_oil(self, oils):
		for i in reverse(range(len(oils)):
			if oils[i].pos == self.position:
				if self.bag + oils[i].weight <= model_const.bag_capacity:
					self.bag += oils[i].price
					self.price += oils[i].price
					oils.remove(i)
	def store_price(self, bases):
		if self.position[0] <= bases[self.index].center[0] + bases[self.index].length/2 \
			and self.position[0] >= bases[self.index].center[0] - bases[self.index].length/2 \
			or self.position[1] <= bases[self.index].center[1] + bases[self.index].length/2 \
			and self.position[1] >= bases[self.index].center[1] - bases[self.index].length/2:
			put_oil(self.price)
			self.price = 0

	def check_collide(self, players):
		collide = []
		sum_of_all = 0
		for player in players:
			if player is self:
				continue
			if Vec.magnitude(player.position - self.position) <= 2 * model_const.size:
				collide.append(player.index)
				sum_of_all += player.price
		self.price = sum_of_all / len(collide)
		
	def update(self, direction, oils, bases):
		if self.position[0] + direction[0] < model_const.size \
			or self.position[0] + direction[0] > view_const.size - model_const.size:
			direction[0] = 0
		elif self.position[1] + direction[1] < model_const.size \
			or self.position[1] + direction[1] > view_const.size - model_const.size:
			direction[1] = 0
		self.position += Vec(direction)
		pick_oil(oils)
		store_price(bases)
		check_collide(players)









