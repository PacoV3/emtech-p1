def find_user(username, users):
    '''Function to find the user by username inside the list of all users'''
    for id, user in enumerate(users):
        if username == user['username']:
            return id
    return -1


def check_password(password, users, user_id):
    '''Function to check the correct password of an specific user'''
    return password == users[user_id]['password']


def login(users):
    '''Function run the entire login process'''
    # Take the first input
    username = input('Ingrese su nombre de usuario: ')
    user_id = find_user(username, users)
    # Check for different users if the first one is not found
    while user_id == -1:
        username = input(
            'Usuario no encontrado o no valido. Intente de nuevo: ')
        user_id = find_user(username, users)
    # Do the same process for the password
    password = input('Ingrese su contraseña: ')
    while not check_password(password, users, user_id):
        password = input(
            'Contraseña incorrecta o no valida. Intente de nuevo: ')


def products_dict(container):
    products = {}
    for element in container:
        product_id = element[1]
        if product_id in products:
            products[product_id] += 1
        else:
            products[product_id] = 1
    return products


def organize_products(group):
    group_dict = products_dict(group)
    group_items_list = list(group_dict.items())
    result = sorted(group_items_list, key=lambda x: x[1], reverse=True)
    return result


def print_point1(list, lifestore_products, attribute):
    for product_id, value in list:
        product_name = lifestore_products[product_id - 1][1].split(',')[0]
        print(f'"{product_name}" tuvo {value} {attribute}')
    print()


def print_point2(list, attribute):
    for category, value in list:
        print(f'La categoría "{category}" tuvo {value} {attribute}')
    print()


def categories_dict(container, lifestore_products):
    categories = {}
    for element in container:
        product_id = element[1]
        category = lifestore_products[product_id-1][3]
        if category in categories:
            categories[category] += 1
        else:
            categories[category] = 1
    return categories


def organize_categories(group, lifestore_products):
    group_dict = categories_dict(group, lifestore_products)
    group_items_list = list(group_dict.items())
    result = sorted(group_items_list, key=lambda x: x[1])
    return result


def main():
    # Import the store variables
    from lifestore_file import lifestore_products, lifestore_sales, lifestore_searches
    # Create some users for the program
    users = [{'username': 'paco123', 'password': 'pass123'},
             {'username': 'paco456', 'password': 'pass456'},
             {'username': 'javier123', 'password': 'javier123'},
             {'username': 'javier456', 'password': 'javier456'}]
    # Go through the login process
    # login(users)
    # print()
    print('------------------- BEST SELLERS -------------------------------------------------------')
    sellers = organize_products(lifestore_sales)
    print_point1(sellers[0:50], lifestore_products, 'ventas')
    print('------------------ MOST SEARCHED -------------------------------------------------------')
    most_search = organize_products(lifestore_searches)
    print_point1(most_search[0:100], lifestore_products, 'búsquedas')
    print('------------- WORST SELLERS BY CATEGORY ------------------------------------------------')
    category_sellers = organize_categories(lifestore_sales, lifestore_products)
    print_point2(category_sellers, 'ventas')
    print('------------- LEAST SEARCHED BY CATEGORY -----------------------------------------------')
    category_least_search = organize_categories(lifestore_searches, lifestore_products)
    print_point2(category_least_search, 'búsquedas')


if __name__ == '__main__':
    main()
