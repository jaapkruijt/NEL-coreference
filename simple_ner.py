import spacy
from tempfile import TemporaryDirectory
from pathlib import Path
from named_entity_linking import NamedEntityLinker

utt = "Hi this is my friend Bram and his supervisor Piek"
# Idea: can the system search for NP's in the surroundings of a NE, and remember those


def named_entity_recognition(utterance, nel: NamedEntityLinker):
    processor_name = "spaCy"

    doc = nlp(utterance)

    tokens = [token.text for token in doc]

    entity_label = [ent.label_ for ent in doc.ents]
    entity_text = [ent.text.lower() for ent in doc.ents]

    entities = []
    for ent_text in entity_text:
        name = nel.link_entities(ent_text)
        entities.append(name)

    return entities


def main(log_path):
    nel = NamedEntityLinker(address="http://localhost:7200/repositories/sandbox",
                            log_dir=log_path)
    results = named_entity_recognition(utt, nel)
    return results


if __name__ == "__main__":
    nlp = spacy.load('en_core_web_sm')
    with TemporaryDirectory(prefix="brain-log") as log_path:
        res = main(Path(log_path))
        print(res)