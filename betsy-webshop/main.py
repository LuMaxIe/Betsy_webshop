__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

import models
import helpers
import peewee
import cli
from fuzzywuzzy import fuzz


def reset_database():  # <---!!! Warning: Resets database with cleared Tables !!!--->
    helpers.recreate_tables([
        models.Tag,
        models.Product,
        models.ProductTag,
        # models.User,
        models.UserProduct,
        models.Transaction
    ])


def add_user(name: str, age: int, country: str, city: str, address: str, card_number: str):
    try:
        models.User.create(
            user_name=name.lower(),
            age=age,
            country=country.lower(),
            city=city.lower(),
            address=address.lower(),
            card_number=card_number.lower()
        )
    except peewee.IntegrityError as Error:
        print(Error)
    else:
        print('User added')


def add_tags(tags: list):
    try:
        checked_tags = helpers.check_for_new_tags(tags)
        if len(checked_tags) > 0:
            tags_to_add = [{'name': tag['name'].lower()}
                           for tag in checked_tags]
            models.Tag.insert_many(tags_to_add).execute()
        else:
            raise ValueError
    except TypeError as Error:
        print(Error)
    except ValueError:
        print('Suggested tags already existing')
    except peewee.IntegrityError as Error:
        print(Error)


def add_product(name: str, description: str, price: float, amount: int, tags: list, user: str):
    try:
        # Check if user is an user stored in db
        user_in_session = models.User.get(
            models.User.user_name == user.lower())

        # Add new tags to database if needed
        if len(tags) == 0:
            raise ValueError
        else:
            add_tags(tags)

        # Add new product to product table
        product = models.Product.create(
            name=name, description=description, price=price, quantity=amount
        )

        # Add product-user connection in UserProduct table
        models.UserProduct.create(user=user_in_session, product=product.id)

        # Add product-tag connection in ProductTag table
        for tag in tags:
            db_tag = models.Tag.select().where(models.Tag.name == tag.lower())
            models.ProductTag.create(
                tag=db_tag[0].id,
                product=product
            )

    except ValueError:
        print('You must use at least one tag to create this product')
    except peewee.IntegrityError as Error:
        print(Error)
    else:
        print("Added product")


def search(term):
    try:
        items = models.Product.select(
            models.Product.name,
            models.Product.description,
            models.Product.price
        ).where(
            (fuzz.ratio(models.Product.name, term.lower()) > 95) |
            (fuzz.partial_ratio(models.Product.name, term.lower()) > 95) |
            (fuzz.token_sort_ratio(models.Product.description, term) > 95)
        )
        if len(items) == 0:
            raise ValueError
        else:
            for item in items:
                print(fuzz.ratio(item.name, term.lower()))
                print(fuzz.partial_ratio(item.name, term.lower()))
                print(fuzz.token_sort_ratio(item.description, term))
                print(
                    f"""\nProduct: {item.name}\nDescription: {item.description}\nPrice: {item.price}\n""")

    except ValueError:  # Must change to prevent bare exception
        print(f"No items found with keyword: {term}")


def list_user_products(user_id):
    try:
        products = (models.Product
                    .select()
                    .join(models.UserProduct)
                    .join(models.User)
                    .where(models.User.id == user_id))

        for prod in products:
            print(prod.name)

    except peewee.IntegrityError as Error:
        print(Error)


def list_products_per_tag(tag_id):
    try:
        products = (models.Product
                    .select()
                    .join(models.ProductTag)
                    .join(models.Tag)
                    .where(models.Tag.id == tag_id))

        for prod in products:
            print(prod.name)

    except peewee.IntegrityError as Error:
        print(Error)


def update_stock(product_id, new_quantity):
    try:
        models.Product.update({models.Product.quantity: new_quantity}).where(
            models.Product.id == product_id).execute()
    except peewee.IntegrityError as Error:
        print(Error)
    else:
        print("product quantity updated")


def purchase_product(product_id, buyer_id, seller_id, quantity):
    try:
        models.Transaction.create(
            buyer=buyer_id,
            seller=seller_id,
            product=product_id,
            amount=quantity
        )
    except peewee.IntegrityError as Error:
        print(Error)
    else:
        print("Transaction added")


def remove_product(product_id):
    try:
        models.Product.delete().where(models.Product.id == product_id).execute()
    except peewee.IntegrityError as Error:
        print(Error)
    else:
        print("Product deleted")


user_input = cli.cli_interface()
command = user_input.pop("Command")
function_params = [user_input[key] for key in user_input]
locals()[command](*function_params)
