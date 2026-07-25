#!/bin/bash

# Modern terminal colors
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0;34m' # No Color
RESET='\033[0m'

echo -e "${PURPLE}====================================================${RESET}"
echo -e "${CYAN}     ⚡ FIVEM CFX FINDER & IP RESOLVER ⚡${RESET}"
echo -e "${CYAN}             Arena.ai Web Tool${RESET}"
echo -e "${PURPLE}====================================================${RESET}"
echo ""

echo -e "${YELLOW}[*] Checking Python dependencies...${RESET}"
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[+] Dependencies are verified and installed!${RESET}"
else
    echo -e "${RED}[-] Dependency installation failed. Trying fallback...${RESET}"
    pip install flask requests beautifulsoup4
fi

echo ""
echo -e "${GREEN}[+] starting the application on http://localhost:5000 ...${RESET}"
echo -e "${CYAN}[i] Press Ctrl+C to stop the server.${RESET}"
echo ""

python3 app.py
