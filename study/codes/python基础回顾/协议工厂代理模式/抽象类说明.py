import abc
class A(abc.ABC):
    def ls(self):
        raise NotImplementedError
class myA(A):

    def ls(self):
        print("ls")

def do(a:A):
    a.ls()


if __name__ == '__main__':
    do(myA())

