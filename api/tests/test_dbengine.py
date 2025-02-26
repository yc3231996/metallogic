import unittest
from db.dbengine import DatabaseManager


class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        # Set up the DatabaseManager instance with a test connection string
        self.db_manager = DatabaseManager(connection_string=r"postgresql://datagpt:datagpt@localhost/datagpt")

    def test_is_connected(self):
        # Test if the database manager is connected
        self.assertTrue(self.db_manager.is_connected())

    def test_get_tables(self):
        # Test getting tables from the database
        tables = self.db_manager.get_tables()
        self.assertIsNotNone(tables)
        self.assertIsInstance(tables, list)

    def test_describe_table(self):
        # Test describing a table in the database
        table_name = "salesdata"
        fields = self.db_manager.describe_table(table_name)

        print("describe table:", fields)
        for field in fields:
            print(type(field), field)

        self.assertIsNotNone(fields)
        self.assertIsInstance(fields, list)

    def test_execute_query(self):
        # Test executing a query on the database
        query = "SELECT * FROM salesdata"
        results = self.db_manager.execute_query(query)

        print(query, ":")
        if results:
            for row in results:
                print(type(row), row)

        self.assertIsNotNone(results)
        self.assertIsInstance(results, list)

    def test_execute_query_with_params(self):
        # Test executing a query with parameters on the database
        '''
        "SELECT * FROM salesdata WHERE year = :year"
        params = {"year": 2022}
        '''
        query = "SELECT * FROM salesdata"
        results = self.db_manager.execute_query(query)
        self.assertIsNotNone(results)
        self.assertIsInstance(results, list)

if __name__ == "__main__":
    unittest.main()
