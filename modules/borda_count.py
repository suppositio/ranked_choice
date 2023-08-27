def borda_count(votes):
    candidates = set().union(*votes)
    num_candidates = len(candidates)

    scores = {candidate:0 for candidate in candidates}
    for vote in votes:
        for candidate, rank in vote.items():
            scores[candidate] += num_candidates - rank + 1

    sorted_candidates = sorted(scores, key=scores.get, reverse = True)

    result = {}
    previous_score = None
    previous_rank = None
    for rank, candidate in enumerate(sorted_candidates, start = 1):
        score = scores[candidate]
        if score == previous_score:
            rank = previous_rank
        else:
            previous_rank = rank
        result[candidate] = rank
        previous_score = score

    return result        

