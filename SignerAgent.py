from mesa import Agent
from SignAcquisition import *


class SignerAgent(Agent):
    """An agent with an age, age of acquisition and a vocabulary"""

    def __init__(self, unique_id, iconicity_model, age, aoa, semantic_components, initial_degree_of_iconicity,
                 word_length, initial_error, learning_error, l2_radius):
        super().__init__(unique_id, iconicity_model)
        self.unique_id = unique_id
        self.iconicity_model = iconicity_model
        self.initial_degree_of_iconicity = initial_degree_of_iconicity
        self.semantic_components = semantic_components
        self.vocab_size = len(semantic_components)
        self.word_length = word_length
        self.initial_error = initial_error
        self.learning_error = learning_error
        self.l2_radius = l2_radius
        self.age = age
        self.aoa = aoa
        self.vocabulary, self.iconicity_degrees = self.generate_initial_vocabulary()

    def add_word(self, semantic_component, phonological_component):
        """Add a word to the agent's dictionary: key is semantic component and value is phonological component"""
        self.vocabulary[semantic_component] = phonological_component
        self.iconicity_degrees[semantic_component] = self.calculate_iconicity_degree(semantic_component,
                                                                                     phonological_component)

    def age_up(self):
        """Increase the age of an agent"""
        self.age += 1

    def non_empty_vocab(self):
        """Checks whether the dictionary contains phonological components"""
        amount_of_non_empty_entries = len(list(filter(lambda p: p != "N/A", list(self.vocabulary.values()))))
        return amount_of_non_empty_entries > 0

    def has_phonological_component(self, semantic_component):
        """Checks whether a semantic component has a phonological component"""
        phonological_component = self.vocabulary[semantic_component]
        return phonological_component != "N/A"

    def get_neighbours(self, acquisition_radius=1):
        """Fetches all 8 neighbours of an agent on the grid"""
        # Get all 8 neighbouring coordinates, excluding the position of the agent itself in the centre
        neighbour_positions = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=True,
                                                               radius=acquisition_radius)
        # returns a list of the agents of the cells in the provided cell list
        neighbours = self.model.grid.get_cell_list_contents(neighbour_positions)
        # return this list
        if acquisition_radius == 1:
            return neighbours
        # for L2 signers we need random neighbours from across the grid within a certain radius
        else:
            if len(neighbours) > 8:
                return random.sample(neighbours, 8)
            else:
                return neighbours

    def generate_initial_vocabulary(self):
        """Creates a vocabulary for the agent - with no phonological components"""
        vocab = dict()
        degrees = dict()
        for semantic_component in self.semantic_components:
            vocab[semantic_component] = "N/A"
            degrees[semantic_component] = "N/A"
        return vocab, degrees

    def fill_initial_vocabulary(self):
        """Adds the initial phonological components to the vocabulary of generation 0"""
        for semantic_component in self.vocabulary:
            phonological_component = self.create_phonological_component(semantic_component)
            self.vocabulary[semantic_component] = phonological_component
            self.iconicity_degrees[semantic_component] = self.initial_degree_of_iconicity

    def create_phonological_component(self, word):
        """Create a phonological component, changing a few bits - amount of bits is stored in initial_error"""
        semantic_component = [bit for bit in word]
        length = len(semantic_component)
        # random bits that will be flipped
        idxs = random.sample(range(0, length), self.initial_error)

        for idx in idxs:
            # select bit
            old_bit = int(semantic_component[idx])
            # flip the bit
            new_bit = 1 - old_bit
            semantic_component[idx] = str(new_bit)

        return ''.join(semantic_component)

    def calculate_iconicity_degree(self, semantic_component, phonological_component):
        """Calculates the iconicity for a sign"""
        matched_bits = 0
        semantic_bits = [bit for bit in semantic_component]
        phonological_bits = [bit for bit in phonological_component]

        for idx in range(self.word_length):
            if semantic_bits[idx] == phonological_bits[idx]:
                matched_bits += 1

        return matched_bits / self.word_length

    def average_iconicity_degree(self):
        """Calculates the average iconicity for an agents vocabulary"""
        iconicity_degrees = list(self.iconicity_degrees.values())
        filtered_degrees = list(filter(lambda p: p != "N/A", iconicity_degrees))

        if len(filtered_degrees) > 0:
            return (sum(filtered_degrees) / self.vocab_size) * 100
        else:
            return 0

    def step(self):
        """Advance the agent by one step"""
        self.age_up()
