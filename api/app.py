from flask import Flask, request, jsonify
import json
from functools import wraps
from dbengine import DatabaseManager
from metastore import MetadataStore
from api_key_manager import load_api_keys

app = Flask(__name__)

# API Key Authentication
def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key:
            return jsonify({"error": "No API key provided"}), 401
        
        api_keys = load_api_keys()
        if api_key not in api_keys:
            return jsonify({"error": "Invalid API key"}), 401
        
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def hello_world():
	return jsonify({"message": "Hello, World!"})


@app.route('/connect', methods=['POST'])
def connect_to_database():
    try:
        data = request.get_json()
        
        conn_str = data.get('conn_str')
        db_type = data.get('db_type')
        username = data.get('username')
        password = data.get('password')
        host = data.get('host')
        port = data.get('port')
        database = data.get('database')
        workspace = data.get('workspace') # worksapce as worksapce id, mutable identifier
        workspace_name = data.get('workspace_name')
        
        # if connection_string is provided, ignore other parameters, otherwise create connection string for persistence
        if not conn_str and all([db_type, username, password, host, port, database]):
            conn_str = f"{db_type}://{username}:{password}@{host}:{port}/{database}"

        if not conn_str:
            raise ValueError("Insufficient parameters provided for database connection")
        
        # test connectivitity
        db_manager = DatabaseManager(connection_string=conn_str)
        tables = db_manager.get_tables()

        # if no exception, save the connection string of workspace
        save_conn_string(workspace or "default", conn_str)
        
        return jsonify({"tables": tables})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# TODO, may need to enhance to return a JSON, which contains other attributes for the worksapce, like workspace name, description, etc.
def get_conn_string(workspace=None):
    # use a special name to avoid confliction with worksapce name
    return MetadataStore("all-workspaces").query(workspace)


def save_conn_string(workspace, conn_str):
    MetadataStore("all-workspaces").insert_or_update(workspace, conn_str)


# return default workspace if workspace is not provided
def get_dbmanager(workspace):
    connection_string = get_conn_string(workspace or "default")
    return DatabaseManager(connection_string=connection_string)


@app.route('/workspaces', methods=['GET'])
def get_workspaces():
    # workspaces = list(conn_pool.keys())
    workspaces = [{"id": key, "name": key} for key in get_conn_string().keys()]
    return jsonify({"workspaces": workspaces})


@app.route('/<workspace>/<table>/fields', methods=['GET'])
def inspect_table(workspace, table):
    try:
        # Get connection string based on workspace
        db_manager = get_dbmanager(workspace)
        fields = db_manager.describe_table(table)
        
        return jsonify({"fields": fields})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/<workspace>/tables', methods=['GET'])
def inspect_workspace(workspace):
    try:
        db_manager = get_dbmanager(workspace)
        tables = db_manager.get_tables()

        return jsonify({"tables": tables})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# upsert metadata for a table in a workspace, request json format: {"table_name": "table1", "table_description": "table1 description", "fields": [{"name":"field name", "type": "field type, number|varcar|bool", "description": "field description"}]} 
@app.route('/<workspace>/<table>/metadata', methods=['POST'])
def save_metadata(workspace, table):
    try:
        data = request.get_json()
        if data.get('table_name') != table:
            raise ValueError("Table name in URL does not match table name in request body")
        MetadataStore(workspace).insert_or_update(data.get('table_name'), data)
        return jsonify({"message": "Metadata saved successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/<workspace>/<table>/metadata', methods=['GET'])
def get_metadata(workspace, table):
    try:
        data = MetadataStore(workspace).query(table)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

# return from metastore, {"table1": {"table_name": "table1", "table_description": "table description", "fields": [{"name":"field name", "type": "field type, number|varcar|bool", "description": "field description"}]}
@app.route('/<workspace>/metadata', methods=['GET'])
def get_all_metadata(workspace):
    try:
        data = MetadataStore(workspace).query()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# reall from database directly, contains everything
@app.route('/schema/<workspace>', methods=['GET'])
def get_whole_schema(workspace):
    try:
        db_manager = get_dbmanager(workspace)
        schema = db_manager.get_schema()

        return jsonify({"schema": schema})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/execute_sql', methods=['POST'])
def execute_sql():
    try:
        data = request.get_json()
        
        sql = data.get('sql')
        workspace = data.get('workspace')

        db_manager = get_dbmanager(workspace)
        result = db_manager.execute_query(sql)
        return jsonify({"data": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
	app.run(debug=True)