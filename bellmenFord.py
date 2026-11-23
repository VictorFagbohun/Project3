def bellmenFord(nodes, edges, source_index=0):
    path_lengths = {}
    paths = {}

    for v in nodes:
        path_lengths[v] = float('inf')
        paths[v] = []
    
    path_lengths[source_index] = 0
    paths[source_index] = [source_index]

    for  _ in range(len(nodes) - 1):
        for (u,v), w_uv in edges.items():
            if path_lengths[u] + w_uv < path_lengths[v]: #Checking to see if the new proposed length is shorter than the length we already have
                path_lengths[v] = path_lengths[u] + w_uv 
                paths[v] = paths[u] + [v]       
    
    
    return path_lengths, paths