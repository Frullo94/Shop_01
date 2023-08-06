import json

class Product:
    def __init__(self, name, quantity, selling_price, buying_price):
        self.name = name
        self.quantity = quantity
        self.selling_price = selling_price
        self.buying_price = buying_price
    
    def to_dict(self):
        return {
            "name": self.name,
            "quantity": self.quantity,
            "selling_price": self.selling_price,
            "buying_price": self.buying_price
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["quantity"], data["selling_price"], data["buying_price"])

class Shop:
    def __init__(self):
        self.products = {}

    def add_product(self, name, quantity, selling_price, buying_price):
        if name in self.products:
            self.products[name].quantity += quantity
        else:
            self.products[name] = Product(name, quantity, selling_price, buying_price)

    def list_products(self):
        for product in self.products.values():
            print(f"Name: {product.name}, Quantity: {product.quantity}, Selling Price: {product.selling_price}, Buying Price: {product.buying_price}")

    def record_sell(self, name, quantity):
        if name in self.products and self.products[name].quantity >= quantity:
            self.products[name].quantity -= quantity
        else:
            raise Exception("Quantity higher thann availability")
        
    def profits(self):
        gross_profit = sum(product.selling_price * product.quantity for product in self.products.values())
        total_costs = sum(product.buying_price * product.quantity for product in self.products.values())
        net_profit = gross_profit - total_costs
        return gross_profit, net_profit
    
    def help_command(self):
        print("List of commands:")
        print("1. add product: add_product(name, quatity, selling_price, buying_price)")
        print("2. list product: list_products()")
        print("3. record sell: record_sell(name, quantity)")
        print("4. show profits: profits")
    
    def save_data(self, filename="data.json"):
        try:
            with open(filename, 'w') as f:
                data = {name: product.to_dict() for name, product in self.products.items()}
                json.dump(data, f)
        except FileNotFoundError:
            pass
    
    def load_data(self, filename="data.json"):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                self.products = {name: Product.from_dict(product_data) for name, product_data in data.items()}
        except FileExistsError:
            pass

def main():
    shop = Shop()
    shop.load_data()
    while True:
        try:
            command = input("digit a command (digit help to see the commands available)")
            if command == "help":
                    shop.help_command()
            elif command == "add_product":
                    name = input("write the name of the product: ")
                    quantity = int(input("Write the quantity of the product: "))
                    selling_price = float(input("Write the selling price: "))
                    buying_price = float(input("Write the buying price: "))
                    shop.add_product(name, quantity, selling_price, buying_price)
            elif command == "list_products":
                    shop.list_products()
            elif command == "record_sell":
                    name = input("Write the name of the product sold: ")
                    quantity = int(input("Write the quantity sold: "))
                    shop.record_sell(name, quantity)
            elif command == "profits":
                    gross_profit, net_profit = shop.profits()
                    print(f"Gross profit: {gross_profit}, Net profit: {net_profit}")
            elif command == "close":
                    print("Bye bye")
                    break
            else:
                    print("command not found")
                
            shop.save_data()

        except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    main()


