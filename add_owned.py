import requests
from requests.auth import HTTPBasicAuth
import sys
import argparse

url = "http://127.0.0.1:7474/db/data/transaction/commit"

username = "neo4j"
password = "bloodhound"


def run(file_name, obj):

    f = open(file_name).readlines()

    for line in f:

        statement = 'MATCH (n:{obj}) where n.name="{uname}" set n.owned=true return n'.format(uname=line.upper().strip(),obj=obj)
        data = {"statements":[{"statement":statement}]}
        headers = {'Content-type': 'application/json', 'Accept': 'application/json; charset=UTF-8'}

        auth = HTTPBasicAuth(username, password)

        r = requests.post(url, auth=auth, headers=headers, json=data)

        fail_resp = '{"results":[{"columns":["n"],"data":[]}],"errors":[]}'

        if r.text == fail_resp:
            print(obj + ": " + line.upper().strip() + " could not be added")
        else:
            print(obj + ": " + line.upper().strip() + " added successfully")


def main():

    parser = argparse.ArgumentParser()

    group = parser.add_argument_group("Main Arguments")

    mutex_group = group.add_mutually_exclusive_group(required=True)
    mutex_group.add_argument("--comp",dest="add_comp",default=False,action="store_true",help="Designation that the owned items are computers")
    mutex_group.add_argument("--user",dest="add_user",default=False,action="store_true",help="Designation that the owned items are users")

    parser.add_argument("filename")

    args = parser.parse_args()

    obj = ""
    if (args.add_comp):
        obj = "Computer"
    else:
        obj = "User"

    run(args.filename, obj)


if __name__ == "__main__":
    main()
