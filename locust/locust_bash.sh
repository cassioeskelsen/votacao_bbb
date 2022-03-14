#!/bin/bash

LOG_LEVEL=error
LOG=locust.log
MASTER_PORT=5557
MASTER_IP=127.0.0.1
COUNT_OF_USERS=10000
cores=8
SERVER_HOST=https://bbbpython.azurewebsites.net
WEB_PORT=80
TOTAL_TIME=30s

echo -e "\nStart LOCUST MASTER\n"
locust -f locustfile.py --headless -L $LOG_LEVEL --logfile=$LOG --master-bind-port=$MASTER_PORT \
--master-bind-host=$MASTER_IP -u $COUNT_OF_USERS  --print-stats --master --expect-workers=$cores --web-port=$WEB_PORT --host=$SERVER_HOST -t $TOTAL_TIME&
PID_MASTER=$!
echo "LOCAST MASTER PID = $PID_MASTER"
sleep 5

# start SLAVE (clients)
echo -e "\nStart LOCUST SLAVES\n"
PID_SLAVES=( )
for ((i = 1; i <= $cores; i++));do
  locust -f locustfile.py --worker --master-host=$MASTER_IP --master-port=$MASTER_PORT -L $LOG_LEVEL --logfile=$LOG &
  PID_SLAVES+=( $! )
done
echo "LOCAST SLAVE PIDs = ${PID_SLAVES[@]}"


