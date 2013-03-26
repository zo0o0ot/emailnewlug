emailnewlug.py
============

A python script to automate the sending of the weekly "This Week..." email 
to the NEWLUG mailing list.

To be run via cron on Mondays 8:30am central time.

#example
30 8 * * 1 /usr/local/bin/python /home/newlug/crons/emailnewlug.py --user USER --pass PASSWORD RECIPIENT
