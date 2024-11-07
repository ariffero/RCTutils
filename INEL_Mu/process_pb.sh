#!/bin/bash

echo fill = $3
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

echo root -b -q -l GetScalersForRun.C\($1,$3\)
root -b -q -l GetScalersForRun.C\($1,$3\) >logs/$1_$3_ZDC.log
ZDC=$(cat logs/$1_$3_ZDC.log | grep "Ratepp" | awk '{print $7}' | sed 's/Ratepp://')
ZDCSTART=$(cat logs/$1_$3_ZDC.log | grep "ratepp_start" | sed 's/.*ratepp_start = //')
ZDCMID=$(cat logs/$1_$3_ZDC.log | grep "ratepp_mid" | sed 's/.*ratepp_mid = //')
ZDCEND=$(cat logs/$1_$3_ZDC.log | grep "ratepp_end" | sed 's/.*ratepp_end = //')
echo "RUN=$1 FILL=$3 ZDCIR=$ZDC"
echo "RUN=$1 FILL=$3 ZDCIR=$ZDC" >> stats

echo "RUN=$1 FILL=$3 ZDCIRstart=$ZDCSTART"
echo "RUN=$1 FILL=$3 ZDCIRstart=$ZDCSTART" >> stats

echo "RUN=$1 FILL=$3 ZDCIRmid=$ZDCMID"
echo "RUN=$1 FILL=$3 ZDCIRmid=$ZDCMID" >> stats

echo "RUN=$1 FILL=$3 ZDCIRend=$ZDCEND"
echo "RUN=$1 FILL=$3 ZDCIRend=$ZDCEND" >> stats
					
										      
