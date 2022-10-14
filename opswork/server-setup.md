# Production Settings for Veeta

## Change permissions to allow scripts to run

chmod u+x start.sh

## Allow root to run a script as djangoadmin

sudo echo 'root ALL=(djangoadmin) /home/djangoadmin/start.sh' | EDITOR='tee -a' visudo

sudo echo 'root ALL=(djangoadmin) /home/djangoadmin/start-veeta.sh' | EDITOR='tee -a' visudo
