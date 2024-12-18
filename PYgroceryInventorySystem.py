#CHING JIA ZHONG
#TP074569



def Write_to_inventorytxt(list_inventory):
    try:
        with open("inventory.txt", "w") as handle:
            for record in list_inventory:
                recordstring = ','.join(str(data) for data in record) #joins all details of an item together with ","
                handle.write(recordstring + "\n") #the next item with its record will be store on next line of the file
    except IOError:
        print("file not found")

def Write_to_userdatatxt(list_user):
    try:
       with open("userdata.txt","w") as handle:
          for record in list_user:
             recordString=",".join(str(data) for data in record)
             handle.write(recordString + "\n")
    except IOError:
        print("file not found")


def AddNewUser(User,reference):
    flag = False
    print("Add New User")

    NewUserName = input("Enter new username: ")
    NewPassword = input("Enter password: ")
    NewUserType = input("Enter user type(admin/inventory-checker/purchaser): ") #assume admin will enter according to choice listed.
    flag = validate_access(NewUserType,reference)
    if flag == False:
        print("access type invalid")
    else:
        UserInfo=[NewUserName,NewPassword,NewUserType] #small list to be insert into master list
        User.append(UserInfo)
        print("New User entered successfully")
        Write_to_userdatatxt(User)



def UserAuthentication(User):#return access type if username and password correct,else return none
    UserName = input("Enter username: ")
    Password = input("Enter password: ")

    for data in User:
       if (data[0] == UserName.strip()) and (data[1] == Password.strip()): #.strip() to remove trailing spaces to ensure data integrity
           return data[2]

    print("Incorrect password or username.")
    return None

def validate_access(AccessM,Mreference):
    found = False
    for data in Mreference:
        if AccessM.lower() == data: #.lower() to lowercase characters to standardise the comparison data
            found = True
            break
    return found

def validate_item_category(Mcategory,Mreference):
    found = False
    for data in Mreference:
        if Mcategory.lower() == data:
            found = True
            break
    return found

def validate_item_unit(units,Mreference):
    found = False
    for data in Mreference:
        if units.lower() == data:
            found = True
            break
    return found

def InsertItem(inventory,reference):
    flag = False #initialising
    found = False
    print("Insert New Item")

    code = input("Please enter item code: ")
    description = input("Please enter item description: ")
    category = input("Please enter item category: ")
    flag = validate_item_category(category,reference) #validate data
    unit = input("Please enter item unit: ")
    found = validate_item_unit(unit,reference)
    price = input("Please enter item price: ")
    quantity = input("Please enter item quantity: ")
    minimum = input("Please enter item minimum threshold: ")

    if found == False:
        print("unit invalid, item not inserted")
    elif flag == False:
        print("category invalid, item not inserted")
    else:
    # small list to be insert into master list inventory
        Item=[code,description,category,unit,float(price),int(quantity),int(minimum)]
        inventory.append(Item)
        print("item inserted")
        Write_to_inventorytxt(inventory)


def UpdateItem(inventory,reference):
    print("Update Item Detail")

    SearchCode=input("Please enter the code of item: ")
    print("Field: code/description/category/unit/price/quantity/minimum")
    Attribute=input("Please enter the field to be change: ")
    NewAttribute=input("Please enter the updated detail: ")
    flag = True
    if Attribute.lower() == "category":
        flag = validate_item_category(NewAttribute, reference)
    elif Attribute.lower() == "unit":
        flag = validate_item_unit(NewAttribute ,reference)

    if flag == False: #to validate data that will stay in the file for a long time without being changed
        print("invalid category or unit entered.")
    else:
        found = False #intialise a flag that indicate details havent been updated
        for record in inventory:
            if SearchCode == record[0]:
                if Attribute.lower() == "code" : #.lower() standardise the letter for compare
                    record[0] = NewAttribute
                    found = True
                    break
                elif Attribute.lower() == "description":
                    record[1] = NewAttribute
                    found = True
                    break
                elif Attribute.lower() == "category":
                    record[2] = NewAttribute
                    found = True
                    break
                elif Attribute.lower() == "unit":
                    record[3] = NewAttribute
                    found = True
                    break
                elif Attribute == "price":
                    record[4] = NewAttribute
                    found = True
                    break
                elif Attribute == "quantity":
                    record[5] = NewAttribute
                    found = True
                    break
                elif Attribute == "minimum":
                    record[6] = NewAttribute
                    found = True
                    break   #when updated in list, break the loop
                else:
                    print("field invalid")
                    break


        if found == True:
            print("Item detail updated successfully")
        else:
            print("item not found")

        Write_to_inventorytxt(inventory)


