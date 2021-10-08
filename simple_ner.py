import spacy
from tempfile import TemporaryDirectory
from pathlib import Path
from named_entity_linking import NamedEntityLinker
from brain_processing import scenario_utterance_to_capsule

# These modules are imported for the added let's-chat stuff
from emissor.persistence import ScenarioStorage
from emissor.representation.annotation import AnnotationType, Token, NER
from emissor.representation.container import Index
from emissor.representation.scenario import Modality, ImageSignal, TextSignal, Mention, Annotation, Scenario
import uuid
import time

# These modules are not included in NEL-coreference at the moment!! Won't work outside this machine
import capsule_utils
import driver_util as d_util
import text_to_triple as ttt

utt = "Hi this is Jaap and his father Bart"
# Idea: can the system search for NP's in the surroundings of a NE, and remember those

# TODO Testing linking separate from NER (by e.g. using hashes and a dict) (NamedEntityRecognizer)

# Make linking independent from ner function (so not nested inside the ner function but use its output), CHECK!
# Updating the brain: a lot of it is already done automatically in the LTM update() function
# If I do it here as well then it is done twice; what is the right way to approach this?
# Using dummy triples that don't require an utterance?


# def named_entity_recognition(utterance, nel: NamedEntityLinker):
#     # processor_name = "spaCy"
#
#     doc = nlp(utterance)
#
#     # tokens = [token.text for token in doc]
#
#     # entity_label = [ent.label_ for ent in doc.ents]
#     entity_text = [ent.text.lower() for ent in doc.ents]
#
#     return entity_text

def add_ner_annotation(signal: TextSignal):
    processor_name = "spaCy"
    utterance = ''.join(signal.seq)

    doc = nlp(utterance)

    offsets, tokens = zip(*[(Index(signal.id, token.idx, token.idx + len(token)), Token.for_string(token.text))
                            for token in doc])

    ents = [NER.for_string(ent.label_) for ent in doc.ents]
    entity_list = [ent.text.lower() for ent in doc.ents]
    segments = [token.ruler for token in tokens if token.value in entity_list]

    annotations = [Annotation(AnnotationType.TOKEN.name.lower(), token, processor_name, int(time.time()))
                   for token in tokens]
    ner_annotations = [Annotation(AnnotationType.NER.name.lower(), ent, processor_name, int(time.time()))
                       for ent in ents]

    signal.mentions.extend([Mention(str(uuid.uuid4()), [offset], [annotation])
                            for offset, annotation in zip(offsets, annotations)])
    signal.mentions.extend([Mention(str(uuid.uuid4()), [segment], [annotation])
                            for segment, annotation in zip(segments, ner_annotations)])
    return entity_list


def utterance_processor(utterance, scenario, brain, author):
    text_signal = d_util.create_text_signal(scenario, utterance)
    # @TODO
    ### Apply some processing to the text_signal and add annotations
    entity_text = add_ner_annotation(text_signal)
    scenario.append_signal(text_signal)
    ## Post triples to the brain:

    subj, pred, obj = ttt.getTriplesFromEntities(entity_text, text_signal.id)

    response = {}
    if not subj == "":
        print('Subject:', subj, 'Predicate:', pred, 'Object:', obj)
        perspective = {"certainty": 1, "polarity": 1, "sentiment": 1}

        capsule = scenario_utterance_to_capsule(scenario, text_signal, author, perspective, subj, pred, obj)
        # perspective is a dict instead of a str?

        # print('Capsule:', capsule)
        response = brain.update(capsule, reason_types=True)
        # print(thoughts)


def main(log_path):
    nel = NamedEntityLinker(address="http://localhost:7200/repositories/sandbox",
                            log_dir=log_path)
    entity_text = add_ner_annotation(utt)

    # link_entities expects a list with all entities in one
    # but the new ner gives a list with a single entity per utterance(?)
    entities = nel.link_entities(entity_text)

    return entities


if __name__ == "__main__":
    nlp = spacy.load('en_core_web_sm')
    with TemporaryDirectory(prefix="brain-log") as log_path:
        res = main(Path(log_path))
        print(res)