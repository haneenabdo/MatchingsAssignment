from models import ProblemInstance


def gale_shapley(instance: ProblemInstance):

    # returns matches in the form of a list of length n where matches[h] = student_id matched to hospital (h+1)
    # returns tot num of proposals made

    n = instance.n

    hosp_prefs = instance.hospital_prefs
    stud_prefs = instance.student_prefs

    # edge case n = 0 (juuust in case)
    if n == 0:
        return [], 0

    # student_rank[s][h] = how much student (s+1) likes hospital (h+1), lower numb is better
    stud_rank = []

    for prefs in stud_prefs:
        rank = [0] * (n + 1)

        for i, h_id in enumerate(prefs):
            rank[h_id] = i
        stud_rank.append(rank)

    # matches_h[h] = student id matched to hospital (h+1), 0 means unmatched
    matches_h = [0] * n
    # same as above
    matches_s = [0] * n

    # next_choice[h] is index in hospital h's pref list to propose to next
    next_choice = [0] * n

    proposals = 0

    # loop while some hospital is unmatched & still has someone to propose to
    def find_free_hosp():
        for h in range(n):
            if matches_h[h] == 0 and next_choice[h] < n:
                return h
        return None


    while True:
        h = find_free_hosp()
        if h is None:
            break

        s_id = hosp_prefs[h][next_choice[h]]
        next_choice[h] += 1
        proposals += 1

        s = s_id - 1

        # if student free, accept right away
        if matches_s[s] == 0:
            matches_s[s] = h + 1
            matches_h[h] = s_id
            continue

        # if not, student compares current hospital vs new hospital
        current_h_id = matches_s[s]

        if stud_rank[s][h + 1] < stud_rank[s][current_h_id]:
            # this means student prefers the new hospital
            matches_s[s] = h + 1
            matches_h[h] = s_id

            # old hospital = unmatched again
            old_h_index = current_h_id - 1
            matches_h[old_h_index] = 0
        # otherwise student rejects new hospital, hospital stays unmatched and will just try again

    return matches_h, proposals
