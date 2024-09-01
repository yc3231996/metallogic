## API KEY管理
生成新的 API 密钥：python api_key_manager.py generate <user_id>
删除 API 密钥：python api_key_manager.py delete <api_key>
列出所有 API 密钥：python api_key_manager.py list
在发送请求时，在请求头中添加 'X-API-Key' 字段，值为有效的 API 密钥

## metastore
metastore存放的路径由环境变量“METASTORE_PATH”指定
如果没有这个环境变量，则会在程序运行的当前目录下新建一个名为"metastore"作为存储目录(所以，项目中这个文件夹应该加入gitignore)
metastore目录下，名为all-worksapces的文件存储了当前所有的workspace，格式如下:
  ```
  {"ws-name1": "db_type://username:password@host:port/database", "ws-name2": "postgresql://datagpt:datagpt@localhost/datagpt"}
  ```
metastore目录下，每一个workspace都一个同名的文件，为存储该workspace的元数据存储文件，格式如下：
  ```
    {
    "table_name": {
        "fields": [
        {
            "autoincrement": "False",
            "comment": "\u9500\u552e\u91d1\u989d",
            "default": "None",
            "description": "\u9500\u552e\u91d1\u989d",
            "name": "amount",
            "nullable": "False",
            "type": "NUMERIC(10, 2)"
        }],
        "table_description": "",
        "table_name": "productionplan"
        }
    }
  ```


## 使用docker-compose启动
docker build -t yc3231996/metallogic-api:latest .
docker push yc3231996/metallogic-api:latest
docker run -p 8000:8000 yc3231996/metallogic-api:latest 
