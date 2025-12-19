FROM langchain/langgraph-api:3.11
# 设置非交互式安装
ENV DEBIAN_FRONTEND=noninteractive

# 使用清华大学镜像源加速（如果在中国）
RUN sed -i 's/archive.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list || \
    sed -i 's/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list || true

# 先安装基础工具
RUN apt-get update && apt-get install -y \
    curl \
    pandoc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
    
# 使用清华大学镜像源加速（如果在中国）
RUN sed -i 's/archive.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list || \
    sed -i 's/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list || true

# LaTeX 安装
RUN apt-get update && apt-get install -y \
    texlive-xetex \
    texlive-latex-base \
    # texlive-lang-chinese \
    lmodern \
    fonts-wqy-microhei \
    fonts-liberation \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# # 安装 LaTeX 相关依赖
# RUN apt-get update && \
#     apt-get install -y --no-install-recommends \
#     texlive-xetex \
#     texlive-fonts-recommended \
#     texlive-lang-chinese \
#     lmodern \
#     fonts-liberation \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*

# -- Installing local requirements --
ADD ../requirements.txt /deps/outer-all_agent/src/requirements.txt

RUN PYTHONDONTWRITEBYTECODE=1 uv pip install --system --no-cache-dir -c /api/constraints.txt -r /deps/outer-all_agent/src/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
# -- End of local requirements install --

# -- Adding non-package dependency all_agent --
ADD .. /deps/outer-all_agent/src
RUN set -ex && \
    for line in '[project]' \
                'name = "all_agent"' \
                'version = "0.1"' \
                '[tool.setuptools.package-data]' \
                '"*" = ["**/*"]' \
                '[build-system]' \
                'requires = ["setuptools>=61"]' \
                'build-backend = "setuptools.build_meta"'; do \
        echo "$line" >> /deps/outer-all_agent/pyproject.toml; \
    done
# -- End of non-package dependency all_agent --


# -- Installing all local dependencies --

RUN for dep in /deps/*; do             echo "Installing $dep";             if [ -d "$dep" ]; then                 echo "Installing $dep";                 (cd "$dep" && PYTHONDONTWRITEBYTECODE=1 uv pip install --system --no-cache-dir -c /api/constraints.txt -e . -i https://pypi.tuna.tsinghua.edu.cn/simple);             fi;         done

# -- End of local dependencies install --

ENV LANGGRAPH_STORE='{"enabled": true}'

ENV LANGSERVE_GRAPHS='{"agent": "/deps/outer-all_agent/src/agent.py:agent"}'

# -- Ensure user deps didn't inadvertently overwrite langgraph-api
RUN mkdir -p /api/langgraph_api /api/langgraph_runtime /api/langgraph_license && touch /api/langgraph_api/__init__.py /api/langgraph_runtime/__init__.py /api/langgraph_license/__init__.py
RUN PYTHONDONTWRITEBYTECODE=1 uv pip install --system --no-cache-dir --no-deps -e /api  -i https://pypi.tuna.tsinghua.edu.cn/simple
# -- End of ensuring user deps didn't inadvertently overwrite langgraph-api --
# -- Removing build deps from the final image ~<:==~~~
RUN pip uninstall -y pip setuptools wheel
RUN rm -rf /usr/local/lib/python*/site-packages/pip* /usr/local/lib/python*/site-packages/setuptools* /usr/local/lib/python*/site-packages/wheel* && find /usr/local/bin -name "pip*" -delete || true
RUN rm -rf /usr/lib/python*/site-packages/pip* /usr/lib/python*/site-packages/setuptools* /usr/lib/python*/site-packages/wheel* && find /usr/bin -name "pip*" -delete || true
# RUN uv pip uninstall --system pip setuptools wheel && rm /usr/bin/uv /usr/bin/uvx


WORKDIR /deps/outer-all_agent/src