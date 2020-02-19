public class HillClimb {
	private int n = 0;

	public HillClimb(int n) {
		this.n = n;
	}

	public NQPosition Climb() {
		NQPosition best_pos = null;
		int best_value = Integer.MAX_VALUE;
		int LOOP_LIMIT = 10;

		for (int i = 0; i < 20; i++) {
			NQPosition this_pos = new NQPosition(n);
			int curr_value = this_pos.value();
			int steady = 0;
			while (true) {
				int[] stuff = this_pos.bestMove();
				if (stuff[0] == -1 || stuff[2] > curr_value || steady > LOOP_LIMIT) {
					// no improvement, give up
					if (curr_value < best_value) {
						best_pos = this_pos;
						best_value = curr_value;
					}
					break;
				}
				else {
					if (stuff[2] == 0) {
						this_pos.makeMove(stuff);
						return this_pos;
					}
					if (stuff[2] == curr_value) {
						steady++;
					}
					else {
						steady = 0;
					}
					// position improves, keep searching
					curr_value = stuff[2];
					this_pos.makeMove(stuff);
				}
			}
		}
		return best_pos;
	}

	public static void main(String[] args) {
		long a = System.nanoTime();
		for (int i = 0; i < 100; i++) {
//			System.out.println("Doing " + i);
			HillClimb climb = new HillClimb(15);
			NQPosition stuff = climb.Climb();
//			System.out.println("Final value " + stuff.value());
//			System.out.println(Arrays.toString(stuff.board));
//			System.out.println();
		}
		long b = System.nanoTime() - a;
		System.out.println(b);
	}

}

