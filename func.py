def find_edges(nodeCoords, n, k):
    mt = [-1] * k
    g = list()
    for i in range(n):
        g.append([])
    for key, value in nodeCoords["left"].items():
        for node in value[0]:
            g[key].append(node)

    for v in range(n):
        used = [False] * n
        try_kuhn(v, used, mt, g)

    return mt


def try_kuhn(v, used, mt, g):
    if used[v]:
        return False
    used[v] = True
    for i in range(len(g[v])):
        to = g[v][i]
        if mt[to] == -1 or try_kuhn(mt[to], used, mt, g):
            mt[to] = v
            return True
    return False





