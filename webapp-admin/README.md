This is a [Next.js](https://nextjs.org/) project bootstrapped with [`create-next-app`](https://github.com/vercel/next.js/tree/canary/packages/create-next-app).

## Getting Started
change backend settings in config/index.ts
yarn dev

## 使用docker-compose启动
docker build -t yc3231996/metallogic-admin:latest .
docker push yc3231996/metallogic-admin:latest
docker run -d -p 3000:3000 -e API_BASE_URL=http://host.docker.internal:5000 -e API_KEY=p2QtZ91ujRN2db0OyVWPXmvmv7e9zQLBswOiL4REZcY yc3231996/metallogic-admin:latest
docker run -d -p 3000:3000 --env-file .env.local yc3231996/metallogic-admin:latest


## 使用shadcn/ui 库
### 第一次先初始化
npx shadcn-ui@latest init
### 添加组件
npx shadcn-ui@latest add toast