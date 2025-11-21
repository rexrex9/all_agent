from langchain_core.runnables.config import var_child_runnable_config
def get_thread_id(runtime=None):
    """从 runtime config 中获取 thread_id"""
    config = getattr(runtime, 'config', None)
    if config is None:
        configurable = getattr(runtime, 'context', None)
    else:
        configurable = config.get('configurable', None)
    if configurable is None:
        configurable = var_child_runnable_config.get().get("configurable", {})

    thread_id = configurable.get('thread_id', 'default')
    return thread_id