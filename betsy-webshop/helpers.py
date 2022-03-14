import peewee
import models
from playhouse.migrate import SqliteMigrator, migrate
from fuzzywuzzy import fuzz

db = peewee.SqliteDatabase(
    'Betsy.db',
)

migrator = SqliteMigrator(db)


def add_column_to_table(table, column_name, field):
    migrate(
      migrator.add_column(table, column_name, field)
    )


def drop_column_of_table(table, column_name):
    migrate(
      migrator.drop_column(table, column_name)
    )


def recreate_tables(db_models):
    db.drop_tables(db_models)
    db.create_tables(db_models)


def check_for_new_tags(product_tags: list) -> list:
    db_tags = [tag.name.lower() for tag in models.Tag.select()]
    new_tags = [{'name': new_tag} for new_tag in product_tags if new_tag.lower() not in db_tags]
    return new_tags


def search_ratios(keyword, product_name, product_description, value):
    ratio = fuzz.ratio(product_name, keyword)
    p_ratio = fuzz.partial_ratio(product_name, keyword)
    tokenized = fuzz.partial_token_set_ratio(product_description, keyword)

    if ratio > value or p_ratio > value or tokenized > value:
        return True
