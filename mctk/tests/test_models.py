from collections import defaultdict
import json
from mctk.models import *



# test KripkeStruct(ks_json)
def test_ks_load_creation():
    pass
    '''
    # create a model from JSON file
    model_path = "./model.json"
    with open(model_path, "r") as f:
        ks_json = json.load(f)
    ks = KripkeStruct(ks_json)
    '''


# test KripkeStruct()
def test_ks_runtime_creation():
    ks = KripkeStruct()
    assert ks.atoms == ()
    assert ks.states == {}
    assert ks.states_labels == set()
    assert ks.starts == ()
    assert ks.trans == defaultdict(list)
    assert ks.trans_inverted == defaultdict(list)


# test ks.set_atoms(atoms)
def test_ks_set_atoms():
    ks = KripkeStruct()
    atoms = ["a", "b", "c", "d"]
    ks.set_atoms(atoms)
    assert ks.atoms == ('a', 'b', 'c', 'd')

    # if any state exists, can't reset atoms
    try:
        ks.add_state("s1", 0b1000)
        atoms = ["a"]
        ks.set_atoms(atoms)
        assert False
    except Exception as e:
        assert str(e) == "Can't reset Atoms after States are Created"


# test ks.get_atoms()
def test_ks_get_atoms():
    ks = KripkeStruct()
    atoms = ["a", "b", "c", "d"]
    ks.set_atoms(atoms)
    assert ks.get_atoms() == atoms


# test ks.add_state(state)
def test_ks_add_state():
    ks = KripkeStruct()
    atoms = ["a", "b", "c", "d"]
    ks.set_atoms(atoms)
    ks.add_state("s1", 0b1000)
    assert ks.states == {"s1": 0b1000}

    # if the state name exists, can't add again
    try:
        ks.add_state("s1", 0b1111)
        assert False
    except Exception as e:
        assert str(e) == "Can't add an Exisiting State Name again"

    # if the state label exisits, can't add again
    try:
        ks.add_state("s8", 0b1000)
        assert False
    except Exception as e:
        assert str(e) == "Can't add an Exisiting State Label again"


# test ks.add_states(states)
def test_ks_add_states():
    ks = KripkeStruct()
    atoms = ["a", "b", "c", "d"]
    ks.set_atoms(atoms)
    states = {
        "s2": 0b1100,  # s2 has labels "a", "b"
        "s3": 0b0110,  # s3 has labels "b", "c"
        "s4": 0b0111,  # s4 has labels "b", "c", "d"
        "s5": 0b0100,  # s5 has label "b"
        "s6": 0b0010,  # s6 has label "c"
        "s7": 0b0001,  # s7 has label "d"
    }
    ks.add_states(states)
    assert ks.states == states


# test ks.get_states()
def test_ks_get_states():
    ks = KripkeStruct()
    atoms = ["a", "b", "c", "d"]
    ks.set_atoms(atoms)
    ks.add_state("s1", 0b1000)
    assert ks.get_states() == {"s1": 0b1000}


# test ks.remove_state(state)
def test_ks_remove_state():
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


# test ks.test_ks_remove_states(states)
def test_ks_remove_states():
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
