def topological_sort(odict):
    # Create a graph and in-degree counter
    graph = defaultdict(set)
    in_degree = defaultdict(int)
    
    
    # Populate the graph and in-degree counter
    for key, values in odict.items():
        for value in values:
            if value != '':
                graph[value].add(key)
                in_degree[key] += 1
                if value not in in_degree:
                    in_degree[value] = 0
    print(in_degree)
    # Find all nodes with no incoming edges
    zero_in_degree_queue = deque([node for node in in_degree if in_degree[node] == 0])

    # Perform topological sort
    sorted_list = []
    while zero_in_degree_queue:
        node = zero_in_degree_queue.popleft()
        sorted_list.append(node)

        # Decrease the in-degree of each neighbor
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                zero_in_degree_queue.append(neighbor)

    # Check if the topological sort succeeded
    if len(sorted_list) == len(in_degree):
        return sorted_list
    else:
        raise ValueError("Circular reference detected")


try:
    sorted_keys = topological_sort(alias_map)
    print("Sorted keys:", sorted_keys)
except ValueError as e:
    print("Error:", e)
