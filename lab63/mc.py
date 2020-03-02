import random

def make_move(pos, move):
	# move is column of where to drop the ball
	pos["empty"] -= 1
	pos["slots"][move[1]] -= 1
	pos["board"][move[0]][move[1]] = move[2]
	pos["turn"] = (pos["turn"] % 2) + 1


def revert_move(pos, move):
	pos["empty"] += 1
	pos["slots"][move[1]] += 1
	pos["board"][move[0]][move[1]] = 0
	pos["turn"] = (pos["turn"] % 2) + 1


def dump_pos(pos):
	# print board
	print()
	for line in pos["board"]:
		print("|" + "".join(["X" if slot == 1 else ("O" if slot == 2 else " ") for slot in line]) + "|")
	print("|" + "".join(map(lambda x: str(x), [i for i in range(7)])) + "|")
	print()


def parse_move(pos, column: int):
	return pos["slots"][column] - 1, column, pos["turn"]


def parse_move_thing(pos, column: int, player):
	return pos["slots"][column] - 1, column, player


def simulate(pos, move, side):
	moves = [move]
	make_move(pos, move)
	sidey = side
	if evaluate_board(pos["board"])[0] == 1:
		revert_move(pos, move)
		return "WIN"
	elif pos["empty"] == 0:
		revert_move(pos, move)
		return "DRAW"
	while True:
		to_return = False
		sidey = sidey % 2 + 1
		movey = random.choice(list(map(lambda x: parse_move_thing(pos, x, sidey), [i for i in range(7) if pos["slots"][i] != 0])))
		moves.append(movey)
		make_move(pos, movey)
		if evaluate_board(pos["board"])[0] == 1:
			to_return = True
			if sidey == side:
				bingo = "WIN"
			else:
				bingo = "LOSS"
		elif pos["empty"] == 0:
			to_return = True
			bingo = "DRAW"
		if to_return:
			for movex in moves[::-1]:
				revert_move(pos, movex)
			return bingo


def pure_mc(pos, N=200):
	# get
	me = pos["turn"]
	initial_moves = list(map(lambda x: parse_move(pos, x), [i for i in range(7) if pos["slots"][i] != 0]))
	# counters for each move
	win_counts = dict((move, 0) for move in initial_moves)

	for move in initial_moves:
		for i in range(N):
			# mängi juhuslikult seis kuni lõpuni
			res = simulate(pos, move, me)
			if res == "WIN":
				win_counts[move] += 1
			elif res == "DRAW":
				win_counts[move] += 0.5

	most_wins = 0
	best_move = None
	for key in win_counts.keys():
		if win_counts[key] > most_wins:
			best_move = key
			most_wins = win_counts[key]
	return best_move


def play_game(player_num):

	# declare dictionary used for storing game data
	pos = dict()
	pos["turn"] = 1
	pos["board"] = [[0 for _ in range(7)] for _ in range(6)]
	pos["empty"] = 7 * 6
	pos["slots"] = [6 for _ in range(7)]

	playing = True
	while playing:
		if pos["turn"] == player_num:
			# print the board to user
			dump_pos(pos)
			print(f"Your piece: {'X' if player_num == 1 else 'O'}")
			move_str = input("Insert move as number from 0 to 6\n")
			if not move_str.isnumeric() or 0 > int(move_str) > 6:
				print("Invalid move inserted, try again")
				continue
			if pos["slots"][int(move_str)] == 0:
				print("Invalid move, that column is full")
				continue
			move = parse_move(pos, int(move_str))
		else:
			move = pure_mc(pos)

		make_move(pos, move)

		# check if game is over
		evaluation = evaluate_board(pos["board"])
		if evaluation[0] == 1 or pos["empty"] == 0:
			playing = False
			if evaluation[0] == 1:
				print(f"Winner is {'X' if evaluation[1] == 1 else 'O'}")
			else:
				print("Draw")


# returns tuple
# first number is state: 0 for nothing, 1 for win
# second number is whose side, only useful for win
def evaluate_board(board: list):
	DIAG_RIGHT_STARTS = [(0, 3, 4), (0, 2, 5), (0, 1, 6), (0, 0, 6), (1, 0, 5), (2, 0, 4)]
	DIAG_LEFT_STARTS = [(2, 6, 4), (1, 6, 5), (0, 6, 6), (0, 5, 6), (0, 4, 5), (0, 3, 4)]

	for y in range(6):
		streak = 0
		side = 0
		for x in range(7):
			current = board[y][x]
			if current != 0:
				if current == side:
					streak += 1
					if streak == 4:
						return 1, side
				else:
					side = current
					streak = 1
			else:
				streak = 0
				side = 0

	for x in range(7):
		streak = 0
		side = 0
		for y in range(6):
			current = board[y][x]
			if current != 0:
				if current == side:
					streak += 1
					if streak == 4:
						return 1, side
				else:
					side = current
					streak = 1
			else:
				streak = 0
				side = 0

	for move in DIAG_RIGHT_STARTS:
		y = move[0]
		x = move[1]
		streak = 0
		side = 0
		for i in range(move[2]):
			current = board[y + i][x + i]
			if current != 0:
				if current == side:
					streak += 1
					if streak == 4:
						return 1, side
				else:
					side = current
					streak = 1
			else:
				streak = 0
				side = 0

	for move in DIAG_LEFT_STARTS:
		y = move[0]
		x = move[1]
		streak = 0
		side = 0
		for i in range(move[2]):
			current = board[y + i][x - i]
			if current != 0:
				if current == side:
					streak += 1
					if streak == 4:
						return 1, side
				else:
					side = current
					streak = 1
			else:
				streak = 0
				side = 0

	return 0, 0


if __name__ == '__main__':
	if input("X starts. Type X to be X, anything else to be O\n").lower() == "x":
		print("You're X")
		play_game(1)
	else:
		print("You're O")
		play_game(2)
