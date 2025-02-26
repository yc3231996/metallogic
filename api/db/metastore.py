import json
import os

# use worksapce_id as filename
# not thread safe, add lock ilater
class MetadataStore:
    def __init__(self, filename):
        self._ensure_directory_exists()
        self.filename = filename  
        self.filepath = os.path.join(self.basepath, filename)
        self._ensure_file_exists()
    
    def _ensure_directory_exists(self):
        base_path = os.getenv('METASTORE_PATH')
        if not base_path:
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'metastore'))
        self.basepath = base_path
        os.makedirs(self.basepath, exist_ok=True)
        print(f"Metadata store directory at {self.basepath}")

    def _ensure_file_exists(self):
        try:
            if not os.path.exists(self.filepath):
                with open(self.filepath, 'w') as f:
                    json.dump({}, f)
                    print(f"Metadata store file at {self.filepath}")
        except Exception as e:
            print(f"Error creating file: {e}")

    @staticmethod
    def check_workspace_exist(workspace: str) -> None:
        all_workspaces = MetadataStore("all-workspaces").query()
        if workspace not in all_workspaces:
            raise ValueError(f"workspace '{workspace}' not exist")

    def _load_store(self):
        with open(self.filepath, 'r') as f:
            return json.load(f)

    def _save_store(self, store):
        with open(self.filepath, 'w') as f:
            json.dump(store, f, indent=2)

    def insert_or_update(self, table_name, ddl):
        store = self._load_store()
        store[table_name] = ddl
        self._save_store(store)

    def query(self, table_name=None):
        store = self._load_store()
        if table_name:
            return store.get(table_name)
        return store

    def delete(self, table_name=None):
        store = self._load_store()
        if table_name:
            if table_name in store:
                del store[table_name]
                self._save_store(store)
                return True
            return False
        else:
            self._save_store({})
            return True


if __name__ == "__main__":
    metadata_store = MetadataStore("test_metastore.text")

    metadata_store.insert_or_update("users", "CREATE TABLE users (id INT PRIMARY KEY, name VARCHAR(100), email VARCHAR(100))")
    metadata_store.insert_or_update("orders", "CREATE TABLE orders (id INT PRIMARY KEY, user_id INT, product VARCHAR(100), quantity INT)")
    metadata_store.insert_or_update("users", "CREATE TABLE users2 (id INT PRIMARY KEY, name VARCHAR(100), email VARCHAR(100))")

    print(metadata_store.query("users"))
    print(metadata_store.query())