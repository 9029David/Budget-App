# ---------------- Aplicacion Presupuesto ---------------- # 
class Category:
    def __init__ (self, category):
        self.category = category
        self.ledger = []
    # Formato de salida
    def __str__(self):
        ticket = f"{self.category:*^30}\n"
        for gasto in self.ledger:
            amount = f"{gasto['amount']:.2f}"
            description = gasto['description'][:23]
            ticket += f"{description:<23}{amount:>7}\n"
        ticket += f"Total:{self.get_balance():>7.2f}"  
        return ticket
    # Formato de diccionario
    def _aux(self, amount, description = ''):
        return  {'amount': float(amount), 'description': description}
    # Deposito
    def deposit (self, amount, description = ''):
        if amount <= 0:
            return False
        self.ledger.append(self._aux(amount, description = description)) 
        return True
    # Retiro     
    def withdraw (self, amount, description = ''):
        if not self.check_funds(amount):
            return False
        self.ledger.append(self._aux(amount * (-1), description = description)) 
        return True
    # Total
    def get_balance (self):
        return sum(item['amount'] for item in self.ledger)
    # Chequeo de fondos
    def check_funds (self, amount):
        return amount <= self.get_balance()
    # Transferencia  
    def transfer (self, amount, category):
        if not self.check_funds(amount):
            return False
        self.withdraw(amount, f'Transfer to {category.category}')
        category.deposit(amount,f'Transfer from {self.category}')
        return True
    # Total de retiros
    def  get_withdrawals(self):
        return sum(-item['amount'] for item in self.ledger if item['amount'] < 0)

# ---------------- main ---------------- # 

def create_spend_chart(categories):
    total_withdrawals = sum(cat.get_withdrawals() for cat in categories)
    percentages = [(cat.get_withdrawals() / total_withdrawals) * 100 for cat in categories]

    chart = "Percentage spent by category\n"
    for i in range(100, -10, -10):
        chart += f"{i:>3}|"
        for percentage in percentages:
            if percentage >= i:
                chart += " o "
            else:
                chart += "   "
        chart += " \n"

    chart += "    " + "-" * (3 * len(categories) + 1) + "\n"
    
    max_length = max(len(cat.category) for cat in categories)
    for i in range(max_length):
        chart += "    "
        for cat in categories:
            if len(cat.category) > i:
                chart += f" {cat.category[i]} "
            else:
                chart += "   "
        chart += " \n"

    return chart.rstrip("\n")

# Prueba de la clase y la función de gráficos
food = Category('Food')
food.deposit(1000, 'Initial deposit')
food.withdraw(10.15, 'groceries')
food.withdraw(15.89, 'restaurant and more food for dessert')
print(food)

clothing = Category('Clothing')
food.transfer(50, clothing)
clothing.withdraw(25.55)
print(clothing)

auto = Category('Auto')
auto.deposit(1000, 'Initial deposit')
auto.withdraw(15)
print(auto)

categories = [food, clothing, auto]
print(create_spend_chart(categories))