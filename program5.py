import numpy as np
from numpy import inf

# Given distances between cities
d = np.array([[0, 10, 12, 11, 14],
              [10, 0, 13, 15, 8],
              [12, 13, 0, 9, 14],
              [11, 15, 9, 0, 16],
              [14, 8, 14, 16, 0]])

iteration = 100
n_ants = 5
n_cities = 5

# Initialization
m = n_ants
n = n_cities
e = 0.5  # evaporation rate
alpha = 1  # pheromone factor
beta = 2   # visibility factor

# Calculate visibility = 1/distance, avoid division by zero
visibility = 1 / d
visibility[visibility == inf] = 0  # Replace infinite with zero

# Initialize pheromone levels on paths between cities (n x n matrix)
pheromone = 0.1 * np.ones((n, n))

# Initialize routes of ants: each ant's route length is n+1 (return to start)
routes = np.ones((m, n + 1), dtype=int)

for ite in range(iteration):
    # Start all ants at city 1 (index 1)
    routes[:, 0] = 1

    for i in range(m):  # For each ant
        temp_visibility = np.array(visibility)  # Copy visibility matrix
        visited = [1]  # Keep track of visited cities for ant i

        for j in range(n - 1):
            cur_loc = routes[i, j] - 1  # Current city index (0-based)

            # Set visibility to zero for already visited cities
            for v in visited:
                temp_visibility[:, v - 1] = 0

            # Calculate the probability for each city to be chosen next
            pheromone_feature = np.power(pheromone[cur_loc, :], alpha)
            visibility_feature = np.power(temp_visibility[cur_loc, :], beta)

            combined_feature = pheromone_feature * visibility_feature
            total = np.sum(combined_feature)
            if total == 0:
                probs = combined_feature  # all zeros; no next city
            else:
                probs = combined_feature / total

            # Calculate cumulative probabilities
            cum_prob = np.cumsum(probs)

            r = np.random.random_sample()
            next_city = np.where(cum_prob > r)[0][0] + 1  # City numbering from 1

            routes[i, j + 1] = next_city
            visited.append(next_city)

        # Add the last unvisited city to complete the route
        unvisited = list(set(range(1, n + 1)) - set(visited))
        if unvisited:
            routes[i, -2] = unvisited[0]
        else:
            routes[i, -2] = routes[i, -3]  # fallback if none left

        # Return to starting city
        routes[i, -1] = 1

    routes_opt = np.array(routes)

    dist_cost = np.zeros(m)

    # Calculate total distance of the tour for each ant
    for i in range(m):
        s = 0
        for j in range(n):
            s += d[routes_opt[i, j] - 1, routes_opt[i, j + 1] - 1]
        dist_cost[i] = s

    dist_min_loc = np.argmin(dist_cost)
    dist_min_cost = dist_cost[dist_min_loc]
    best_route = routes_opt[dist_min_loc, :]

    # Evaporation
    pheromone = (1 - e) * pheromone

    # Update pheromone based on route quality
    for i in range(m):
        delta = 1 / dist_cost[i]
        for j in range(n):
            from_city = routes_opt[i, j] - 1
            to_city = routes_opt[i, j + 1] - 1
            pheromone[from_city, to_city] += delta
            pheromone[to_city, from_city] += delta  # Assuming undirected graph

print('Routes of all the ants at the end:')
print(routes_opt)
print()
print('Best path:', best_route)
print('Cost of the best path:', int(dist_min_cost))
