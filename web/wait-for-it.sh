#!/bin/sh
# wait-for-it.sh

# This script waits until a TCP host and port are available.

TIMEOUT=15
HOST="$1"
PORT="$2"
shift 2
CMD="$@"

echo "Waiting for $HOST:$PORT to be available..."

for i in `seq $TIMEOUT`; do
    nc -z "$HOST" "$PORT" && echo "$HOST:$PORT is available" && exec $CMD
    echo "$HOST:$PORT is not yet available, waiting..."
    sleep 1
done

echo "Timeout reached. $HOST:$PORT is not available."
exit 1