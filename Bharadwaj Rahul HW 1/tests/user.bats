load harness

@test "user-1" {
  check '3 % 2' '1'
}

@test "user-2" {
  check '-2 * 3 % 2' '0'
}

@test "user-3" {
  check '5 % 3 % 2' '0'
}

@test "user-4" {
  check '5 * 3 % 1' '0'
}

@test "user-5" {
  check '0 % 1 * 1' '0'
}