import random
import time

class NQPosition:
	def __init__(self, n):
		self.board = [random.randint(0, n - 1) for _ in range(n)]
		self.n = n
		self.cur_val = self.value()

	def value(self):
		return self.value_c(self.board)

	def value_c(self, xs):
		conflicts = 0
		for a, queen in enumerate(xs):
			for b, other in enumerate(xs[0:a]):
				t = a - b
				conflicts += (queen - t == other) + (queen + t == other) + (queen == other)
		return conflicts

	def make_move(self, move):
		self.board[move[0]] = move[1]
		self.cur_val = self.value()

	def best_move(self):
		best_move = None
		best_value = self.cur_val
		copy = self.board.copy()
		for i, queen in enumerate(self.board):
			for j in range(self.n):
				if queen != j:
					copy[i] = j
					value = self.value_c(copy)
					if best_value > value or best_value == value and random.randint(1, 2) == 1:
						best_value = value
						best_move = [i, j]
						# return best_move, best_value
			copy[i] = queen
		return best_move, best_value


def hill_climbing(n):
	best_pos = None
	best_value = float("inf")
	LOOP_LIMIT = 10

	for _ in range(20):
		this_pos = NQPosition(n)
		curr_value = this_pos.value()
		steady = 0
		while True:
			move, new_value = this_pos.best_move()
			if move is None or new_value > curr_value or steady > LOOP_LIMIT:
				# no improvement, give up
				if (curr_value < best_value):
					best_pos = this_pos
					best_value = curr_value
				break
			else:
				if new_value == 0:
					this_pos.make_move(move)
					return this_pos, 0
				if new_value == curr_value:
					steady += 1
				else:
					steady = 0
				# position improves, keep searching
				curr_value = new_value
				this_pos.make_move(move)
	return best_pos, best_value

t = time.process_time()
for i in range(100):
	# print("Doing ", str(i))
	best_pos, best_value = hill_climbing(15)
	# print("Final value", best_value)
	# print("Board: ", best_pos.board)
	# print()
elapsed_time = time.process_time() - t
print(elapsed_time)