import java.util.ArrayList;
import java.util.Random;

public class NQPosition {

	public int[] board;
	private int n;
	private int curVal;
	private Random random;
//	private int randomFire;

	public NQPosition(int n) {
		this.board = new int[n];
		random = new Random();
		for (int i = 0; i < n; i++) {
			board[i] = random.nextInt(n);
		}
		this.n = n;
		this.curVal = this.value();
	}

	public int value() {
		int conflicts = 0;
//		ArrayList<Integer> temp = new ArrayList<>(n);
//		int l = 0;
		for (int i = 0; i < n; i++) {
			int queen = board[i];
			for (int j = 0; j < i; j++) {
				int other = board[j];
				int t = i - j;
//				l = conflicts;
				conflicts += (queen - t == other ? 1 : 0) + (queen + t == other ? 1 : 0) + (queen == other ? 1 : 0);
//				if (l != conflicts) {
//					temp.add(i);
//				}
			}
		}
//		if (!temp.isEmpty()) {
//			randomFire = temp.get(random.nextInt(temp.size()));
//		}
		return conflicts;
	}

	public void makeMove(int[] move) {
		board[move[0]] = move[1];
		curVal = value();
	}

	public boolean threatened(int i) {
		int queen = board[i];
		for (int j = 0; j < n; j++) {
			if (i == j) {
				continue;
			}
			int other = board[j];
			int t = i - j;
			if (queen - t == other || queen + t == other || queen == other) {
				return true;
			}
		}
		return false;
	}

	public int[] bestMove() {
		int[] best_move = new int[]{-1, -1, curVal};
		int best_value = curVal;
		int i = random.nextInt(n);
//		int i = randomFire;
		for (int x = 0; x < n; x++) {
			int queen = board[i];
			if (threatened(i)) {
				int j = random.nextInt(n);
				for (int y = 0; y < n; y++) {
					if (queen != j) {
						board[i] = j;
						int value = value();
						if (best_value > value || best_value == value && random.nextBoolean()) {
							best_value = value;
							best_move = new int[]{i, j, value};
//							return new int[]{i, j, value};

						}
					}
					j++;
					if (j >= n) {
						j = 0;
					}

				}
				board[i] = queen;
				if (best_value < curVal) {
					return best_move;
				}
			}
			i++;
			if (i >= n) {
				i = 0;
			}
		}
		return best_move;
	}
}
