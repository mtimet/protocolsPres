protocolsPres
=============

Presidential elections round 1 protocols

***Run the script***

    git clone https://github.com/radproject/protocolsPres.git
    apt-get install python-setuptools
    easy_install beautifulsoup4
    python script.py 

***Convert xlslx to csv***

the script needs python3. (easiest path to properly handle unicode strings)

It depends on openpyxl and pandas libraries and their dependencies.

the output will be saved to csvout

	python tocsv.py 

