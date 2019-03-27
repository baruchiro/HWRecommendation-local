workflow "Python test" {
  resolves = ["python-nose-test"]
  on = "pull_request"
}

action "python-nose-test" {
  uses = "CyberZHG/github-action-python-test@0.0.1"
}
