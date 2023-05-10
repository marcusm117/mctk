# Authors: marcusm117
# License: Apache 2.0
"""This Module contains functions to perform Explicit-State Model Checking on CTL properties on a Kripke Structure.

Examples:
    >>> from mctk import *
    >>> ks_json = {
    ...     "Atoms": ("a", "b", "c", "d"),
    ...     "States": {
    ...         "s1": 0b1000,  # s1 has labels "a"
    ...         "s2": 0b1100,  # s2 has labels "a", "b"
    ...         "s3": 0b0110,  # s3 has labels "b", "c"
    ...         "s4": 0b0111,  # s4 has labels "b", "c", "d"
    ...         "s5": 0b0100,  # s5 has label "b"
    ...         "s6": 0b0010,  # s6 has label "c"
    ...         "s7": 0b0001,  # s7 has label "d"
    ...     },
    ...     "Starts": ["s1"],
    ...     "Trans": {
    ...         's1': ['s2'],
    ...         's2': ['s3', 's4'],
    ...         's3': ['s4'],
    ...         's4': ['s7'],
    ...         's5': ['s6'],
    ...         's6': ['s7', 's5'],
    ...         's7': ['s5'],
    ...     },
    ... }
    >>> ks = KripkeStruct(ks_json)
    >>> sat_states = SAT_atom(ks, "a")
    >>> print(sat_states)
    {'s1', 's2'}
    >>> sat_states = AND(SAT_atom(ks, "b"), SAT_atom(ks, "c"))
    >>> print(sat_states)
    {'s3', 's4'}
    >>> sat_states = EX(ks, SAT_atom(ks, "a"))
    >>> print(sat_states)
    {'s2'}
    >>> sat_states = EU(ks, SAT_atom(ks, "a"), SAT_atom(ks, "b"))
    >>> print(sat_states)
    {'s1', 's2', 's3', 's4', 's5'}
    >>> sat_states = EG(tmp_ks, SAT_atom(tmp_ks, "a"))
    >>> print(sat_states)
    set()

"""


# Standard Libraries
from copy import deepcopy
from typing import Set

# Internal Modules
from .models import KripkeStruct, KripkeStructError


def SAT_atom(ks: KripkeStruct, atomic_property: str) -> Set[str]:
    """Evaluate an atomic propositional property on a Kripke Structure.

    Return a set of states where the atomic propositional property is satisfied.

    Args:
        ks: a Kripke Structure
        atomic_property: an atomic propositional property represented as a string

    Returns:
        a set of states where the atomic propositional property is satisfied

    Raises:
        KripkeStructError: if the atomic property is not in the Kripke Structure

    """
    sat_states = set()

    if atomic_property == "True":
        return set(ks.states.keys())
    if atomic_property == "False":
        return set()
    if atomic_property not in ks.atoms:
        raise KripkeStructError("Can't check on an atom that's not in the Kripke Structure")

    for state in ks.states:
        # get the set of labels for the state
        label_set = ks.get_state_label_set(state)

        # if the atomic property is in the Label Set, then this state satisfies the atomic property
        if atomic_property in label_set:
            sat_states.add(state)

    return sat_states


def NOT(ks: KripkeStruct, property1: Set[str]) -> Set[str]:
    """Implement the NOT operator on a CTL property.

    Return a set of states where the CTL formula "NOT property" is satisfied.

    Args:
        ks: a Kripke Structure
        property: a CTL property represented as a set of states that satisfy the property

    Returns:
        a set of states where the CTL formula "NOT property" is satisfied

    """
    # complement of the set
    return set(ks.states.keys()) - property1


def AND(property1: Set[str], property2: Set[str]) -> Set[str]:
    """Implement the AND operator on two CTL properties.

    Return a set of states where the CTL formula "property1 AND property2" is satisfied.

    Args:
        ks: a Kripke Structure
        property1: a CTL property represented as a set of states that satisfy the property
        property2: a CTL property represented as a set of states that satisfy the property

    Returns:
        a set of states where the CTL formula "property1 AND property2" is satisfied

    """
    # intersection of the two sets
    return property1 & property2


