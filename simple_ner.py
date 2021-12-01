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
from datetime import datetime

# These modules are not included in NEL-coreference at the moment!! Won't work outside this machine
from src.chatbots.util import driver_util, capsule_util
from src.chatbots.dummies import text_to_triple as ttt

from rdflib.namespace import RDFS

utt = "Carl likes Bart"
# Idea: can the system search for NP's in the surroundings of a NE, and remember those

# TODO Testing linking separate from NER (by e.g. using hashes and a dict) (NamedEntityRecognizer)

# Using dummy triples that don't require an utterance?

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
    text_signal = driver_util.create_text_signal(scenario, utterance)

    entity_text = add_ner_annotation(text_signal)
    scenario.append_signal(text_signal)

    return entity_text


def main(log_path, utterance):
    nel = NamedEntityLinker(address="http://localhost:7200/repositories/sandbox",
                            log_dir=log_path)
    scenario_path = './data'
    scenario_id = 'test_scenario'
    scenario_storage = driver_util.create_scenario(scenario_path, scenario_id)
    scen = scenario_storage.create_scenario(scenario_id, datetime.now().microsecond, datetime.now().microsecond, 'AGENT')
    entity_text = utterance_processor(utterance, scen, nel, 'Jaap')

    # link_entities expects a list with all entities in one
    # but the new ner gives a list with a single entity per utterance(?)

    entities = nel.link_entities(entity_text)

    return entities


if __name__ == "__main__":
    nlp = spacy.load('en_core_web_sm')
    with TemporaryDirectory(prefix="brain-log") as log_path:
        res = main(Path(log_path), utt)
        print(res)