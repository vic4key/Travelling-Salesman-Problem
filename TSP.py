# -*- coding: utf-8 -*-

'''''''''''''''''''''''''''''''''
@Author : Vic P.
@Email  : vic4key@gmail.com
@Name   : Traveling Salesman Opt.
'''''''''''''''''''''''''''''''''

import sys, random
from Vutils import Others, Statistic, Math
from simanneal import Annealer
import matplotlib.pyplot as plt

# https://en.wikipedia.org/wiki/Simulated_annealing
# https://en.wikipedia.org/wiki/Travelling_salesman_problem

cities = []
cities.append((60, 200))
cities.append((180, 200))
cities.append((80, 180))
cities.append((140, 180))
cities.append((20, 160))
cities.append((100, 160))
cities.append((200, 160))
cities.append((140, 140))
cities.append((40, 120))
cities.append((100, 120))
cities.append((180, 100))
cities.append((60, 80))
cities.append((120, 80))
cities.append((180, 60))
cities.append((20, 40))
cities.append((100, 40))
cities.append((200, 40))
cities.append((20, 20))
cities.append((60, 20))
cities.append((160, 20))

class TravelingSalesman(Annealer):

	def __init__(self, state):
		super(TravelingSalesman, self).__init__(state)

		self.figure, self.axes = plt.subplots(ncols=2, nrows=2)
		self.graph_visusal, self.graph_cost = self.axes[0]
		self.graph_temp, self.graph_accept  = self.axes[1]
		self.figure.show()

		self.val_temps = []
		self.val_steps = []
		self.val_bests = []
		self.val_acpts = []

		self.improved_cout = 0

		self.IMPROVED_NUM = 3
		self.IMPROVED_MIN = 0.003

		return

	def move(self):
		v1 = random.randint(0, len(self.state) - 1)
		v2 = random.randint(0, len(self.state) - 1)
		if v1 == 0 or v2 == 0: return
		self.state[v1], self.state[v2] = self.state[v2], self.state[v1]
		return

	def energy(self):
		distance = 0.
		for i in range(0, len(self.state) - 1):
			distance += Math.Distance2D(self.state[i], self.state[i + 1])
		return distance

	def update(self, *args, **kwargs):
		super(TravelingSalesman, self).update(*args, **kwargs)

		# Data of the current iteration

		Xs, Ys = zip(*self.state)

		val_step, val_temp, val_best, val_acpt, val_impr =\
			args[0], args[1], args[2], args[3], args[4]

		self.val_steps.append(val_step)
		self.val_temps.append(val_temp)
		self.val_bests.append(val_best)
		self.val_acpts.append(val_acpt)

		# Visualization Graph

		self.graph_visusal.clear()
		self.graph_visusal.grid(True)
		self.graph_visusal.axis("equal")
		self.graph_visusal.set_xlabel("X-axis")
		self.graph_visusal.set_ylabel("Y-axis")
		self.graph_visusal.plot(Xs, Ys, "-o")

		# Cost Graph

		self.graph_cost.clear()
		self.graph_cost.grid(True)
		self.graph_cost.axis("auto")
		self.graph_cost.set_xlabel("Iteration")
		self.graph_cost.set_ylabel("Cost")
		self.graph_cost.set_xlim(0, self.steps)
		# self.graph_cost.set_ylim(self.Tmin, self.Tmax)
		self.graph_cost.plot(self.val_steps, self.val_bests, color="blue")

		# Temperature Graph

		self.graph_temp.clear()
		self.graph_temp.grid(True)
		self.graph_temp.axis("auto")
		self.graph_temp.set_xlabel("Iteration")
		self.graph_temp.set_ylabel("Temperature")
		self.graph_temp.set_xlim(0, self.steps)
		self.graph_temp.set_ylim(self.Tmin, self.Tmax)
		self.graph_temp.plot(self.val_steps, self.val_temps, color="red")

		# Acceptance Graph

		self.graph_accept.clear()
		self.graph_accept.grid(True)
		self.graph_accept.axis("auto")
		self.graph_accept.set_xlabel("Iteration")
		self.graph_accept.set_ylabel("%")
		self.graph_accept.set_xlim(0, self.steps)
		self.graph_accept.set_ylim(0, 1)
		self.graph_accept.plot(self.val_steps, self.val_acpts, color="green")

		# Performs updating graphs

		self.figure.canvas.draw()
		self.figure.canvas.flush_events()

		# Stop if finished

		if val_impr != None:
			if val_impr <= self.IMPROVED_MIN: self.improved_cout += 1
			else: self.improved_cout = 0
			if self.improved_cout >= self.IMPROVED_NUM:
				print(R"Finished at step %d / %d" % (val_step, self.steps))
				self.user_exit = True
			pass
		pass

		return

	def pause(self):
		plt.show()
		return

def main():
	print("Howdy, Vic P.")

	tsp = TravelingSalesman(cities)
	# result = tsp.auto(10)
	tsp.steps = 100000
	result = tsp.anneal()
	print("The final solution is", result)
	tsp.pause()

	return 0

if __name__ == "__main__":
	try:
		main()
	except (Exception, KeyboardInterrupt): Others.LogException(sys.exc_info())
	sys.exit()