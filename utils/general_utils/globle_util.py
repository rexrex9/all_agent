import hashlib
import uuid
# 生成hash值
def gen_hash(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()

# 生成uuid
def get_uuid():
    return uuid.uuid4().hex




if __name__ == '__main__':
    print(len(gen_hash("123")))