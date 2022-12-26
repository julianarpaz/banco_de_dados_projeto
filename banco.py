import mysql.connector
import pandas as pd
from dash import Dash, html, dcc, Output, Input
import plotly.express as px
from mysql.connector import errorcode

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

db_connection = mysql.connector.connect(host='localhost', user='root', password='root', database='db_projeto_banco')

cursor = db_connection.cursor()

orders_top_10 = []
amount_orders_top_10 = []
employees_top_10 = []
employees_sales = []
contador = 1
items_total_top_10 = []
product_id_top_10 = []
categoryID =[]
category_name = []
category_description = []
options = ['Orders', 'Products']
products_id_sale = []
products_sale_top_5 = []


sql_total_categories = ("SELECT OrderID, COUNT(*) AS full_order FROM tbl_order_details GROUP BY OrderID")
sql_products_sale = ("SELECT ProductID, count(ProductID) as products_sale FROM tbl_order_details GROUP BY ProductID ORDER BY products_sale DESC LIMIT 5")
sql_orders_total_price = ("SELECT OrderID, SUM(Quantity * UnitPrice) AS order_total_price FROM tbl_order_details GROUP BY OrderID ORDER BY order_total_price DESC LIMIT 5")
sql_top_10_employees = ("SELECT EmployeeID, count(EmployeeID) as top_employees FROM tbl_orders GROUP BY EmployeeID ORDER BY top_employees DESC LIMIT 5")

cursor.execute(sql_orders_total_price)

for (OrderID, order_total_price) in cursor:
    orders_top_10.append(str(OrderID))
    amount_orders_top_10.append(order_total_price)
print("\n")

cursor.execute(sql_top_10_employees)
    
for (EmployeeID, top_employees) in cursor:
    employees_top_10.append(str(EmployeeID))
    employees_sales.append(top_employees)
    
cursor.execute(sql_products_sale)

for (ProductID, products_sale) in cursor:
    products_id_sale.append(str(ProductID))
    products_sale_top_5.append(products_sale)
print("\n")


for (ProductID, products_sale) in cursor:
    print(ProductID, products_sale)
print("\n")

#while contador <= 77:
    #sql = (str("SELECT SUM(Quantity) AS product_total_sales FROM tbl_order_details WHERE ProductID =" + str(contador)))
    #cursor.execute(sql)
    #for(order_total_price) in cursor:
        #product_id_top_10.append(contador)
        #items_total_top_10.append(order_total_price)
            

def orders(self):
    cursor.execute(sql_orders_total_price)
    for (OrderID, order_total_price) in cursor:
      orders_top_10.append(str(OrderID))
      amount_orders_top_10.append(order_total_price)
    print("\n")
    
def categories(self):
    cursor.execute(sql_total_categories)
    for (CategoryID, CategoryName, CategoryDescription) in cursor:
      categoryID.append(str(CategoryID))
      category_name.append(CategoryName)
      category_description(CategoryDescription)
    print("\n")
    
def employees(self):
    cursor.execute(sql_top_10_employees)
    for (EmployeeID, top_employees) in cursor:
      employees_top_10.append(str(EmployeeID))
      employees_sales.append(top_employees)
    print("\n")

#for (CategoryID, CategoryName, Description) in cursor:
      #print(CategoryID, CategoryName, Description)
      #print("\n")

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

app = Dash(__name__)


df_orders = pd.DataFrame({
    "OrderID": orders_top_10,
    "Amount":  amount_orders_top_10,
    "TOP 5": ["TOP", "TOP", "TOP", "SF", "SF"]})

fig = px.bar(df_orders, x="OrderID", y="Amount", color="TOP 5", barmode="group")

df_employees = pd.DataFrame({
    "EmployeeID": top_employees,
    "Quantity":  employees_sales,
    "TOP 5": ["TOP", "TOP", "TOP", "SF", "SF"]})

#fig = px.bar(df_employees, x="EmployeeID", y="Quantity", color="TOP 5", barmode="group")

df_products = pd.DataFrame({
    "ProductID": products_id_sale,
    "Quantity":  products_sale_top_5,
    "TOP 5": ["TOP", "TOP", "TOP", "SF", "SF"]})



fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Dados das compras e vendas',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Uma aplicação prática para os seus dados.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    
    #html.Div([
    #html.H4(children='Foods Categories of Exportation'),
    #generate_table(categories)])

    
    dcc.Dropdown(options, value='Orders', id='top_10'),

    dcc.Graph(
        id='top_10_graph',
        figure=fig
    )    
])

@app.callback(
    Output('top_10_graph', 'figure'),
    Input('top_10', 'value'))
    
def update_output(value):
    if value == 'Orders':
        fig = px.bar(df_orders, x="OrderID", y="Amount", color="TOP5 5", barmode="group")
    elif value == 'Products':
        fig = px.bar(df_products, x="ProductID", y="Quantity", color="TOP 5", barmode="group")
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)





    
    

 


 