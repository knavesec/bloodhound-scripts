# Custom Userful Cypher Queries

## Notes - A little bit about Cypher and BloodHound's usage of such

#### Description

Neo4j is the backend database that combines nodes and relationship edges to display and connect data in new ways. In this case, BloodHound nodes are AD objects and edges are ACL and privilege escalation relationships between the nodes. This provides lateral movement and pivoting

#### Node Type

Creating a raw node is simple, but it's often beneficial to group nodes into certain types. These types can be queried during searches and grouped easier.

Return all nodes of the type `Type`
```
MATCH (n:<Type>) RETURN n
```
Note: without return, the query will not return nodes/information

BloodHound types are:
- User
- Group
- Computer
- Domain
- GPO
- OU

#### Node Attributes

Each node (object) has attributes associated with it, these store information and can be used to request specific information. These attributes are specified accessed with `n.attr`

Return `User` with name `USER1@DOMAIN.LOCAL`
```
MATCH (n:User) WHERE n.name="USER1@DOMAIN.LOCAL" RETURN n
```

A few common & useful attributes are:
- name
- objectsid
- email
- domain

Some helpful BloodHound specific attributes are:
- owned
- highvalue
- dontreqpreauth
- hasspn
- unconstraineddelegation

#### Edges

An edge is a one-way directional link that represents a relationship between two nodes. BloodHound uses edges to display when one node has a privilege over another (or many other reasons), malicious actors can use these edges to move laterally

```
-------     edge     -------
|node1| -----------> |node2|
-------              -------
```

1. Display each user that a computer has a session for
2. Display all edges between two nodes
```
1. MATCH (n:User), (m:Computer) MATCH p=(m)-[r:HasSession]->(n) RETURN p

2. MATCH (n:User {name:"USER1@DOMAIN.LOCAL"}), (m:Computer {name:"COMPUTER1.DOMAIN.LOCAL"}) RETURN (n)-[]-(m)
```

