from minio import Minio
from configs import config as cfg

# 115.190.35.205:9090
class MinioConn:
    def __init__(self):
        self.client = self.create_client()
        self.bucket_name = 'stores'

    def create_client(self):
        """连接MINIO客户端"""
        return Minio(
            cfg.MINIO.ENDPOINT,
            access_key=cfg.MINIO.ACCESS_KEY,
            secret_key=cfg.MINIO.SECRET_KEY,
            secure=False
        )

    def upload_obj(self, object_name, file_path):
        """
        上传文件
        :param object_name: minio文件名
        :param file_path:  本地路径
        :return:
        """
        self.client.fput_object(self.bucket_name, object_name, file_path)


    def gen_presigned_url(self, object_name):
        """
        生成下载的url
        :param object_name: minio文件名
        :return: 下载的url
        """
        return self.client.presigned_get_object(self.bucket_name, object_name)

if __name__ == "__main__":

    mc = MinioConn()
    print(mc.upload_obj('test.txt', 'D:/test.txt'))
