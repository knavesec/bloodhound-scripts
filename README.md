# Bloodhound helper scripts and docs

## add_owned.py

#### Description

A quick script to add lists of compromised users and computers to BloodHound

#### Usage

TODO:
Add your Neo4j username and password to the start of the script

```
usage: add_owned.py [-h] (--comp | --user) filename

positional arguments:
  filename

optional arguments:
  -h, --help  show this help message and exit

Main Arguments:
  --comp      Designation that the owned items are computers
  --user      Designation that the owned items are users
```

Examples
```
python3 add_owned.py --users ./userfile
python3 add_owned.py --comp ./computerfile
```

Example files. Note: the name of the computers/users to add must match usernames and computer names already in BloodHound
- users must have @domain.local appended
- computers must have .domain.local appended (also cannot be added by IP)

Users:
```
user01@domain.local      <- will be added
user02@domain.local      <- will be added
user02                   <- will not be added  
```
Computers:
```
computer01.domain.local  <- will be added
computer02.domain.local  <- will be added
computer02               <- will not be added
```

## get_info.py

#### Description

Script to pull various forms of information out of BloodHound including lists of:
- Computers with Service Principal Names configured (only compatible with custom BH version)
- All Domain Users
- All Domain Admins
- All Computers/Users configured with Unconstrained Delegation
- Computers that an input user ```UNAME``` has local administrator privileges over
- Users that are administrators of input computer ```COMP```

#### Usage

TODO:
Add your Neo4j username and password to the start of the script

```
usage: get_info.py [-h]
                   (--spns | --users | --da | --unconstrained | --adminto UNAME | --adminsof COMP)

Helper script to pull lists of information from BloodHound for use

optional arguments:
  -h, --help       show this help message and exit

Main Arguments:
  --spns           Return a list of computers configured with a SPN
                   relationship
  --users          Return a list of all users
  --da             Return a list of all Domain Admins
  --unconstrained  Return a list of all objects configured with Unconstrained
                   Delegation
  --adminto UNAME  Return a list of computers that UNAME is a local
                   administrator to
  --adminsof COMP  Return a list of users that are administrators to COMP
```

Examples
```
python3 get_info.py --spns
python3 get_info.py --users
python3 get_info.py --da
python3 get_info.py --unconstrained
python3 get_info.py --adminto user01@domain.local
python3 get_info.py --adminsof computer01.domain.local
```
