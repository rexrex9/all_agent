from deepagents.middleware import SkillsMiddleware
from content.others import mybackend

class MySkillMiddleware(SkillsMiddleware):
    def __init__(self, backend,sources):
        # 父类初始化
        super().__init__(backend=backend,sources=sources)

    # 重写_get_backend方法
    def _get_backend(self, state, runtime, config):
        # 得到懒加载后端实例
        self._backend = mybackend.LazyFilesystemBackend(runtime)._ensure_backend()
        # 经过父类方法处理
        return super()._get_backend(state, runtime, config)