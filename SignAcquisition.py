import random


def sign_acquisition(agent):
    # list of semantic components for which a phonological component can be acquired
    semantic_components = list(agent.vocabulary.keys())
    # choose an initial random semantic component to acquire
    random_semantic_component = random.choice(semantic_components)
    # get interlocutors to acquire from
    interlocutors = get_interlocutors(agent)
    # list of semantic components for which a phonological component has been acquired
    learned_components = []

    # for each interlocutor, the following is done
    for _ in interlocutors:
        # choose a random semantic component for which a phonological component hasn't been acquired yet
        while random_semantic_component in learned_components:
            random_semantic_component = random.choice(semantic_components)
        learned_components.append(random_semantic_component)
        filtered_interlocutors = filter_interlocutors(interlocutors, random_semantic_component)

        if len(filtered_interlocutors) > 0:
            # get the phonological component that has the highest occurrence among neighbours for that random sem. comp.
            phonological_component = random_semantic_component  # default 100% iconic, but will be replaced
            if agent.aoa == "L1":
                phonological_component = select_highest_occurrence(random_semantic_component,
                                                                   filtered_interlocutors)
            if agent.aoa == "L2":
                phonological_component = select_most_iconic_occurrence(random_semantic_component,
                                                                       filtered_interlocutors)

            # add an error in the acquired phonological component
            learned_phonological_component = learn_phonological_component(agent, phonological_component)

            # add the acquired phonological component to the vocabulary of the agent that acquires it
            agent.add_word(random_semantic_component, learned_phonological_component)


def get_interlocutors(agent):
    interlocutors = []

    if agent.aoa == "L1":
        # filter children + sem comp that don't have phon comp
        interlocutors = list(filter(lambda a: a.age > 0, agent.get_neighbours()))
    elif agent.aoa == "L2":
        # filter children + empty vocabs out
        acquisition_radius = agent.l2_radius
        interlocutors = list(filter(lambda a: a.age > 0, agent.get_neighbours(acquisition_radius)))

    return interlocutors


def filter_interlocutors(interlocutors, semantic_component):
    return list(filter(lambda i: i.has_phonological_component(semantic_component), interlocutors))


def select_highest_occurrence(semantic_component, neighbours):
    # keep a counter (value) for each phonological component (key) of a semantic component in a dictionary
    phonological_counters = dict()

    # for every neighbour we check if the semantic component has a phonological component
    for neighbour in neighbours:
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

    #  for every interlocutor we do the following
    for interlocutor in interlocutors:
        # we fetch the phonological component
        phonological_component = interlocutor.vocabulary[semantic_component]
        # calculate the degree of iconicity
        degree_of_iconicity = calculate_degree_of_iconicity(semantic_component, phonological_component)

        # we add the phonological component to the degree dictionary with their calculated degree
        if phonological_component not in degrees_of_iconicity:
            degrees_of_iconicity[phonological_component] = degree_of_iconicity

    # the phonological component with the maximum degree of iconicity in the counter dictionary
    max_phonological_component = max(degrees_of_iconicity, key=degrees_of_iconicity.get)
    # the degree of iconicity associated with it, which should be the highest
    max_degree = degrees_of_iconicity[max_phonological_component]
    # fetch the all phonological components that have this maximum degree (might be more than the one we found)
    phonological_components_with_max_degree = [p for p, d in degrees_of_iconicity.items()
                                               if d == max_degree]
    # if multiple phonological components have the this degree of iconicity, the mode will be taken
    if len(phonological_components_with_max_degree) > 1:
        most_common_phonological_component = get_mode(semantic_component, phonological_components_with_max_degree,
                                                      interlocutors)
        return most_common_phonological_component
    else:
        return max_phonological_component


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


def get_mode(semantic_component, phonological_components, interlocutors):
    # keep a counter for each occurrence of a phonological components in the interlocutors' vocabulary
    counters = dict()

    # for each interlocutor we do the following
    for interlocutor in interlocutors:
        # get the phonological component associated with the semantic component
        phonological_components_of_interlocutor = interlocutor.vocabulary[semantic_component]
        # we check whether phonological component is one that has max degree of iconicity (listed in phon_components)
        for phonological_component in phonological_components:
            # if they are the same, increase the counter or introduce one
            if phonological_component == phonological_components_of_interlocutor:
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
