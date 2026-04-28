# 使用 LangGraph 官方提供的 Python 3.11 基础镜像
FROM langchain/langgraph-api:3.11

# ============================================
# 添加非 pip 包依赖: all_agent_study
# ============================================

# 将当前目录（构建上下文）的所有内容复制到容器内的依赖目录中
# 这个目录存放用户自定义的 agent 代码
ADD . /deps/outer-all_agent_study/src
RUN pip install langchain_openai -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 创建一个动态生成 pyproject.toml 文件的脚本块
# set -ex: 执行时显示每条命令，遇到错误立即退出
RUN set -ex && \
    # 循环写入 pyproject.toml 的配置内容
    for line in '[project]' \           # 项目配置段
                'name = "all_agent_study"' \  # 项目名称
                'version = "0.1"' \           # 项目版本
                '[tool.setuptools.package-data]' \  # setuptools 包数据配置
                '"*" = ["**/*"]' \                # 包含所有文件作为包数据
                '[build-system]' \                # 构建系统配置段
                'requires = ["setuptools>=61"]' \ # 构建依赖
                'build-backend = "setuptools.build_meta"'; do \  # 构建后端
        # 将每一行写入 /deps/outer-all_agent_study/pyproject.toml
        echo "$line" >> /deps/outer-all_agent_study/pyproject.toml; \
    done
# 这样做的目的是让用户代码可以被 pip 以可编辑模式安装

# ============================================
# 安装所有本地依赖
# ============================================

# 遍历 /deps 目录下的所有子目录
RUN for dep in /deps/*; do             \
        echo "Installing $dep";        \
        # 检查是否为目录
        if [ -d "$dep" ]; then         \
            echo "Installing $dep";    \
            # 进入依赖目录，使用 uv 包管理器以可编辑模式安装
            # -e: 可编辑模式安装（develop mode）
            # --system: 安装到系统 Python 环境
            # --no-cache-dir: 不使用缓存
            # -c /api/constraints.txt: 使用约束文件锁定版本
            (cd "$dep" && PYTHONDONTWRITEBYTECODE=1 uv pip install --system --no-cache-dir -c /api/constraints.txt -e .); \
        fi;                            \
    done

# ============================================
# 配置 LangServe 图（Graph）入口
# ============================================

# 设置环境变量，告诉 LangGraph API 服务的图定义位置
# JSON 格式：键为图名称，值为 Python 模块路径
# 指向 all_agent.py 文件中的 agent 变量
ENV LANGSERVE_GRAPHS='{"agent": "/deps/outer-all_agent_study/src/all_agent.py:agent"}'

# ============================================
# 确保用户依赖没有意外覆盖 langgraph-api
# ============================================

# 创建必要的目录和空的 __init__.py 文件
# 确保 langgraph_api、langgraph_runtime、langgraph_license 包结构存在
RUN mkdir -p /api/langgraph_api /api/langgraph_runtime /api/langgraph_license && \
    touch /api/langgraph_api/__init__.py /api/langgraph_runtime/__init__.py /api/langgraph_license/__init__.py

# 重新安装 langgraph-api 自身（以可编辑模式）
# --no-deps: 不安装依赖（避免覆盖用户安装的依赖）
# 这样可以确保 langgraph-api 的核心代码不会被用户依赖中的同名包覆盖
RUN PYTHONDONTWRITEBYTECODE=1 uv pip install --system --no-cache-dir --no-deps -e /api

# ============================================
# 从最终镜像中移除构建工具和包管理器
# ============================================

# 卸载 pip、setuptools、wheel（构建工具）
RUN pip uninstall -y pip setuptools wheel

# 删除残留的 pip/setuptools/wheel 文件和目录（系统级 Python）
# || true: 即使删除失败也继续执行（防止镜像构建失败）
RUN rm -rf /usr/local/lib/python*/site-packages/pip* \
           /usr/local/lib/python*/site-packages/setuptools* \
           /usr/local/lib/python*/site-packages/wheel* && \
    find /usr/local/bin -name "pip*" -delete || true

# 删除系统 Python 目录中的构建工具
RUN rm -rf /usr/lib/python*/site-packages/pip* \
           /usr/lib/python*/site-packages/setuptools* \
           /usr/lib/python*/site-packages/wheel* && \
    find /usr/bin -name "pip*" -delete || true

# 使用 uv 包管理器卸载构建工具，并删除 uv 可执行文件本身
# 最终镜像中不保留任何包管理工具（减小镜像体积，提高安全性）
# 项目中的excel-mcp用到了uv, 所以保留uv
# RUN uv pip uninstall --system pip setuptools wheel && \
#    rm /usr/bin/uv /usr/bin/uvx

# ============================================
# 设置工作目录
# ============================================

# 将工作目录切换到用户 agent 代码所在目录
# 这样运行时可以方便地访问用户代码和相对路径资源
WORKDIR /deps/outer-all_agent_study/src