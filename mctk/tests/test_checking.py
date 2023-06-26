# Authors: marcusm117
# License: Apache 2.0

# Standard Libraries
from copy import deepcopy

# External Libraries
import pytest

# Internal Modules to be tested
from mctk import KripkeStruct, KripkeStructError
from mctk import SAT_atom, NOT, AND, OR, IMPLIES, IFF, EX, AX, EU, EF, AG, EG, AF, AU


ks_json = {
    "Atoms": ["a", "b", "c", "d"],
    "States": {
        "s1": ["a"],
        "s2": ["a", "b"],
        "s3": ["b", "c"],
        "s4": ["b", "c", "d"],
        "s5": ["b"],
        "s6": ["c"],
        "s7": ["d"],
    },
    "Starts": ["s1"],
    "Trans": {
        's1': ['s2'],
        's2': ['s3', 's4'],
        's3': ['s4'],
        's4': ['s7'],
        's5': ['s6'],
        's6': ['s7', 's5'],
        's7': ['s5'],
    },
}
ks = KripkeStruct(ks_json)


def test_ESMC_SAT_atom():
    sat_states = SAT_atom(ks, "a")
    assert sat_states == {"s1", "s2"}

    sat_states = SAT_atom(ks, "b")
    assert sat_states == {"s2", "s3", "s4", "s5"}

    sat_states = SAT_atom(ks, "c")
    assert sat_states == {"s3", "s4", "s6"}

    sat_states = SAT_atom(ks, "d")
    assert sat_states == {"s4", "s7"}

    # if the atomic property is not in the Kripke Structure, can't check it
    with pytest.raises(KripkeStructError) as error_info:
        sat_states = SAT_atom(ks, "e")
    assert str(error_info.value) == "Can't check on an atom that's not in the Kripke Structure"

    sat_states = SAT_atom(ks, "True")
    assert sat_states == set(ks.get_states().keys())

    sat_states = SAT_atom(ks, "False")
    assert sat_states == set()


def test_ESMC_NOT():
    sat_states = NOT(ks, SAT_atom(ks, "a"))
    assert sat_states == set(ks.get_states().keys()) - {"s1", "s2"}

    sat_states = NOT(ks, SAT_atom(ks, "b"))
    assert sat_states == set(ks.get_states().keys()) - {"s2", "s3", "s4", "s5"}

    sat_states = NOT(ks, SAT_atom(ks, "True"))
    assert sat_states == set()

    sat_states = NOT(ks, SAT_atom(ks, "False"))
    assert sat_states == set(ks.get_states().keys())


def test_ESMC_AND():
    sat_states = AND(SAT_atom(ks, "a"), SAT_atom(ks, "b"))
    assert sat_states == {"s2"}

    sat_states = AND(SAT_atom(ks, "a"), SAT_atom(ks, "c"))
    assert sat_states == set()

    sat_states = AND(SAT_atom(ks, "b"), SAT_atom(ks, "c"))
    assert sat_states == {"s3", "s4"}


def test_ESMC_OR():
    sat_states = OR(SAT_atom(ks, "a"), SAT_atom(ks, "b"))
    assert sat_states == {"s1", "s2", "s3", "s4", "s5"}

    sat_states = OR(SAT_atom(ks, "a"), SAT_atom(ks, "c"))
    assert sat_states == {"s1", "s2", "s3", "s4", "s6"}


def test_ESMC_IMPLIES():
    sat_states = IMPLIES(ks, SAT_atom(ks, "a"), SAT_atom(ks, "b"))
    assert sat_states == {"s2", "s3", "s4", "s5", "s6", "s7"}

    sat_states = IMPLIES(ks, SAT_atom(ks, "a"), SAT_atom(ks, "c"))
    assert sat_states == {"s3", "s4", "s5", "s6", "s7"}

    sat_states = IMPLIES(ks, SAT_atom(ks, "b"), SAT_atom(ks, "c"))
    assert sat_states == {"s1", "s3", "s4", "s6", "s7"}


def test_ESMC_IFF():
    sat_states = IFF(ks, SAT_atom(ks, "a"), SAT_atom(ks, "b"))
    assert sat_states == {"s2", "s6", "s7"}

    sat_states = IFF(ks, SAT_atom(ks, "a"), SAT_atom(ks, "c"))
    assert sat_states == {"s5", "s7"}

    sat_states = IFF(ks, SAT_atom(ks, "b"), SAT_atom(ks, "c"))
    assert sat_states == {"s1", "s3", "s4", "s7"}


