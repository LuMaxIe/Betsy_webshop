import argparse


def cli_interface():
    parser = argparse.ArgumentParser(description='Betsy Webshop')

    subparsers = parser.add_subparsers(
        title='Subcommands',
        description='Perform different actions in Betsy webshop',
        dest='Command'
    )

    # Add product
    product_parser = subparsers.add_parser("add_product")
    product_parser.add_argument(
        "--name", help="Name of the product", required=True)
    product_parser.add_argument(
        "--description", help="Short description of the product", required=True)
    product_parser.add_argument(
        "--price", type=float, help="The price of the product", required=True)
    product_parser.add_argument(
        "--amount", type=int, help="Amount of the product", required=True)
    product_parser.add_argument("--tags", action='append',
                                help="List of tags to add to the product (1 min)", required=True)
    product_parser.add_argument(
        "--user", type=str, help="The name of the user the product belongs to", required=True)

    # New user
    new_user_parser = subparsers.add_parser("add_user")
    new_user_parser.add_argument(
        "--name", required=True, help="Name of the user to add")
    new_user_parser.add_argument(
        "--age", type=int, required=True, help="Age of the user in integers")
    new_user_parser.add_argument(
        "--country", required=True, help="Country of origin")
    new_user_parser.add_argument(
        "--city", required=True, help="City where the user lives")
    new_user_parser.add_argument(
        "--address", required=True, help="Address off the user")
    new_user_parser.add_argument(
        "--card_number", required=True, help="Bank account number")

    # Reset database
    subparsers.add_parser("reset_database")

    # Add tags
    tags = subparsers.add_parser("add_tags")
    tags.add_argument("--tags_list", action='append', required=True,
                      help="One ore more tags to catogorize the product")

    # Search product
    products = subparsers.add_parser("search")
    products.add_argument("--keyword", required=True,
                          help="The name of the product to search")

    # List user products
    user_prods = subparsers.add_parser("list_user_products")
    user_prods.add_argument("--user_id", required=True,
                            type=int, help="user id/key of the User Table")

    # List products per tag
    product_tags = subparsers.add_parser("list_products_per_tag")
    product_tags.add_argument("--tag_id", required=True)

    # Update stock
    product_update = subparsers.add_parser("update_stock")
    product_update.add_argument(
        "--product_id", required=True, help="Key of the product to alter")
    product_update.add_argument(
        "--new_quantity", required=True, help="Integer to change the quantity into")

    # Purchase product
    product_purchase = subparsers.add_parser("purchase_product")
    product_purchase.add_argument(
        "--product_id", required=True, help="Key of product table")
    product_purchase.add_argument(
        "--buyer_id", required=True, help="Key of User table")
    product_purchase.add_argument(
        "--seller_id", required=True, help="the id of the user that sells the product")
    product_purchase.add_argument(
        "--quantity", required=True, help="The amount of products sold in the transaction")

    # Remove product
    product_removal = subparsers.add_parser("remove_product")
    product_removal.add_argument(
        "--product_id", required=True, help="Id of the product to remove from product table")

    return parser.parse_args().__dict__
