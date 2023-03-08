# Authors: marcusm117
# License: Apache 2.0

from typing import List, Dict
from collections import defaultdict


class KripkeStructException(Exception):
    pass


class KripkeStruct:
    def __init__(self, model_json=None):
        self.atoms = ()
        self.states = {}
        self.starts = ()
        self.trans = defaultdict(list)
        self.trans_inverted = defaultdict(list)

        if model_json is not None:
            self.set_atoms(model_json["Atoms"])
            self.add_states(model_json["States"])
            self.set_starts(model_json["Starts"])
            self.add_trans(model_json["Trans"])

    def __str__(self) -> str:
        return (
            f"Atoms: {self.atoms}\n"
            + f"States: {self.states}\n"
            + f"Starts: {self.starts}\n"
            + f"Trans: {dict(self.trans)}"
        )

    def set_atoms(self, atoms: List[str]):
        # if any state exists, can't reset atoms
        if self.states:
            raise KripkeStructException("Can't reset Atoms after States are Created")
        else:
            self.atoms = tuple(atoms)

    def get_atoms(self):
        return list(self.atoms)

    def add_state(self, state: str, label: int):
        # if the state or the label exisits, can't add again
        if state in self.states:
            raise KripkeStructException("Can't add an Exisiting State Name again")
        elif label in self.states.values():
            raise KripkeStructException("Can't add an Exisiting State Label again")
        else:
            self.states[state] = label

    def add_states(self, states: Dict[str, int]):
        for state, label in states.items():
            self.add_state(state, label)

    def get_states(self):
        return self.states

    def remove_state(self, state: str):
        if state in self.states:
            self.states.pop(state)
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
        for start in starts:
            # if start state doesn't exist, can't set it
            if start not in self.states:
                raise KripkeStructException("Can't set a Non-Exisiting State as Start State")
        self.starts = tuple(starts)

    def get_starts(self):
        return list(self.starts)

    def add_trans(self, trans: Dict[str, List[str]]):
        for state, next_states in trans.items():
            # if source state doesn't exist, can't add transition
            if state not in self.states:
                raise KripkeStructException("Can't add Transition from a Non-Exisiting Source State")

            for next_state in next_states:
                # if target state doesn't exist, can't add transition
                if next_state not in self.states:
                    raise KripkeStructException("Can't add Transition to a Non-Exisiting Target State")
                self.trans[state].append(next_state)
                self.trans_inverted[next_state].append(state)

    def get_trans(self):
        return dict(self.trans)

    def get_trans_inverted(self):
        return dict(self.trans_inverted)

    def remove_trans(self, trans: Dict[str, List[str]]):
        for state, next_states in trans.items():
            for next_state in next_states:
                if state in self.states and next_state in self.trans[state]:
                    self.trans[state].remove(next_state)
                    self.trans_inverted[next_state].remove(state)
