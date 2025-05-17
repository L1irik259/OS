#!/bin/bash

PID_FILE=".pid"
PID_FILE2=".pid2"

OUTPUT_FILE="top_monitor.log"

SCRIPT_PID=$(cat "$PID_FILE")
SCRIPT_PID2=$(cat "$PID_FILE2")


echo "Top Monitoring Script Started at $(date)" > "$OUTPUT_FILE"
echo "----------------------------------------" >> "$OUTPUT_FILE"

while true; do
    TOP_OUTPUT=$(top -b -n 1)
    
    MEM_INFO=$(echo "$TOP_OUTPUT" | head -n 5 | tail -n 2)
    
    SCRIPT_INFO=$(echo "$TOP_OUTPUT" | grep "$SCRIPT_PID")
    SCRIPT_INFO2=$(echo "$TOP_OUTPUT" | grep "$SCRIPT_PID2")
    
    TOP5=$(echo "$TOP_OUTPUT" | awk 'NR>7 && NR<=12 {print $1,$12}')
    
    echo -e "\nTimestamp: $(date)" >> "$OUTPUT_FILE"
    echo "----------------------------------------" >> "$OUTPUT_FILE"
    
    echo "Memory Info:" >> "$OUTPUT_FILE"
    echo "$MEM_INFO" >> "$OUTPUT_FILE"
    
    echo -e "\nScript Process (PID $SCRIPT_PID):" >> "$OUTPUT_FILE"
    echo "$SCRIPT_INFO" >> "$OUTPUT_FILE"

    echo -e "\nScript Process (PID $SCRIPT_PID2):" >> "$OUTPUT_FILE"
    echo "$SCRIPT_INFO2" >> "$OUTPUT_FILE"

    echo -e "\nTop 5 Processes:" >> "$OUTPUT_FILE"
    echo "$TOP5" | awk '{print "PID: " $1 ", Command: " $2}' >> "$OUTPUT_FILE"
    
    sleep 0.5
done