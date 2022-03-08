from asyncio import events
from asyncore import write
from csv import DictReader, DictWriter, writer
from itertools import product
import os
from dotenv import load_dotenv

load_dotenv() 

file = os.getenv("FILEPATH")

def read_products_from_csv():
    with open(file, "r") as csv_file:
        reader = DictReader(csv_file)
        products = list(reader)

        for product in products:
            for key, value in product.items():
                if key == "price":
                    product[key] = float(value)
                if key == "id":
                    product[key] = int(value)
        return products


def read_products_specific_from_csv(page, per_page):
    initial_item_id = page * per_page - (per_page -1)
    finish_item_id = initial_item_id + (per_page -1)
    with open(file, "r") as csv_file:
        reader = DictReader(csv_file)
        products = list(reader)

        for product in products:
            for key, value in product.items():
                if key == "price":
                    product[key] = float(value)
                if key == "id":
                    product[key] = int(value)

        products_show = []
        for product in products: 
            if product["id"] >= initial_item_id and product["id"] <= finish_item_id:
                products_show.append(product)            
        return products_show
                

def validate_keys(payload: dict, expected_keys: set):
    bory_keys_set = set(payload.keys())

    invalis_keys = bory_keys_set - expected_keys

    if invalis_keys:
        raise KeyError(
            {
                "error":"invalid_keys",
                "expected":list(expected_keys),
                "received":list(bory_keys_set),
            }
        )

def write_products_in_csv(payload:dict):
    with open(file, "a") as csv_file:
        id_value = len(read_products_from_csv()) + 1

        payload["id"] = id_value
        fieldnames=["id", "name", "price"]

        writer = DictWriter(csv_file, fieldnames)

        writer.writerow(payload)

        return payload


def rewrite_products_in_csv(payload:list[dict]):
    with open(file, "w") as csv_file:
        fieldsnames = ["id", "name", "price"]

        writer = DictWriter(csv_file, fieldsnames)

        writer.writeheader()
        writer.writerows(payload)


def validate_id(id):
    products =read_products_from_csv()

    for product in products:
        if product["id"] == id:
            return True

    return False


