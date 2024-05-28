#!/bin/bash

set -e

host="$1"
shift
cmd="$@"

until nc -z "$host" 61613; do
  echo "Waiting for ActiveMQ at $host:61613..."
  sleep 2
done

>&2 echo "ActiveMQ is up - executing command"
exec $cmd