def OR(property1: Set[str], property2: Set[str]) -> Set[str]:
    """Implement the OR operator on two CTL properties.

    Return a set of states where the CTL formula "property1 OR property2" is satisfied.

    Args:
        ks: a Kripke Structure
        property1: a CTL property represented as a set of states that satisfy the property
        property2: a CTL property represented as a set of states that satisfy the property

    Returns:
        a set of states where the CTL formula "property1 OR property2" is satisfied

    """
    # union of the two sets
    return property1 | property2


def IMPLIES(ks: KripkeStruct, property1: Set[str], property2: Set[str]) -> Set[str]:
    """Implement the IMPLIES operator on two CTL properties.

    Return a set of states where the CTL formula "property1 IMPLIES property2" is satisfied.

    Args:
        ks: a Kripke Structure
        property1: a CTL property represented as a set of states that satisfy the property
        property2: a CTL property represented as a set of states that satisfy the property

    Returns:
        a set of states where the CTL formula "property1 IMPLIES property2" is satisfied

    """
    # complement of property1, then union property2
    # p IMPLIES q = NOT(p) OR q
    return NOT(ks, property1) | property2


def IFF(ks: KripkeStruct, property1: Set[str], property2: Set[str]) -> Set[str]:
    """Implement the IFF operator on two CTL properties.

    Return a set of states where the CTL formula "property1 IFF property2" is satisfied.

    Args:
        ks: a Kripke Structure
        property1: a CTL property represented as a set of states that satisfy the property
        property2: a CTL property represented as a set of states that satisfy the property

    Returns:
        a set of states where the CTL formula "property1 IFF property2" is satisfied

    """
    # (p IFF q) = (p IMPLIES q) AND (q IMPLIES p)
    return IMPLIES(ks, property1, property2) & IMPLIES(ks, property2, property1)


def EX(ks: KripkeStruct, property1: Set[str]) -> Set[str]:
    """Implement the EX operator on a CTL property.

    Return a set of states where the CTL formula "EX property" is satisfied.

    Args:
        ks: a Kripke Structure
        property: a CTL property represented as a set of states that satisfy the property

    Returns:
        a set of states where the CTL formula "EX property" is satisfied

    """
    sat_states = set()

    for state in ks.states:
        # get the successors of the state
        successors = ks.trans[state]

        for successor in successors:
            # test if the successors satisfy the property
            if successor in property1:
                sat_states.add(state)

    return sat_states


def AX(ks: KripkeStruct, property1: Set[str]) -> Set[str]:
    """Implement the AX operator on a CTL property.

    Return a set of states where the CTL formula "AX property" is satisfied.

    Args:
        ks: a Kripke Structure
        property: a CTL property represented as a set of states that satisfy the property

    Returns:
        a set of states where the CTL formula "AX property" is satisfied

    """
    # AX p = NOT (EX NOT(p))
    return NOT(ks, EX(ks, NOT(ks, property1)))


def EU(ks: KripkeStruct, property1: Set[str], property2: Set[str]) -> Set[str]:
    """Implement the EU operator on two CTL properties.

    Return a set of states where the CTL formula "E property1 U property2" is satisfied.

    Args:
        ks: a Kripke Structure
        property1: a CTL property represented as a set of states that satisfy the property
        property2: a CTL property represented as a set of states that satisfy the property

    Returns:
        a set of states where the CTL formula "E property1 U property2" is satisfied

    """
    # if a state satisfies property2, then it satisfies "E property1 U property2" by definition
    # therefore we intialize set_stats to be property2
    sat_states = property2
    size = len(sat_states)

    # we keep adding states that can reach "sat_states" in 1 step, and also satisfy property1
    # until we reach a fixed point
    # i.e. no new states are added to "sat_states"
    # i.e. size of "sat_states" does not change
    while True:
        # get the predecessors of all states in "sat_states"
        predecessors = set()
        for state in sat_states:
            predecessors = predecessors | set(ks.trans_inverted[state])

        # add states that can reach "sat_states" in 1 step, and also satisfy property1
        sat_states = sat_states | (property1 & predecessors)

        # if no new states are added, then we have reached a fixed point
        new_size = len(sat_states)
        if new_size == size:
            break
        size = new_size

    return sat_states


