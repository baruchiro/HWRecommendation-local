workflow "New workflow" {
  on = "push"
  resolves = ["python"]
}

action "python" {
  uses = "python"
  runs = "retrieve.py"
}
