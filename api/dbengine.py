from sqlalchemy import MetaData, create_engine, text, inspect
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.engine import URL
from sqlalchemy.schema import CreateTable
from contextlib import contextmanager
import re

class DatabaseManager:
    def __init__(self, connection_string=None, db_type=None, username=None, password=None, host=None, port=None, database=None):
        if connection_string:
            self.connection_string = connection_string
        elif all([db_type, username, password, host, port, database]):
            self.connection_string = f"{db_type}://{username}:{password}@{host}:{port}/{database}"
        else:
            raise ValueError("Insufficient parameters provided for database connection")
        self.engine = create_engine(self.connection_string)

    @contextmanager
    def _get_connection(self):
        connection = self.engine.connect()
        try:
            yield connection
        finally:
            connection.close()

    # can only execute query, other functions are forbidden
    # only return maxium 100 rows
    def execute_query(self, query, params=None):
        with self._get_connection() as conn:
            try:
                if not self._is_safe_query(query):
                    raise ValueError("SQL contains dangerous operations")

                # need convert sqlalchemy Row to dict type to avoid exception when jsonify it, sqlalchemy Row is not serializable
                result = conn.execute(text(query), params or {})
                return [row._asdict() for row in result.fetchmany(100)]
            except SQLAlchemyError as e:
                print(f"An error occurred: {e}")
                return None

    def is_connected(self):
        try:
            with self._get_connection() as conn:
                return True
        except SQLAlchemyError:
            return False

    def get_tables(self):
        with self._get_connection() as conn:
            try:
                inspector = inspect(conn)
                tables = inspector.get_table_names()
                return tables
            except SQLAlchemyError as e:
                print(f"An error occurred: {e}")
                return None


    # get schema of all tables, need to change to only return schema for select ones       
    def get_schema(self):
        with self._get_connection() as conn:
            try:
                metadata = MetaData()
                metadata.reflect(bind=self.engine)
                inspector = inspect(conn)

                # use \ before \n to escape newline in json response
                result = ""
                for table_name in metadata.tables:
                    result += f"{table_name}:\\n"
                    columns = inspector.get_columns(table_name)

                    for column in columns:
                        column_name = column['name']
                        column_type = str(column['type'])
                        column_comment = str(column['comment'])
                        result += f"{column_name}, {column_type}, {column_comment};\\n"

                    result += "\n"
                return result
            except SQLAlchemyError as e:
                print(f"An error occurred: {e}")
                return None


    def describe_table(self, table_name):
        with self._get_connection() as conn:
            try:
                # <class 'sqlalchemy.sql.sqltypes.VARCHAR'> will cause error when jsonify it, do str() convert for every value
                inspector = inspect(conn)
                columns = inspector.get_columns(table_name)
                return [{k: str(v) for k, v in column.items()} for column in columns]
            except SQLAlchemyError as e:
                print(f"An error occurred: {e}")
                return None

    
    def _is_safe_query(self, query):
        # remove comments
        query = re.sub(r'--.*$', '', query, flags=re.MULTILINE)
        query = re.sub(r'/\*.*?\*/', '', query, flags=re.DOTALL)
        
        # 转convedrt to uppercase
        query_upper = query.upper()
        
        # inspect dangerous operations
        dangerous_operations = ['INSERT', 'UPDATE', 'DELETE', 'DROP', 'TRUNCATE', 'ALTER', 'CREATE', 'REPLACE']
        for op in dangerous_operations:
            if re.search(r'\b' + op + r'\b', query_upper):
                return False
        
        # makesure the query starts with WITH or SELECT
        if not re.match(r'^\s*(WITH|SELECT)', query_upper):
            return False
        
        return True


if __name__ == "__main__":
    db_manager = DatabaseManager(connection_string=r"postgresql://datagpt:datagpt@localhost/datagpt")
    query = "SELECT * FROM salesdata"
    results = db_manager.execute_query(query)
    print(results)
