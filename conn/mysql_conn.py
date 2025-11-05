import pymysql
from configs import config as cfg
from utils.general_utils import globle_util as gu
from pymysql.cursors import DictCursor


class MysqlConn:

    def __init__(self):
        self.conn = pymysql.connect(
            host=cfg.MYSQL.HOST,
            port=int(cfg.MYSQL.PORT),
            user=cfg.MYSQL.USER,
            password=cfg.MYSQL.PASSWORD,
            database=cfg.MYSQL.DATABASE,
            cursorclass=DictCursor # 设置查询返回字典
        )

    # 插入数据
    def insert(self,table_name, datas):
        """
        :param table_name:  表名
        :param datas: 字典列表的数据 数据：[{'question': '问题1', 'answer': '答案1'}, {'question': '问题2', 'answer': '答案2'}]
        :return: 插入的ID或ids列表, 示例 [uuid_1,uuid_2]
        """
        self.conn.ping(reconnect=True)
        if not datas:
            return []
        if not isinstance(datas, list):
            datas = [datas]
        for d in datas:
            d['id']=d.get('id',gu.get_uuid()) #若无则随机生成id
        with self.conn.cursor() as cursor:
            sql = f"INSERT INTO `{table_name}` ({','.join(datas[0].keys())}) VALUES ({','.join(['%s'] * len(datas[0]))})\n"
            ds = [tuple(d.values()) for d in datas]
            cursor.executemany(sql,ds)
        self.conn.commit()
        ids = [d['id'] for d in datas]
        if len(ids) == 1:
            return ids[0]
        else:
            return ids


    # 普通查询
    def search_by_sql(self,sql):
        """
        :param sql: 示例 sql: "SELECT * FROM table WHERE question='问题1'"
        :return: 查询结果  list 示例 [{'question': '问题1', 'answer': '答案1'}, {'question': '问题2', 'answer': '答案2'}]
        """
        self.conn.ping(reconnect=True)
        with self.conn.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()

    # 参数化查询
    def search_with_params(self,sql,params):
        """
        :param sql: 示例 sql: "SELECT * FROM table WHERE question=%s"
        :param params: 参数元组 示例 params = ('问题1',)
        :return: 查询结果  list 示例 [{'question': '问题1', 'answer': '答案1'}, {'question': '问题2', 'answer': '答案2'}]
        """
        self.conn.ping(reconnect=True)
        with self.conn.cursor() as cursor:
            cursor.execute(sql,params)
            return cursor.fetchall()

    # 查询所有
    def searh_all(self,table_name,cols):
        """
        :param table_name: 表名
        :param cols: 列名
        :return: 查询结果  list 示例 [{'question': '问题1', 'answer': '答案1'}, {'question': '问题2', 'answer': '答案2'}]
        """
        self.conn.ping(reconnect=True)
        return self.search_by_sql(f"SELECT {','.join(cols)} FROM {table_name}")

    # 执行SQL
    def execute(self,sql):
        """
        :param sql: 示例 sql: "DELETE FROM table WHERE question='问题1'"
        :return: None
        """
        self.conn.ping(reconnect=True)
        with self.conn.cursor() as cursor:
            cursor.execute(sql)
        self.conn.commit()

    def close(self):
        self.conn.close()



if __name__ == '__main__':
    mc = MysqlConn()
    print(mc.conn.ping(reconnect=True))