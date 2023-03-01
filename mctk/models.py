# Authors: marcusm117
# License: AGPL v3.0

from typing import List, Dict
from collections import defaultdict




class KripkeStruct:
    def __init__(self, model_json=None):
        if model_json is not None:
            self.atoms = tuple(model_json["atoms"])

            self.states = model_json["states"]
            self.states_labels = set()
            for label in self.states.values():
                self.states_labels.add(label)
            self.starts = model_json["starts"]

            self.trans = defaultdict(list, model_json["trans"])
            self.trans_inverted = defaultdict(list)
            for state, next_states in self.trans.items():
                for next_state in next_states:
                    self.trans_inverted[next_state].append(state)
        else:
            self.atoms = ()
            self.states = {}
            self.states_labels = set()
            self.starts = ()
            self.trans = defaultdict(list)
            self.trans_inverted = defaultdict(list)
                 

    def __str__(self) -> str:
        return "Atoms: " + str(self.atoms) +\
               "States: " + str(self.states) +\
               "Starts: " + str(self.starts) +\
               "Trans: " + str(self.trans)


    def set_atoms(self, atoms: List[str]):
        # if any state exists, can't reset atoms
        if self.states:
            raise Exception("Can't reset Atoms after States are Created")
        else:
            self.atoms = tuple(atoms)


    def get_atoms(self):
        return list(self.atoms)


    def add_state(self, state: str, label: int):
        # if the state or the label exisits already, can't add again
        if state in self.states:
            raise Exception("Can't add an Exisiting State Name again")
        elif label in self.states_labels:
            raise Exception("Can't add an Exisiting State Label again")
        else:
            self.states[state] = label
            self.states_labels.add(label)


    def add_states(self, states: Dict[str, int]):
        for state, label in states.items():
            self.add_state(state, label)


    def get_states(self):
        return self.states


    def remove_state(self, state: str):
        if state in self.states:
            label = self.states.pop(state)
            self.states_labels.remove(label)

            # removing state will remove related transitions
            if state in self.trans:
                next_states = self.trans.pop(state)
                for next_state in next_states:
                    self.trans_inverted[next_state].remove(state)
            if state in self.trans_inverted:
                prev_states = self.trans_inverted.pop(state)
                for prev_state in prev_states:
                    self.trans[prev_state].remove(state)


    def remove_states(self, states: List[str]):
        for state in states:
            self.remove_state(state)


    def set_starts(self, starts: List[str]):
        # if start state doesn't exist, can't set it
        for start in starts:
            if start not in self.states:
                raise Exception("Can't set a Non-Exisiting State as Start State")
        self.starts = tuple(starts)


    def get_starts(self):
        return list(self.starts)


    def add_trans(self, trans: Dict[str, List[str]]):
        for state, next_states in trans.items():
            if state not in self.states:
                raise Exception("Can't add Transition from a Non-Exisiting State")
            for next_state in next_states:
                if next_state not in self.states:
                    raise Exception("Can't add Transition to a Non-Exisiting State")
                self.trans[state].append(next_state)
                self.trans_inverted[next_state].append(state)


    def remove_trans(self, trans: Dict[str, List[str]]):
        for state, next_states in trans.items():
            for next_state in next_states:
                if state in self.states and next_state in self.trans[state]:
                    self.trans[state].remove(next_state)
                    self.trans_inverted[next_state].remove(state)


    def get_trans(self):
        return dict(self.trans)


    def get_tran_inverted(self):
        return dict(self.trans_inverted)