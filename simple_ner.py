import spacy
import named_entity_linking
import make_data_and_query


def named_entity_recognition(utterance, graph):
    processor_name = "spaCy"

    doc = nlp(utterance)

    tokens = [token.text for token in doc]

    entity_label = [ent.label_ for ent in doc.ents]
    entity_text = [ent.text for ent in doc.ents]

    entities = []
    for ent_text in entity_text:
        print(f"Working on entity {ent_text}")
        name, pop = named_entity_linking.nel_popularity(ent_text, graph)
        entities.append((name, pop))

    return entities


if __name__ == "__main__":
    nlp = spacy.load('en_core_web_sm')
    utt = "Hi my name is Jaap and this is my friend Bart"
    data = make_data_and_query.make_fake_data()
    results = named_entity_recognition(utt, data)
    print(results)