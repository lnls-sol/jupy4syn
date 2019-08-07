#!/bin/bash

echo "Remote machine hostname: "
read HOSTNAME

USERNAME=$USER
SCRIPT="/usr/local/bin/connect_display.py"

ssh -o StrictHostKeyChecking=no -X ${USERNAME}@${HOSTNAME} "${SCRIPT}"