Notes:
- Store a relationship in variable `p`
- Syntax to look at a relationship with edges `(node)-[edge]->(node)`
- Note the `>` to indicate direction of the edge in the first (which requires a direction) but not the second (which is general and doesn't require a direction)
- New way to specify attributes `{attr:value}`

BloodHound edges:
- AdminTo
- HasSession
- MemberOf

Detailed BloodHound edges:
- CanRDP
- WriteDacl
- ExecuteDCOM
- etc

#### Relationships and paths

The goal of Neo4j is creating relationships between nodes and finding paths between nodes. BloodHound uses this to escalate privileges. The two functions primarily used are `shortestPath` and `allShortestPaths`.

1. Find the shortest path between `USER1@DOMAIN.LOCAL` and `COMPUTER1.DOMAIN.LOCAL` using ONLY `HasSession`,`AdminTo`,`MemberOf` edges
2. Find all short paths between `USER1@DOMAIN.LOCAL` and `COMPUTER1.DOMAIN.LOCAL` using all edges
3. Same query as 2. but manually specifying each edge, this allows you to remove one if desired
```
1. MATCH (n:User {name:"USER1@DOMAIN.LOCAL"}), (m:Computer {name:"COMPUTER1.DOMAIN.LOCAL"}) MATCH p=shortestPath((n)-[r:HasSession|AdminTo|MemberOf*1..]->(m)) RETURN p

2. MATCH (n:User {name:"USER1@DOMAIN.LOCAL"}), (m:Computer {name:"COMPUTER1.DOMAIN.LOCAL"}) MATCH p=allShortestPaths((n)-[r*1..]->(m)) RETURN p

3. MATCH (n:User {name:"USER1@DOMAIN.LOCAL"}), (m:Computer {name:"COMPUTER1.DOMAIN.LOCAL"}) MATCH p=allShortestPaths((n)-[r:MemberOf|HasSession|AdminTo|AllExtendedRights|AddMember|ForceChangePassword|GenericAll|GenericWrite|Owns|WriteDacl|WriteOwner|CanRDP|ExecuteDCOM|AllowedToDelegate|ReadLAPSPassword|Contains|GpLink|AddAllowedToAct|AllowedToAct|SQLAdmin*1..]->(m)) RETURN p
```
Notes:
- `*1..` allows for multi-node edge relationships

#### BloodHound Custom Query vs Neo4j Browser Query

The BloodHound custom query bar is used to run custom Cypher queries. The Neo4j browser is accessible at http://localhost:7474/browser/ and can also be used to run Cypher commands. Each have their own pros/cons:

BH:
- All nodes displayed in typical BH format with structure

- Queries won't tell you if there is a syntax error
- Can only return nodes, rather than raw data (like strings, numbers, attributes, etc)

Neo4j:
- Can get feedback on specific syntax issues
- Can output non-node data (like strings, numbers, attributes, etc)

- Returned node diagrams have no structure and are difficult to decipher (decypher lol)

Personally, I use the Neo4j browser to test queries, then execute them in the BH application when they are complete.


## Custom Queries

#### List all owned objects

```
MATCH (n) WHERE n.owned=True RETURN n
```

#### List all groups with “ADMIN” in the name

```
MATCH (n:Groups) WHERE n.name=~".*ADMIN.*" RETURN n
```

#### List all groups with “ADMIN” or “KEYWORD” in the name

```
MATCH (n:Groups) WHERE n.name=~".*ADMIN.*|.*KEYWORD.*" RETURN n
```

#### List all HVTs

```
MATCH (n) WHERE n.highvalue=true RETURN n
```

#### show all unconstrained delegation systems

```
MATCH (n) WHERE n.unconstraineddelegation=True RETURN n
```

#### Unset all owned users

```
MATCH (n) WHERE n.owned=true SET n.owned=false RETURN n
```

#### List all active relations of a certain type

```
MATCH (n) MATCH (m) MATCH p=(n)-[r:HasSession*1..]-(m) return p
```

#### List all users explicitly admin to certain computers

```
MATCH (n:User), (m:Computer) MATCH p=(n)-[r:AdminTo]->(m) RETURN p
```

#### Search from one object to another while being able to remove specific edges

```
MATCH (n:User) WHERE n.name=~'USER1@DOMAIN.LOCAL' MATCH (m:Group) WHERE m.name =~ 'DOMAIN ADMINS@DOMAIN.LOCAL' MATCH p=allShortestPaths((n)-[r:MemberOf|HasSession|AdminTo|AllExtendedRights|AddMember|ForceChangePassword|GenericAll|GenericWrite|Owns|WriteDacl|WriteOwner|CanRDP|ExecuteDCOM|AllowedToDelegate|ReadLAPSPassword|Contains|GpLink|AddAllowedToAct|AllowedToAct|SQLAdmin*1..]->(m)) RETURN p
```

#### Remove relationship from all nodes or specific (when one specific relationship is polluting search results)

```
1. MATCH (n)-[r:EDGE]-() DELETE r

2. MATCH (n) WHERE n.name="DOMAIN USERS@DOMAIN.LOCAL" MATCH (n)-[r:EDGE]-() DELETE r
```

#### shortest path from user to unconstrained delegation systems

```
MATCH (n) WHERE n.name='username' MATCH (m) WHERE m.unconstraineddelegation=True MATCH p=allShortestPaths((n)-[r:MemberOf|HasSession|AdminTo|AllExtendedRights|AddMember|ForceChangePassword|GenericAll|GenericWrite|Owns|WriteDacl|WriteOwner|CanRDP|ExecuteDCOM|AllowedToDelegate|ReadLAPSPassword|Contains|GpLink|AddAllowedToAct|AllowedToAct|SQLAdmin*1..]->(m)) RETURN p
```

#### shortest path from any owned principal to unconstrained delegation system

```
MATCH (n {owned: true}),(m {unconstraineddelegation: true}),p=shortestPath((n)-[r:MemberOf|HasSession|AdminTo|AllExtendedRights|AddMember|ForceChangePassword|GenericAll|GenericWrite|Owns|WriteDacl|WriteOwner|CanRDP|ExecuteDCOM|AllowedToDelegate|ReadLAPSPassword|Contains|GpLink|AddAllowedToAct|AllowedToAct|SQLAdmin*1..]->(m)) RETURN p
```