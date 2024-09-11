# FROM --platform=linux/amd64 node:19-bullseye-slim

# WORKDIR /app

# COPY . .

# RUN yarn install
# RUN yarn build

# EXPOSE 3000

# CMD ["yarn","start"]



# 构建阶段
FROM --platform=linux/amd64 node:19-bullseye-slim AS builder

WORKDIR /app

# 复制 package.json 和 yarn.lock（如果存在）
COPY package.json yarn.lock* ./

# 安装依赖
RUN yarn install --frozen-lockfile

# 复制源代码, and make sure env file gets copied
COPY . .
COPY .env.production .env.production

# 构建应用
RUN yarn build

# 生产阶段
FROM --platform=linux/amd64 node:19-bullseye-slim

WORKDIR /app

# 复制构建阶段的产物和必要文件
COPY --from=builder /app/next.config.js ./
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

# 设置环境变量, affect .env.$(NODE_ENV)
ENV NODE_ENV production

# 暴露端口
EXPOSE 3000

# 启动命令
CMD ["yarn", "start"]