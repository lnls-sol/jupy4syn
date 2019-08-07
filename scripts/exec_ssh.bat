set /p HOSTNAME="Remote machine hostname:"

USERNAME=%USERNAME%
SCRIPT="/usr/local/bin/connect_display.py"

plink -X %USERNAME%@%HOSTNAME% %SCRIPT%
