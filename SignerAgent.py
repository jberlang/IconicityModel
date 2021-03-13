from mesa import Agent
from SignAcquisition import *


class SignerAgent(Agent):
    """An agent with an age, age of acquisition and a vocabulary"""

    def __init__(self, unique_id, iconicity_model, age, aoa, semantic_components, word_length, initial_error,
                 learning_error):
        super().__init__(unique_id, iconicity_model)
        self.unique_id = unique_id
        self.iconicity_model = iconicity_model
        self.semantic_components = semantic_components
        self.vocab_size = len(semantic_components)
        self.word_length = word_length
        self.initial_error = initial_error
        self.learning_error = learning_error
        self.age = age
        self.aoa = aoa
        self.vocabulary = self.generate_initial_vocabulary()

    def add_word(self, semantic_component, phonological_component):
        """Add a word to the agent's dictionary: key is semantic component and value is phonological component"""
        print("add word")
        self.vocabulary[semantic_component] = phonological_component

    def age_up(self):
        """Increase the age of an agent"""
        print("age up")
        self.age += 1

    def non_empty_vocab(self):
        """Checks whether the dictionary contains phonological components"""
        print("non empty vocab")
        amount_of_non_empty_entries = len(list(filter(lambda p: p == "N/A", list(self.vocabulary.items()))))
        return amount_of_non_empty_entries > 0

    def has_phonological_component(self, semantic_component):
        """Checks whether a semantic component has a phonological component"""
        print("has phonological component")
        phonological_component = self.vocabulary[semantic_component]
        return phonological_component != "N/A"

    def get_neighbours(self):
        """Fetches all 8 neighbours of an agent on the grid"""
        print("get neighbours")
        # Get all 8 neighbouring coordinates, excluding the position of the agent itself in the centre
        neighbour_positions = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=True)
        # returns a list of the agents of the cells in the provided cell list
        neighbours = self.model.grid.get_cell_list_contents(neighbour_positions)
        # return this list
        return neighbours

    def generate_initial_vocabulary(self):
        """Creates a vocabulary for the agent - with no phonological components"""
        print("generate initial vocabulary")
        vocab = dict()
        for semantic_component in self.semantic_components:
            vocab[semantic_component] = "N/A"
        return vocab

    def fill_initial_vocabulary(self):
        """Adds the initial phonological components to the vocabulary of generation 0"""
        print("fill initial vocabulary")
        for semantic_component in self.vocabulary:
            phonological_component = self.create_phonological_component(semantic_component)
            self.vocabulary[semantic_component] = phonological_component

    def create_phonological_component(self, word):
        """Create a phonological component, changing a few bits - amount of bits is stored in initial_error"""
        print("create phonological component")
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

    def iconicity_ratio(self):
        """Calculates the average iconicity for an agent's vocabulary"""
        print("calculate iconicity ratio of " + str(self.aoa) + ", age: " + str(self.age))
        ratios = []
        vocab = self.vocabulary

        for semantic_component, phonological_component in vocab.items():
            if phonological_component != "N/A":
                matched_bits = 0
                semantic_bits = [bit for bit in semantic_component]
                phonological_bits = [bit for bit in phonological_component]

                for idx in range(self.word_length):
                    if semantic_bits[idx] == phonological_bits[idx]:
                        matched_bits += 1
                ratios.append(matched_bits / self.word_length)

        if len(ratios) > 0:
            return sum(ratios) / len(ratios)
        else:
            return 0

    def step(self):
        """Advance the agent by one step"""
        sign_acquisition(self)
        self.age_up()
