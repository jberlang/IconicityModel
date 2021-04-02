import random


def sign_acquisition(agent):
    interlocutors = []
    acquired_signs = dict()

    if agent.aoa == "L1":
        # filter children + sem comp that don't have phon comp
        interlocutors = list(filter(lambda a: a.age > 0, agent.get_neighbours()))
    elif agent.aoa == "L2":
        # filter children + empty vocabs out
        acquisition_radius = agent.l2_radius
        interlocutors = list(filter(lambda a: a.age > 0, agent.get_neighbours(acquisition_radius)))

    for interlocutor in interlocutors:
        semantic_components = list(filter(lambda c: interlocutor.has_phonological_component(c),
                                          interlocutor.semantic_components))
        random_semantic_component = random.choice(semantic_components)

        if random_semantic_component not in acquired_signs:
            # information for each phonological component associated with the random semantic component
            frequencies = dict()
            iconicity_levels = dict()

            for i in interlocutors:
                phonological_component = i.vocabulary[random_semantic_component]
                iconicity_level = i.iconicity_degree[random_semantic_component]

                if phonological_component != "N/A":

                    # update frequencies
                    if phonological_component not in frequencies:
                        frequencies[phonological_component] = 1
                    else:
                        old_frequency = frequencies[phonological_component]
                        frequencies[phonological_component] = old_frequency + 1

                    # update iconicity level
                    if phonological_component not in iconicity_levels:
                        iconicity_levels[phonological_component] = iconicity_level

            if agent.aoa == "L1":
                acquired_sign = max(frequencies, key=frequencies.get)
                acquired_signs[random_semantic_component] = acquired_sign
                agent.add_word(random_semantic_component, acquired_sign)
            elif agent.aoa == "L2":
                # the phonological component with the maximum degree of iconicity in the counter dictionary
                max_phonological_component = max(iconicity_levels, key=iconicity_levels.get)
                # the degree of iconicity associated with it, which should be the highest
                max_degree = iconicity_levels[max_phonological_component]
                # fetch the all phonological components that have this maximum degree
                phonological_components_with_max_degree = [p for p, d in iconicity_levels.items()
                                                           if d == max_degree]

                # take mode if there are more than 1 phon comp with an equal degree of iconicity
                most_common_and_iconic_phon_comp = max_phonological_component
                for component in phonological_components_with_max_degree:
                    if frequencies[component] > frequencies[most_common_and_iconic_phon_comp]:
                        most_common_and_iconic_phon_comp = component

                acquired_sign = most_common_and_iconic_phon_comp
                acquired_signs[random_semantic_component] = acquired_sign
                agent.add_word(random_semantic_component, acquired_sign)
        else:
            agent.add_word(random_semantic_component, acquired_signs[random_semantic_component])