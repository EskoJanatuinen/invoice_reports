import requests
import pandas as pd
import config
import jwt_token
import jwt_functions
import graphql
import reports


# JWT authentication:

if jwt_functions.has_token_expired():
    access_token = jwt_functions.create_jwt()
    jwt_functions.write_jwt(access_token)
    print("JWT expired: a new token was created")
else:
    access_token = jwt_token.jwt
    print("JWT is valid")


# GraphQL querys:


def post_request(q):
    res = requests.post(
        config.url_hasura,
        json={"query": q},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    if res.status_code == 200:
        return res
    else:
        raise Exception(f"Query failed. HTTP status code: {res.status_code}.")


res1 = post_request(graphql.sales_orders)
res2 = post_request(graphql.sales_orders_201)


# Query -> DataFrame

df1 = pd.json_normalize(res1.json()["data"]["sales_order"])

df1 = df1.filter(
    items=[
        "order_date",
        "extra_id",
        "delivery.name",
        "delivery.delivery_method",
        "order_no",
    ]
)
print(df1)

df1 = df1.rename(
    columns={
        "order_date": "Pvm",
        "extra_id": "Tilausnum",
        "delivery.name": "Asiakas",
        "sales_order_rows.warehouse": "Varasto",
        "delivery.delivery_method": "Toimitustapa",
        "order_no": "Myyntitilaus",
    }
)

df2 = pd.json_normalize(res2.json()["data"]["sales_order_row"])
df2 = df2.rename(columns={"order_no": "Myyntitilaus", "warehouse": "Varasto"})


# Creating settlement reports

reports.posti(df1, df2)
reports.matkahuolto()