def DeleteItem(inventory):
    print("Delete Item")

    SearchCode = input("Please input code of item to be removed: ")
    found = False
    for record in inventory:
        if record[0] == SearchCode:
            found = True
            inventory.remove(record) #remove record from inventory list.
            print("Item removed successfully")
            break
    if found == False:
        print("Item not found")
    Write_to_inventorytxt(inventory)

def DeleteUser(User):
    print("Delete User")

    SearchUser = input("Enter user's name to be removed: ")
    found = False
    for record in User:
        if record[0] == SearchUser:
            found = True
            User.remove(record)  #remove user from list
            print("User successfully removed")
            break
    if found == False:
        print("User not found")
    Write_to_userdatatxt(User)

def StockTaking(inventory):#to confirm or change quantity
    print("Stock taking")

    SearchCode = input("Please enter the code of item: ")
    found = False
    for record in inventory:
        if record[0] == SearchCode:
            found = True
            print("Item found")
            print("Quantity available: ", record[5])
            NewQuantity = input("Please enter new quantity(Press enter if want to keep the same): ")
            if NewQuantity != '': #if user press enter ,quantity no change
                record[5]=NewQuantity
            print("Stock-taking successful.")
            Write_to_inventorytxt(inventory)
    if found == False:
        print("Item not found.")

def View_replenish_list(inventory):
    replenish_list = [] #a list for item to be replenished
    for record in inventory:
        if int(record[5]) < int(record[6]): #quantity less than minimum threshold
            replenish_list.append(record)

    if replenish_list:
        print("Item for replenish:")
        print("----------------------")
        for record in replenish_list:
            print("Code: ", record[0])
            print("Description: ", record[1])
            print("Quantity: ", record[5])
            print("Minimum threshold: ", record[6])
            print("------------------------")
    else:
        print("No item need to be replenished.")

def Stock_replenishment(inventory): #add quantity to replenish item
    print("Stock replenishment")

    SearchCode = input("Please enter code of item: ")
    AddQuantity = int(input("Please enter the quantity to be added: "))
    found = False
    for record in inventory:
        if record[0] == SearchCode:
            found = True
            print("Quantity before replenishment: ", record[5])
            record[5] = int(record[5]) + AddQuantity  #record[5]=record[5]+AddQuantity
            print("Updated quantity: ", record[5])
            Write_to_inventorytxt(inventory)
            break
    if found == False:
        print("Item not found")

def SearchItems(inventory):
    print("Search Item")
    #let user make choices on method of search
    print("   1. Search item by description")
    print("   2. Search item by code range")
    print("   3. Search item in a specific category")
    print("   4. Search item in a specific price range")
    choice = input("Please enter choice of search method: ")
    ItemFound = False  #initialise a flag that indicate item havent found

    if choice == "1":
        description = input("Enter item description: ")
        for record in inventory:
            if record[1].lower() == description.lower():
                print(str(record) +"\n") #need to convert recordwhich is a list to string to join with other string which is "\n"
                ItemFound = True #flag become true when found
    elif choice == "2":
        min_code = int(input("Enter minimum code: "))#convert to int because need search between 2 numbers
        max_code = int(input("Enter maximum code: "))
        for record in inventory:
            if (int(record[0]) >= min_code) and (int(record[0]) <= max_code):
                print(str(record) + "\n")
                ItemFound = True
    elif choice == "3":
        category = input("Enter item category: ")
        for record in inventory:
            if record[2].lower() == category.lower():
                print(str(record) + "\n")
                ItemFound = True
    elif choice == "4":
        min_price = float(input("Enter minimum price: "))
        max_price = float(input("Enter maximum price: "))
        for record in inventory:
            if (record[4] >= min_price) and (record[4] <= max_price):
                print(str(record) + "\n")
                ItemFound = True
    else: #if user enter number outside of choice available
        print("Invalid search option")

    if ItemFound == True:
        print("Item Found.")
    else:
        print("No items found.")

