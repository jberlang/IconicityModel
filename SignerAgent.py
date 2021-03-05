from mesa import Agent
from SignAcquisition import *


class SignerAgent(Agent):
    """An agent with an age, age of acquisition and a vocabulary"""

    def __init__(self, unique_id, iconicity_model, age, aoa, vocab_size, word_length, initial_error,
                 learning_error):
        super().__init__(unique_id, iconicity_model)
        self.unique_id = unique_id
        self.iconicity_model = iconicity_model
        self.vocab_size = vocab_size
        self.word_length = word_length
        self.initial_error = initial_error
        self.learning_error = learning_error
        self.age = age
        self.aoa = aoa
        self.vocabulary = self.generate_iconic_vocabulary()

    def add_word(self, semantic_component, phonological_component):
        """Add a word to the agent's dictionary: key is semantic component and value is phonological component"""
        self.vocabulary[semantic_component] = phonological_component

    def get_vocab_size(self):
        """Gets the size of the vocabulary"""
        return len(self.vocabulary)

    def age_up(self):
        """Increase the age of an agent"""
        self.age += 1

    def get_neighbours(self):
        """Fetches all 8 neighbours of an agent on the grid"""
        # Get all 8 neighbouring coordinates, excluding the position of the agent itself in the centre
        neighbour_positions = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        # returns a list of the agents of the cells in the provided cell list
        neighbours = self.model.grid.get_cell_list_contents(neighbour_positions)
        # return this list
        return neighbours

    def generate_iconic_vocabulary(self):
        """Creates a vocabulary for the agent - empty if the agent is a child"""
        vocab = dict()
        if self.age > 0:
            while len(vocab) < self.vocab_size:
                semantic_component = self.create_random_semantic_component()
                if semantic_component not in vocab:
                    phonological_component = self.create_phonological_component(semantic_component)
                    vocab[semantic_component] = phonological_component
        return vocab

    def create_random_semantic_component(self):
        """Creates a phonological component based on a semantic component"""
        bits = []

        for _ in range(self.word_length):
            b = str(random.randint(0, 1))
            bits.append(b)

        return ''.join(bits)

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

    def iconicity_ratio(self):
        """Calculates the average iconicity for an agent's vocabulary"""
        ratios = []
        vocab = self.vocabulary
        vocab_size = self.get_vocab_size()

        if vocab_size > 0:  # if dictionary is empty
            for key, value in vocab.items():
                matched_bits = 0
                semantic_component = [bit for bit in key]
                phonological_component = [bit for bit in value]

                for idx in range(self.word_length):
                    if semantic_component[idx] == phonological_component[idx]:
                        matched_bits += 1
                ratios.append(matched_bits / self.word_length)

        if vocab_size > 0:
            return sum(ratios) / self.get_vocab_size()
        else:
            return 0

    def step(self):
        """Advance the agent by one step - PH - STILL TO BE IMPLEMENTED"""
        # choose random agent
        # other_agent = self.random.choice(self.model.schedule.agents)
        # PH - placeholder: choose random neighbour
        sign_acquisition(self)
        self.age_up()
