def resolve(current, clause):
    pass



def resolution_solver(KB, neg_alpha):
    # KB: list of known clauses
    #           clause example: a v b v -c v d
    #           choose your own representation, e.g. ("a", "b", "-c", "d")
    # neg_alpha: query clause, already negated
    # returns True if proof found, False otherwise

    # initialize
    todo = [neg_alpha]
    done = KB.copy()

    # process the todo list one by one
    while todo:
        current = todo.pop()

        # check if current is redundant
        for clause in done + todo:
            # if clause is a subset of current, throw current away
            # and pick next from todo list

        # combine current clause with all clauses we've already seen
        for clause in done:
            # apply resolution rule
            resolvents = resolve(current, clause)
            # handle new clauses generated by the resolution rule
            for resolvent in resolvents:
                # some important things that can happen here:
                # 1. resolvent is empty: proof found that KB->alpha!
                # 2. resolvent is always true: throw it away, useless clause
                # ONLY if neither of these things happen:
                    todo.append(resolvent)

        # we're done with this clause
        done.append(current)

    # loop ended without proof
    return False