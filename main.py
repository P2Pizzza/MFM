interaction_model = AgentInteractionModelNormal()

results_biased = interaction_model.batch_simulate_biased(200, 2000, 50)

plt.figure(figsize=(10, 6))
for result in results_biased:
    plt.hist(result[1], label=f'{result[0]} stubborn agents', edgecolor='white')

plt.legend(loc='best')
plt.xlabel('SD of Final Vowel Distribution in the Population')
plt.ylabel('Number of Simulations')
plt.show()

results_size = interaction_model.batch_simulate_size(10000, 50)

plt.figure(figsize=(10, 6))
for result in results_size:
    plt.hist(result[1], label=f'{result[0]} agents', edgecolor='white')

plt.legend(loc='best')
plt.xlabel('SD of Final Vowel Distribution in the Population')
plt.ylabel('Number of Simulations')     
plt.show()
