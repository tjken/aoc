public class Dial {
    private int position;
    private final int MOD = 100;

    public Dial(int initialPosition) {
        this.position = initialPosition;
    }
    public void rotate(Direction d, int amount) {
        if (amount <= 0) throw new IllegalArgumentException("Invalid amount");

        // Full rotations and greater are not handled without MOD
        amount %= MOD;
        if (amount == 0) return;

        switch (d) {
            case LEFT:
                position = (position - amount + MOD) % MOD;
                break;
            case RIGHT:
                position = (position + amount) % MOD;
                break;
            default:
                throw new IllegalArgumentException("Invalid direction");
        }
    }

    public int getPosition() {
        return position;
    }
}
