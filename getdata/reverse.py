
def sortInteger(A):
    if A is None: return A
    n = len(A)
    if n == 1 or n == 0: return A
    return quickSort(A, 0, n - 1)

def quickSort(List, left, right):
    if left >= right:
        return List
    key = List[left]
    low = left
    high = right
    while left < right:
        while left < right and List[right] >= key:
            right -= 1
        List[left], List[right] = List[right], List[left]
        while left < right and List[left] <= key:
            left += 1
        List[right], List[left] = List[left], List[right]
    quickSort(List, low, left - 1)
    quickSort(List, left + 1, high)
    return List

def sortFile(inputFilePath,outputFilePath):
    ints = list()
    with open(inputFilePath) as fin:
        ints_str = fin.readlines()
    for int_str in ints_str:
        ints.append(int(int_str.strip("\n")))
    ints_sorted = sortInteger(ints)
    with open(outputFilePath,'w') as fout:
        for int_sorted in ints_sorted:
            fout.write(str(int_sorted))
            fout.write("\n")

if __name__ == '__main__':
    inputFilePath="C:/Users/ssfve/Desktop/input.txt"
    outputFilePath="C:/Users/ssfve/Desktop/output.txt"
    sortFile(inputFilePath,outputFilePath)
