def unify(x, y, subs=None):
    if subs is None:
        subs = {}
    if x == y:
        return subs
    if isinstance(x, str) and x.islower():
        subs[x] = y
        return subs
    if isinstance(y, str) and y.islower():
        subs[y] = x
        return subs
    if isinstance(x, tuple) and isinstance(y, tuple) and len(x) == len(y):
        for a, b in zip(x, y):
            result = unify(a, b, subs)
            if result is None:
                return None
            subs = result
        return subs
    return None

# Example 1: unify Likes(x, y) with Likes(Alice, Bob)
a = ("Likes", "x", "y")
b = ("Likes", "Alice", "Bob")
print("Unification result 1:", unify(a, b))  # Output: {'x': 'Alice', 'y': 'Bob'}

# Example 2: unify Knows(John, x) with Knows(y, Mary)
c = ("Knows", "John", "x")
d = ("Knows", "y", "Mary")
print("Unification result 2:", unify(c, d))  # Output: {'y': 'John', 'x': 'Mary'}