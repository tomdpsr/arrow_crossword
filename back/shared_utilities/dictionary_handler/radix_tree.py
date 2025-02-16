class RadixNode:
    def __init__(self):
        self.children = {}
        self.is_word = False
        self.word = None

class RadixTree:
    def __init__(self):
        self.root = RadixNode()
        self.forbidden = set()

    def insert(self, word: str) -> None:
        node = self.root
        while word:
            # Find matching prefix
            prefix = None
            for edge in node.children:
                for i in range(min(len(edge), len(word))):
                    if edge[i] != word[i]:
                        break
                    if i == len(edge) - 1:
                        prefix = edge
                        break

            if prefix is None:
                # No matching prefix, create new node
                node.children[word] = RadixNode()
                node = node.children[word]
                node.is_word = True
                node.word = word
                break
            else:
                # Follow existing prefix
                node = node.children[prefix]
                word = word[len(prefix):]

    def contains(self, word: str) -> bool:
        if word in self.forbidden:
            return False

        node = self.root
        while word:
            found = False
            for edge in node.children:
                if word.startswith(edge):
                    node = node.children[edge]
                    word = word[len(edge):]
                    found = True
                    break
            if not found:
                return False
        return node.is_word

    def find_matches(self, pattern: str) -> list[str]:
        matches = []

        def dfs(node: RadixNode, remaining_pattern: str) -> None:
            if not remaining_pattern:
                if node.is_word and node.word not in self.forbidden:
                    matches.append(node.word)
                return

            if remaining_pattern[0] == '.':
                # For wildcard, try all edges
                for edge, child in node.children.items():
                    if len(edge) <= len(remaining_pattern):
                        # Check if the rest of the edge matches the pattern
                        valid = True
                        for i in range(1, len(edge)):
                            if i < len(remaining_pattern) and remaining_pattern[i] != '.' and remaining_pattern[i] != \
                                    edge[i]:
                                valid = False
                                break
                        if valid:
                            dfs(child, remaining_pattern[len(edge):])
            else:
                # For regular character, follow matching edges
                for edge, child in node.children.items():
                    if edge.startswith(remaining_pattern[0]):
                        if len(edge) <= len(remaining_pattern):
                            # Check if the edge matches the pattern
                            valid = True
                            for i in range(len(edge)):
                                if remaining_pattern[i] != '.' and remaining_pattern[i] != edge[i]:
                                    valid = False
                                    break
                            if valid:
                                dfs(child, remaining_pattern[len(edge):])

        dfs(self.root, pattern)
        return matches