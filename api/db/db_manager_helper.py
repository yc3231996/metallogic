import json
from .dbengine import DatabaseManager
from .bigquery import BigQueryManager
from .metastore import MetadataStore

def get_dbmanager(workspace):
    """
    根据workspace获取适当的数据库管理器实例
    
    Args:
        workspace (str): 工作区名称
        
    Returns:
        DatabaseManager or BigQueryManager: 数据库管理器实例
        
    Raises:
        Exception: 如果获取数据库管理器失败
    """
    conn_info_str = MetadataStore("all-workspaces").query(workspace)
    
    try:
        # 尝试解析连接信息
        conn_info = json.loads(conn_info_str)
        
        if not isinstance(conn_info, dict):
            # 如果不是字典，则可能是旧格式的连接字符串
            return DatabaseManager.get_instance(conn_info_str)
        
        # 根据类型创建相应的数据库管理器
        if conn_info.get('type') == 'bigquery':
            return BigQueryManager.get_instance(
                project_id=conn_info.get('project_id'),
                credentials_json_str=conn_info.get('credentials_json_str')
            )
        else:
            # 其他类型的数据库使用conn_str
            return DatabaseManager.get_instance(conn_info.get('conn_str'))
            
    except json.JSONDecodeError:
        # 兼容旧格式：如果不是JSON，则假定为普通的连接字符串
        return DatabaseManager.get_instance(conn_info_str)
    except Exception as e:
        # 处理其他异常
        raise Exception(f"Failed to get database manager: {str(e)}") 