package aoc._2024.day11;

import java.util.*;

public class StoneBlinker {

  static Map<Long, Long[]> stoneInfoMap = new HashMap<>();

  public StoneBlinker() {
  }

  record QueueInfo(long remainingBlinks, long stoneNumber)
  implements Comparable<QueueInfo> {
    @Override
    public int compareTo(QueueInfo queueInfo) {
      return Long.compare(this.remainingBlinks, queueInfo.remainingBlinks);
    }
  }

  static Long runBlinks(long blinks, Long[] stones) {

    if (blinks == 0L) {
      return 1L;
    }

    Queue<QueueInfo> workingQueue = initializeWorkingQueue(blinks, stones);
    long result = 0L;

    while (!workingQueue.isEmpty()) {
      var workingStone = workingQueue.poll();

      if (workingStone.remainingBlinks == 0) {
        result += 1L;
        continue;
      }

      Long[] blinkedStones = getBlinkedStones(workingStone.stoneNumber);
      Arrays.stream(blinkedStones)
          .forEach(s -> {
            workingQueue.add(new QueueInfo(
                workingStone.remainingBlinks - 1,
                s
            ));
          });
    }

    return result;
  }

  private static PriorityQueue<QueueInfo> initializeWorkingQueue(long blinks, Long[] stones) {
    PriorityQueue<QueueInfo> q = new PriorityQueue<>();
    Arrays.stream(stones)
        .forEach(s -> {
          q.add(new QueueInfo(blinks, s));
        });
    return q;
  }

  private static Long[] getBlinkedStones(long stone) {
    Long[] result = stoneInfoMap.get(stone);
    if (result != null) {
      return result;
    }

    List<Long> blinkedStones = new LinkedList<>();
    var stoneString = String.valueOf(stone);

    // Rule 1
    if (stone == 0L) {
      blinkedStones.add(1L);
    }

    // Rule 2
    else if (stoneString.length() % 2 == 0) {
      var index = stoneString.length() / 2;
      blinkedStones.add(Long.valueOf(stoneString.substring(0, index)));
      blinkedStones.add(Long.valueOf(stoneString.substring(index)));
    }

    // Rule 3
    else {
      blinkedStones.add(stone * 2024L);
    }
    return blinkedStones.toArray(new Long[0]);
  }

}

