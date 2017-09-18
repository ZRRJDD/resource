#python批量存储数据   将DataFrame中的数据存储到数据库中
def insertTableData(df):
    conn = getConn()
    cur = conn.cursor()
    # 进行数据批量绑定的准备操作
    cur.execute("select count(*) from STO_HSGT_CHANNEL_TRADE")
    cur.bindarraysize = 2000
    db_types = (d[1] for d in cur.description)
    cur.setinputsizes(*db_types)

    cur.prepare('''insert into STO_HSGT_CHANNEL_TRADE (
                          TRADEDATE, SECURITY_CODE, SECURITY_JC,SYSTEM_HOLD_SHARE,SHARE_LIQA_PCT_PUBLIC,SHARE_LIQA_PCT_COMPUTE,EXCHANGE,SYSTEM_HOLD_SHARE_DAY
                          )
                       VALUES(
                          :1, :2, :3, :4, :5, :6,:7,:8
                          )
                    ''')
    # 从DataFrame获取数据并保存为待传入参数的列表
    param = df.values.tolist()

    # 防止数据过长造成异常，分段处理
    M = []
    for i in range(0, len(param)):
        M.append(param[i])
        if i % 500 == 499:
            cur.executemany(None, M)
            conn.commit()
            del M[:]
    cur.executemany(None, M)
    conn.commit()
    cur.close()
    conn.close()
