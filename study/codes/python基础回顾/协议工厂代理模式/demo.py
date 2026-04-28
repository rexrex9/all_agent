
class Backend():

    def ls_info(self):
        return "假装的ls"


class agent():

    def __init__(self,backend):
        self.backend = backend

    def _get_backend(self):
        if callable(self.backend): # 判断backend是否是一个函数
            return self.backend() # 执行函数
        return self.backend # 返回backend本身

    def ls_info(self):
        return self._get_backend().ls_info()

def backend_factory()-> Backend:
    print("执行了什么")
    return Backend()



def create_agent(backend):
    return agent(backend)






if __name__ == "__main__":
    #backend = Backend()
    agent = create_agent(backend_factory)
    print(agent.ls_info())

