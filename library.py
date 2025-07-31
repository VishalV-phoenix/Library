from pymongo import MongoClient

opt = 0
ext = ""
g = ""

client = MongoClient("mongodb://localhost:27017/")
db = client["Library"]

print('Welcome to the library')

def usernames():
    global username
    username = input("Enter your Username: ")
    existing_user = db.users.find_one({"username": username})
    if existing_user:
        print(f"User '{username}' already exists.")
    else:
        db.users.insert_one({"username": username})
        print(f"User '{username}' has been registered.")

usernames()

def book_list():
    for index, book in enumerate(db.books.find({"present": True}), start=1):
        print(f"{index}: {book['name']}")

def menu():
    global opt
    print(f'\nHow can I help you, {username}?')
    print('1 = List of available books\n2 = Borrow\n3 = Return\n4 = Exit')
    opt = int(input('Enter 1/2/3/4: \n'))

menu()

def borrow():
    global ext
    print('Which book would you like to borrow?')
    search = input('Enter your book name: ')
    found_book = db.books.find_one({"name": search, "present": True})
    if found_book:
        print(f"{search} has been added to your cart.")
        db.books.update_one({"name": search}, {"$set": {"present": False}})
        db.users.update_one(
            {"username": username},
            {"$addToSet": {"cart": search}}
        )
    else:
        print(f"{search} is not available or does not exist.")
    ext = input('Would you like to add another book to your cart? (y/q): ')

def book_return():
    global g
    user = db.users.find_one({"username": username})
    cart = user.get("cart", [])

    if not cart:
        print("Your cart is empty.")
        

    print("Books in your cart:")
    for index, book in enumerate(cart, start=1):
        print(f"{index}. {book}")

    give = input("Enter the name of the book you want to return: ")

    if give in cart:
        db.books.update_one({"name": give}, {"$set": {"present": True}})
        db.users.update_one(
            {"username": username},
            {"$pull": {"cart": give}}
        )
        print(f"'{give}' has been returned.")
    else:
        print(f"'{give}' is not in your cart.")

    g = input("Do you want to return any other book? (y/q): ")
    print("Thank you.")

# Main loop
while True:
    if opt == 1:
        book_list()
        menu()

    elif opt == 2:
        ext = ""
        while ext != 'q':
            borrow()
        menu()

    elif opt == 3:
        g = ""
        while g != 'q':
            book_return()
        menu()

    elif opt == 4:
        print("Come back again!\nThank You!")
        break

    else:
        print("Invalid option.")
        menu()
