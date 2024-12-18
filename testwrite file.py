inventory=[]
item = []
code = input("Please enter item code: ")
description = input("Please enter item description: ")
category = input("Please enter item category: ")
unit = input("Please enter item unit: ")
price = input("Please enter item price: ")
quantity = input("Please enter item quantity: ")
minimum = input("Please enter item minimum threshold: ")

item = [code, description, category, unit, price, int(quantity), int(minimum)]
inventory.append(item)
try:
   with open("testingwrite.txt", "a") as handle:
       for record in inventory:
           recordstring = '\t'.join(f'{str(item):<10}' for item in record)
           handle.write(recordstring + '\n')
except IOError:
    print("file not found")