def Load_inventory(InventoryList): #to load data from their respective files to their respective lists
    try:
        with open("inventory.txt","r") as handle:
            for row in handle.readlines():
                detail = row.strip().split(",")
                item = [detail[0], detail[1], detail[2], detail[3], float(detail[4]), int(detail[5]), int(detail[6])]
                InventoryList.append(item) #store detail list to item list to manipulate the data type of price, quantity and minimum
    except IOError:
        print("inventory file not found")

def Load_userdata(UserList):
    try:
        with open("userdata.txt","r") as handle:
            for row in handle.readlines():
                detail = row.strip().split(",")
                UserList.append(detail)
    except IOError:
        print("userdata file not found")

def Load_reference(referenceList): #load data from the category, unit and access type reference files
    try:
        with open("CategoryRef.txt","r") as handle:
            for row in handle.readlines():
                referenceList.append(row.strip())
    except IOError:
        print("category reference file not found")

    try:
        with open("UnitRef.txt","r") as handleString:
            for line in handleString.readlines():
                referenceList.append(line.strip())
    except IOError:
        print("unit reference file not found")

    try:
        with open("AccessRef.txt","r") as destFile:
            for record in destFile.readlines():
                referenceList.append(record.strip())
    except IOError:
        print("access reference file not found")

def main_menu(AccessType,InventoryList,UserList,ReferenceList): #to display the tasks available for user based on access type
    while True:
       if AccessType == "admin":  #admin menu
           print("Welcome admin")
           print("   1. Add new user")
           print("   2. Insert new item")
           print("   3. Update item details")
           print("   4. Delete item")
           print("   5. Perform stock-taking")
           print("   6. View replenish list")
           print("   7. Perform stock replenishment")
           print("   8. Search item")
           print("   9. Delete user")
           choice = input("Enter choice: ")
           if choice == "1":
               AddNewUser(UserList,ReferenceList)
           elif choice == "2":
               InsertItem(InventoryList,ReferenceList)
           elif choice == "3":
               UpdateItem(InventoryList,ReferenceList)
           elif choice == "4":
               DeleteItem(InventoryList)
           elif choice == "5":
               StockTaking(InventoryList)
           elif choice == "6":
               View_replenish_list(InventoryList)
           elif choice == "7":
               Stock_replenishment(InventoryList)
           elif choice == "8":
               SearchItems(InventoryList)
           elif choice == "9":
               DeleteUser(UserList)
           else:
               print("invalid entry")

       elif AccessType == "inventory-checker": #inventory-checker menu
           print("Welcome inventory-checker")
           print("   1. Perform stock-taking")
           print("   2. Search for items")
           choice = input("Enter choice: ")
           if choice == "1":
               StockTaking(InventoryList)
           elif choice == "2":
               SearchItems(InventoryList)
           else:
               print("invalid entry")

       elif AccessType == "purchaser":   #purchaser menu
           print("Welcome purchaser!")
           print("   1. View replenish list")
           print("   2. Perform stock replenishment")
           print("   3. To search for items")
           choice = input("Enter choice: ")
           if choice == "1":
               View_replenish_list(InventoryList)
           elif choice == "2":
               Stock_replenishment(InventoryList)
           elif choice == "3":
               SearchItems(InventoryList)
           else:
               print("invalid entry")

       else:
           print("invalid user type.")

       print("Do you want to continue?")  #ask if user wants to continue or not
       option = input("Press any key to continue//Press N to log out: ")
       if option == "N":
           break  #logout

    print("logged out successfully")

def run_system():
    MasterReference = [] #inititisliased to empty
    MasterInventory = []
    UsersData = []
    Load_reference(MasterReference)
    Load_inventory(MasterInventory) #loaded data from their respective files
    Load_userdata(UsersData)
    access = None#initialise access to nothing

    while access == None:#function keep being called if user and its access is not found
        access = UserAuthentication(UsersData)

    print("Welcome to Grocery Store Inventory System!")
    main_menu(access,MasterInventory,UsersData,MasterReference)

run_system()  #run the function that run the inventory system.