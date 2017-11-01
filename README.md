# CheckingForBusyHours

### 1.Pip
If you dont have install pip3 (this works in linux) `$ sudo apt-get -y install python3-pip`

After that navigate to folder where repository is located `$ cd /your/directory/with/this/repository`
Add execution permission to file `$ chmod u+x name_of_script.py`
After that install dependencies  `$ pip3 install -r requirements.txt`

### 2. Running program
`$./busy_hours.py <start_date> <end_date> <your_token_here>`

You need to get api-token from giosg.
There is also possibility to use default values. api-token is not included so you have to add it.
`$ ./busy_hours.py`



