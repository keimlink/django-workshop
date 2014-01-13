# encoding: utf-8
import random
import sys


class Fixture(tuple):
    def get_random_id(self):
        return random.randint(1, len(self))

    def get_random_item(self):
        return self[random.randrange(0, len(self))]


def get_random_zipcode():
    return ''.join(map(str, random.sample(range(0, 10), 5)))


def drop_tables():
    sql = """DROP TABLE IF EXISTS "city";
    DROP TABLE IF EXISTS "address";
    """
    return sql


def create_tables():
    sql = """CREATE TABLE "city" (
        "id" integer NOT NULL PRIMARY KEY,
        "name" varchar(255) NOT NULL
    );
    CREATE TABLE "address" (
        "id" integer NOT NULL PRIMARY KEY,
        "first_name" varchar(100) NOT NULL,
        "last_name" varchar(100) NOT NULL,
        "street" varchar(255) NOT NULL,
        "zipcode" varchar(5) NOT NULL,
        "city_id" integer NOT NULL REFERENCES "city" ("id")
    );
    """
    return sql


def insert_cities():
    pk = 1
    sql = ''
    for city in CITIES:
        sql += """INSERT INTO "city" VALUES (
            %d, "%s"
        );
        """ % (pk, city)
        pk += 1
    return sql


def insert_addresses(count):
    pk = 1
    sql = ''
    while pk <= count:
        housenumber = random.randint(1, 100)
        data = {
            'id': pk,
            'first_name': FIRST_NAMES.get_random_item(),
            'last_name': LAST_NAMES.get_random_item(),
            'street': STREETS.get_random_item() + ' %d' % housenumber,
            'zipcode': get_random_zipcode(),
            'city_id': CITIES.get_random_id(),
        }
        sql += """INSERT INTO "address" VALUES (
            %(id)d, "%(first_name)s", "%(last_name)s", "%(street)s", "%(zipcode)s", %(city_id)d
        );
        """ % data
        pk += 1
    return sql


def write(data):
    sys.stdout.write(data)


FIRST_NAMES = Fixture(('Malte', 'Andrea', 'Peter', 'Maria', 'Michaela'))
LAST_NAMES = Fixture(('Meier', 'Schulze', 'Drescher', 'Weiland', 'Hirsch'))
STREETS = Fixture(('Alte Straße', 'Hauptstraße', 'Neuer Ring', 'Brunnengasse', 'Am Markt'))
CITIES = Fixture(('Berlin', 'Dresden', 'Hamburg', 'Bonn', 'Bremen', 'Stuttgart'))


if __name__ == '__main__':
    try:
        ADDRESS_COUNT = int(sys.argv[1])
    except IndexError:
        ADDRESS_COUNT = 10
    write('BEGIN;\n')
    write(drop_tables())
    write(create_tables())
    write(insert_cities())
    write(insert_addresses(ADDRESS_COUNT))
    write('COMMIT;')