def EF(ks: KripkeStruct, property1: Set[str]) -> Set[str]:
    """Implement the EF operator on a CTL property.

    Return a set of states where the CTL formula "EF property" is satisfied.

    Args:
        ks: a Kripke Structure
        property: a CTL property represented as a set of states that satisfy the property

    Returns:
        a set of states where the CTL formula "EF property" is satisfied

    """
    # EF p = E true U p
    return EU(ks, set(ks.states.keys()), property1)


def AG(ks: KripkeStruct, property1: Set[str]) -> Set[str]:
    """Implement the AG operator on a CTL property.

    Return a set of states where the CTL formula "AG property" is satisfied.

    Args:
        ks: a Kripke Structure
        property: a CTL property represented as a set of states that satisfy the property

    Returns:
        a set of states where the CTL formula "AG property" is satisfied

    """
    # AG p = NOT (EF NOT(p))
    return NOT(ks, EF(ks, NOT(ks, property1)))


def EG(ks: KripkeStruct, property1: Set[str]) -> Set[str]:
    """Implement the EG operator on a CTL property.

    Return a set of states where the CTL formula "EG property" is satisfied.

    Args:
        ks: a Kripke Structure
        property: a CTL property represented as a set of states that satisfy the property

    Returns:
        a set of states where "EG property" is satisfied

    """
    sat_states = set()

    # creat a sub-graph of the original Kripke Structure ks
    # where we remove all states that do not satisfy property
    # since we need to modify the reversed graph, we create a deepcopy of self
    sub_graph = deepcopy(ks)
    for state in ks.states:
        if state not in property1:
            sub_graph.remove_state(state)

    # compute all Strongly Connected Components (SCCs) of the sub-graph
    # SCCs is a set of SCCs, where each SCC is a set of states
    SCCs = sub_graph.get_SCCs()

    # add all non-trivial SCCs to sat_states
    for SCC in SCCs:
        if len(SCC) > 1:
            sat_states = sat_states | SCC

    # if there are no non-trivial SCCs, then no states satisfy EG property
    if not sat_states:
        return sat_states

    # otherwise, we keep adding states that can reach "sat_states" in 1 step
    # until we reach a fixed point
    # i.e. no new states are added to "sat_states"
    # i.e. size of "sat_states" does not change
    size = len(sat_states)
    while True:
        # get the predecessors of all states in "sat_states"
        predecessors = set()
        for state in sat_states:
            predecessors = predecessors | set(sub_graph.trans_inverted[state])

        # add states that can reach "sat_states" in 1 step
        sat_states = sat_states | predecessors

        # if no new states are added, then we have reached a fixed point
        new_size = len(sat_states)
        if new_size == size:
            break
        size = new_size

    return sat_states


def AF(ks: KripkeStruct, property1: Set[str]) -> Set[str]:
    """Implement the AF operator on a CTL property.

    Return a set of states where the CTL formula "AF property" is satisfied.

    Args:
        ks: a Kripke Structure
        property: a CTL property represented as a set of states that satisfy the property

    Returns:
        a set of states where the CTL formula "AF property" is satisfied

    """
    # AF p = NOT (EG NOT(p))
    return NOT(ks, EG(ks, NOT(ks, property1)))


def AU(ks: KripkeStruct, property1: Set[str], property2: Set[str]) -> Set[str]:
    """Implement the AU operator on two CTL properties.

    Return a set of states where the CTL formula "A property1 U property2" is satisfied.

    Args:
        ks: a Kripke Structure
        property1: a CTL property represented as a set of states that satisfy the property
        property2: a CTL property represented as a set of states that satisfy the property

    Returns:
        a set of states where the CTL formula "A property1 U property2" is satisfied

    """
    # A p1 U p2 = NOT (E NOT(p2) U (NOT(p1) AND NOT(p2))) AND NOT (EG NOT(p2))
    return NOT(ks, EU(ks, NOT(ks, property2), NOT(ks, property1) & NOT(ks, property2))) & NOT(
        ks, EG(ks, NOT(ks, property2))
    )
