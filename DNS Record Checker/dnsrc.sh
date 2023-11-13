#!/bin/bash

while [ -n "$1" ]
do
        case "$1" in
                -u) address="$2" 
                shift ;;
                -r) record="$2" 
                shift ;;
                --list) file="$2" 
                shift ;;
                *) echo -e "Usage: dnsrc [-u example.com] [-r TXT] [--list example.txt]\n\t-u The option specifies the domain name of the remote host.\n\t-r The option specifies the record on the domain name for which information is to be retrieved.\n\t--list The option points to a file with a list of records that need to be checked." ;;
        esac
        shift
done

if [[ "$file" ]] && [[ ! "$record" ]] && [[ "$address" ]]
then
        for line in $(cat $file)
        do
                #echo "$line"
                RESULT=$(dig +nocmd +noquestion +noauthority +noadditional +nocomments +nostats +nomultiline +noshort @8.8.8.8 $address $line)
                if [[ "$RESULT" ]]
                then
                        echo -e "\033[1;33m$line \033[0;37m----> $RESULT"
                fi
        done
elif [[ "$record" ]] && [[ ! "$file" ]] && [[ "$address" ]]
then
        dig +nocmd +noquestion +noauthority +noadditional +nocomments +nostats +nomultiline +noshort @8.8.8.8 $address $record
else
        echo -e "Usage: dnsrc [-u example.com] [-r TXT] [--list example.txt]\n\t-u The option specifies the domain name of the remote host.\n\t-r The option specifies the record on the domain name for which information is to be retrieved.\n\t--list The option points to a file with a list of records that need to be checked."
fi
