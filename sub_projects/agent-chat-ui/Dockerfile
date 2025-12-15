# 使用Node.js 24作为基础镜像
FROM node:24-alpine

# 设置工作目录
WORKDIR /app

# 安装pnpm
RUN npm install -g pnpm

# 复制项目文件（.dockerignore会排除.env文件）
COPY . .

# 安装依赖
RUN pnpm install --frozen-lockfile

# 构建生产版本
RUN pnpm build


# 启动应用
CMD ["pnpm", "start"]
