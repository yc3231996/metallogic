from sqlalchemy import MetaData, create_engine, text, inspect
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
import re
from sqlalchemy.pool import QueuePool
from threading import Lock

# 支持SQL数据库
class DatabaseManager:
    _instances = {}  # 用于缓存DatabaseManager实例
    _lock = Lock()   # 用于线程同步

    def __init__(self, connection_string=None, db_type=None, username=None, password=None, host=None, port=None, database=None):
        if connection_string:
            self.connection_string = connection_string
        elif all([db_type, username, password, host, port, database]):
            self.connection_string = f"{db_type}://{username}:{password}@{host}:{port}/{database}"
        else:
            raise ValueError("Insufficient parameters provided for database connection")
        
        self._create_engine()

    def _create_engine(self):
        self.engine = create_engine(
            self.connection_string,
            poolclass=QueuePool,
            pool_size=5,  # 连接池的大小
            max_overflow=10,  # 超过pool_size后的最大连接数
            pool_timeout=30,  # 获取连接的超时时间
            pool_recycle=1800  # 连接重置时间，防止连接过期
        )

    @classmethod
    def get_instance(cls, connection_string):
        """
        获取DatabaseManager实例的线程安全方法
        如果实例不存在或已失效，则创建新实例
        """
        with cls._lock:
            instance = cls._instances.get(connection_string)
            
            # 检查实例是否存在且连接是否有效
            if instance is not None:
                try:
                    if instance.is_connected():
                        return instance
                except Exception:
                    # 如果连接检查失败，删除现有实例并创建新实例
                    if connection_string in cls._instances:
                        try:
                            cls._instances[connection_string].engine.dispose()
                        except:
                            pass
                        del cls._instances[connection_string]
            
            try:
                # 创建新实例
                instance = cls(connection_string=connection_string)
                if instance.is_connected():
                    cls._instances[connection_string] = instance
                    return instance
                else:
                    raise SQLAlchemyError("Failed to establish database connection")
            except Exception as e:
                raise SQLAlchemyError(f"Failed to create database instance: {str(e)}")

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
    # db_manager = DatabaseManager(connection_string=r"postgresql://datagpt:datagpt@localhost/datagpt")
    db_manager = DatabaseManager(connection_string=r"postgresql://postgres.ntzacakldnwbrjuuvlyg:KUgmcvYUwQmb4b8s@aws-0-us-west-1.pooler.supabase.com:6543/postgres")
    query = "SELECT * FROM test"
    results = db_manager.execute_query(query)
    print(results)
