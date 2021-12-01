from emissor.representation.scenario import Modality, ImageSignal, TextSignal, Mention, Annotation, Scenario
from cltl.combot.backend.api.discrete import UtteranceType
from cltl.brain.infrastructure.rdf_builder import RdfBuilder
from rdflib import RDFS
from datetime import date
from random import getrandbits
import requests


def seq_to_text (seq):
    text = ""
    for c in seq:
        text+=c
    return text


def scenario_utterance_to_capsule(scenario: Scenario, signal: TextSignal, author:str, perspective:dict, subj: str, pred:str, obj:str):
    place_id = getrandbits(8)
    location = requests.get("https://ipinfo.io").json()

    capsule = {"chat":scenario.id,
                   "turn":signal.id,
                   "author": "carl",
                    "utterance": seq_to_text(signal.seq),
                    "utterance_type": UtteranceType.STATEMENT,
                    "position": "0-"+str(len(signal.seq)),  #TODO generate the true offset range
                    "subject": {"label": subj, "type": "person"},
                    "predicate": {"type": pred},
                    "object":  {"label": obj, "type": "object"},
                    "perspective": perspective ,
                    "context_id": scenario.scenario.context,
                    "date": date.today(),
                    "place": location['city'],
                    "place_id": place_id,
                    "country": location['country'],
                    "region": location['region'],
                    "city": location['city'],
                    "objects": [{'type': 'chair', 'confidence': 0.59, 'id': 1},
                                {'type': 'table', 'confidence': 0.73, 'id': 1},
                               {'type': 'pillbox', 'confidence': 0.32, 'id': 1}],
                            "people": [{'name': 'Carl', 'confidence': 0.98, 'id': 1}]
                  }
    return capsule


# create a capsule for a TextSignal with a triple and perspective string
def scenario_utterance_and_triple_to_capsule(scenario: Scenario,
                                             place_id: str,
                                             location: str,
                                             signal: TextSignal,
                                             author: str,
                                             utterance_type: UtteranceType,
                                             perspective: dict,
                                             triple: dict):
    value = generate_obl_object_json(author)
    capsule = {"chat": scenario.id,
               "turn": signal.id,
               "author": author,
               "utterance": seq_to_text(signal.seq),
               "utterance_type": utterance_type,
               "position": "0-" + str(len(signal.seq)),  # TODO generate the true offset range
               "subject": {'label': triple['subject']['label'], 'type': triple['subject']['type']},
               "predicate": {'type': triple['predicate']['label']},
               "object": {'label': triple['object']['label'], 'type': triple['object']['type']},
               "perspective": perspective,
               "context_id": scenario.scenario.context,
               ##### standard elements
               "date": date.today(),
               "place": location['city'],
               "place_id": place_id,
               "country": location['country'],
               "region": location['region'],
               "city": location['city'],
               "objects": value['objects'],
               "people": value['people']
               }

    return capsule


# Function to generate bogus elements for capsules. Without these, the update function fails
def generate_obl_object_json(human: str):
    json_string = {
        "objects": [{'type': 'chair', 'confidence': 0.59, 'id': 1},
                    {'type': 'table', 'confidence': 0.73, 'id': 1},
                    {'type': 'pillbox', 'confidence': 0.32, 'id': 1}],
        "people": [{'name': human, 'confidence': 0.98, 'id': 1}]
    }
    return json_string