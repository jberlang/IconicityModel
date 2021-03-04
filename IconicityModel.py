from mesa import Model
from mesa.time import RandomActivation
from mesa.space import SingleGrid  # at most one agent per cell
from mesa.datacollection import DataCollector
from SignerAgent import *
import random


class IconicityModel(Model):
    """A model with its width, height, vocabulary and word size"""

    def __init__(self, width, height, vocab_size, word_length, initial_degree_of_iconicity, learning_error):
        super().__init__()
        # parameters
        self.width = width
        self.height = height
        self.vocab_size = vocab_size
        self.word_length = word_length
        self.initial_error = int(word_length - (round((initial_degree_of_iconicity * word_length) * 10) / 10))
        self.learning_error = learning_error

        # batch runner running status
        self.running = True

        # id counter
        self.current_id = 0

        # amount of agents assuming the grid is a square
        self.num_agents = width * height

        # grid and schedule properties
        self.grid = SingleGrid(width, height, True)
        self.schedule = RandomActivation(self)

        # ranges of agent properties
        self.age_range = [0, 1]
        self.aoa_range = ["L1", "L2"]

        # create agents
        for cell in self.grid.coord_iter():
            # unique iq and position of cell
            x = cell[1]
            y = cell[2]

            # create agent and place in cell
            self.create_agent(x, y, 1, "L1")

        # data collection
        self.datacollector = DataCollector(
            model_reporters={"Iconicity": compute_average_iconicity})

    def random_agents(self, amount):
        """Returns a list of random agents on the grid"""
        positions = []
        i = 0

        while i < amount:
            # generate random coordinates
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)

            # make sure there are no duplicates
            if (x, y) not in positions:
                positions.append((x, y))
            i += 1

        # returns a list of the agents of the cells in the provided cell list
        return self.grid.get_cell_list_contents(positions)

    def create_agent(self, x, y, age, aoa):
        """Creates a new agent and places it in a cell on the grid"""
        unique_id = self.next_id()  # mesa built-in procedure to increment the counter of the ids
        a = SignerAgent(unique_id, self, age, aoa, self.vocab_size, self.word_length, self.initial_error,
                        self.learning_error)
        self.grid.position_agent(a, x, y)
        self.schedule.add(a)

    def remove_agent(self, a):
        """Removes an agent from the model and from the grid"""
        self.schedule.remove(a)
        self.grid.remove_agent(a)

    def replace_agents(self):
        """Clear any dead agents from the model and add new ones"""
        for a in self.schedule.agents:
            if a.age >= 2:
                # get position of agent that is to be replaced
                x, y = a.pos

                # generates new random properties
                new_aoa = random.choice(self.aoa_range)
                new_age = random.choice(self.age_range)

                # a L2 agent can never have
                if new_aoa == "L2":
                    new_age = 1

                # remove the old agent
                self.remove_agent(a)

                # create a new agent and place it at the old agent's location
                self.create_agent(x, y, new_age, new_aoa)

    def step(self):
        """Advance the model by one step"""
        self.schedule.step()
        self.replace_agents()


# # Data collection
# 
# This section contains functions that allows us to collect data from both the model and the agents.

# In[3]:


def compute_average_iconicity(model):
    agent_iconicity_ratios = [agent.iconicity_ratio() for agent in model.schedule.agents]
    number_of_agents = len(agent_iconicity_ratios)
    return sum(agent_iconicity_ratios) / number_of_agents
