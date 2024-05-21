#!/bin/bash
root -b -q -l readGRPmapSingle.C\($1,$2\)

mkdir logs

lastTS=$(cat lastTS)
lastTSend=$(cat lastTSend)
echo root -b -q -l GetScalers.C\(\"$1\",$lastTS\)
root -b -q -l GetScalers.C\(\"$1\",$lastTS\) >logs/$1_$2.log

TRG=$(cat logs/$1_$2.log |grep "0 LMB "|awk '{print $3}')
CLOCK=$(cat logs/$1_$2.log |grep "2 LMB "|awk '{print $3}')
echo $CLOCK
duration=$(echo 24.950785*$CLOCK/1000000000|bc)

echo "RUN=$1 TSstart=$lastTS TSend=$lastTSend TRG=$TRG CLOCK=$CLOCK duration_in_s=$duration"
echo "RUN=$1 TSstart=$lastTS TSend=$lastTSend TRG=$TRG CLOCK=$CLOCK duration_in_s=$duration" >>stats
