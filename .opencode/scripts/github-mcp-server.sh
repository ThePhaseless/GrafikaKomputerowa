#!/bin/sh
export GITHUB_PERSONAL_ACCESS_TOKEN="$(gh auth token)"
exec "$(dirname "$0")/../bin/github-mcp-server" stdio "$@"
