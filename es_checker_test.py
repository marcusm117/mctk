# Authors: marcusm117
# License: AGPL v3.0

from mctk import models
import json




def load_creation_test():
    pass
    '''
    # create a model from JSON file
    model_path = "./model.json"
    with open(model_path, "r") as f:
        model_json = json.load(f)
    model_1 = mctk.ExplicitStateChecker(model_json)
    '''


def runtime_creation_test():
    # create a model during runtime
    model_2 = models.KripkeStruct()

    # add atoms
    atoms = ["a", "b", "c", "d"]
    model_2.set_atoms(atoms)

    # get current atoms
    atoms = model_2.get_atoms()
    print(atoms)
    assert(atoms == ['a', 'b', 'c', 'd'])

    # add states
    model_2.add_state("s1", 0b1000)  # s1 has label "a"
    model_2.add_state("s2", 0b1100)  # s2 has labels "a", "b"
    states = {"s3" : 0b0110,         # s3 has labels "b", "c"
              "s4" : 0b0111,         # s4 has labels "b", "c", "d"
              "s5" : 0b0100,         # s5 has label "b"
              "s6" : 0b0010,         # s6 has label "c"
              "s7" : 0b0001          # s7 has label "d"
             }
    model_2.add_states(states)

    # get current states
    states = model_2.get_states()
    print(states)
    assert(states == {'s1': 8, 's2': 12, 's3': 6, 's4': 7, 's5': 4, 's6': 2, 's7': 1})

    # remove states
    model_2.remove_state("s5")
    states = ["s6", "s7"]
    model_2.remove_states(states)
    print(model_2.get_states())
    assert(model_2.get_states() == {'s1': 8, 's2': 12, 's3': 6, 's4': 7})

    # set start states
    starts = ["s1", "s4"]
    model_2.set_starts(starts)
    model_2.set_starts(["s1"])  # this will reset the start states

    # get current start states
    starts = model_2.get_starts()
    print(starts)
    assert(starts == ['s1'])

    # add transitions
    trans = {"s1" : ["s2"],        # a -> ab
             "s2" : ["s3", "s4"],        # ab -> bc
             "s3" : ["s4", "s1"],  # bc -> bcd, a
             "s4" : ["s2"]         # bcd -> ab
            }
    model_2.add_trans(trans)

    # get current transitions
    trans = model_2.get_trans()
    print(trans)
    assert(trans == {'s1': ['s2'], 's2': ['s3', 's4'], 's3': ['s4', 's1'], 's4': ['s2']})

    # remove transitions
    trans = {"s2" : ["s4"],
            "s4" : ["s2"]
            }
    model_2.remove_trans(trans)
    print(model_2.get_trans())
    assert(model_2.get_trans() == {'s1': ['s2'], 's2': ['s3'], 's3': ['s4', 's1'], 's4': []})

    print("Congrats! All Runtime Creation Tests are Passed.")


def checking_test():
    pass
    '''
    # create a CTL property
    prop = mctk.parse_ctl("EX (a | b)")

    # check CTL property, return boolean indicating SAT or UNSAT
    # defaultly print error trace to console
    model_2.check(prop)

    # write error trace to a file
    out_path = "./result.txt"
    model_2.check(prop, out_path)  
    '''




def main():
    load_creation_test()
    runtime_creation_test()
    checking_test()



if __name__ == "__main__":
    main()