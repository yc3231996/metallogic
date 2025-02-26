from google.cloud import bigquery
from google.oauth2 import service_account
from contextlib import contextmanager
import re
import os
import json
from threading import Lock

# for google bigquery
class BigQueryManager:
    _instances = {}  # 用于缓存BigQueryManager实例
    _lock = Lock()   # 用于线程同步

    def __init__(self, project_id, credentials_json_str):
        """
        初始化 BigQuery 管理器
        :param project_id: Google Cloud 项目 ID
        :param credentials_json_str: 服务账号凭证的 JSON 字符串
        """
        self.project_id = project_id
        self.credentials_json_str = credentials_json_str
        self._create_client()

    def _create_client(self):
        """创建BigQuery客户端"""
        try:
            # 将JSON字符串转换为字典对象
            credentials_info = json.loads(self.credentials_json_str)
            credentials = service_account.Credentials.from_service_account_info(credentials_info)
            self.client = bigquery.Client(
                credentials=credentials,
                project=self.project_id if self.project_id else credentials.project_id,
            )
        except Exception as e:
            raise Exception(f"Failed to create BigQuery client: {str(e)}")

    @classmethod
    def get_instance(cls, project_id, credentials_json_str):
        """
        获取BigQueryManager实例的线程安全方法
        使用credentials_json_str的哈希值作为缓存键
        """
        # 创建简单的缓存键
        cache_key = f"{project_id}:{hash(credentials_json_str)}"
        
        with cls._lock:
            instance = cls._instances.get(cache_key)
            
            # 检查实例是否存在且可用
            if instance is not None:
                try:
                    # 简单的可用性测试
                    instance.client.list_datasets(max_results=1)
                    return instance
                except Exception:
                    # 如果客户端不可用，删除现有实例
                    if cache_key in cls._instances:
                        del cls._instances[cache_key]
            
            try:
                # 创建新实例
                instance = cls(project_id, credentials_json_str)
                # 测试连接
                instance.client.list_datasets(max_results=1)
                cls._instances[cache_key] = instance
                return instance
            except Exception as e:
                raise Exception(f"Failed to create BigQuery instance: {str(e)}")

    def execute_query(self, query, params=None, max_rows=100):
        """
        执行 BigQuery SQL 查询
        :param query: SQL 查询语句
        :param params: 查询参数
        :param max_rows: 最大返回行数
        :return: 查询结果列表
        """
        try:
            if not self._is_safe_query(query):
                raise ValueError("SQL contains dangerous operations")

            job_config = bigquery.QueryJobConfig(
                query_parameters=params if params else []
            )
            
            query_job = self.client.query(query, job_config=job_config)
            
            # 获取结果
            rows = query_job.result(max_results=max_rows)
            
            # 转换结果为字典列表
            results = [dict(row.items()) for row in rows]
            return results

        except Exception as e:
            print(f"执行查询时发生错误: {e}")
            return None

    def get_tables(self, dataset_id=None):
        """
        获取表列表
        :param dataset_id: 数据集 ID（可选）
        :return: 表名列表，格式为 "dataset.table_name"
        """
        try:
            if dataset_id:
                tables = self.client.list_tables(dataset_id)
                return [f"{dataset_id}.{table.table_id}" for table in tables]
            else:
                datasets = list(self.client.list_datasets())
                all_tables = []
                for dataset in datasets:
                    tables = self.client.list_tables(dataset.dataset_id)
                    all_tables.extend([f"{dataset.dataset_id}.{table.table_id}" for table in tables])
                return all_tables
        except Exception as e:
            print(f"获取表列表时发生错误: {e}")
            return None

    def describe_table(self, table_ref, dataset_id=None):
        """
        获取表结构
        :param table_ref: 表ID，如果dataset_id未提供，则格式应为"dataset.table_name"
        :param dataset_id: 数据集 ID（可选）
        :return: 表结构描述（列表格式）
        """
        try:
            if dataset_id:
                table = self.client.get_table(self.client.dataset(dataset_id).table(table_ref))
            else:
                # 解析 dataset.table_name 格式
                dataset_id, table_id = table_ref.split('.')
                table = self.client.get_table(self.client.dataset(dataset_id).table(table_id))
            
            schema_info = []
            for field in table.schema:
                schema_info.append({
                    'name': field.name,
                    'type': str(field.field_type),
                    'comment': field.description or 'No description',
                    'nullable': field.is_nullable
                })
            
            return schema_info
        except Exception as e:
            print(f"获取表结构时发生错误: {e}")
            return None

    def _is_safe_query(self, query):
        """
        检查查询是否安全（只允许 SELECT 语句）
        :param query: SQL 查询语句
        :return: 布尔值表示查询是否安全
        """
        # 移除注释
        query = re.sub(r'--.*$', '', query, flags=re.MULTILINE)
        query = re.sub(r'/\*.*?\*/', '', query, flags=re.DOTALL)
        
        # 转换为大写
        query_upper = query.upper()
        
        # 检查危险操作
        dangerous_operations = ['INSERT', 'UPDATE', 'DELETE', 'DROP', 'TRUNCATE', 'ALTER', 'CREATE', 'REPLACE']
        for op in dangerous_operations:
            if re.search(r'\b' + op + r'\b', query_upper):
                return False
        
        # 确保查询以 WITH 或 SELECT 开头
        if not re.match(r'^\s*(WITH|SELECT)', query_upper):
            return False
        
        return True

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    credentials_path = os.path.join(current_dir, "config", "gen-lang-client-0786739350-9300cb3f1bc9.json")
    # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
    
    # 读取凭证文件内容
    with open(credentials_path, 'r') as f:
        credentials_json_str = f.read()
    
    # 使用凭证字符串初始化
    bq_manager = BigQueryManager(
        project_id = "gen-lang-client-0786739350",
        credentials_json_str = credentials_json_str
    )
    
    # 测试查询
    query = "SELECT * FROM `ODS.tiktok_ad_ods` LIMIT 1"
    results = bq_manager.execute_query(query)
    print(results) 

    # # 测试获取表列表
    # print("\n测试获取表列表：")
    # dataset_id = "ODS"
    # tables = bq_manager.get_tables(dataset_id)
    # print(f"数据集 {dataset_id} 中的表：")
    # for table in tables:
    #     print(f"- {table}")
    #     # 获取并打印表结构
    #     schema = bq_manager.describe_table(table)
    #     print(f"表结构：\n{schema}\n")

    print("\n获取所有表：")
    tables = bq_manager.get_tables()
    print(tables)