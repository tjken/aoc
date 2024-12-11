package aoc._2024;

import java.util.*;
import java.util.stream.IntStream;
import java.math.BigInteger;

public class Day11 {
    private interface Blinkable {
        void blink();
    }

    private class StoneTree implements Blinkable {
        private List<Node> roots;

        StoneTree(int[] stones) {
            this.roots = Arrays.stream(stones)
                    .mapToObj(BigInteger::valueOf)
                    .map(Node::new).toList();
        }

        @Override
        public void blink() {
            roots.forEach(Node::blink);
        }

        public Collection<BigInteger> getValues() {
            List<BigInteger> values = new LinkedList<>();
            for (Node n : this.roots) {
                values.addAll(n.getValues());
            }
            return values;
        }

        private class Node implements Blinkable {
            private static Optional<Node> SENTINEL = Optional.empty();

            private Optional<BigInteger> value;
            private Optional<Node> left, right;

            Node() {
                this(Optional.empty());
            }

            Node(BigInteger value) {
                this(Optional.of(value));
            }

            Node(Optional<BigInteger> value) {
                this.value = value;
                this.left = Node.SENTINEL;
                this.right = Node.SENTINEL;
            }

            public Collection<BigInteger> getValues() {
                List<BigInteger> values = new LinkedList<>();

                // By design, a Node can have a value, or children with value,
                // or neither (SENTINEL), but never both.
                if (this.value.isPresent()) {
                    values.add(this.value.get());
                } else if (this.left.isPresent()) {
                    values.addAll(this.left.get().getValues());
                    values.addAll(this.right.get().getValues());
                }
                return values;
            }

            @Override
            public void blink() {
                if (this.value.isEmpty()) {
                    this.left.get().blink();
                    this.right.get().blink();
                    return;
                }

                // Rule 1
                if (this.value.get().equals(BigInteger.ZERO)) {
                    this.value = Optional.of(BigInteger.ONE);
                    return;
                }

                // Rule 2
                var numString = this.value.get().toString();
                if (numString.length() % 2 == 0) {
                    var sliceIndex = numString.length() / 2;
                    this.left = Optional.of(
                            new Node(new BigInteger(
                                    numString.substring(0, sliceIndex))
                            )
                    );
                    this.right = Optional.of(
                            new Node(new BigInteger(
                                    numString.substring(sliceIndex))
                            )
                    );
                    this.value = Optional.empty();
                    return;
                }

                // Rule 3
                this.value = Optional.of(
                        BigInteger.valueOf(2024).multiply(this.value.get())
                );
            }
        }
    }

    public BigInteger part_1(int[] stones) {
        var tree = new StoneTree(stones);
        IntStream.range(0, 25).forEach(_ -> {
            tree.blink();
        });
        Object[] values = tree.getValues().toArray();
        return BigInteger.valueOf(values.length);
    }

}

