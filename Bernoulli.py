import random
from copy import deepcopy
import matplotlib.pyplot as plt

class AgentInteractionModelBernoulli:
    def __init__(self):
        self.vowels = ['a', 'i']
        self.personalities = ['N', 'Q']

    def create_agent(self, vowel, personality):
        return [vowel, personality]

    def create_identical_population(self, N):
        population = []
        for _ in range(N):
            agent = self.create_agent(self.vowels[1], self.personalities[0])
            population.append(agent)
        return population

    def create_random_population(self, N):
        population = []
        for _ in range(N):
            v = random.randint(0, 1)
            p = random.randint(0, 1)
            agent = self.create_agent(self.vowels[v], self.personalities[p])
            population.append(agent)
        return population

    def calculate_percentage_of_a(self, population):
        count_a = sum(1 for agent in population if agent[0] == 'a')
        return count_a / len(population)

    def choose_pair(self, population):
        i = random.randint(0, len(population) - 1)
        j = random.randint(0, len(population) - 1)
        while i == j:
            j = random.randint(0, len(population) - 1)
        return population[i], population[j]

    def interact_agents(self, listener, producer):
        if listener[0] != producer[0]:
            if listener[1] == 'N':
                listener[0] = deepcopy(producer[0])

    def simulate_interaction(self, n, k):
        population = self.create_random_population(n)
        proportion = []
        for _ in range(k):
            pair = self.choose_pair(population)
            self.interact_agents(pair[0], pair[1])
            proportion.append(self.calculate_percentage_of_a(population))
        return population, proportion

    def batch_simulate_interactions(self, n, k, s):
        results = []
        possible_populations = [0, 1, 2, int(n / 4), int(n / 2), n]
        for p in possible_populations:
            current_results = []
            for _ in range(s):
                new_population, proportion = self.simulate_interaction(n, k)
                current_results.append(proportion)
            results.append(current_results)
        return results
    
    def make_biased_population(self, N, st):
        population = []
        for i in range(st):
            v = random.randint(0, 1)
            agent = self.create_agent(self.vowels[v], self.personalities[1])
            population.append(agent)
        for i in range(N - st):
            v = random.randint(0, 1)
            agent = self.create_agent(self.vowels[v], self.personalities[0])
            population.append(agent)
        return population
        
    def simulate_biased_interaction(self, n, k, st): 
        population = self.make_biased_population(n, st)
        proportion = []
        for i in range(k):
            pair = self.choose_pair(population)
            self.interact_agents(pair[0], pair[1])
            proportion.append(self.calculate_percentage_of_a(population))
        return population, proportion
    
    def batch_simulate_biased_interactions(self, n, k, s): 
        all_results = []
        possible_sts = [0, 1, 2, int(n / 4.), int(n / 2.), n]
        for possible_st in possible_sts:
            current_results = []  
            for _ in range(s):
                new_population, proportion = self.simulate_biased_interaction(n, k, possible_st)
                current_results.append(proportion)
            all_results.append(current_results)
        return all_results
