# Import and configure locale to format the money
from datetime import datetime
import locale
locale.setlocale(locale.LC_ALL, '')


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
    '''Function for finding the ammount of times a product was sold'''
    products = {}
    # For all elements inside the container save in the dict a counter in
    # the product key
    for element in container:
        product_id = element[1]
        if product_id in products:
            products[product_id] += 1
        else:
            products[product_id] = 1
    return products


def organize_products(group):
    '''Function for organizing the products from most sold to least sold'''
    group_dict = products_dict(group)
    group_items_list = list(group_dict.items())
    # Order by the second element in the tuple
    result = sorted(group_items_list, key=lambda x: x[1], reverse=True)
    return result


def print_point11(list, lifestore_products, attribute):
    '''Function for printing the format for the point 1.1'''
    for product_id, value in list:
        product_name = lifestore_products[product_id - 1][1].split(',')[0]
        print(f'"{product_name}" tuvo {value} {attribute}')
    print()


def print_point12(list, attribute):
    '''Function for printing the format for the point 1.2'''
    for category, value in list:
        print(f'La categoría de {category} tuvo {value} {attribute}')
    print()


def print_correct_point12(worst_dict, attribute, lifestore_products):
    '''Correct function for printing the format for the point 1.2'''
    for category, products in worst_dict.items():
        print(f"Menores {attribute[:-1]} para la categoria de {category}")
        print_point11(products, lifestore_products, attribute)

def print_point2(list, lifestore_products, attribute):
    '''Function for printing the format for the point 2'''
    for product_id, value in list:
        product_name = lifestore_products[product_id - 1][1].split(',')[0]
        print(f'"{product_name}" tuvo {value:0.2f} {attribute}')
    print()


def categories_dict(container, lifestore_products):
    '''Function for grouping the categories and assigning the amount of 
    times a product of the categorie was sold'''
    categories = {}
    # For each element in the container get the category and save the counter
    for element in container:
        product_id = element[1]
        category = lifestore_products[product_id-1][3]
        if category in categories:
            categories[category] += 1
        else:
            categories[category] = 1
    return categories


def worst_by_categories(container, lifestore_products, limit):
    '''Function to get the worst products in reviews and sells by categories'''
    categories = {}
    for product_id, type in container[::-1]:
        category = lifestore_products[product_id - 1][3]
        if category in categories:
            if len(categories[category]) < limit:
                categories[category].append((product_id, type))
        else:
            categories[category] = [(product_id, type)]
    return categories


def organize_categories(group, lifestore_products):
    '''Function to organize the categories from most sold to least'''
    group_dict = categories_dict(group, lifestore_products)
    group_items_list = list(group_dict.items())
    # Order by the second element in the tuple
    result = sorted(group_items_list, key=lambda x: x[1])
    return result


def product_reviews_dict(sales):
    '''Function for grouping the products by their review and also the
    amount of times a review was made'''
    reviews = {}
    # For each sale get the review and save it together with a counter
    # to calculate the average review for each product
    for sale in sales:
        refund = sale[4]
        if not refund:
            product_id = sale[1]
            review = sale[2]
            if product_id in reviews:
                reviews[product_id][0] += review
                reviews[product_id][1] += 1
            else:
                reviews[product_id] = [review, 1]
    return reviews


def organize_product_reviews(lifestore_sales):
    '''Function to calculate the average review from all sales'''
    reviews = product_reviews_dict(lifestore_sales)
    reviews_list = list(reviews.items())
    # Calculate the average for all products sold
    result = [(index, vals[0]/vals[1]) for index, vals in reviews_list]
    # Order by average reviews
    result = sorted(result, key=lambda x: x[1])
    return result


def revenue_by_month_n_year(lifestore_sales, lifestore_products):
    '''Function to group all sales by month and year'''
    years_n_months = {}
    # For all sale inside lifestore_sales
    for _, product_id, _, sale_date, refund in lifestore_sales:
        product_price = lifestore_products[product_id-1][2]
        formatted_date = datetime.strptime(sale_date, '%d/%m/%Y')
        year = formatted_date.year
        month = formatted_date.month
        # All products that were not refunded
        if not refund:
            # Logic for grouping by year
            if year in years_n_months:
                # Logic for grouping by month
                if month in years_n_months[year]:
                    years_n_months[year][month] += product_price
                else:
                    years_n_months[year][month] = product_price
            else:
                years_n_months[year] = {month: product_price}
    return years_n_months


