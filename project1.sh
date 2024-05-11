#!/bin/bash

if [ $# -ne 3 ]; then
        echo "useage: ./project1.sh file1 file2 file3 "
        exit 1
fi

echo "************OSS1-Project1************"
echo "*        StudentID : 12234174       *"
echo "*        Name : Soobeen In          *"
echo "*************************************"

flag=1

while [ $flag -eq 1 ]
do
        echo " "
        echo " "
        echo "[MENU]"
        echo "1. Get the data of Heung-Min-Son's Current Club, Appearances, Goals, Assists in players.csv"
        echo "2. Get the team data to enter a league position in teams.csv"
        echo "3. Get the Top-3 Attendance matches in mateches.csv"
        echo "4. Get the team's league position and team's top scorer in teams.csv & players.csv"
        echo "5. Get the data of the winning team by the largest difference on home stadium in teams.csv & matches.csv"
        echo "6. Get the data modified format of date_GMT in matches.csv"
        echo "7. Exit"
        read -p "Enter your CHOICE (1~7):" choice
        case "$choice" in
        "1")
                read -p "Do you want to get the Heung-Min Son's data?(y/n):" answer
                if [ "$answer" == "y" ]
                then
                      cat $2 | awk -F, '$1~"Heung-Min Son"{printf("Team:%s,Apperance:%s,Goal:%s,Assist:%s", $4, $6, $7, $8)}'
                fi;;
        "2")
                read -p "What do you want to get the team data of league_position[1~20]:" answer
                cat $1 | awk -v a=$answer -F, '$6==a{printf("%s %s %s", $6, $1, $2/($2+$3+$4))}';;
        "3")
                read -p "Do you want to know Top-3 attendance data?(y/n):" answer
                if [ "$answer" == "y" ]
                then
                        echo "***Top-3 Attendance Match***"
                        cat $3 | sort -t, -n -r -k 2 |  head -n 3 | awk -F, '{printf("\n%s vs %s (%s)\n%s %s\n", $3, $4, $1, $2, $7)}'
                fi;;
        "4")
                read -p "Do you want to get each team's ranking and the highest-scoring player?(y/n):" answer
                if [ "$answer" == "y" ]
                then
                        IFS=:
                        index=0
                        for i in $( cat $1 | sort -t, -n -k 6 | awk -F, '{print $1":"}');
                        do
                                if [ "$index" != "0" ]; then
                                        echo ""
                                        echo "$index $i" | tr -d "\n"
                                        cat $2 | grep -w "~$i" | LC_ALL=C sort -t, -n -r -k 7 | head -n 1 | awk -F, '{printf("\n%s %s\n", $1, $7)}'

                                fi
                                index=$((index+1))
                        done

                fi;;
        "5")
                read -p "Do you want to modify the format of date?(y/n):" answer
                if [ "$answer" == "y" ]; then
                        cat $3 | sed '1d' | head -n 10 | awk -F, '{print $1}' | awk '{printf("%s/%s/%s %s\n", $3 ,$1 ,$2, $5)}' | sed 's/Jan/01/g' | sed 's/Feb/02/g' | sed 's/Mar/03/g' | sed 's/Apr/04/g' | sed 's/May/05/g' | sed 's/Jun/06/g'| sed 's/Jul/07/g' | sed 's/Aug/08/g' | sed 's/Sep/09/g' | sed 's/Oct/10/g' | sed 's/Nov/11/g' | sed 's/Dec/12/g'
                fi;;
        "6")
                PS3="Enter your team number:"
                IFS=:
                select var in $( cat $1 | sed '1d' | awk -F, '{print $1":"}' | tr -d "\n" )
                do
                        max_gap=$( cat $3 | sed '1d' | awk -F, '$5>$6{printf("%s,%s\n", $3, $5-$6)}' |sort -t, -n -r -k 2 | grep -w "$var" | head -n 1 | awk -F, '{print $2}' )
                        cat $3 | sed '1d' | awk -F, -v a=$var '$3==a{printf("%s,%s,%s,%s,%s,%s\n", $1, $3, $4, $5, $6, $5-$6)}' | awk -F, -v b=$max_gap '$6==b{printf("\n%s\n%s %s vs %s %s\n", $1, $2, $4, $5, $3)}'
                        break;
                done
                ;;
        "7")
                echo "Bye!"
                flag=0;;
        esac
done