def test_ESMC_EX():
    sat_states = EX(ks, SAT_atom(ks, "a"))
    assert sat_states == {"s1"}

    sat_states = EX(ks, SAT_atom(ks, "b"))
    assert sat_states == {"s1", "s2", "s3", "s6", "s7"}

    sat_states = EX(ks, SAT_atom(ks, "c"))
    assert sat_states == {"s2", "s3", "s5"}

    sat_states = EX(ks, SAT_atom(ks, "d"))
    assert sat_states == {"s2", "s3", "s4", "s6"}


def test_ESMC_AX():
    sat_states = AX(ks, SAT_atom(ks, "a"))
    assert sat_states == {"s1"}

    sat_states = AX(ks, SAT_atom(ks, "b"))
    assert sat_states == {"s1", "s2", "s3", "s7"}

    sat_states = AX(ks, SAT_atom(ks, "c"))
    assert sat_states == {"s2", "s3", "s5"}

    sat_states = AX(ks, SAT_atom(ks, "d"))
    assert sat_states == {"s3", "s4"}


def test_ESMC_EU():
    sat_states = EU(ks, SAT_atom(ks, "a"), SAT_atom(ks, "b"))
    assert sat_states == {"s1", "s2", "s3", "s4", "s5"}

    sat_states = EU(ks, SAT_atom(ks, "a"), SAT_atom(ks, "c"))
    assert sat_states == {"s1", "s2", "s3", "s4", "s6"}

    sat_states = EU(ks, SAT_atom(ks, "b"), SAT_atom(ks, "c"))
    assert sat_states == {"s2", "s3", "s4", "s5", "s6"}


def test_ESMC_EF():
    sat_states = EF(ks, SAT_atom(ks, "a"))
    assert sat_states == {"s1", "s2"}

    sat_states = EF(ks, SAT_atom(ks, "b"))
    assert sat_states == {"s1", "s2", "s3", "s4", "s5", "s6", "s7"}

    sat_states = EF(ks, SAT_atom(ks, "c"))
    assert sat_states == {"s1", "s2", "s3", "s4", "s5", "s6", "s7"}

    sat_states = EF(ks, SAT_atom(ks, "d"))
    assert sat_states == {"s1", "s2", "s3", "s4", "s5", "s6", "s7"}


def test_ESMC_AG():
    sat_states = AG(ks, SAT_atom(ks, "a"))
    assert sat_states == set()

    sat_states = AG(ks, SAT_atom(ks, "b"))
    assert sat_states == set()

    sat_states = AG(ks, SAT_atom(ks, "c"))
    assert sat_states == set()

    sat_states = AG(ks, SAT_atom(ks, "d"))
    assert sat_states == set()


def test_ESMC_EG():
    # change s5's label to {"b", "d"}
    # change s6's label to {"c", "d"}
    tmp_ks = deepcopy(ks)
    tmp_ks.set_label_of_state("s5", {"b", "d"})
    tmp_ks.set_label_of_state("s6", {"c", "d"})

    sat_states = EG(tmp_ks, SAT_atom(tmp_ks, "a"))
    assert sat_states == set()

    sat_states = EG(tmp_ks, SAT_atom(tmp_ks, "b"))
    assert sat_states == set()

    sat_states = EG(tmp_ks, SAT_atom(tmp_ks, "c"))
    assert sat_states == set()

    sat_states = EG(tmp_ks, SAT_atom(tmp_ks, "d"))
    assert sat_states == {"s4", "s5", "s6", "s7"}

    tmp_ks.remove_trans({"s4": ["s7"]})
    sat_states = EG(tmp_ks, SAT_atom(tmp_ks, "d"))
    assert sat_states == {"s5", "s6", "s7"}


def test_ESMC_AF():
    # change s7 to "", which is empty set
    tmp_ks = deepcopy(ks)
    tmp_ks.set_label_of_state("s7", set())

    sat_states = AF(tmp_ks, SAT_atom(tmp_ks, "a"))
    assert sat_states == {"s1", "s2"}

    sat_states = AF(tmp_ks, SAT_atom(tmp_ks, "b"))
    assert sat_states == {"s1", "s2", "s3", "s4", "s5", "s6", "s7"}

    sat_states = AF(tmp_ks, SAT_atom(tmp_ks, "c"))
    assert sat_states == {"s1", "s2", "s3", "s4", "s5", "s6", "s7"}

    sat_states = AF(tmp_ks, SAT_atom(tmp_ks, "d"))
    assert sat_states == {"s1", "s2", "s3", "s4"}


