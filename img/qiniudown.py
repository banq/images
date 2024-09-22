from qiniu import Auth, BucketManager
import requests

# 七牛云账号的Access Key和Secret Key
access_key = 'axCnOZ5hHeMMJLejjKhh7O56JdxAGpmEgY11G3EB'
secret_key = 'sGSeH06-V2jiW3gKqzq7R0Rg0ZpJ576G_laLL2AK'
bucket_name = 'newcdnjdon2'

# 初始化Auth状态
q = Auth(access_key, secret_key)

# 初始化BucketManager
bucket = BucketManager(q)

# 列出指定前缀的所有文件
prefix = 'img/'  # 例如：'images/'
limit = 1000  # 每次拉取的最大文件数

marker = None
files_to_download = []

# 列出所有文件
while True:
    ret, eof, info = bucket.list(bucket_name, prefix, marker, limit)
    marker = ret.get('marker', None)
    files_to_download.extend([item['key'] for item in ret['items']])
    
    if eof:  # 列出文件结束
        break

# 下载每个文件
for key in files_to_download:
    # 生成下载链接
    base_url = f'http://img.jdon.com/{key}'
    private_url = q.private_download_url(base_url, expires=3600)  # 有效期1小时

    # 下载文件
    response = requests.get(private_url)
    if response.status_code == 200:
        with open(key.split('/')[-1], 'wb') as f:
            f.write(response.content)
        print(f"{key} 下载完成")
    else:
        print(f"{key} 下载失败")
