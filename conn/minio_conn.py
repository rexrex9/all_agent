from minio import Minio
from configs import config as cfg


class MinioConn:
    def __init__(self):
        self.client = self.create_client()
    def create_client(self):
        """连接MINIO客户端"""
        return Minio(
            cfg.MINIO.ENDPOINT,
            access_key=cfg.MINIO.ACCESS_KEY,
            secret_key=cfg.MINIO.SECRET_KEY,
            secure=False
        )

    def upload_obj(self,bucket_name, object_name, file_path):
        """
        上传文件
        :param bucket_name: 桶名
        :param object_name: minio文件名
        :param file_path:  本地路径
        :return:
        """
        self.client.fput_object(bucket_name, object_name, file_path)


    def download_obj(self,bucket_name, object_name, file_path):
        """
        下载文件
        :param bucket_name: 桶名
        :param object_name: minio文件名
        :param file_path: 下载到的本地路径
        :return:
        """

        self.client.fget_object(bucket_name, object_name, file_path)


    def gen_presigned_url(self,bucket_name, object_name):
        """
        生成下载的url
        :param bucket_name: 桶名
        :param object_name: minio文件名
        :return: 下载的url
        """
        return self.client.presigned_get_object(bucket_name, object_name)

if __name__ == "__main__":

    mc = MinioConn()
    print(mc.gen_presigned_url("try","点名器改.exe"))