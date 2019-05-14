import jieba
import pymysql

def read_weibo():
    connect = pymysql.connect(
        host = 'localhost',
        user = 'root',
        password = 'root_123321',
        db = 'travel',
        charset = 'utf8mb4',
        cursorclass = pymysql.cursors.DictCursor
    )
    cursor = connect.cursor()
    sql = "select user,time,contents from 绝地求生_0_1 where number >= 1 and number <= 100"
    cursor.execute(sql)
    contents = cursor.fetchall()

    for content in contents:

        #print(content['contents'])

        cut = jieba.cut(content['contents'])
        print(','.join(cut))



    return

if __name__ == "__main__":
    read_weibo()