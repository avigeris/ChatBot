import dialogue_system
from rules import rules, default_responses



def main():

    rules_list = []
    for pattern, transforms in rules.items():
        pattern = dialogue_system.remove_punct(str(pattern.lower()))
        rules_list.append((pattern, transforms))

    while(True):
        text = input('> ')
        print(dialogue_system.respond(rules_list, text, map(str, default_responses)))

if __name__ == '__main__':
    main()
