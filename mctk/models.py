# Authors: marcusm117
# License: Apache 2.0

from typing import List, Dict
from collections import defaultdict


class KripkeStructError(Exception):
    """Exceptions raised by all instance functions in class KripkeStruct.

    Raised when trying to reset Atoms after States are Created
    Raised when trying to add an Exisiting State Name again
    Raised when trying to add an Exisiting State Label again
    Raised when trying set a Non-Exisiting State as Start State
    Raised when trying to add Transition from a Non-Exisiting Source State
    Raised when trying to add Transition to a Non-Exisiting Target State

    """


class KripkeStruct:
    """Class that implements a Kripke Structure for Model Checking.

    An instance of thie class can be created from a JSON file or from scratch.
    For more information about Kripke Structures, see:
    https://en.wikipedia.org/wiki/Kripke_structure_(model_checking)

    Attributes:
        atoms (tuple): Atoms
        states (dict): States, Key is the state name, Value is the state label
        starts (tuple): Start States
        trans (defaultdict): Transitions, Key is the source state, Value is a list of target states
        trans_inverted (defaultdict): Inverted Transitions, Key is the target state, Value is a list of source states

    """

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

    def set_atoms(self, atoms: List[str]) -> None:
        """Set Atoms of the Kripke Structure.

        Args:
            atoms: a list of strings representing the Atoms

        Raises:
            KripkeStructError: if any state exists, can't reset atoms

        """
        # if any state exists, can't reset atoms
        if self.states:
            raise KripkeStructError("Can't reset Atoms after States are Created")
        self.atoms = tuple(atoms)

    def get_atoms(self) -> List[str]:
        """Get Atoms of the Kripke Structure.

        Returns:
            a list of strings representing the Atoms

        """
        return list(self.atoms)

    def add_state(self, state: str, label: int) -> None:
        """Add a State to the Kripke Structure.

        The State Label is represented by an integer.
        Its binary form of which indicates which Atoms are ture for this State.
        For example, if the Atoms are ("p", "q", "r"),
        and a State Label is 6 whose binary form is 110,
        then the State is lablled as {"p", "q"}.

        Args:
            state: a string representing the State Name
            label: an int representing the State Label, you are encouraged to input in the binary from

        Raises:
            KripkeStructError: if a State Name or a State Label exisits, can't add again

        """
        # if the state or the label exisits, can't add again
        if state in self.states:
            raise KripkeStructError("Can't add an Exisiting State Name again")
        if label in self.states.values():
            raise KripkeStructError("Can't add an Exisiting State Label again")
        self.states[state] = label

    def add_states(self, states: Dict[str, int]) -> None:
        """Add multiple States to the Kripke Structure.

        Args:
            states: a dict, Key is the State Name, Value is the State Label

        Raises:
            KripkeStructError: if a State Name or a State Label exisits, can't add again

        """
        for state, label in states.items():
            self.add_state(state, label)

    def get_states(self) -> Dict[str, int]:
        """Get States of the Kripke Structure.

        Returns:
            a dict, Key is the State Name, Value is the State Label

        """
        return self.states

    def remove_state(self, state: str) -> None:
        """Remove a State from the Kripke Structure.

        Args:
            state: a string representing the State Name

        """
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

    def remove_states(self, states: List[str]) -> None:
        """Remove multiple States from the Kripke Structure.

        Args:
            states: a list of strings representing the State Names

        """
        for state in states:
            self.remove_state(state)

    def set_starts(self, starts: List[str]) -> None:
        """Set Start States of the Kripke Structure.

        Args:
            starts: a list of strings representing the Start States

        Raises:
            KripkeStructError: if start state doesn't exist, can't set it

        """
        for start in starts:
            # if start state doesn't exist, can't set it
            if start not in self.states:
                raise KripkeStructError("Can't set a Non-Exisiting State as Start State")
        self.starts = tuple(starts)

    def get_starts(self) -> List[str]:
        """Get Start States of the Kripke Structure.

        Returns:
            a list of strings representing the Start States

        """
        return list(self.starts)

    def add_trans(self, trans: Dict[str, List[str]]) -> None:
        """Add multiple Transitions to the Kripke Structure.

        Args:
            trans: a dict, Key is the Source State Name, Value is a list of Target State Names

        Raises:
            KripkeStructError: if Source or Target State doesn't exist, can't add transition

        """
        for state, next_states in trans.items():
            # if source state doesn't exist, can't add transition
            if state not in self.states:
                raise KripkeStructError("Can't add Transition from a Non-Exisiting Source State")

            for next_state in next_states:
                # if target state doesn't exist, can't add transition
                if next_state not in self.states:
                    raise KripkeStructError("Can't add Transition to a Non-Exisiting Target State")
                self.trans[state].append(next_state)
                # adding Transitions will also update the Inverted Transitions
                # which will be used to remove related Transitions when revmoing a State
                self.trans_inverted[next_state].append(state)

    def get_trans(self) -> Dict[str, List[str]]:
        """Get Transitions of the Kripke Structure.

        Returns:
            a dict, Key is the Source State Name, Value is a list of Target State Names

        """
        return dict(self.trans)

    def get_trans_inverted(self) -> Dict[str, List[str]]:
        """Get Inverted Transitions of the Kripke Structure.

        Returns:
            a dict, Key is the Target State Name, Value is a list of Source State Names

        """
        return dict(self.trans_inverted)

    def remove_trans(self, trans: Dict[str, List[str]]) -> None:
        """Remove multiple Transitions from the Kripke Structure.

        Args:
            trans: a dict, Key is the Source State Name, Value is a list of Target State Names

        """
        for state, next_states in trans.items():
            for next_state in next_states:
                if state in self.states and next_state in self.trans[state]:
                    self.trans[state].remove(next_state)
                    self.trans_inverted[next_state].remove(state)
