import spacy


def named_entity_recognition(utterance):
    processor_name = "spaCy"

    doc = nlp(utterance)

    tokens = [token.text for token in doc]

    entity_label, entity_text = zip(*[(ent.label_ for ent in doc.ents), (ent.text for ent in doc.ents)])

    return entity_label, entity_text
