from typing import List

def sort_list(numbers: List[int]) -> List[int]:
    """
    Sorts a list of integers in ascending order using the merge sort algorithm.

    Merge Sort is a divide-and-conquer algorithm that splits the list into smaller sublists,
    recursively sorts each sublist, and merges the sorted sublists to produce the final sorted list.

    Time Complexity:
        - Average case: O(n log n)
        - Worst case: O(n log n)
        - Best case: O(n log n)
    
    Space Complexity:
        - O(n), because merge sort requires additional space to hold the merged result.

    Args:
        numbers (List[int]): A list of integers to sort.

    Returns:
        List[int]: A new list containing the sorted integers.
    """
    # Base case: a list of zero or one element is already sorted
    if len(numbers) <= 1:
        return numbers

    # Split the list into two halves
    mid = len(numbers) // 2
    left_half = sort_list(numbers[:mid])
    right_half = sort_list(numbers[mid:])

    # Merge the sorted halves
    return merge(left_half, right_half)

def merge(left: List[int], right: List[int]) -> List[int]:
    """
    Merges two sorted lists into one sorted list.

    This function takes two sorted lists and combines them into a single sorted list by comparing 
    elements from each list in order. This process continues until all elements from both lists 
    have been added to the final sorted list.

    Time Complexity:
        - O(n), where n is the total number of elements in 'left' and 'right'.

    Args:
        left (List[int]): A sorted list of integers.
        right (List[int]): A sorted list of integers.

    Returns:
        List[int]: A new list containing all elements from 'left' and 'right', sorted.
    """
    sorted_list = []
    i = j = 0

    # Merge elements from both lists in sorted order
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            sorted_list.append(left[i])
            i += 1
        else:
            sorted_list.append(right[j])
            j += 1

    # Add any remaining elements from the left or right half
    sorted_list.extend(left[i:])
    sorted_list.extend(right[j:])

    return sorted_list

# Example usage
if __name__ == "__main__":
    nums = [3, 2, 7, 4, 8, 6, 9, 1, 5]
    print("Original list:", nums)
    print("Sorted list:", sort_list(nums))
