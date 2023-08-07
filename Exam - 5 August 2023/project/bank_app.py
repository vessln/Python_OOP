from project.clients.adult import Adult
from project.clients.student import Student
from project.loans.mortgage_loan import MortgageLoan
from project.loans.student_loan import StudentLoan


class BankApp:
    VALID_LOANS = {"StudentLoan": StudentLoan,
                   "MortgageLoan": MortgageLoan}

    VALID_CLIENTS = {"Student": Student, "Adult": Adult}

    def __init__(self, capacity):
        self.capacity = capacity
        self.loans = []
        self.clients = []

    def find_client_by_id(self, cl_id):
        return [c for c in self.clients if c.client_id == cl_id]

    def find_loan_by_type(self, l_type):
        return [loan for loan in self.loans if type(loan).__name__ == l_type]

    def add_loan(self, loan_type):
        if loan_type not in BankApp.VALID_LOANS.keys():
            raise Exception("Invalid loan type!")

        new_loan = BankApp.VALID_LOANS[loan_type]()
        self.loans.append(new_loan)
        return f"{loan_type} was successfully added."

    def add_client(self, client_type, client_name, client_id, income):
        if client_type not in BankApp.VALID_CLIENTS.keys():
            raise Exception("Invalid client type!")

        if len(self.clients) >= self.capacity:
            return "Not enough bank capacity."

        new_client = BankApp.VALID_CLIENTS[client_type](client_name, client_id, income)
        self.clients.append(new_client)
        return f"{client_type} was successfully added."

    def grant_loan(self, loan_type, client_id):
        client = self.find_client_by_id(client_id)[0]

        if type(client).__name__ == "Student" and loan_type != "StudentLoan":
            raise Exception("Inappropriate loan type!")

        if type(client).__name__ == "Adult" and loan_type != "MortgageLoan":
            raise Exception("Inappropriate loan type!")

        current_loan = self.find_loan_by_type(loan_type)[0]
        self.loans.remove(current_loan)
        client.loans.append(current_loan)
        return f"Successfully granted {loan_type} to {client.name} with ID {client.client_id}."

    def remove_client(self, client_id):
        if not self.find_client_by_id(client_id):
            raise Exception("No such client!")

        client = self.find_client_by_id(client_id)[0]
        if len(client.loans) > 0:
            raise Exception("The client has loans! Removal is impossible!")
        else:
            self.clients.remove(client)
            return f"Successfully removed {client.name} with ID {client.client_id}."

    def increase_loan_interest(self, loan_type):
        changed_loans = 0
        current_loans = self.find_loan_by_type(loan_type)
        for loan in current_loans:
            loan.increase_interest_rate()
            changed_loans += 1

        return f"Successfully changed {changed_loans} loans."

    def increase_clients_interest(self, min_rate):
        changed_rates = 0
        for client in self.clients:
            if client.interest < min_rate:
                client.increase_clients_interest()
                changed_rates += 1

        return f"Number of clients affected: {changed_rates}."

    def get_statistics(self):
        result = [f"Active Clients: {len(self.clients)}"]
        avg_rate = 0
        total_income = 0
        granted_loans_count = 0
        granted_sum = 0
        for client in self.clients:
            total_income += client.income
            granted_loans_count += len(client.loans)
            granted_sum += client.sum_of_all_loans()
            avg_rate += client.interest

        try:
            avg_client_rate = avg_rate / len(self.clients)
        except ZeroDivisionError:
            avg_client_rate = 0

        result.append(f"Total Income: {total_income:.2f}")
        result.append(f"Granted Loans: {granted_loans_count}, Total Sum: {granted_sum:.2f}")

        sum_loans = 0
        for loan in self.loans:
            sum_loans += loan.amount

        result.append(f"Available Loans: {len(self.loans)}, Total Sum: {sum_loans:.2f}")

        result.append(f"Average Client Interest Rate: {avg_client_rate:.2f}")

        return '\n'.join(result)


bank = BankApp(3)

print(bank.add_loan('StudentLoan'))
print(bank.add_loan('MortgageLoan'))
print(bank.add_loan('StudentLoan'))
print(bank.add_loan('MortgageLoan'))


print(bank.add_client('Student', 'Peter Simmons', '1234567891', 500))
print(bank.add_client('Adult', 'Samantha Peters', '1234567000', 1000))
print(bank.add_client('Student', 'Simon Mann', '1234567999', 700))
print(bank.add_client('Student', 'Tammy Smith', '1234567555', 700))

print(bank.grant_loan('StudentLoan', '1234567891'))
print(bank.grant_loan('MortgageLoan', '1234567000'))
print(bank.grant_loan('MortgageLoan', '1234567000'))

print(bank.remove_client('1234567999'))

print(bank.increase_loan_interest('StudentLoan'))
print(bank.increase_loan_interest('MortgageLoan'))

print(bank.increase_clients_interest(1.2))
print(bank.increase_clients_interest(3.5))

print(bank.get_statistics())
