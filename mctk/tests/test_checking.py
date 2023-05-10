# Authors: marcusm117
# License: Apache 2.0

# external libraries
import pytest

# module to be tested
from mctk import KripkeStruct, KripkeStructError
from mctk import SAT_atom, NOT, AND, OR, IMPLIES, EX, AX, EU, EF, AG, EG, AF, AU


ks_json = {
    "Atoms": ("a", "b", "c", "d"),
    "States": {
        "s1": 0b1000,  # s1 has labels "a"
        "s2": 0b1100,  # s2 has labels "a", "b"
        "s3": 0b0110,  # s3 has labels "b", "c"
        "s4": 0b0111,  # s4 has labels "b", "c", "d"
        "s5": 0b0100,  # s5 has label "b"
        "s6": 0b0010,  # s6 has label "c"
        "s7": 0b0001,  # s7 has label "d"
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
    assert sat_states == set(ks.states.keys())

    sat_states = SAT_atom(ks, "False")
    assert sat_states == set()


def test_ESMC_NOT():
    sat_states = NOT(ks, SAT_atom(ks, "a"))
    assert sat_states == set(ks.states.keys()) - {"s1", "s2"}

    sat_states = NOT(ks, SAT_atom(ks, "b"))
    assert sat_states == set(ks.states.keys()) - {"s2", "s3", "s4", "s5"}

    sat_states = NOT(ks, SAT_atom(ks, "True"))
    assert sat_states == set()

    sat_states = NOT(ks, SAT_atom(ks, "False"))
    assert sat_states == set(ks.states.keys())


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
    from copy import deepcopy

    # change s5's label to {"b", "d"}
    # change s6's label to {"c", "d"}
    tmp_ks = deepcopy(ks)
    tmp_ks.states["s5"] = 0b0101
    tmp_ks.states["s6"] = 0b0011

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
    from copy import deepcopy

    # change s7 to "", which is empty set
    tmp_ks = deepcopy(ks)
    tmp_ks.states["s7"] = 0b0000

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
