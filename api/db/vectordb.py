import weaviate
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, TypeVar, Generic, Optional, Type
import os
from dotenv import load_dotenv

# 配置管理
class Config:
    def __init__(self):
        load_dotenv()
        self.weaviate_url = os.getenv('WEAVIATE_URL')
        self.weaviate_api_key = os.getenv('WEAVIATE_API_KEY')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')

config = Config()

# 数据模型
@dataclass
class QuestionSql:
    question: str
    sql: str
    id: str = ""

@dataclass
class TermDesc:
    term: str
    desc: str
    id: str = ""

T = TypeVar('T', QuestionSql, TermDesc)

# 抽象类 VectorDB
class VectorDB(ABC, Generic[T]):
    @abstractmethod
    def insert(self, item: T) -> None:
        pass

    @abstractmethod
    def update(self, item: T) -> None:
        pass

    @abstractmethod
    def delete(self, item: T) -> None:
        pass

    @abstractmethod
    def get_all(self) -> List[T]:
        pass

    @abstractmethod
    def delete_all(self) -> None:
        pass

    @abstractmethod
    def batch_insert(self, items: List[T]) -> None:
        pass

    @abstractmethod
    def rebuild_collection(self, items: List[T]) -> None:
        pass

    @abstractmethod
    def search_similar(self, query: str, limit: int = 10) -> List[T]:
        pass

    @abstractmethod
    def search_exact(self, field: str, value: str) -> List[T]:
        pass


# Weaviate 实现类
class WeaviateDB(VectorDB[T]):
    def __init__(self, item_class: Type[T], workspace: str):
        self.workspace = workspace
        # actual class name is used when construct retruned object
        self.actual_class_name = item_class.__name__
        # file names are used to specifiy returned properties when search
        self.field_names = ["question", "sql"] if item_class.__name__ == "QuestionSql" else ["term", "desc"]
        # class name is the collection name used in vector store, use workspace as prefix. In weaviate, collection name must be unique when lowercased
        # weaviate.Client在返回result的时候，比如search，delete等方法，collection的首字母一直是大写，比如similar seach find: {'data': {'Get': {'Testproject3_questionsql': []}}}。所以collection名字都统一保持大写
        self.class_name = f"{workspace}_{self.actual_class_name}".upper()
        self.client = weaviate.Client(
            url=config.weaviate_url,
            auth_client_secret=weaviate.AuthApiKey(api_key=config.weaviate_api_key),
            additional_headers={
                "X-OpenAI-API-Key": config.openai_api_key
            }
        )
        
        self._ensure_schema(item_class)

    def _ensure_schema(self, item_class: Type[T]):
        try:
            # check if collection already exists
            self.client.schema.get(self.class_name)
            print(f"Class '{self.class_name}' already exists. Skipping creation.")
        except weaviate.exceptions.UnexpectedStatusCodeException as e:
            if e.status_code == 404:
                # # delete conflict collection， class names must be unique when lowercased', a workaround for now
                # try:
                #     possbile_conflict_collection = f"{self.workspace}_{self.actual_class_name}" 
                #     self.client.schema.delete_class(possbile_conflict_collection)
                #     print(f"delete conflict collection '{possbile_conflict_collection}'")
                # except weaviate.exceptions.UnexpectedStatusCodeException as e:
                #     if e.status_code != 404:
                #         print(f"error occured when delete collection: {e}")

                # create new collection
                schema = {
                    "classes": [{
                        "class": self.class_name,
                        "vectorizer": "text2vec-openai",
                        "properties": [
                            {"name": "question" if "QuestionSql" == self.actual_class_name else "term", "dataType": ["text"], "vectorizePropertyName": True},
                            {"name": "sql" if "QuestionSql" == self.actual_class_name else "desc", "dataType": ["text"], "vectorizePropertyName": False}
                        ]
                    }]
                }
                self.client.schema.create(schema)
                print(f"Created new class '{self.class_name}'.")
            else:
                print(f"Error: {e}")
                raise

    def insert(self, item: T) -> None:
        properties = {k: v for k, v in item.__dict__.items() if k != 'id'}
        item.id = self.client.data_object.create(
            data_object=properties,
            class_name=self.class_name
        )

    def update(self, item: T) -> None:
        if not item.id:
            raise ValueError("Cannot update item without id")
        properties = {k: v for k, v in item.__dict__.items() if k != 'id'}
        self.client.data_object.update(
            data_object=properties,
            class_name=self.class_name,
            uuid=item.id
        )

    def delete(self, item: T) -> None:
        if not item.id:
            raise ValueError("Cannot delete item without id")
        self.client.data_object.delete(
            uuid=item.id,
            class_name=self.class_name
        )

    def get_all(self) -> List[T]:
        result = self.client.data_object.get(
            class_name=self.class_name,
            with_vector=False
        )
        print(f"get all methond {result}")
        return [self._dict_to_object(obj) for obj in result['objects']]

    def delete_all(self) -> None:
        try:
            result = self.client.batch.delete_objects(
                class_name=self.class_name,
                where={
                    "operator": "NotEqual",
                    "valueString": "this_id_does_not_exist",
                    "path": ["id"]
                }
            )
            print(f"Deleted all objects from {self.class_name}")
            print(f"Deletion result: {result}")
        except Exception as e:
            print(f"An error occurred while deleting all objects: {e}")

    def batch_insert(self, items: List[T]) -> None:
        with self.client.batch as batch:
            for item in items:
                properties = {k: v for k, v in item.__dict__.items() if k != 'id'}
                item.id = batch.add_data_object(
                    data_object=properties,
                    class_name=self.class_name
                )

    def rebuild_collection(self, items: List[T]) -> None:
        self.delete_all()
        self.batch_insert(items)

    def search_similar(self, query: str, limit: int = 10) -> List[T]:
        result = (
            self.client.query
            .get(self.class_name, self.field_names)
            .with_near_text({"concepts": [query]})
            .with_limit(limit)
            .with_additional(['id'])
            .do()
        )
        print(f"search_similar methond: {result}")
        return [self._dict_to_object(obj) for obj in result['data']['Get'][self.class_name]]

    def search_exact(self, field: str, value: str) -> List[T]:
        result = (
            self.client.query
            .get(self.class_name, self.field_names)
            .with_where({
                "path": [field],
                "operator": "Equal",
                "valueString": value
            })
            .with_additional(['id'])
            .do()
        )
        return [self._dict_to_object(obj) for obj in result['data']['Get'][self.class_name]]

    # get_all and search_similar return different format
    # search_similar methond: {'data': {'Get': {'TESTPROJECT4_QUESTIONSQL': [{'_additional': {'id': '6940e1c7-1a42-4a50-bc69-af6fc2a7105a'}, 'question': 'What is the total sales for the year 2023?', 'sql': 'SELECT SUM(sales) FROM transactions WHERE YEAR(date) = 2023;'}]}}}
    # get all methond {'deprecations': [], 'objects': [{'class': 'TESTPROJECT4_QUESTIONSQL', 'creationTimeUnix': 1725994256057, 'id': 'bcaf9065-1698-47da-a1f9-647c9924b731', 'lastUpdateTimeUnix': 1725994256057, 'properties': {'question': 'What is the total sales for the year 2023?', 'sql': 'SELECT SUM(sales) FROM transactions WHERE YEAR(date) = 2023;'}, 'vectorWeights': None}], 'totalResults': 1}
    def _dict_to_object(self, obj: dict) -> T:
        if 'properties' in obj:
            properties = obj['properties']
            properties['id'] = obj['id'] 
        else:
            properties = {field: obj[field] for field in self.field_names}
            properties['id'] = obj['_additional']['id']
        if self.actual_class_name == "QuestionSql":
            return QuestionSql(**properties)
        elif self.actual_class_name == "TermDesc":
            return TermDesc(**properties)
        else:
            raise ValueError(f"Unknown class name: {self.actual_class_name}")



