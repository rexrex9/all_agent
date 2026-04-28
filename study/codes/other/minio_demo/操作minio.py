
import minio
# 连接
url = '127.0.0.1:9000'

minio_client = minio.Minio(
    url,
    access_key='minio',
    secret_key='minio123',
    secure=False # 不去验证安全证书
)

# 创建存储桶
def create_bucket(bucket_name):
    minio_client.make_bucket(bucket_name)

# 删除存储桶
def delete_bucket(bucket_name):
    minio_client.remove_bucket(bucket_name)

# 上传文件
def upload_file(bucket_name, object_name,file_path):
    """
    :param bucket_name: 存储桶的名字
    :param object_name: 在minio上的文件名
    :param file_path:  本地文件所在路径
    :return:
    """
    minio_client.fput_object(bucket_name, object_name, file_path)

# 下载文件
def download_file(bucket_name, object_name,file_path):
    minio_client.fget_object(bucket_name, object_name, file_path)


# 获得下载连接
def get_download_url(bucket_name, object_name):
    return minio_client.presigned_get_object(bucket_name, object_name)


if __name__ == '__main__':
    a = get_download_url('my-bucket','b.txt')
    print(a)