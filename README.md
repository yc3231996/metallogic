# metallogic

# local env prepare
1. install docker and docker compose
2. webapp depends on backend servers, can use cloud services or run them locally using docker




## 在 Docker Compose 文件的同级目录创建一个 .env 文件，Docker Compose 会自动读取这个文件中的变量。
启动的时候，注意用-d， docker compose up -d


## some experenence:
be carefule with volume when run in docker compose model, specially web project, don't mount /app, to avoid ovrride prdocution files
variable starts with NEXT_PUBLIC will be needed in build time and included in client code, will not work in provide in run time 
ignored build issues in webapp-conversation project, configured in next.config.js, need to fix all before production