def test_ESMC_AU():
    sat_states = AU(ks, SAT_atom(ks, "a"), SAT_atom(ks, "b"))
    assert sat_states == {"s1", "s2", "s3", "s4", "s5"}

    sat_states = AU(ks, SAT_atom(ks, "a"), SAT_atom(ks, "c"))
    assert sat_states == {"s1", "s2", "s3", "s4", "s6"}

    sat_states = AU(ks, SAT_atom(ks, "b"), SAT_atom(ks, "c"))
    assert sat_states == {"s2", "s3", "s4", "s5", "s6"}


# Integrated Tests
def test_ESMC_composite_CTL_formula():
    sat_states = EF(ks, SAT_atom(ks, "a") & SAT_atom(ks, "b"))
    assert sat_states == {"s1", "s2"}

    sat_states = AU(ks, NOT(ks, SAT_atom(ks, "a")), SAT_atom(ks, "c"))
    assert sat_states == {"s3", "s4", "s5", "s6", "s7"}

    sat_states = EX(ks, AF(ks, SAT_atom(ks, "b")))
    assert sat_states == {"s1", "s2", "s3", "s4", "s5", "s6", "s7"}

    sat_states = AU(ks, EX(ks, SAT_atom(ks, "b")), SAT_atom(ks, "c"))
    print(sat_states)
    assert sat_states == {"s1", "s2", "s3", "s4", "s6"}


# Integrated Tests: examples in documentations
def test_ESMC_examples():
    # create a Kripke Structure from scratch
    ks = KripkeStruct()

    # set 2 Atomic Propositions in this Kripke Structure
    ks.set_atoms(["p", "q"])

    # add 2 states to the Kripke Structure
    # a State Name is represented by a string, it must be unique
    # a State Label is represented by a binary number, it must be unique
    # for example, 0b10 means the state has the Atoms "p" but not "q"
    ks.add_state("s0", ["p"])
    ks.add_state("s1", ["q"])

    # set the Start States of the Kripke Structure
    # there can be multiple Start States
    ks.set_starts(["s0"])

    # add 2 Transitions to the Kripke Structure
    # a Transition is represented by a key-value pair
    # where key the Source State Name and value is a list of Destination State Names
    ks.add_trans({"s0": ["s1"], "s1": ["s0"]})

    # check if the Kripke Structure satisfies the CTL formula: EX p
    # SAT_atom(ks, "p") returns a set of states that satisfy the Atomic Proposition p
    # EX returns a set of states that satisfy the CTL formula EX p
    sat_states = EX(ks, SAT_atom(ks, "p"))

    # the result should be {"s1"}
    # since the start state "s0" is not in sat_states, ks doesn't satisfy the CTL formula
    assert sat_states == {"s1"}

    # check if the Kripke Structure satisfies the CTL formula: E p U q
    # SAT_atom(ks, "p") returns a set of states that satisfy the Atomic Proposition p
    # SAT_atom(ks, "q") returns a set of states that satisfy the Atomic Proposition q
    # EU returns a set of states that satisfy the CTL formula E p U q
    sat_states = EU(ks, SAT_atom(ks, "p"), SAT_atom(ks, "q"))

    # the result should be {"s0", "s1"}
    # since the start state "s0" is in sat_states, ks satisfies the CTL formula
    assert sat_states == {"s0", "s1"}

    # composite CTL formula is supported as the following
    # check if the Kripke Structure satisfies the CTL formula: EX (p AND EX q)
    sat_states = EX(ks, AND(SAT_atom(ks, "p"), EX(ks, SAT_atom(ks, "q"))))

    # the result should be {"s1"}
    # since the start state "s0" is not in sat_states, ks doesn't satisfy the CTL formula
    assert sat_states == {"s1"}

    # check if the Kripke Structure satisfies the CTL formula: EG (A p U (NOT q))
    sat_states = EG(ks, AU(ks, SAT_atom(ks, "p"), NOT(ks, SAT_atom(ks, "q"))))

    # the result should be set(), empty set
    # since the start state "s0" is not in sat_states, ks doesn't satisfy the CTL formula
    assert sat_states == set()
