from logic import *

library = Symbol("library")
hermione = Symbol("hermione")
harry = Symbol("harry")
ron = Symbol("ron")

knowledge = And(
    # If hermione in library, then harry in library
    Implication(hermione, harry),
    # hermione is in the library
    hermione,
    # ron is not in the library
    Not(ron),
    harry,
    Or(ron, hermione)

)

print(model_check(knowledge, Not(harry)))
