from flask import Flask, request, jsonify, current_app
import json
import logging
import traceback
from functools import wraps
from dbengine import DatabaseManager
from metastore import MetadataStore
from api_key_manager import load_api_keys
from vectordb import QuestionSql, WeaviateDB

app = Flask(__name__)

# API Key Authentication. make sure put this decorator after 
def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key:
            logging.warning("API request without key")
            return jsonify({"error": "No API key provided"}), 401
        
        api_keys = load_api_keys()
        if api_key not in api_keys:
            logging.warning(f"Invalid API key used: {api_key}")
            return jsonify({"error": "Invalid API key"}), 401
        
        current_app.logger.info(f"API request with valid key: {api_key}")
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
@require_api_key
def hello_world():
    return jsonify({"message": "Hello, World!"})
	

@app.route('/connect', methods=['POST'])
@require_api_key
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

        # if no exception, UPSERT connection string for the workspace
        _save_workspace(workspace or "default", conn_str)
        
        return jsonify({"tables": tables})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# TODO, need to enhance to return a JSON other than just workspace id, which contains other attributes like workspace name, description, etc.
def _get_workspace(workspace=None):
    # return all workspaces if workspace=None. 
    return MetadataStore("all-workspaces").query(workspace)


def _save_workspace(workspace, conn_str):
    MetadataStore("all-workspaces").insert_or_update(workspace, conn_str)


def _del_workspace(workspace):
    # Delete connection string
    ws_exist = MetadataStore("all-workspaces").delete(workspace)
    # Delete metadata file content if exists, but will keep the file
    if ws_exist:
        MetadataStore(workspace).delete()


# return true if exists
def _check_workspace_exist(workspace):
    all_workspaces = MetadataStore("all-workspaces").query()
    if workspace not in all_workspaces:
        raise ValueError(f"workspace '{workspace}' not exist")


# return default workspace if workspace is not provided
def get_dbmanager(workspace):
    connection_string = _get_workspace(workspace or "default")
    return DatabaseManager(connection_string=connection_string)


@app.route('/workspaces', methods=['GET'])
@require_api_key
def get_workspaces():
    workspaces = [{"id": key, "name": key} for key in _get_workspace().keys()]
    return jsonify({"workspaces": workspaces})


@app.route('/workspace/<workspace>', methods=['DELETE'])
@require_api_key
def del_workspace(workspace):    
    if not workspace:
        return jsonify({"error": "Workspace parameter not provided"}), 400
    try:
        _check_workspace_exist(workspace)
        _del_workspace(workspace)
        return jsonify({"message": f"Workspace '{workspace}' successfully deleted"})
    except Exception as e:
        return jsonify({"error": f"Error deleting workspace: {str(e)}"}), 500



@app.route('/<workspace>/<table>/fields', methods=['GET'])
@require_api_key
def inspect_table(workspace, table):
    try:
        # Get connection string based on workspace
        db_manager = get_dbmanager(workspace)
        fields = db_manager.describe_table(table)
        
        return jsonify({"fields": fields})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/<workspace>/tables', methods=['GET'])
@require_api_key
def inspect_workspace(workspace):
    try:
        db_manager = get_dbmanager(workspace)
        tables = db_manager.get_tables()

        return jsonify({"tables": tables})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# upsert metadata for a table in a workspace, request json format: {"table_name": "table1", "table_description": "table1 description", "fields": [{"name":"field name", "type": "field type, number|varcar|bool", "description": "field description"}]} 
@app.route('/<workspace>/<table>/metadata', methods=['POST'])
@require_api_key
def save_metadata(workspace, table):
    try:
        data = request.get_json()
        if data.get('table_name') != table:
            raise ValueError("Table name in URL does not match table name in request body")

        _check_workspace_exist(workspace)

        MetadataStore(workspace).insert_or_update(data.get('table_name'), data)
        return jsonify({"message": "Metadata saved successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/<workspace>/<table>/metadata', methods=['GET'])
@require_api_key
def get_metadata(workspace, table):
    try:
        _check_workspace_exist(workspace)

        data = MetadataStore(workspace).query(table)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

# return from metastore, {"table1": {"table_name": "table1", "table_description": "table description", "fields": [{"name":"field name", "type": "field type, number|varcar|bool", "description": "field description"}]}
@app.route('/<workspace>/metadata', methods=['GET'])
@require_api_key
def get_all_metadata(workspace):
    try:
        _check_workspace_exist(workspace)

        data = MetadataStore(workspace).query()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Legacy code, retrieve from database directly, contains everything
@app.route('/schema/<workspace>', methods=['GET'])
@require_api_key
def get_whole_schema(workspace):
    try:
        
        db_manager = get_dbmanager(workspace)
        schema = db_manager.get_schema()

        return jsonify({"schema": schema})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/execute_sql', methods=['POST'])
@require_api_key
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


# get all QuestionSql from vector store
@app.route('/<workspace>/question_sql', methods=['GET'])
@require_api_key
def get_all_question_sql(workspace):
    try:
        _check_workspace_exist(workspace)

        question_sql_db = WeaviateDB(QuestionSql, workspace)
        all_question_sql = question_sql_db.get_all()
        return jsonify({
            "data": [{
                "id": qs.id,
                "question": qs.question,
                "sql": qs.sql
            } for qs in all_question_sql]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# rebuild QuestionSql
@app.route('/<workspace>/question_sql/rebuild', methods=['POST'])
@require_api_key
def rebuild_question_sql(workspace):
    try:
        _check_workspace_exist(workspace)

        data = request.get_json()
        question_sql_list = data.get('question_sql_list', [])
        
        if not question_sql_list:
            return jsonify({"error": "QuestionSql list is empty"}), 400
        
        question_sql_objects = [
            QuestionSql(question=item['question'], sql=item['sql'])
            for item in question_sql_list
        ]
        
        question_sql_db = WeaviateDB(QuestionSql, workspace)
        question_sql_db.rebuild_collection(question_sql_objects)
        
        return jsonify({"message": "QuestionSql rebuild successfully", "count": len(question_sql_objects)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# search QuestionSql based on question,
@app.route('/<workspace>/question_sql/search', methods=['POST'])
@require_api_key
def search_question_sql(workspace):
    try:
        _check_workspace_exist(workspace)

        data = request.get_json()
        question = data.get('question')
        
        if not question:
            return jsonify({"error": "Question is empty"}), 400
        
        question_sql_db = WeaviateDB(QuestionSql, workspace)
        results = question_sql_db.search_similar(question, 3)
        
        # not contain score, may need to enhance to contain score, certainty, distance
        return jsonify({
            "data": [{
                "id": result.id,
                "question": result.question,
                "sql": result.sql
            } for result in results]
        })
    except Exception as e:
        current_app.logger.error(f"Error in execute_sql: {str(e)}")
        current_app.logger.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
	app.run(debug=True)