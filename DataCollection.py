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
