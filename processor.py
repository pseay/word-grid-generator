import random

# setup
data = [[[[False for a in range(26)] for b in range(26)] for c in range(26)] for d in range(26)]
alphabet = "abcdefghijklmnopqrstuvwxyz"
ctn = {}
ntc = {}
for i in range(26):
    ctn[alphabet[i]] = i
    ntc[i] = alphabet[i]
# getting words
words = []
with open('words.txt', 'r') as file:
    words = [line.strip() for line in file.readlines()]
# setting data
for word in words:
    nums = [ctn[char] for char in list(word)]
    data[nums[0]][nums[1]][nums[2]][nums[3]] = True

def nums_to_word(nums):
    letters = [ntc[num] for num in nums]
    return ''.join(letters)

def find_adj(word):
    [a,b,c,d] = [ctn[char] for char in list(word)]
    adj = set()
    for i in range(26):
        if data[i][b][c][d]:
            adj.add(nums_to_word([i,b,c,d]))
        if data[a][i][c][d]:
            adj.add(nums_to_word([a,i,c,d]))
        if data[a][b][i][d]:
            adj.add(nums_to_word([a,b,i,d]))
        if data[a][b][c][i]:
            adj.add(nums_to_word([a,b,c,i]))
    adj.remove(word)
    return adj

def find_between(word_a, word_b):
    return find_adj(word_a) & find_adj(word_b)

def rand_path_from(word, length=7):
    path = [word]
    from_word = word
    for _ in range(length-1):
        next = find_adj(from_word)
        from_word = random.choice(list(next))
        path.append(from_word)
    return path


def find_path_between(start_word, end_word, length=7):
    """
    Bidirectional search algorithm to find a path between two words.

    Args:
        start_word (str): Starting word.
        end_word (str): Ending word.
        length (int, optional): Maximum length of the path. Defaults to 7.

    Returns:
        list: A list of words representing the path from start_word to end_word.
    """
    # Initialize forward and backward search queues
    forward_queue = [(start_word, [start_word])]
    backward_queue = [(end_word, [end_word])]

    # Initialize forward and backward search sets
    forward_visited = set([start_word])
    backward_visited = set([end_word])

    # Initialize forward and backward search dictionaries
    forward_paths = {start_word: [start_word]}
    backward_paths = {end_word: [end_word]}

    # Perform bidirectional search
    while forward_queue and backward_queue:
        # Forward search
        word, path = forward_queue.pop(0)
        if len(path) > length:
            break
        for adj in find_adj(word):
            if adj not in forward_visited:
                forward_queue.append((adj, path + [adj]))
                forward_visited.add(adj)
                forward_paths[adj] = path + [adj]
                if adj in backward_visited:
                    # Found a common word, construct the path
                    common_word = adj
                    forward_path = forward_paths[common_word]
                    backward_path = backward_paths[common_word][::-1]
                    return forward_path + backward_path[1:]

        # Backward search
        word, path = backward_queue.pop(0)
        if len(path) > length:
            break
        for adj in find_adj(word):
            if adj not in backward_visited:
                backward_queue.append((adj, path + [adj]))
                backward_visited.add(adj)
                backward_paths[adj] = path + [adj]
                if adj in forward_visited:
                    # Found a common word, construct the path
                    common_word = adj
                    forward_path = forward_paths[common_word]
                    backward_path = backward_paths[common_word][::-1]
                    return forward_path + backward_path[1:]

    # No path found
    return None


def lengthen_path_to(path, length):
    if path == None or path == []:
        return None
    new_path = [word for word in path]
    while len(new_path) < length:
        insertion_index = random.randint(1,len(path)-1)
        before_set = find_adj(path[insertion_index-1])
        after_set = find_adj(path[insertion_index])
        if len(before_set & after_set) > 0:
            new_path.insert(insertion_index, random.choice(list(before_set & after_set)))
    return new_path

def find_path_of_length_between(start, end, length=7):
    path = find_path_between(start, end, length)
    longer = lengthen_path_to(path, length)
    return longer

print(rand_path_from("bare", 4)) # fun fact: bare is most connected 4-letter word (has the most neighbors)
print(find_path_of_length_between("code", "bugs", 7)) # there are many ways that code and bugs are related