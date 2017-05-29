# es-curator
Elasticsearch-curator Ansible Module


## Example

```
---
- hosts: hosts
  tasks:
  - name: Run curator ACTION_FILE on remote hosts
    curator:
      path: "/home/ubuntu/snapshot.yml"
      config: "/home/ubuntu/.curator/curator.yml"
...
```
