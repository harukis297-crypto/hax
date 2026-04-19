#!/data/data/com.termux/files/usr/bin/bash

C1="\e[38;5;45m"
C2="\e[38;5;81m"
C3="\e[38;5;117m"
C4="\e[38;5;159m"
C5="\e[38;5;195m"
W="\e[1;37m"
R="\e[0m"

clear

echo -e "${C1}"
echo "  ██   ██  █████  ██████  ██   ██   ██   ██ ██"
echo "  ██   ██ ██   ██ ██   ██ ██  ██    ██   ██ ██"
echo "  ███████ ███████ ██████  █████     ██   ██ ██"
echo "  ██   ██ ██   ██ ██   ██ ██  ██    ██   ██ ██"
echo "  ██   ██ ██   ██ ██   ██ ██   ██ .  █████  ██"
echo -e "${C3}            H A R U K I   O S${R}"

sleep 1

for i in {1..50}
do
    echo -ne "${C2}═${R}"
    sleep 0.01
done

echo ""

user=$(whoami)

echo -e "\n${C1}╔══════════════════════════════╗${R}"
echo -e "${C3}║        HARUKI TERMINAL      ║${R}"
echo -e "${C1}╚══════════════════════════════╝${R}"

echo ""
echo -e "${C4}USER   :${W} $user${R}"

echo ""
echo -ne "${C2}SYSTEM LOAD : ${R}"

for i in {1..30}
do
    echo -ne "${C3}█${R}"
done

echo ""

echo -e "\n${C1}STATUS:${R}"
echo -e "${C4}• System Stable"
echo -e "${C5}• Services Running"
echo -e "${C3}• No Errors Detected${R}"
