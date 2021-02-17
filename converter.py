import pandas as pd

def split_details(product):
    details = product.split('→')
    if len(details) < 2:
        return None, None, None, None

    name_n_qty = details[0]
    cost = details[-1]
    other_details = []
    count = 1
    if len(details) > 2:
        for i in range(1, len(details) - 1):
            other_details.append(details[i])
            count = int(details[i].split('x')[0].replace(' ', ''))

    name_n_qty = name_n_qty.split('(')
    name = name_n_qty[0]
    qty = 'None'
    if len(name_n_qty) > 1:
        qty = name_n_qty[-1].replace(')', '')

    return name, qty, count, cost

def elaborate_products(product_list, new_df):
    try:
        store_n_products = product_list.split('\n- ')
        store = store_n_products[0].split('→')[0]
        products = store_n_products[1:]
        for product in products:
            name, qty, count, cost = split_details(product)
            new_df = new_df.append({'Date': df.iloc[i].Date, 
                                    'Store': store, 
                                    'Name': name, 
                                    'Volume': qty, 
                                    'Quantity': count, 
                                    'Cost': cost}, 
                                    ignore_index=True)
    except:
        print('Elements not found', product_list)
    return new_df

def write_to_csv(df, file):
    df.to_csv(file, index=False)

if __name__ == "__main__":
    df = pd.read_csv('Expenses/2021/January.csv')
    df = df.loc[df.Category == 'Groceries']
    empty_data = {'Date': [],
                  'Store': [],
                  'Name': [],
                  'Volume': [],
                  'Quantity': [],
                  'Cost': []}
    filename = 'Expenses/2021/Groceries/January.csv'
    empty_df = pd.DataFrame(empty_data, columns=['Date', 'Store', 'Name', 'Volume', 'Quantity', 'Cost'])
    updated_df = empty_df

    for i in range(0, len(df)):
        new_df = elaborate_products(df.iloc[i].Comments, empty_df)
        updated_df = updated_df.append(new_df)

    write_to_csv(updated_df, filename)