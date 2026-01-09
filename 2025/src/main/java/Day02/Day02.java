void main(String[] args) throws IOException {
    if (args.length != 1) {throw new IllegalArgumentException("Unexpected input!");}

    IO.println("2025 - Day 02");
    List<Long> uncheckedIDs =
            parseIDRanges(List.of(Files.readString(Path.of(args[0])).strip().split(",")));

    IO.println("Part 1: " + part1(uncheckedIDs));
}

long part1(List<Long> ids) {
    long answer = 0;
    for (long id : ids) {
        String s_id = String.valueOf(id);
        int s_id_len = s_id.length();
        if (s_id.substring(0, s_id_len / 2).equals(s_id.substring(s_id_len / 2))) {
            answer += Long.parseLong(s_id.substring(0, s_id_len));
        }
    }
    return answer;
}

int part2(List<Integer> ids) {
    return 0;
}

private List<Long> parseIDRanges(Iterable<String> ranges) {
    List<Long> ids = new ArrayList<>();
    for (String range : ranges) {
        String[] bounds = range.split("-");
        LongStream r = LongStream.rangeClosed(Long.parseLong(bounds[0]), Long.parseLong(bounds[1]));
        for (Long i : r.toArray()) {
            ids.add(i);
        }
    }
    return ids;
}

