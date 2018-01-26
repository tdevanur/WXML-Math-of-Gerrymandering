import random
import math

"""
Mathematics of Gerrymandering, Phase 1
 Washington Experimental Mathematics Lab, 18 Wi
 Project Description: https://weifanjiang.github.io/WXML-18wi-Research/
 Project GitHub: https://github.com/weifanjiang/WXML-18wi-Research

 This file contains a sampling program based on the Metropolis Algorithm
 and the Ising Model.
"""


class MetropolisIsing:

    def __init__(self, m, n, beta, N):
        """
        Constructs a new Metropolis-Ising model based on input parameters.
        :param m: width of input 2D grid
        :param n: height of input 2D grid
        :param beta: constant used to evaluate probability vector
        :param N: number of iterations when simulating random walk
        :return: a new MetropolisIsing object
        """

        # Check input validity and initiate class fields
        assert m > 0 and n > 0 and N > 0
        self.m, self.n, self.beta, self.N = m, n, beta, N

        # Record edges within the input graph G with an adjacent matrix:
        # Suppose the vertices in original input graph G is numbered 0 to nm - 1 such as:
        #
        #  0  -  1  -  2  -  3  - ... - m-1
        #  |     |     |     |           |
        #  m  - m+1 - m+2 - m+3 - ... - 2m-1
        #  |     |     |     |           |
        # ... - ... - ... - ... - ... - ...
        #
        # We can use a 2D array to record the edges between these numbered vertices.
        # For vertices i, j such that 0 <= i, j <= nm - 1, in 2D array Edges
        # Edges[i][j] = true if and only if there's an edge between vertices i and j.
        # Similarly, we have Edges[i][j] == Edges[j][i] always.

        self.Edges = []
        for x in range(self.n * self.m):
            row = [0, ] * self.m * self.n
            self.Edges.append(row)
        # Edges = n by m matrix with 0 at all entries.

        for vertex in range(self.m * self.n):
            # Four possible neighbors of current vertex:
            #   two vertices left and right: vertex + 1, - 1
            #   two vertices top and bottom: vertex + m, - m
            neighbors = [vertex - 1, vertex + 1, vertex - self.m, vertex + self.m]
            for neighbor in neighbors:
                if 0 <= neighbor <= n*m - 1:  # Check if each neighbor is valid
                    self.Edges[vertex][neighbor] = self.Edges[neighbor][vertex] = 1

    def get_random_vertex(self):
        """
        Give caller a random vertex in the G_tilde graph
        :return: a n*m-length list which represents a vertex in G_tilde
        """
        rand_vertex = [1, ] * self.n * self.m
        for i in range(len(rand_vertex)):
            if random.randint(0, 2) == 2:
                rand_vertex[i] = -1
        return rand_vertex

    def get_random_neighbor(self, vertex):
        """
        Return a random neighbor of vertex in G_tilde
        :param vertex: a vertex in G_tilde, which is a n*m-length list with entries being {1, -1}
        :return: another n*m-length list which only differs in one entry with vertex
        """
        neighbor = vertex[:]
        rand_index = random.randint(-1, len(neighbor) - 1)
        neighbor[rand_index] = neighbor[rand_index] * -1
        return neighbor

    def get_raw_probability(self, vertex):
        """
        Get the raw (not normalized) probability vector component of vertex
        :param vertex: a vertex in G_tilde, which is a n by m matrix with entries being {-1. 1}
        :return: a double equals to the raw probability value of vertex in G_tilde
        """

        # Compute sum_{(v1, v2) in E_tilde} f(v1)*f(v2)
        neighbor_sum = 0.0
        for i in range(0, self.n * self.m):
            for j in range(i + 1, self.n * self.m):
                # Note: checking two entries at the same time for assertion
                if self.Edges[i][j] == 1 and self.Edges[j][i]:
                    neighbor_sum = neighbor_sum + vertex[i] * vertex[j]

        # Multiply by beta!!!
        # Remember to multiply by 1.0 since do not want to lose accuracy
        result = neighbor_sum * 1.0 * self.beta

        # Calculate exponential and return
        result = math.exp(result)
        return result

    def get_probability_ratio(self, curr, neighbor):
        """
        Get the f_beta(neighbor)/f_beta(curr) ratio
        :param curr: current vertex in G_tilde that we are on
        :param neighbor: neighbor which is a candidate of next movement
        :return: a double which equals the ratio
        """
        neighbor_uw = self.get_raw_probability(neighbor)
        curr_uw = self.get_raw_probability(curr)
        return neighbor/curr

    def get_rand_walk_iterations(self):
        """
        Get numbers of iterations set for random walk
        :return: self.beta
        """
        return self.beta

    def get_next_movement(self, curr):
        """
        Get the next movement of random walk on G_tilde
        :param curr: current vertex in G_tilde that random walk is on
        :return: next vertex in G_tilde that random walk will advance to
        """
        candidate = self.get_random_neighbor(curr)
        r = self.get_probability_ratio(curr, candidate)
        if r >= 1:
            return candidate
        else:
            rand_num = random.uniform(0.0, 1.0)
            if rand_num < r:
                return candidate
            else
                return curr[:]

    @staticmethod
    def run():
        """
        static method which executes a round of sampling
        which asks user for arguments, then construct a model instance and start sampling.
        """

        raw_in = input('Please input the n, m, beta, N parameters, separated by space: ')

        [n, m, beta, N] = raw_in.split(' ')
        n, m, beta, N = int(n), int(m), float(beta), int(N)
        model = MetropolisIsing(n, m, beta, N)
        print('Set up complete.')
        see_intermediate = input('Display all intermediate steps? (y/n) ')

        x0 = model.get_random_vertex()
        print('x0 = ' + str(x0))
        curr = x0
        for count in range(N):
            curr = model.get_next_movement(curr)
            if see_intermediate == 'y':
                print('x' + str(count + 1) + ' = ' + str(curr))





MetropolisIsing.run()
