# Betsy_webshop

## Dependencies
fuzzywuzzy 0.18.0
peewee 3.14.9

## Optional dependencies
python-Levenshtein 0.12.2 (This speeds op fuzzywuzzy actions)

---
## Known limitations & improvements
- "Listing per 'x'" functionalities currently require Keys instead of names
- CLI subcommands should come with flags. I.e. "products -l" & "users -l" instead of "list_products". Overall CLI commands could be improved.
 
---

## Usage Guide

### Set-up
This program comes with some CLI functionality. It also has some pre-configured data. If you wish to start with a clean sheet please run the (sub)command "reset_database". Warning this will reset everything and you must add new user to use the rest of the program.

### List data
Start by running al three "list subcommands" to get a view of what data is available. This will also show the keys for each entry to use in other commands.

*If you wish to add more data, please follow the add_product, add_user & add_tags commands.*

### List products per user
Supply a key from "list_users" and review all products submitted for that user.

### List products per tag
Supply a key from "list_tags" and review all products submitted for that tag.

### Update stock quantity
Supply a key from "list_products" and supply a new quantity for the product.

### Add a transaction
Supply product, buyer and seller IDs + the quantity of products in the transaction

### remove a product
Remove a product by supplying an product ID