#This is our laptop shop Prepared by;
            #FA23-BSE-077  (Shiraz kamran)
            #FA23-BSE-092  (Asad ali shah)
            #FA23-BSE-120  (Rai Sardar)


#working of our program:

    # 1) role is entered
        # 1.1) if role is admin
            # 1.1.1) admin panel is displayed
                # 1.1.1.1) admin can add, remove laptops and exit the panel
        # 1.2) if role is user
            # 1.2.1) available laptops are displayed
            # 1.2.2) user can order laptop.

#other details:
    #\033 is an escape character, it helps in printing colourful text in terminal.(It uses ANSI codes)


#Module to hide password in terminal while entering.
import getpass

#Available laptops stored in a dictionary
laptops = [
    {"index": 1, "Model": "HP OMEN 14", "RAM": "8GB", "SSD": "256GB", "Generation": "i5", "Price": 100000},
    {"index": 2, "Model": "HP Pavillion 14", "RAM": "16GB", "SSD": "512GB", "Generation": "i7", "Price": 140000},
    {"index": 3, "Model": "Acer Nitro 2", "RAM": "64GB", "SSD": "2TB", "Generation": "i9", "Price": 240000},
    {"index": 4, "Model": "Lenovo Thinkbook", "RAM": "4GB", "SSD": "128GB", "Generation": "i3", "Price": 60000},
    {"index": 5, "Model": "Dell Precision 15", "RAM": "32GB", "SSD": "512GB", "Generation": "i9", "Price": 150000},
    {"index": 6, "Model": "Chromebook series 2", "RAM": "4GB", "SSD": "256GB", "Generation": "i5", "Price": 80000},
    {"index": 7, "Model": "Toshiba Gamingpad 2", "RAM": "16GB", "SSD": "1TB", "Generation": "i7", "Price": 120000},
]

#Admin credentials are hard coded
admin_user = "admin"
admin_pass = "mshk"

#displaying available laptops
def display_laptops():
    print()
    print("We have the following Laptops:")
    print()
    print("Index | Model                 | RAM  | SSD   | Gen   | Price")
    print("------------------------------------------------------------------------")
    for laptop in laptops:
        print(f"{laptop['index']:5} | {laptop['Model']:<21} | {laptop['RAM']:<4} | {laptop['SSD']:<5} | {laptop['Generation']:<5} | RS-/ {laptop['Price']} Only")
    print()


                            #actions that only admin can do
#admin panel function
def admin_panel():
    while True:
        print()
        print("\n\033[1;33m>>>Admin Panel<<<:\033[0m")
        print("1. \033[1;34mAdd Laptop\033[0m")
        print("2. \033[1;31mRemove Laptop\033[0m")
        print("3. \033[1;37mExit\033[0m")
        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            Model = input("Enter the Model: ")
            RAM = input("Enter the RAM: ")
            SSD = input("Enter the SSD: ")
            Generation = input("Enter the Generation: ")
            Price = int(input("Enter the Price: "))
            index = len(laptops) + 1
            laptops.append({"index": index, "Model": Model, "RAM": RAM, "SSD": SSD, "Generation": Generation, "Price": Price})
            print()
            print("\033[1;32mLaptop added successfully!\033[0m")

        elif choice == "2":
            display_laptops()
            laptop_remove = int(input("Enter the index of the laptop to remove:"))
            laptops[:] = [laptop for laptop in laptops if laptop["index"] != laptop_remove]
            print("\033[1;31mLaptop removed successfully!\033[0m")

        elif choice == "3":
            break

        else:
            print("\033[1;31mInvalid choice. Please enter a valid option.\033[0m")


                            #actions that only the user can do
            
#displaying available laptops
def user_menu():
    display_laptops()
    order = int(input("Type index of laptop you want to purchase(0:exit) :"))
    if order == 0:
        return

    #Ordering laptops
    laptop_ordeer = next((laptop for laptop in laptops if laptop["index"] == order), None)

    if laptop_ordeer:
        print()
        print("\033[1;35mOrder Details:\033[0m")
        print()
        print("Model      :", laptop_ordeer["Model"])
        print("RAM        :", laptop_ordeer["RAM"])
        print("SSD        :", laptop_ordeer["SSD"])
        print("Generation :", laptop_ordeer["Generation"])
        print("Price      : RS-/", laptop_ordeer["Price"])
        print()
        print("\033[1;32mThank you for your order!\033")
        print()
        print("\033[1;33mPlease Visit the shop again!")

    else:
        print("\033[1;31mInvalid index. Kindly enter a valid index.\033[0m")

#Main console; which verifies and runs the other functions
print("\n\033[1;32mWelcome to Shiraz, Sardar and Asad Laptop Shop!\033[0m")
while True:
    print()
    print()
    role = input("Please enter your role (\033[1;32madmin\033[0m/\033[1;34muser\033[0m):")

    if role.lower() == "admin":
        username = input("Enter your username: ")
        password = getpass.getpass("Enter password: ")
        while username != admin_user and password != admin_pass:
            username = input("Wrong credentials, Enter admin username again: ")
            password = getpass.getpass("Wrong credentials, Enter admin password again: ")

        if username == admin_user and password == admin_pass:
            admin_panel()
        else:
            print("\033[1;31mInvalid credentials. Please try again.\033[0m")

    elif role.lower() == "user":
        user_menu()

    else:
        print("\033[1;31mInvalid role. Please enter 'admin' or 'user'.\033[0m")
    print()