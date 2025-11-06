
from conn.minio_conn import MinioConn

def get_minio_tools():
    mc = MinioConn()
    return [mc.create_client,
            mc.client.list_buckets,
            mc.client.make_bucket,
            mc.client.bucket_exists,
            mc.client.list_objects,
            mc.upload_obj,
            mc.download_obj,
            mc.gen_presigned_url
            ]

if __name__ == "__main__":
    tools = get_minio_tools()
    print(tools)