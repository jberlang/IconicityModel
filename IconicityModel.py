from mesa import Model
from mesa.time import RandomActivation
from mesa.space import SingleGrid  # at most one agent per cell
from mesa.datacollection import DataCollector
from SignerAgent import *
from DataCollection import *
from SignAcquisition import *


class IconicityModel(Model):
    """A model with its width, height, vocabulary and word size"""

    def __init__(self, width, height, vocab_size, word_length, turnover_chance, turnover_threshold,
                 initial_degree_of_iconicity, learning_error_degree, l2_radius, l2_replace_chance):
        super().__init__()
        # parameters
        self.width = width
        self.height = height
        self.vocab_size = vocab_size
        self.word_length = word_length
        self.initial_degree_of_iconicity = initial_degree_of_iconicity / 100
        self.semantic_components = self.generate_semantic_components()
        # chance of an adult agent to die and be replaced
        self.turnover_chance = turnover_chance / 100
        self.turnover_threshold = turnover_threshold
        # initial phonological error in dictionaries of children
        self.initial_error = word_length - round((initial_degree_of_iconicity / 100) * word_length)
        # error of adults when acquiring a new phonological component
        self.learning_error = round((learning_error_degree / 100) * word_length)
        # radius of agent from which an L2 learner can acquire signs from
        self.l2_radius = l2_radius
        # chance of an old agent being replaced by an L2 agent
        self.l2_replace_chance = l2_replace_chance / 100

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
        self.aoa_range = ["L1", "L2"]

        # create agents
        for cell in self.grid.coord_iter():
            # unique iq and position of cell
            x = cell[1]
            y = cell[2]

            # create agent and place in cell
            self.create_agent(x, y, 0, "L1", True)

        # data collection
        self.datacollector = DataCollector(
            model_reporters={"Total avg. iconicity": compute_total_average_iconicity,
                             "L1 avg. iconicity": compute_l1_average_iconicity,
                             "L2 avg. iconicity": compute_l2_average_iconicity})

    def generate_semantic_components(self):
        """Generates the semantic components that will be used in the model"""
        components = []

        # generate the components
        while len(components) < self.vocab_size:
            bits = []
            # generate the bitstring
            for _ in range(self.word_length):
                b = str(random.randint(0, 1))
                bits.append(b)
            component = ''.join(bits)

            # check if the generated component is not a duplicate
            if component not in components:
                components.append(component)

        return components

    def create_agent(self, x, y, age, aoa, generation_zero):
        """Creates a new agent and places it in a cell on the grid"""
        unique_id = self.next_id()  # mesa built-in procedure to increment the counter of the ids
        a = SignerAgent(unique_id, self, age, aoa, self.semantic_components, self.initial_degree_of_iconicity,
                        self.word_length, self.initial_error, self.learning_error, self.l2_radius)
        self.grid.position_agent(a, x, y)
        self.schedule.add(a)

        # If generation zero, the phonological components must be initialised
        if generation_zero:
            a.fill_initial_vocabulary()

    def remove_agent(self, a):
        """Removes an agent from the model and from the grid"""
        self.schedule.remove(a)
        self.grid.remove_agent(a)

    def replace_agents(self):
        """Clear any dead agents from the model and add new ones"""
        for a in self.schedule.agents:
            # generate a random number between 0 and 1 to be compared with turnover_chance later
            dying_chance = random.uniform(0, 1)
            replace_chance = random.uniform(0, 1)
            # agents have a possibility of dying when age > 2, but are guaranteed to die over turnover_threshold
            if (a.age >= 2 and dying_chance <= self.turnover_chance) or a.age > self.turnover_threshold:
                # get position of agent that is to be replaced
                x, y = a.pos

                # generates new random properties
                new_aoa = "L1"
                new_age = 0

                if replace_chance <= self.l2_replace_chance:
                    new_aoa = "L2"
                    new_age = 1

                # remove the old agent
                self.remove_agent(a)
                # create a new agent and place it at the old agent's location
                self.create_agent(x, y, new_age, new_aoa, False)

    def for_each_agent(self, f):
        for agent in self.schedule.agents:
            f(agent)

    def step(self):
        """Advance the model by one step"""
        self.schedule.step()
        self.replace_agents()
        self.for_each_agent(sign_acquisition)
        self.datacollector.collect(self)
