# Authors: marcusm117
# License: Apache 2.0

# Standard Libraries
from collections import defaultdict

# External Libraries
import pytest

# Internal Modules to be tested
from mctk import KripkeStruct, KripkeStructError


# Tests for KripkeStruct()
def test_KS_default_init():
    ks = KripkeStruct()
    assert ks.atoms == ()
    assert ks.states == {}
    assert ks.starts == set()
    assert ks.trans == defaultdict(list)
    assert ks.trans_inverted == defaultdict(list)


# Tests for KripkeStruct(ks_json)
def test_KS_file_init():
    ks_json = {
        "Atoms": ("a", "b", "c", "d"),
        "States": {"s1": 8, "s2": 12, "s3": 6, "s4": 7},
        "Starts": ["s1"],
        "Trans": {"s1": ["s2"], "s2": ["s3", "s4"], "s3": ["s4"]},
    }
    ks = KripkeStruct(ks_json)

    assert ks.atoms == ("a", "b", "c", "d")
    assert ks.states == {"s1": 8, "s2": 12, "s3": 6, "s4": 7}
    assert ks.starts == {"s1"}
    assert dict(ks.trans) == {"s1": ["s2"], "s2": ["s3", "s4"], "s3": ["s4"]}


# Tests for ks.__str__()
def test_KS_str_rep():
    ks_json = {
        "Atoms": ("a", "b", "c", "d"),
        "States": {"s1": 8, "s2": 12, "s3": 6, "s4": 7},
        "Starts": {"s1"},
        "Trans": {"s1": ["s2"], "s2": ["s3", "s4"], "s3": ["s4"]},
    }
    ks = KripkeStruct(ks_json)
    assert str(ks) == (
        "Atoms: ('a', 'b', 'c', 'd')\n"
        + "States: {'s1': 8, 's2': 12, 's3': 6, 's4': 7}\n"
        + "Starts: {'s1'}\n"
        + "Trans: {'s1': ['s2'], 's2': ['s3', 's4'], 's3': ['s4']}"
    )


def test_KS_set_atoms():
    ks = KripkeStruct()
    atoms = ["a", "b", "c", "d"]
    ks.set_atoms(atoms)
    assert ks.atoms == ("a", "b", "c", "d")

    # if any state exists, can't reset atoms
    with pytest.raises(KripkeStructError) as error_info:
        ks.add_state("s1", 0b1000)
        atoms = ["a"]
        ks.set_atoms(atoms)
    assert str(error_info.value) == "Can't reset Atoms after States are Created"


def test_KS_get_atoms():
    ks = KripkeStruct()
    atoms = ["a", "b", "c", "d"]
    ks.set_atoms(atoms)
    assert ks.get_atoms() == atoms


def test_KS_add_state():
    ks = KripkeStruct()
    atoms = ["a", "b", "c", "d"]
    ks.set_atoms(atoms)
    ks.add_state("s1", 0b1000)
    assert ks.states == {"s1": 0b1000}

    # if the state name exists, can't add again
    with pytest.raises(KripkeStructError) as error_info:
        ks.add_state("s1", 0b1111)
    assert str(error_info.value) == "Can't add an Exisiting State Name again"

    # if the state label exisits, can't add again
    with pytest.raises(KripkeStructError) as error_info:
        ks.add_state("s8", 0b1000)
    assert str(error_info.value) == "Can't add an Exisiting State Label again"


def test_KS_add_states():
    ks = KripkeStruct()
    atoms = ["a", "b", "c", "d"]
    ks.set_atoms(atoms)
    states = {
        "s1": 0b1000,  # s1 has labels "a"
        "s2": 0b1100,  # s2 has labels "a", "b"
        "s3": 0b0110,  # s3 has labels "b", "c"
        "s4": 0b0111,  # s4 has labels "b", "c", "d"
        "s5": 0b0100,  # s5 has label "b"
        "s6": 0b0010,  # s6 has label "c"
        "s7": 0b0001,  # s7 has label "d"
    }
    ks.add_states(states)
    assert ks.states == states


def test_KS_get_states():
    ks = KripkeStruct()
    atoms = ["a", "b", "c", "d"]
    ks.set_atoms(atoms)
    ks.add_state("s1", 0b1000)
    assert ks.get_states() == {"s1": 0b1000}


def test_KS_get_state_label_set():
    ks = KripkeStruct()
    atoms = ["a", "b", "c", "d"]
    ks.set_atoms(atoms)
    ks.add_state("s1", 0b1001)
    assert ks.get_state_label_set("s1") == {"a", "d"}

    # if the state doesn't exist, can't get the Label Set of it
    with pytest.raises(KripkeStructError) as error_info:
        assert ks.get_state_label_set("s2")
    assert str(error_info.value) == "Can't get the Label Set of a Non-Exisiting State"


