import peewee

db = peewee.SqliteDatabase(
    'Betsy.db',
    pragmas={'journal_mode': 'wal', 'cache_size': 10000, 'foreign_keys': 1}
)


class BaseModel(peewee.Model):
    class Meta:
        database = db


class Tag(BaseModel):
    name = peewee.CharField()

    class Meta:
        constraints = [peewee.SQL('UNIQUE ("name" COLLATE NOCASE)')]


class Product(BaseModel):
    name = peewee.CharField(unique=True, index=True)
    description = peewee.CharField(null=False)
    price = peewee.DecimalField(decimal_places=2, auto_round=True)
    quantity = peewee.IntegerField()

    class Meta:
        constraints = [peewee.SQL('UNIQUE ("name" COLLATE NOCASE)')]


class ProductTag(BaseModel):
    product = peewee.ForeignKeyField(Product)
    tag = peewee.ForeignKeyField(Tag)


class User(BaseModel):
    user_name = peewee.CharField(unique=True)
    age = peewee.IntegerField()
    country = peewee.CharField()
    city = peewee.CharField()
    address = peewee.CharField()
    card_number = peewee.CharField(unique=True)


class UserProduct(BaseModel):
    user = peewee.ForeignKeyField(User)
    product = peewee.ForeignKeyField(Product)

    class Meta:
        indexes = (
            (('user', 'product'), True),
        )


class Transaction(BaseModel):
    buyer = peewee.ForeignKeyField(User)
    seller = peewee.ForeignKeyField(User)
    product = peewee.ForeignKeyField(Product)
    amount = peewee.IntegerField()
