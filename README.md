# Emailbox-Python

## Purpose
The System is designed to improve the delivery efficiency by helping people to receive the parcel when he/she is not at home.
## Structure

![structure](http://imgur.com/Ac08dq8.jpg)
    
## How to Use
### - Hardware
You will need the following stuffs to assemble, also you can find GPIO definitions in **Emailbox** **.py**, then you can search for the datasheet of [L293D](http://www.ti.com/lit/ds/symlink/l293.pdf) to wire them up!
1. Raspberry Pi 3
2. Electromagnetic * 2
3. L293D ic chip
4. 9v battery
5. Box(you can find the layout at the directory " /Layout ")
### - Software 
1. Go to directory  " **/API/Config.py** " , then change the following two variables 

```python
#Gmail Account for Sending System Email
#You need to set up account id and password
GMAIL_ACCOUNT = None
GMAIL_PASSWORD = None
```

2. Go to directory  " **/API/CreateDatabase.py** ", find the function " **AddSystemData** ", then follow the instruction below to add your own data.

```python
#Add Your Own Data
cursor.execute("INSERT INTO CLIENTS VALUES(NULL, 'Floor', 'First Name', 'Last Name', 'test@gmail.com')")
```

3. Install it

```shell
python setup.py install
```

4. Give it a shot!

```
python -m Emailbox
```

# Result
![result](http://imgur.com/xgkZQJS.jpg)
