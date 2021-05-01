import random
from fuzzywuzzy import fuzz


def play_language_game(agent):
    # get interlocutors
    interlocutors = agent.get_neighbours()
    # select a hearer from the interlocutors
    hearer = random.choice(interlocutors)
    # get interlocutors' vocabulary
    hearer_vocab = hearer.vocabulary
    # get hearer's semantic components
    hearer_semantic_components = list(hearer_vocab.keys())
    # get hearers' phonological components
    hearer_signs = list(hearer_vocab.values())

    # get signs of speaker
    semantic_components = agent.semantic_components
    # select a random sign to communicate
    speaker_semantic_component = random.choice(semantic_components)
    # get the sign the speaker has memorised for that semantic component
    speaker_sign = agent.vocabulary[speaker_semantic_component]

    # calculate how similar the agent's sign is to the phon. comp. of the interlocutor
    # (package: fuzzywuzzy - Levenshtein's distance; calculating difference of strings)
    distances = [fuzz.ratio(hearer_sign, speaker_sign) for hearer_sign in hearer_signs]
    max_similarity = max(distances)

    # check whether the interlocutor recognises the sign (Levenshtein's distance >= 60)
    if max_similarity >= 60:
        # interlocutor recognises it
        max_similarity_idx = distances.index(max_similarity)
        most_similar_hearer_sign = hearer_signs[max_similarity_idx]
        # get the semantic component that the interlocutor linked to that sign
        hearer_semantic_component = hearer_semantic_components[max_similarity_idx]

        if speaker_semantic_component == hearer_semantic_component:
            # communicative success
            if speaker_sign != most_similar_hearer_sign:
                modified_hearer_sign = modify_hearer_sign(speaker_sign, most_similar_hearer_sign)
                hearer.add_sign(hearer_semantic_component, modified_hearer_sign)
            # else: recognised and completely the same, do nothing
        # else: communicative failure: not recognised, do nothing


def modify_hearer_sign(speaker_sign, hearer_sign):
    # turn sign into a list
    speaker_bits = [bit for bit in speaker_sign]
    hearer_bits = [bit for bit in hearer_sign]
    # indices for which the signs differ
    differences_idxs = []

    # collect the indices for which the signs differ
    for idx, (fst, snd) in enumerate(zip(speaker_bits, hearer_bits)):
        if fst != snd:
            differences_idxs.append(idx)

    # select a bit to correct
    idx = random.choice(differences_idxs)
    # change the bit
    original_bit = int(hearer_bits[idx])
    hearer_bits[idx] = str(1 - original_bit)

    return ''.join(hearer_bits)
