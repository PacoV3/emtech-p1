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


def print_point11(list, lifestore_products, attribute):
    for product_id, value in list:
        product_name = lifestore_products[product_id - 1][1].split(',')[0]
        print(f'"{product_name}" tuvo {value} {attribute}')
    print()


def print_point12(list, attribute):
    for category, value in list:
        print(f'La categoría "{category}" tuvo {value} {attribute}')
    print()


def print_point2(list, lifestore_products, attribute):
    for product_id, value in list:
        product_name = lifestore_products[product_id - 1][1].split(',')[0]
        print(f'"{product_name}" tuvo {value:0.2f} {attribute}')
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


def product_reviews_dict(sales):
    reviews = {}
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
    reviews = product_reviews_dict(lifestore_sales)
    reviews_list = list(reviews.items())
    result = [(index, vals[0]/vals[1]) for index, vals in reviews_list]
    result = sorted(result, key=lambda x: x[1])
    return result


def revenue_by_month_n_year(lifestore_sales, lifestore_products):
    years_n_months = {}
    for _, product_id, _, sale_date, refund in lifestore_sales:
        product_price = lifestore_products[product_id-1][2]
        formatted_date = datetime.strptime(sale_date, '%d/%m/%Y')
        year = formatted_date.year
        month = formatted_date.month
        if not refund:
            if year in years_n_months:
                if month in years_n_months[year]:
                    years_n_months[year][month] += product_price
                else:
                    years_n_months[year][month] = product_price
            else:
                years_n_months[year] = {month: product_price}
    return years_n_months


def calc_total_revenue(revenue_dict):
    total_revenue = 0
    for months in revenue_dict.values():
        total_revenue += sum(months.values())
    return total_revenue


def calc_revenue_by_year(revenue_dict):
    year_revenue = {}
    for year, months in revenue_dict.items():
        if year in year_revenue:
            year_revenue[year] += sum(months.values())
        else:
            year_revenue[year] = sum(months.values())
    return year_revenue


def print_total_revenue(total_revenue):
    print(f'Ingresos totales: {locale.currency(total_revenue, grouping=True)} MXN')
    print()


def print_revenue_by_year(year_dict):
    year_total = list(year_dict.items())
    year_total = sorted(year_total, key=lambda x: x[0])
    for year, total in year_total:
        print(f'Ingresos en el año {year}: {locale.currency(total, grouping=True)} MXN')
    print()


def print_revenue_by_month(revenue_dict):
    last_year = max(revenue_dict.keys())
    months_of_last_year = list(revenue_dict[last_year].items())
    months_of_last_year = sorted(months_of_last_year, key=lambda x: x[0])
    max_month = max(months_of_last_year, key=lambda x: x[1])
    for month, total in months_of_last_year:
        month_name = datetime.strptime(str(month), "%m").strftime('%B')
        print(f'Ingresos en el mes de {month_name} del año {last_year}: {locale.currency(total, grouping=True)} MXN')
    print()
    month_name = datetime.strptime(str(max_month[0]), "%m").strftime('%B')
    print(f'El mes de {month_name} del año {last_year} tuvo la mayor cantidad ingresos con: {locale.currency(max_month[1], grouping=True)} MXN')



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
    print_point11(sellers[0:50], lifestore_products, 'ventas.')
    print('------------------ MOST SEARCHED -------------------------------------------------------')
    most_search = organize_products(lifestore_searches)
    print_point11(most_search[0:100], lifestore_products, 'búsquedas.')
    print('------------- WORST SELLERS BY CATEGORY ------------------------------------------------')
    category_sellers = organize_categories(lifestore_sales, lifestore_products)
    print_point12(category_sellers, 'ventas.')
    print('------------- LEAST SEARCHED BY CATEGORY -----------------------------------------------')
    category_least_search = organize_categories(lifestore_searches, lifestore_products)
    print_point12(category_least_search, 'búsquedas.')
    print('--------------- BEST REVIEWS BY PRODUCT ------------------------------------------------')
    reviews = organize_product_reviews(lifestore_sales)
    print_point2(reviews[:-20:-1], lifestore_products, 'en calificación.')
    print('--------------- WORST REVIEWS BY PRODUCT -----------------------------------------------')
    print_point2(reviews[:20], lifestore_products, 'en calificación.')
    print('------------------------- REVENUE ------------------------------------------------------')
    year_n_month_sells = revenue_by_month_n_year(lifestore_sales, lifestore_products)
    total_revenue = calc_total_revenue(year_n_month_sells)
    print_total_revenue(total_revenue)
    year_revenue = calc_revenue_by_year(year_n_month_sells)
    print_revenue_by_year(year_revenue)
    print_revenue_by_month(year_n_month_sells)


if __name__ == '__main__':
    main()
