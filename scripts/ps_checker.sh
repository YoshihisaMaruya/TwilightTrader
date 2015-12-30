bash ${TT_HOME}/collect/scripts/alive.sh > mail_body.txt
python3.4 ${TT_HOME}/scripts/gmailer.py ps_checker mail_body.txt
