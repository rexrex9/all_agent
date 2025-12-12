from minio import Minio
from base import configs as cfg


class MinioConn:
    def __init__(self):
        self.client = self.create_client()
        self.bucket_name = 'stores'
        self._init_bucket()

    def create_client(self):
        """连接MINIO客户端"""
        return Minio(
            cfg.MINIO.ENDPOINT,
            access_key=cfg.MINIO.ACCESS_KEY,
            secret_key=cfg.MINIO.SECRET_KEY,
            secure=False
        )
    def _init_bucket(self):
        """创建bucket"""
        if self.client.bucket_exists(self.bucket_name):
            return
        self.client.make_bucket(self.bucket_name)


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
        presigned_url = self.client.presigned_get_object(self.bucket_name, object_name)
        return presigned_url