def calc_total_revenue(revenue_dict):
    '''Function to calculate the total revenue'''
    total_revenue = 0
    # For all years in the revenue dict
    for year in revenue_dict.values():
        # Sum the revenue of all months (year.values()) and return the total
        total_revenue += sum(year.values())
    return total_revenue


def calc_revenue_by_year(revenue_dict):
    '''Function to calculate the total revenue by all years'''
    year_revenue = {}
    # For all years and months sum the total by month and store it
    # by each year
    for year, months in revenue_dict.items():
        if year in year_revenue:
            year_revenue[year] += sum(months.values())
        else:
            year_revenue[year] = sum(months.values())
    return year_revenue


def print_total_revenue(total_revenue):
    '''Function to print the total revenue of the company'''
    print(
        f'Ingresos totales: {locale.currency(total_revenue, grouping=True)} MXN')
    print()


def print_revenue_by_year(year_dict):
    '''Function to print the total revenue by all years'''
    year_total = list(year_dict.items())
    year_total = sorted(year_total, key=lambda x: x[0])
    for year, total in year_total:
        print(
            f'Ingresos en el año {year}: {locale.currency(total, grouping=True)} MXN')
    print()


def print_revenue_by_month(revenue_dict):
    '''Function to print the total revenue by all months and the best month of the last year'''
    # Find the last year
    last_year = max(revenue_dict.keys())
    months_of_last_year = list(revenue_dict[last_year].items())
    # Sort the months
    months_of_last_year = sorted(months_of_last_year, key=lambda x: x[0])
    max_month = max(months_of_last_year, key=lambda x: x[1])
    for month, total in months_of_last_year:
        month_name = datetime.strptime(str(month), "%m").strftime('%B')
        print(
            f'Ingresos en el mes de {month_name} del año {last_year}: {locale.currency(total, grouping=True)} MXN')
    print()
    month_name = datetime.strptime(str(max_month[0]), "%m").strftime('%B')
    print(
        f'El mes de {month_name} del año {last_year} tuvo la mayor cantidad ingresos con: {locale.currency(max_month[1], grouping=True)} MXN')


def main():
    # Import the store variables
    from lifestore_file import lifestore_products, lifestore_sales, lifestore_searches
    # Create some users for the program
    users = [{'username': 'paco123', 'password': 'pass123'},
             {'username': 'paco456', 'password': 'pass456'},
             {'username': 'javier123', 'password': 'javier123'},
             {'username': 'javier456', 'password': 'javier456'}]
    # Go through the login process
    login(users)
    print()
    # Pass through all the different types of analysis
    print('------------------- BEST SELLERS -------------------------------------------------------')
    sellers = organize_products(lifestore_sales)
    print_point11(sellers[0:15], lifestore_products, 'ventas.')
    print('------------------ MOST SEARCHED -------------------------------------------------------')
    most_search = organize_products(lifestore_searches)
    print_point11(most_search[0:20], lifestore_products, 'búsquedas.')
    print('------------- WORST SELLERS BY CATEGORY ------------------------------------------------')
    category_sellers = organize_categories(lifestore_sales, lifestore_products)
    print_point12(category_sellers, 'ventas.') # This one is different from what it was needed
    worst_sells_categories = worst_by_categories(sellers, lifestore_products, 5)
    print_correct_point12(worst_sells_categories, 'ventas.', lifestore_products)
    print('------------- LEAST SEARCHED BY CATEGORY -----------------------------------------------')
    category_least_search = organize_categories(
        lifestore_searches, lifestore_products)
    print_point12(category_least_search, 'búsquedas.') # This one is different from what it was needed
    worst_reviews_categories = worst_by_categories(most_search, lifestore_products, 20)
    print_correct_point12(worst_reviews_categories, 'búsquedas.', lifestore_products)
    print('--------------- BEST REVIEWS BY PRODUCT ------------------------------------------------')
    reviews = organize_product_reviews(lifestore_sales)
    print_point2(reviews[:-10:-1], lifestore_products, 'en calificación.')
    print('--------------- WORST REVIEWS BY PRODUCT -----------------------------------------------')
    print_point2(reviews[:10], lifestore_products, 'en calificación.')
    print('------------------------- REVENUE ------------------------------------------------------')
    year_n_month_sells = revenue_by_month_n_year(
        lifestore_sales, lifestore_products)
    total_revenue = calc_total_revenue(year_n_month_sells)
    print_total_revenue(total_revenue)
    year_revenue = calc_revenue_by_year(year_n_month_sells)
    print_revenue_by_year(year_revenue)
    print_revenue_by_month(year_n_month_sells)


if __name__ == '__main__':
    main()
