import mctk
import json

# create a model from JSON file
model_path = "./model.json"
with open(model_path, "r") as f:
    model_json = json.load(f)
model_1 = mctk.ExplicitStateChecker(model_json)

# create a model during runtime
model_2 = mctk.ExplicitStateChecker()
atoms = ["a", "b", "c", "d"]
model_2.add_atoms(atoms)

# add states
model_2.add_state("a")
model_2.add_state("ab")
states = ["bc", "bcd"]
model_2.add_states(states)

# add transitions
model_2.add_tran("a", ["ab", "bc"])
trans = {"ab" : ["bc"], 
         "bc" : ["bcd", "a"], 
         "bcd" : ["ab"]
         }
model_2.add_trans(trans)

# create a CTL property
prop = "EX (a | b)"

# check CTL property, return boolean indicating SAT or UNSAT
# defaultly print error trace to console
model_2.check(prop) 

# write error trace to a file
out_path = "./result.txt"
model_2.check(prop, out_path)  



