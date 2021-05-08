from itertools import combinations

# Data collection
# This section contains functions that allows us to collect data from both the model and the agents.


def compute_total_average_iconicity(model):
    """Calculates the average iconicity over the whole model"""
    all_agents = list(filter(lambda a: a.non_empty_vocab(), model.schedule.agents))
    all_agent_iconicity_ratios = [agent.average_iconicity_degree() for agent in all_agents]
    total_number_of_agents = len(all_agent_iconicity_ratios)
    if total_number_of_agents > 0:
        return round((sum(all_agent_iconicity_ratios) / total_number_of_agents) * 100) / 100
    else:
        return 0


def compute_l1_average_iconicity(model):
    """Calculates the average iconicity among L1 signers"""
    all_agents = list(filter(lambda a: a.non_empty_vocab(), model.schedule.agents))
    l1_agents = list(filter(lambda a: a.aoa == "L1", all_agents))

    l1_iconicity_ratios = [agent.average_iconicity_degree() for agent in l1_agents]
    number_of_l1_agents = len(l1_iconicity_ratios)

    if number_of_l1_agents > 0:
        return round((sum(l1_iconicity_ratios) / number_of_l1_agents) * 100) / 100
    else:
        return 0


def compute_l2_average_iconicity(model):
    """Calculates the average iconicity among L2 signers"""
    all_agents = list(filter(lambda a: a.non_empty_vocab(), model.schedule.agents))
    l2_agents = list(filter(lambda a: a.aoa == "L2", all_agents))

    l2_iconicity_ratios = [agent.average_iconicity_degree() for agent in l2_agents]
    number_of_l2_agents = len(l2_iconicity_ratios)

    if number_of_l2_agents > 0:
        return round((sum(l2_iconicity_ratios) / number_of_l2_agents) * 100) / 100
    else:
        return 0


def compute_average_convergence_ratio(model):
    """Computes the convergence ratio for the whole model"""
    all_agents = list(filter(lambda a: a.non_empty_vocab(), model.schedule.agents))

    # get all pairwise combinations of agents
    all_agent_combinations = list(combinations(all_agents, 2))
    # for each of these pairs, calculate their convergence ratio
    average_convergence_ratios = [average_convergence_ratio(c) for c in all_agent_combinations]
    number_of_combinations = len(all_agent_combinations)

    if number_of_combinations > 0:
        return round((sum(average_convergence_ratios) / number_of_combinations) * 100) / 100
    else:
        return 0


def average_convergence_ratio(combination):
    convergence_ratios = []

    fst_agent = combination[0]
    snd_agent = combination[1]

    fst_phonological_components = list(fst_agent.vocabulary.values())
    snd_phonological_components = list(snd_agent.vocabulary.values())

    for fst_comp, snd_comp in zip(fst_phonological_components, snd_phonological_components):
        convergence_ratio = calculate_similarity(fst_comp,snd_comp)
        convergence_ratios.append(convergence_ratio)

    return sum(convergence_ratios) / len(convergence_ratios)


def calculate_similarity(fst_comp, snd_comp):
    matched_bits = 0
    fst_bits = [bit for bit in fst_comp]
    snd_bits = [bit for bit in snd_comp]
    length = len(fst_bits)

    for idx in range(length):
        if fst_bits[idx] == snd_bits[idx]:
            matched_bits += 1

    return (matched_bits / length) * 100
