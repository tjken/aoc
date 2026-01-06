import main.java.Day01.Dial;
import main.java.Day01.Direction;

record Transaction(Direction direction, int amount) {
    static Transaction parse(String s) {
        return switch (s.charAt(0)) {
            case 'R' -> new Transaction(Direction.RIGHT, Integer.parseInt(s.substring(1)));
            case 'L' -> new Transaction(Direction.LEFT, Integer.parseInt(s.substring(1)));
            default -> throw new IllegalArgumentException("Invalid direction");
        };
    }
}

void main(String[] args) throws IOException {
    if (args.length != 1) {throw new IllegalArgumentException("Unexpected input!");}
    IO.println("2025 - Day 01");
    List<Transaction> transactions =
            Files.readAllLines(new File(args[0]).toPath()).stream().map(Transaction::parse).toList();
    IO.println("Part 1: " + part1(transactions));
    IO.println("Part 2: " + part2(transactions));
}

int part1(List<Transaction> transactions) {
    int answer = 0;
    Dial d = new Dial(50);
    for (Transaction t : transactions) {
        d.rotate(t.direction(), t.amount());
        if (d.getPosition() == 0) {answer++;}
    }
    return answer;
}

int part2(List<Transaction> transactions) {
    int answer = 0;
    Dial d = new Dial(50);
    for (Transaction t : transactions) {
        int oldPosition = d.getPosition();
        d.rotate(t.direction(), t.amount());
        int newPosition = d.getPosition();

        // Add passed zeroes from full rotations
        int passed = t.amount / 100;
        if (passed > 0) {
            answer += passed;
        }
        if (oldPosition == 0) continue;
        switch (t.direction()) {
            case LEFT:
                if (oldPosition < newPosition) {
                    answer++;
                }
                else if (newPosition == 0) {
                    answer++;
                }
                break;
            case RIGHT:
                if (oldPosition > newPosition) {
                    answer++;
                }
                break;
        }
    }
    return answer;
}