if __name__ == "__main__":
    question_sql_db = WeaviateDB(QuestionSql, workspace="unittest")

    question_sql_db.delete_all()

    # test connectivity
    try:
        new_question_sql = QuestionSql(
            question="What is the total sales for the year 2023?",
            sql="SELECT SUM(sales) FROM transactions WHERE YEAR(date) = 2023;"
        )
        question_sql_db.insert(new_question_sql)
        print(f"成功连接到 Weaviate 服务器并插入了一条记录。记录 ID: {new_question_sql.id}")
    except Exception as e:
        print(f"连接或插入失败: {str(e)}")


    # # test rebuild
    # new_questions = [
    #     QuestionSql(question="How many customers do we have?", sql="SELECT COUNT(*) FROM customers;"),
    #     QuestionSql(question="What's our best-selling product?", sql="SELECT product_name, SUM(quantity) as total_sold FROM sales GROUP BY product_name ORDER BY total_sold DESC LIMIT 1;")
    # ]
    # question_sql_db.rebuild_collection(new_questions)

    # retrieve all    
    allPairs = question_sql_db.get_all()
    print(f"retrieved {len(allPairs)}")
    for p in allPairs:
        print(f"{p}")

    # search
    similar_questions = question_sql_db.search_similar("What are our total sales?", limit=2)
    print(f"Similar questions found: {similar_questions} ")
    for q in similar_questions:
        print(f"- Question: {q.question}")
        print(f"  SQL: {q.sql}")
        print(f"  ID: {q.id}")
