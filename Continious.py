import random
from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns 

class AgentInteractionModelNormal:
    def __init__(self):
        self.vowel_means = [-1., 1.]
        self.personalities = ['F', 'S']

    def create_agent(self, vowel_mean, personality):
        return [vowel_mean, personality]

    def create_population(self, N):
        population = []
        for _ in range(N):
            m = random.randint(0, 1)
            p = random.randint(0, 1)
            agent = self.create_agent(self.vowel_means[m], self.personalities[p])
            population.append(agent)
        return population

    def choose_utterance(self, agent): 
        agent_utterance = np.random.normal(agent[0], 0.25)
        return agent_utterance

    def learn(self, utterance, agent):
        if agent[1] == 'F':
            new_mean = (agent[0] + utterance) / 2.
        else:
            difference = abs(utterance - agent[0])
            if utterance > agent[0]:
                new_mean = agent[0] + (difference / 10.)
            else:
                new_mean = agent[0] - (difference / 10.)
        agent[0] = deepcopy(new_mean)

    def interact(self, agent1, agent2): 
        agent1_utterance = self.choose_utterance(agent1)
        agent2_utterance = self.choose_utterance(agent2)

        if agent1[0] != agent2[0]:
            self.learn(agent2_utterance, agent1)
            self.learn(agent1_utterance, agent2)

        return agent1_utterance, agent2_utterance, agent1, agent2

    def simulate(self, n, k):
        initial_population = self.create_population(n)
        population = deepcopy(initial_population)

        for _ in range(k):
            agent1, agent2 = self.choose_pair(population)
            self.interact(agent1, agent2)

        return initial_population, population

    def compute_mean(self, population):
        total = 0.
        for agent in population:
            total += agent[0]
        return total / len(population)

    def batch_simulate(self, n, k, s):
        batch_final = []
        for _ in range(s):
            initial_population, new_population = self.simulate(n, k)
            new_mean = self.compute_mean(new_population)
            batch_final.append(new_mean)
        return batch_final

    def compute_standard_deviation(self, population):
        pop_means = [agent[0] for agent in population]
        pop_sd = np.std(pop_means)
        return pop_sd

    def batch_simulate_biased(self, n, k, s):
        all_results = []
        possible_sts = [0, int(n / 10.), int(n / 4.), int(n / 2.), int(3 * n / 4.), n]

        for st in possible_sts:
            current_results = [] 
            for _ in range(s):
                initial_population, new_population = self.simulate_biased(n, k, st)
                sd = self.compute_standard_deviation(new_population)
                current_results.append(sd)
            all_results.append([st, current_results])
        return all_results

    def make_biased_population(self, N, st):
        population = []
        for i in range(st):
            m = random.randint(0, 1)
            agent = self.create_agent(self.vowel_means[m], self.personalities[1])
            population.append(agent)
        for i in range(N - st):
            m = random.randint(0, 1)
            agent = self.create_agent(self.vowel_means[m], self.personalities[0])
            population.append(agent)
        return population

    def simulate_biased(self, n, k, st): 
        initial_population = self.make_biased_population(n, st)
        population = deepcopy(initial_population)

        for _ in range(k):
            agent1, agent2 = self.choose_pair(population)
            self.interact(agent1, agent2)

        return initial_population, population
    
    def plot_distribution_changes(self, initial_population, new_population):
        initial_means = [agent[0] for agent in initial_population]
        final_means = [agent[0] for agent in new_population]
        plt.hist(initial_means, label='Initial Means')
        plt.hist(final_means, label='Final Means')
        plt.legend(loc='upper center')
        plt.show()

    def batch_simulate_size(self, k, s):
        all_results = []
        possible_sizes = [50, 150, 250, 350, 450, 550, 650]
        for n in possible_sizes:
            print(n)
            current_results = []
            for _ in range(s):
                initial_population, new_population = self.simulate(n, k)
                sd = self.compute_standard_deviation(new_population)
                current_results.append(sd)

            all_results.append([n, current_results])

        return all_results
