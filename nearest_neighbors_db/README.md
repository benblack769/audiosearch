
The Nearest neighbor DB takes in a set of embeddings at initialization. It is not currently able to update the database dynamically, but only respond to requests.

### Initialization

Database can be started with

### Query API

Get with fields:

```
{
    "query": <Hex64 encoding of query vector>,
    "comparator": "cosine"
}
```

#### Format of query vector


#### Comparator types

Currently, only supported query type is cosine distance.
