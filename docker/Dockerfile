FROM langchain/langgraph-api:3.11

# -- Adding non-package dependency all_agent_study --
ADD . /deps/outer-all_agent_study/src
# 安装依赖
# ！！1. 安装requirements.txt中的依赖
RUN pip install -r /deps/outer-all_agent_study/src/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

# ！！2. 装pdf引擎
# 设置非交互式安装
ENV DEBIAN_FRONTEND=noninteractive

# 使用清华大学镜像源加速（如果在中国）
RUN sed -i 's/archive.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list || \
    sed -i 's/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list || true

# 安装基础包和XeLaTeX
# 时间太慢, 分层安装
RUN apt-get update && apt-get install -y curl pandoc
RUN apt-get install -y  texlive-xetex
RUN apt-get install -y  texlive-latex-base
RUN apt-get install -y  texlive-fonts-recommended
RUN apt-get install -y  lmodern
RUN apt-get install -y  fonts-wqy-microhei
RUN apt-get install -y  fonts-wqy-zenhei


# 第二层：安装中文支持（需要重新 update）
RUN apt-get update && apt-get install -y \
    texlive-lang-chinese \
    fonts-noto-cjk \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*




RUN set -ex && \
    for line in '[project]' \
                'name = "all_agent_study"' \
                'version = "0.1"' \
                '[tool.setuptools.package-data]' \
                '"*" = ["**/*"]' \
                '[build-system]' \
                'requires = ["setuptools>=61"]' \
                'build-backend = "setuptools.build_meta"'; do \
        echo "$line" >> /deps/outer-all_agent_study/pyproject.toml; \
    done
# -- End of non-package dependency all_agent_study --



# -- Installing all local dependencies --

RUN for dep in /deps/*; do             echo "Installing $dep";             if [ -d "$dep" ]; then                 echo "Installing $dep";                 (cd "$dep" && PYTHONDONTWRITEBYTECODE=1 uv pip install --system --no-cache-dir -c /api/constraints.txt -e .);             fi;         done

# -- End of local dependencies install --

ENV LANGSERVE_GRAPHS='{"agent": "/deps/outer-all_agent_study/src/all_agent.py:agent"}'




# -- Ensure user deps didn't inadvertently overwrite langgraph-api
RUN mkdir -p /api/langgraph_api /api/langgraph_runtime /api/langgraph_license && touch /api/langgraph_api/__init__.py /api/langgraph_runtime/__init__.py /api/langgraph_license/__init__.py
RUN PYTHONDONTWRITEBYTECODE=1 uv pip install --system --no-cache-dir --no-deps -e /api
# -- End of ensuring user deps didn't inadvertently overwrite langgraph-api --
# -- Removing build deps from the final image ~<:===~~~ --
RUN pip uninstall -y pip setuptools wheel
# ！！* 为了让Agent运行时更强大，不要删除pip和setuptools
# RUN rm -rf /usr/local/lib/python*/site-packages/pip* /usr/local/lib/python*/site-packages/setuptools* /usr/local/lib/python*/site-packages/wheel* && find /usr/local/bin -name "pip*" -delete || true
# RUN rm -rf /usr/lib/python*/site-packages/pip* /usr/lib/python*/site-packages/setuptools* /usr/lib/python*/site-packages/wheel* && find /usr/bin -name "pip*" -delete || true
# ！！3. 项目中的excel-mcp用到了uv, 所以保留uv
# RUN uv pip uninstall --system pip setuptools wheel && rm /usr/bin/uv /usr/bin/uvx



WORKDIR /deps/outer-all_agent_study/src