import random
import string

def respond(rules, input, default_responses):

    input = input.split()  # match_pattern expects a list of tokens

    # Look through rules and find input patterns that matches the input.
    matching_rules = []
    for pattern, transforms in rules:
        pattern = pattern.split()
        replacements = match_pattern(pattern, input)
        if replacements:
            matching_rules.append((transforms, replacements))

    # When rules are found, choose one and one of its responses at random.
    # If no rule applies, we use the default rule.
    if matching_rules:
        responses, replacements = random.choice(matching_rules)
        response = random.choice(responses)
    else:
        replacements = {}
        response = random.choice(list(default_responses))

    # Replace the variables in the output pattern with the values matched from
    # the input string.
    for variable, replacement in replacements.items():
        replacement = ' '.join(change_pronouns(replacement))
        if replacement:
            response = response.replace('?' + variable, replacement)

    return response

def match_pattern(pattern, input, bindings=None):

    # Check to see if matching failed before we got here.
    if bindings is False:
        return False

    # When the pattern and the input are identical, we have a match, and
    # no more bindings need to be found.
    if pattern == input:
        return bindings

    bindings = bindings or {}

    # Match input and pattern according to their types.
    if is_variable(pattern):
        token = pattern[0]  # segment variable is the first token
        var = token[2:]  # segment variable is of the form ?*x
        return match_segment(var, pattern[1:], input, bindings)
    elif contains_tokens(pattern) and contains_tokens(input):
        # Recurse:
        # try to match the first tokens of both pattern and input.  The bindings
        # that result are used to match the remainder of both lists.
        return match_pattern(pattern[1:],
                             input[1:],
                             match_pattern(pattern[0], input[0], bindings))
    else:
        return False

def match_segment(var, pattern, input, bindings, start=0):

    if not pattern:
        return match_variable(var, input, bindings)

    word = pattern[0]
    try:
        pos = start + input[start:].index(word)
    except ValueError:
        return False

    var_match = match_variable(var, input[:pos], dict(bindings))
    match = match_pattern(pattern, input[pos:], var_match)

    if not match:
        return match_segment(var, pattern, input, bindings, start + 1)

    return match

def match_variable(var, replacement, bindings):
    binding = bindings.get(var)
    if not binding:
        bindings.update({var: replacement})
        return bindings
    if replacement == bindings[var]:
        return bindings
    return False

def contains_tokens(pattern):
    return type(pattern) is list and len(pattern) > 0

def is_variable(pattern):
    return (type(pattern) is list
            and pattern
            and len(pattern[0]) > 2
            and pattern[0][0] == '?'
            and pattern[0][1] == '*'
            and pattern[0][2] in string.ascii_letters
            and ' ' not in pattern[0])

def change_pronouns(words):
    replacements = {'i': 'you', 'you': 'i', 'me': 'you', 'my': 'your', 'am': 'are', 'are': 'am'}
    return [replacements.get(word) if replacements.get(word) else word  for word in words]

def remove_punct(string):
    if string[-1] == '?':
        string = string[:-1]
    return (string.replace(',', '').replace('.', '').replace(';', '').replace('!', ''))