def test_KS_remove_state():
    ks = KripkeStruct()
    atoms = ["a", "b", "c", "d"]
    ks.set_atoms(atoms)
    states = {
        "s1": 0b1000,  # s1 has labels "a"
        "s2": 0b1100,  # s2 has labels "a", "b"
        "s3": 0b0110,  # s3 has labels "b", "c"
        "s4": 0b0111,  # s4 has labels "b", "c", "d"
        "s5": 0b0100,  # s5 has label "b"
        "s6": 0b0010,  # s6 has label "c"
        "s7": 0b0001,  # s7 has label "d"
    }
    ks.add_states(states)
    ks.remove_state("s7")
    states.pop("s7")
    assert ks.states == states

    # removing non-existing state won't have any effect
    ks.remove_state("s8")
    assert ks.states == states


def test_KS_remove_states():
    ks = KripkeStruct()
    atoms = ["a", "b", "c", "d"]
    ks.set_atoms(atoms)
    states = {
        "s1": 0b1000,  # s1 has labels "a"
        "s2": 0b1100,  # s2 has labels "a", "b"
        "s3": 0b0110,  # s3 has labels "b", "c"
        "s4": 0b0111,  # s4 has labels "b", "c", "d"
        "s5": 0b0100,  # s5 has label "b"
        "s6": 0b0010,  # s6 has label "c"
        "s7": 0b0001,  # s7 has label "d"
    }
    ks.add_states(states)
    ks.remove_states(["s6", "s7"])
    states.pop("s7")
    states.pop("s6")
    assert ks.states == states


def test_KS_set_starts():
    ks = KripkeStruct()
    atoms = ["a", "b", "c", "d"]
    ks.set_atoms(atoms)
    states = {
        "s1": 0b1000,  # s1 has labels "a"
        "s2": 0b1100,  # s2 has labels "a", "b"
        "s3": 0b0110,  # s3 has labels "b", "c"
        "s4": 0b0111,  # s4 has labels "b", "c", "d"
    }
    ks.add_states(states)

    starts = ["s1", "s4"]
    ks.set_starts(starts)
    assert ks.starts == set(starts)

    # resetting the start states is allowed
    starts = ["s1"]
    ks.set_starts(starts)
    assert ks.starts == set(starts)

    # if state doesn't exist, can't set as start state
    with pytest.raises(KripkeStructError) as error_info:
        ks.set_starts(["s5"])
    assert str(error_info.value) == "Can't set a Non-Exisiting State as Start State"


def test_KS_get_starts():
    ks = KripkeStruct()
    atoms = ["a", "b", "c", "d"]
    ks.set_atoms(atoms)
    states = {
        "s1": 0b1000,  # s1 has labels "a"
        "s2": 0b1100,  # s2 has labels "a", "b"
        "s3": 0b0110,  # s3 has labels "b", "c"
        "s4": 0b0111,  # s4 has labels "b", "c", "d"
    }
    ks.add_states(states)

    starts = ["s1", "s4"]
    ks.set_starts(starts)
    assert set(ks.get_starts()) == set(starts)


def test_KS_add_trans():
    ks = KripkeStruct()
    atoms = ["a", "b", "c", "d"]
    ks.set_atoms(atoms)
    states = {
        "s1": 0b1000,  # s1 has labels "a"
        "s2": 0b1100,  # s2 has labels "a", "b"
        "s3": 0b0110,  # s3 has labels "b", "c"
        "s4": 0b0111,  # s4 has labels "b", "c", "d"
    }
    ks.add_states(states)
    ks.set_starts(["s1"])

    trans = {
        "s1": ["s2"],  # a -> ab
        "s2": ["s3", "s4"],  # ab -> bc
        "s3": ["s4", "s1"],  # bc -> bcd, a
        "s4": ["s2"],  # bcd -> ab
    }
    ks.add_trans(trans)
    assert trans == {"s1": ["s2"], "s2": ["s3", "s4"], "s3": ["s4", "s1"], "s4": ["s2"]}

    # if source state doesn't exist, can't add transition from it
    with pytest.raises(KripkeStructError) as error_info:
        trans = {"s7": ["s1"]}
        ks.add_trans(trans)
    assert str(error_info.value) == "Can't add Transition from a Non-Exisiting Source State"

    # if target state doesn't exist, can't add transition to it
    with pytest.raises(KripkeStructError) as error_info:
        trans = {"s1": ["s7"]}
        ks.add_trans(trans)
    assert str(error_info.value) == "Can't add Transition to a Non-Exisiting Target State"


