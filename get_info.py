import requests
from requests.auth import HTTPBasicAuth
import sys
import argparse
import json

url = "http://127.0.0.1:7474/db/data/transaction/commit"

username = "neo4j"
password = "bloodhound"


def do_query(args):

    queries = {
        "spns" : "MATCH p=(n:User)-[r:HasSPNConfigured]-(m) RETURN m.name",
        "users" : "MATCH (n:User) RETURN n.name",
        "das" : "MATCH p =(n:User)-[r:MemberOf*1..]->(g:Group) where g.name=~'DOMAIN ADMINS@.*' return n.name",
        "unconstrained" : "MATCH (n) WHERE n.unconstraineddelegation=TRUE RETURN n.name",
        "local-admin" : "MATCH p=shortestPath((m:User {{name:\"{uname}\"}})-[r:AdminTo|MemberOf*1..]->(n:Computer)) return n.name,m.name"
    }

    query = ""
    if (args.users):
        query = queries["users"]
    elif (args.spns):
        query = queries["spns"]
    elif (args.das):
        query = queries["das"]
    elif (args.unconstrained):
        query = queries["unconstrained"]
    else:
        query = queries["local-admin"].format(uname=args.uname.upper().strip())

    data = {"statements":[{"statement":query}]}
    headers = {'Content-type': 'application/json', 'Accept': 'application/json; charset=UTF-8'}

    auth = HTTPBasicAuth(username, password)

    r = requests.post(url, auth=auth, headers=headers, json=data)
    x = json.loads(r.text)
    entry_list = x["results"][0]["data"]

    for value in entry_list:
        print(value["row"][0])


def main():

    parser = argparse.ArgumentParser(description="Helper script to pull lists of information from BloodHound for use")

    group = parser.add_argument_group("Main Arguments")

    mutex_group = group.add_mutually_exclusive_group(required=True)
    mutex_group.add_argument("--spns",dest="spns",default=False,action="store_true",help="Return a list of computers configured with a SPN relationship")
    mutex_group.add_argument("--users",dest="users",default=False,action="store_true",help="Return a list of all users")
    mutex_group.add_argument("--da",dest="das",default=False,action="store_true",help="Return a list of all Domain Admins")
    mutex_group.add_argument("--unconstrained",dest="unconstrained",default=False,action="store_true",help="Return a list of all objects configured with Unconstrained Delegation")
    mutex_group.add_argument("--adminto",dest="uname",default="",help="Return a list of computers that UNAME is a local administrator to")

    args = parser.parse_args()

    do_query(args)


if __name__ == "__main__":
    main()