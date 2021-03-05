import random


def sign_acquisition(agent):
    # DO WE DO THIS FOR EACH NEIGHBOUR WITH A FOR-LOOP OR JUST ONE RANDOM NEIGHBOUR?

    # depending on the properties of the acquiring agent, it will acquire the word differently
    if agent.aoa == "L1":  # if agent is an L1 signer
        if agent.age == 0:
            # neighbours are fetched of the agent that needs to acquire a word
            neighbours = list(filter(lambda a: a.age == 1 and a.get_vocab_size() > 0,
                                     agent.get_neighbours()))  # filter children + empty vocabs out

            if len(neighbours) > 0:
                # random neighbour is chosen
                random_neighbour = random.choice(neighbours)
                neighbour_vocabulary = random_neighbour.vocabulary

                if len(neighbour_vocabulary) > 0:  # vocabulary should not be empty
                    semantic_components = list(neighbour_vocabulary.keys())

                    # choose random word
                    random_semantic_component = random.choice(semantic_components)
                    phonological_component = select_highest_occurrence(random_semantic_component, neighbours)

                    # add word with most common phonological component
                    agent.add_word(random_semantic_component, phonological_component)

    # depending on the properties of the acquiring agent, it will acquire the word differently
    if agent.aoa == "L2":  # if agent is an L2 signer
        if agent.age == 1:
            # get random agents from across the grid
            interlocutors = list(filter(lambda a: a.age == 1 and a.get_vocab_size() > 0,
                                        agent.model.random_agents(8)))  # filter children + empty vocabs out

            if len(interlocutors) > 0:
                # random agent is chosen
                random_interlocutor = random.choice(interlocutors)
                interlocutor_vocabulary = random_interlocutor.vocabulary
                semantic_components = list(interlocutor_vocabulary.keys())

                # choose random word
                random_semantic_component = random.choice(semantic_components)
                phonological_component = select_most_iconic_occurrence(random_semantic_component, interlocutors)
                learned_phonological_component = learn_phonological_component(agent, phonological_component)

                # add word with the most iconic phonological component - if same for every interlocutor, then take mode
                agent.add_word(random_semantic_component, learned_phonological_component)


def select_highest_occurrence(semantic_component, neighbours):
    # keep a counter (value) for each phonological component (key) of a semantic component in a dictionary
    phonological_counters = dict()

    # for every neighbour we check if they have the semantic component in their vocabulary
    for neighbour in neighbours:
        if semantic_component in neighbour.vocabulary:
            # if so, we fetch the phonological component
            phonological_component = neighbour.vocabulary[semantic_component]

            # we add the phonological component to the counter dictionary with their updated counter
            if phonological_component in phonological_counters:
                old_counter = phonological_counters[phonological_component]
                phonological_counters[phonological_component] = old_counter + 1
            else:
                phonological_counters[phonological_component] = 1

    # getting the key with maximum value in counter dictionary
    return max(phonological_counters, key=phonological_counters.get)


def select_most_iconic_occurrence(semantic_component, interlocutors):
    # keep degree of iconicity (value) for each phonological component (key) of a semantic component in a dictionary
    degrees_of_iconicity = dict()

    # for every interlocutor we check if they have the semantic component in their vocabulary
    for interlocutor in interlocutors:
        if semantic_component in interlocutor.vocabulary:
            # if so, we fetch the phonological component
            phonological_component = interlocutor.vocabulary[semantic_component]
            # calculate the degree of iconicity
            degree_of_iconicity = calculate_degree_of_iconicity(semantic_component, phonological_component)

            # we add the phonological component to the degree dictionary with their calculated degree
            if phonological_component not in degrees_of_iconicity:
                degrees_of_iconicity[phonological_component] = degree_of_iconicity

    # getting the key with maximum value in counter dictionary
    max_degree = max(degrees_of_iconicity, key=degrees_of_iconicity.get)
    # if multiple phonological components have the this degree of iconicity, the mode will be taken
    if len([p for p, d in degrees_of_iconicity.items() if d == max_degree]) > 1:
        get_mode(list(degrees_of_iconicity.keys()), interlocutors)
    else:
        return max_degree


def calculate_degree_of_iconicity(semantic_component, phonological_component):
    matched_bits = 0
    semantic_bits = [char for char in semantic_component]
    phonological_bits = [char for char in phonological_component]

    # check how many bits the semantic and phonological component have in common
    for idx in range(len(semantic_bits)):
        if semantic_bits[idx] == phonological_bits[idx]:
            matched_bits += 1

    # amount of common bits divided by total amount of bits, resulting in the degree of iconicity
    return matched_bits / len(semantic_bits)


def get_mode(phonological_components, interlocutors):
    # keep a counter for each occurrence of a phonological components in the interlocutors' vocabulary
    counters = dict()

    # for each phonological component, we keep a counter
    for phonological_component in phonological_components:
        # we check the vocabulary of each of the interlocutors
        for interlocutor in interlocutors:
            # update counter
            if phonological_component in interlocutor.vocabulary:
                if phonological_component in counters:
                    old_counter = counters[phonological_component]
                    counters[phonological_component] = old_counter + 1
                else:
                    counters[phonological_component] = 1

    # return the phonological component that has the highest counter
    return max(counters, key=counters.get)


def learn_phonological_component(agent, phonological_component):
    phonological_bits = [bit for bit in phonological_component]
    length = len(phonological_bits)
    # random bits that will be flipped
    idxs = random.sample(range(0, length), agent.learning_error)

    for idx in idxs:
        # select bit
        old_bit = int(phonological_bits[idx])
        # flip the bit
        new_bit = 1 - old_bit
        phonological_bits[idx] = str(new_bit)

    return ''.join(phonological_bits)
