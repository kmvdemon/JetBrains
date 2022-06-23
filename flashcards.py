import json
import random
import io
import argparse


class Card:

    library = []
    export_lib = False

    def __init__(self, term, definition):
        self.term = term
        self.definition = definition


class ExistanseError(Exception):
    pass


def menu():
    while True:
        log_print("Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):")
        user_input = log_input()
        if user_input == "add":
            create_card()
        elif user_input == "remove":
            remove_card()
        elif user_input == "import":
            import_cards()
        elif user_input == "export":
            export_cards()
        elif user_input == "ask":
            question()
        elif user_input == "exit":
            if Card.export_lib is False:
                log_print("bye bye")
                log_file.close()
            else:
                uploader(pars.export_to)
                log_print("bye bye")
                log_file.close()
            break
        elif user_input == "log":
            save_log()
        elif user_input == "hardest card":
            hardest_card()
        elif user_input == "reset stats":
            reset_stats()
            log_print("Card statistics have been reset.")
        elif user_input == "lib":
            print(Card.library)


def reset_stats():
    for item in Card.library:
        item[2] = 0

def hardest_card():
    mistakes = [x[2] for x in Card.library if x[2] != 0]
    if not mistakes:
        log_print("There are no cards with errors.")
    else:
        hardest = []
        mistakes_made = []
        hardest_value = max(mistakes)
        for term_index in range(len(Card.library)):
            if Card.library[term_index][2] == hardest_value:
                hardest.append(Card.library[term_index][0])
                mistakes_made.append(Card.library[term_index][2])

        if len(hardest) == 1:
            log_print(f'The hardest card is "{hardest[0]}". You have {mistakes_made[0]} errors answering it.')
        elif len(hardest) == 0:
            log_print("There are no card with errors.")
        else:
            log_print(f'The hardest cards are "{hardest[0]}", "{hardest[1]}". You have {mistakes_made[0]} errors answering them.')


def log_print(message):
    print(message)
    log_file.read()
    log_file.write(message + "\n")


def log_input():
    user_input = input()
    log_file.read()
    log_file.write(user_input + "\n")
    return user_input


def save_log():
    log_print("File name: ")
    file_name = log_input()
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(log_file.getvalue())
    log_print("The log has been saved.")


def remove_card():
    log_print("Which card?")
    card = log_input()
    if card in [x[0] for x in Card.library]:
        del Card.library[[x[0] for x in Card.library].index(card)]
        log_print("The card has been removed")
    else:
        log_print(f"""Can't remove "{card}": there is no such card.""")


def import_cards():
    log_print("File name")
    file_name = log_input()
    try:
        loaded_dict = json.load(open(f"{file_name}"))
        Card.library = updator(Card.library, loaded_dict)
        log_print(f"{len(loaded_dict)} cards have been loaded.")
    except FileNotFoundError:
        log_print("File not found")


# Updates current log(library) from uploaded file
def updator(a, b):
    terms_to_update = [x[0] for x in a]
    existed_term = [x[0] for x in b]
    if a == []:
        a = b
    else:
        for term in terms_to_update:
            if term in existed_term:
                a[terms_to_update.index(term)][1] = b[terms_to_update.index(term)][1]
                a[terms_to_update.index(term)][2] = b[terms_to_update.index(term)][2]
            else:
                a.append(b[terms_to_update.index(term)])
    return a


def export_cards():
    log_print("File name:")
    file_name = log_input()
    with open(file_name, 'w') as outfile:
        json.dump(Card.library, outfile)
    log_print(f"{len(Card.library)} cards have been saved.")


def create_card():

        check = None
        log_print("The card:")
        while check != "pass":
            term = log_input()
            check = check_term("term", term)

        check = None
        log_print("The definition of the card:")
        while check != "pass":
            definition = log_input()
            check = check_term("definition", definition)

        Card.library.append([term, definition, 0])
        log_print(f'The pair ("{term}":"{definition}") has been added.')


def question():
    log_print("How many times to ask?")
    questions_number = int(log_input())
    while questions_number > 0:

        random_index = random.randint(0, len(Card.library)-1)
        term = Card.library[random_index][0]
        definition = Card.library[random_index][1]
        log_print(f'Print the definition of "{term}":')
        answer = log_input()
        questions_number -= 1
        definitions = [x[1] for x in Card.library]
        terms = [x[0] for x in Card.library]
        if answer == definition:
            log_print("Correct!")
        elif answer != definition and answer in definitions:
            term_for_guess = terms[definitions.index(answer)]
            log_print(f'Wrong. The right answer is "{definition}", but your definition'
                      f' is correct for "{term_for_guess}"')
            Card.library[random_index][2] += 1  # adding mistake
        else:
            log_print(f'Wrong. The right answer is "{definition}."')
            Card.library[random_index][2] += 1  # adding mistake



def check_term(item_to_check, content):
    if item_to_check == "term":
        place_to_check = [x[0] for x in Card.library]
        item_to_print = "card"
    else:
        place_to_check = [x[1] for x in Card.library]
        item_to_print = "definitions"

    try:
        if content not in place_to_check:
            return "pass"
        else:
            raise ExistanseError
    except ExistanseError:
        log_print(f'The {item_to_print} "{content}" already exists. Try again:')
        return "not pass"


def start_loader(file_name):
    loaded_dict = json.load(open(f"{file_name}"))
    Card.library = updator(Card.library, loaded_dict)
    log_print(f"{len(loaded_dict)} cards have been loaded.")


def uploader(file_name):
    with open(file_name, 'w') as outfile:
        json.dump(Card.library, outfile)
    log_print(f"{len(Card.library)} cards have been saved.")


log_file = io.StringIO()
parser = argparse.ArgumentParser()
parser.add_argument("--import_from", default=None)
parser.add_argument("--export_to", default=None)
pars = parser.parse_args()
if pars.import_from is not None:
    start_loader(pars.import_from)
if pars.export_to is not None:
    Card.export_lib = True




if __name__ == "__main__":
    menu()
