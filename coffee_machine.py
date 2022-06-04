import sys

class CoffeeMachine():


    def __init__(self):

        self.machine_status = {'cash': 550, 'water': 400, 'beans': 120, 'milk': 540, 'cups': 9}
        self.espresso = {'cost': 4, 'water': 250, 'milk': 0, 'beans': 16}
        self.latte = {'cost': 7, 'water': 350, 'milk': 75, 'beans': 20}
        self.cappuccino = {'cost': 6, 'water': 200, 'milk': 100, 'beans': 12}

    def choose_function(self):

        print("Write action (buy, fill, take, remaining, exit):")
        choise = input()
        if choise == "buy":
            self.buy_coffee()
        elif choise == "fill":
            self.fill_machine()
        elif choise == "take":
            self.money_extraction()
        elif choise == "remaining":
            self.print_status()
        elif choise == "exit":
            sys.exit()


    def buy_coffee(self):
        print("What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:")
        choise = input()
        name = None
        if choise == "1":
            name = self.espresso
        elif choise == "2":
            name = self.latte
        elif choise == "3":
            name = self.cappuccino
        elif choise == "back":
            return

        if name['water'] <= self.machine_status['water'] and \
        name['milk'] <= self.machine_status['milk'] and \
        name['beans'] <= self.machine_status['beans']:
                self.machine_status['water'] -= name['water']
                self.machine_status['milk'] -= name['milk']
                self.machine_status['beans'] -= name['beans']
                self.machine_status['cash'] += name['cost']
                self.machine_status['cups'] -= 1
                print("I have enough resources, making you a coffee!")
        else:
            water = self.machine_status['water'] - name['water']
            milk = self.machine_status['milk'] - name['milk']
            beans = self.machine_status['beans'] - name['beans']
            cups = self.machine_status['cups'] - 1
            ingridients = {water: 'water', milk: 'milk', beans: 'coffee beans', cups: 'cups'}
            for ingridient in ingridients:
                if ingridient < 0:
                    print("Sorry, not enough " + ingridients[ingridient] + "!")


    def fill_machine(self):
        print("Write how many ml of water you want to add:")
        water = input()
        print("Write how many ml of milk you want to add:")
        milk = input()
        print("Write how many grams of coffee beans you want to add:")
        beans = input()
        print("Write how many disposable cups you want to add:")
        cups = input()
        self.machine_status['water'] += int(water)
        self.machine_status['milk'] += int(milk)
        self.machine_status['beans'] += int(beans)
        self.machine_status['cups'] += int(cups)



    def money_extraction(self):
        print(f"I gave you ${self.machine_status['cash']}")
        self.machine_status['cash'] = 0



    def print_status(self):
        status = self.machine_status
        print("The coffee machine has:")
        print(f"{status['water']} ml of water")
        print(f"{status['milk']} ml of milk")
        print(f"{status['beans']} g of coffee beans")
        print(f"{status['cups']} disposable cups")
        print(f"${status['cash']} of money")
        print()



def main():

    coffee_machine = CoffeeMachine()
    while True:
        coffee_machine.choose_function()


if __name__ == '__main__':
    main()


