
from conn.minio_conn import MinioConn

def get_minio_tools():
    mc = MinioConn()
    return [mc.create_client,
            mc.upload_obj,
            mc.gen_presigned_url
            ]

if __name__ == "__main__":
    tools = get_minio_tools()
    print(tools)