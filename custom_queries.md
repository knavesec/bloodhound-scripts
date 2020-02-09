# Custom Queries

## Description

Some custom Cypher queries for use with Bloodhound

### List all owned objects

```
MATCH (n) WHERE n.owned=True RETURN n
```

### List all groups with “ADMIN” in the name

```
MATCH (n:Groups) WHERE n.name=~".*ADMIN.*" RETURN n
```

### List all groups with “ADMIN” or “KEYWORD” in the name

```
MATCH (n:Groups) WHERE n.name=~".*ADMIN.*|.*KEYWORD.*" RETURN n
```

### List all HVTs

```
MATCH (n) WHERE n.highvalue=true RETURN n
```

### Show all unconstrained delegation systems

```
MATCH (n) WHERE n.unconstraineddelegation=True RETURN n
```

### Unset all owned users

```
MATCH (n) WHERE n.owned=true SET n.owned=false RETURN n
```

### List all active relations of a certain type

```
MATCH (n) MATCH (m) MATCH p=(n)-[r:HasSession*1..]-(m) return p
```

### List all users explicitly admin to certain computers

```
MATCH (n:User), (m:Computer) MATCH p=(n)-[r:AdminTo]->(m) RETURN p
```

### Search from one object to another while being able to remove specific edges

```
MATCH (n:User) WHERE n.name=~'USER1@DOMAIN.LOCAL' MATCH (m:Group) WHERE m.name =~ 'DOMAIN ADMINS@DOMAIN.LOCAL' MATCH p=allShortestPaths((n)-[r:MemberOf|HasSession|AdminTo|AllExtendedRights|AddMember|ForceChangePassword|GenericAll|GenericWrite|Owns|WriteDacl|WriteOwner|CanRDP|ExecuteDCOM|AllowedToDelegate|ReadLAPSPassword|Contains|GpLink|AddAllowedToAct|AllowedToAct|SQLAdmin*1..]->(m)) RETURN p
```

### Remove relationship from all nodes or from specific node (when one specific relationship is polluting search results)

```
1. MATCH (n)-[r:EDGE]-() DELETE r

2. MATCH (n) WHERE n.name="DOMAIN USERS@DOMAIN.LOCAL" MATCH (n)-[r:EDGE]-() DELETE r
```

### Shortest path from user to unconstrained delegation systems

```
MATCH (n) WHERE n.name='username' MATCH (m) WHERE m.unconstraineddelegation=True MATCH p=allShortestPaths((n)-[r:MemberOf|HasSession|AdminTo|AllExtendedRights|AddMember|ForceChangePassword|GenericAll|GenericWrite|Owns|WriteDacl|WriteOwner|CanRDP|ExecuteDCOM|AllowedToDelegate|ReadLAPSPassword|Contains|GpLink|AddAllowedToAct|AllowedToAct|SQLAdmin*1..]->(m)) RETURN p
```

### Shortest path from any owned principal to unconstrained delegation system

```
MATCH (n {owned: true}),(m {unconstraineddelegation: true}),p=shortestPath((n)-[r:MemberOf|HasSession|AdminTo|AllExtendedRights|AddMember|ForceChangePassword|GenericAll|GenericWrite|Owns|WriteDacl|WriteOwner|CanRDP|ExecuteDCOM|AllowedToDelegate|ReadLAPSPassword|Contains|GpLink|AddAllowedToAct|AllowedToAct|SQLAdmin*1..]->(m)) RETURN p
```