def test_KS_get_trans():
    ks = KripkeStruct()
    atoms = ["a", "b", "c", "d"]
    ks.set_atoms(atoms)
    states = {
        "s1": 0b1000,  # s1 has labels "a"
        "s2": 0b1100,  # s2 has labels "a", "b"
        "s3": 0b0110,  # s3 has labels "b", "c"
        "s4": 0b0111,  # s4 has labels "b", "c", "d"
    }
    ks.add_states(states)
    ks.set_starts(["s1"])
    trans = {
        "s1": ["s2"],  # a -> ab
        "s2": ["s3", "s4"],  # ab -> bc
        "s3": ["s4", "s1"],  # bc -> bcd, a
        "s4": ["s2"],  # bcd -> ab
    }
    ks.add_trans(trans)
    assert ks.get_trans() == {"s1": ["s2"], "s2": ["s3", "s4"], "s3": ["s4", "s1"], "s4": ["s2"]}


def test_KS_get_trans_inverted():
    ks = KripkeStruct()
    atoms = ["a", "b", "c", "d"]
    ks.set_atoms(atoms)
    states = {
        "s1": 0b1000,  # s1 has labels "a"
        "s2": 0b1100,  # s2 has labels "a", "b"
        "s3": 0b0110,  # s3 has labels "b", "c"
        "s4": 0b0111,  # s4 has labels "b", "c", "d"
    }
    ks.add_states(states)
    ks.set_starts(["s1"])
    trans = {
        "s1": ["s2"],  # a -> ab
        "s2": ["s3", "s4"],  # ab -> bc
        "s3": ["s4", "s1"],  # bc -> bcd, a
        "s4": ["s2"],  # bcd -> ab
    }
    ks.add_trans(trans)
    assert ks.get_trans_inverted() == {"s1": ["s3"], "s2": ["s1", "s4"], "s3": ["s2"], "s4": ["s2", "s3"]}


def test_KS_remove_trans():
    ks = KripkeStruct()
    atoms = ["a", "b", "c", "d"]
    ks.set_atoms(atoms)
    states = {
        "s1": 0b1000,  # s1 has labels "a"
        "s2": 0b1100,  # s2 has labels "a", "b"
        "s3": 0b0110,  # s3 has labels "b", "c"
        "s4": 0b0111,  # s4 has labels "b", "c", "d"
    }
    ks.add_states(states)
    ks.set_starts(["s1"])
    trans = {
        "s1": ["s2"],  # a -> ab
        "s2": ["s3", "s4"],  # ab -> bc
        "s3": ["s4", "s1"],  # bc -> bcd, a
        "s4": ["s2"],  # bcd -> ab
    }
    ks.add_trans(trans)

    trans = {"s2": ["s4"], "s4": ["s2"]}
    ks.remove_trans(trans)
    assert ks.get_trans() == {"s1": ["s2"], "s2": ["s3"], "s3": ["s4", "s1"], "s4": []}

    # removing non-existing transition won't have any effect
    trans = {"s2": ["s4"]}
    ks.remove_trans(trans)
    assert ks.get_trans() == {"s1": ["s2"], "s2": ["s3"], "s3": ["s4", "s1"], "s4": []}


def test_KS_get_SCCs():
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
    SCC_1 = frozenset({"s1"})
    SCC_2 = frozenset({"s2"})
    SCC_3 = frozenset({"s3"})
    SCC_4 = frozenset({"s4"})
    SCC_5 = frozenset({"s5", "s6", "s7"})
    assert ks.get_SCCs() == {SCC_1, SCC_2, SCC_3, SCC_4, SCC_5}

    ks.add_trans({"s4": ["s2"]})
    SCC_6 = frozenset({"s2", "s3", "s4"})
    assert ks.get_SCCs() == {SCC_1, SCC_6, SCC_5}

    ks.remove_states(["s3", "s4", "s6"])
    SCC_7 = frozenset({"s5"})
    SCC_8 = frozenset({"s7"})
    assert ks.get_SCCs() == {SCC_1, SCC_2, SCC_7, SCC_8}


# Integration Tests: removing state will remove related transitions
def test_KS_remove_states_will_remove_related_trans():
    ks = KripkeStruct()
    atoms = ["a", "b", "c", "d"]
    ks.set_atoms(atoms)
    states = {
        "s1": 0b1000,  # s1 has labels "a"
        "s2": 0b1100,  # s2 has labels "a", "b"
        "s3": 0b0110,  # s3 has labels "b", "c"
        "s4": 0b0111,  # s4 has labels "b", "c", "d"
    }
    ks.add_states(states)
    ks.set_starts(["s1"])
    trans = {
        "s1": ["s2"],  # a -> ab
        "s2": ["s3", "s4"],  # ab -> bc
        "s3": ["s4", "s1"],  # bc -> bcd, a
        "s4": ["s2"],  # bcd -> ab
    }
    ks.add_trans(trans)

    ks.remove_state("s2")
    assert ks.get_trans() == {'s1': [], 's3': ['s4', 's1'], 's4': []}
    assert ks.get_trans_inverted() == {'s3': [], 's4': ['s3'], 's1': ['s3']}
