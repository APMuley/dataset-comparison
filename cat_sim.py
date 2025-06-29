from collections import Counter

def jaccard_similarity(list1, list2, order=1):
    # Case 1: When order doesn't matter (order = 1)
    if order == 1:
        # Use Counter to get frequency counts for both lists
        counter1 = Counter(list1)
        counter2 = Counter(list2)

        # Calculate the intersection count by taking the minimum of frequencies
        intersection_count = sum((counter1 & counter2).values())  # Minimum of corresponding counts
        print(f"Intersection Count: {intersection_count}")  # Debugging line

        # Calculate the union count by taking the maximum of frequencies
        union_count = sum((counter1 | counter2).values())  # Maximum of corresponding counts
        print(f"Union Count: {union_count}")  # Debugging line

        # Return the Jaccard similarity score
        if union_count == 0:
            return 0  # To avoid division by zero if both lists are empty
        score = (intersection_count / union_count) * 100
        print(f"Jaccard Similarity (Order doesn't matter): {score:.2f}%")
        return score

    # Case 2: When order matters (order = 0)
    else:
        # Break both lists into sublists of 5 elements
        sublists1 = [list1[i:i + 5] for i in range(0, len(list1), 5)]
        sublists2 = [list2[i:i + 5] for i in range(0, len(list2), 5)]

        # Calculate Jaccard similarity for each pair of sublists and average the results
        total_score = 0
        count = 0
        for sublist1, sublist2 in zip(sublists1, sublists2):
            # Use Counter to compare sublists
            counter1 = Counter(sublist1)
            counter2 = Counter(sublist2)

            # Calculate the intersection and union counts
            intersection_count = sum((counter1 & counter2).values())
            union_count = sum((counter1 | counter2).values())

            # Calculate the Jaccard similarity score for the sublist
            if union_count != 0:
                score = (intersection_count / union_count) * 100
                total_score += score
                count += 1

        if count == 0:
            return 0  # To avoid division by zero if there are no sublists
        average_score = total_score / count
        print(f"Jaccard Similarity (Order matters, averaged over sublists): {average_score:.2f}%")
        return average_score


# Example usage
list1 = [
    'Apple', 'Banana', 'Mango', 'Orange', 'Grapes',
    'Apple', 'Banana', 'Mango', 'Orange', 'Grapes',
    'Apple', 'Banana', 'Mango', 'Orange', 'Grapes',
    'Apple', 'Banana', 'Mango', 'Orange', 'Grapes',
    'Apple', 'Banana', 'Mango', 'Orange', 'Grapes',
    'Apple', 'Banana', 'Mango', 'Orange', 'Grapes',
    'Apple', 'Banana', 'Mango', 'Orange', 'Grapes'
]

list2 = [
    'Apple', 'Banana', 'Lime', 'Tomato', 'Grapes',
    'Apple', 'Banana', 'Lime', 'Tomato', 'Grapes',
    'Apple', 'Banana', 'Lime', 'Tomato', 'Grapes',
    'Apple', 'Banana', 'Lime', 'Tomato', 'Grapes',
    'Apple', 'Banana', 'Lime', 'Tomato', 'Grapes',
    'Apple', 'Banana', 'Lime', 'Tomato', 'Grapes',
    'Apple', 'Banana', 'Lime', 'Tomato', 'Grapes'
]

# Order doesn't matter
jaccard_similarity(list1, list2, order=1)

# Order matters
jaccard_similarity(list1, list2, order=0)
