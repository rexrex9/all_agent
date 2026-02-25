# 该代码仅为了解Python操作Minio所用，与项目无关
from minio import Minio

client = Minio(
    "localhost:9000", # url
    access_key="rexrex92", # 账户
    secret_key="rexrex92", # 密码
    secure=False # 目前无https域名，所以安全设置为false
)

# 创建bucket
def create_bucket(bucket_name):
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)
        print(f"Bucket '{bucket_name}' 成功创建")
    else:
        print(f"Bucket '{bucket_name}' 已经存在")

# 展示bucket
def list_buckets():
    buckets = client.list_buckets()
    for bucket in buckets:
        print(bucket.name, bucket.creation_date)

# 上传文件
def upload_file(bucket_name, object_name, file_path):
    client.fput_object(bucket_name, object_name, file_path)

# 下载文件
def download_file(bucket_name, object_name, file_path):
    client.fget_object(bucket_name, object_name, file_path)


# 生成下载的url
def gen_presigned_url(bucket_name, object_name):
    """
    生成下载的url
    :param object_name: minio文件名
    :return: 下载的url
    """
    presigned_url = client.presigned_get_object(bucket_name, object_name)
    return presigned_url


if __name__ == "__main__":

    bucket_name = "demo1"
    create_bucket(bucket_name)

    # 列出所有存储桶
    list_buckets()

    # 上传文件
    upload_file(bucket_name, "hello.txt", "hello.txt")
    print("文件上传成功")

    # 下载文件
    download_file(bucket_name, "hello.txt", "hello1.txt")
    print("文件下载成功")

    # 生成下载的url
    print(gen_presigned_url(bucket_name, "hello.txt"))