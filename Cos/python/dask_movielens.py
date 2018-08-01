# 基準の実装
import time
import numpy as np
import pandas as pd
from dask import delayed
import dask.dataframe as dd
from dask.multiprocessing import get

def cos_sim(v1, v2):
    v1_ = np.array(v1)
    v2_ = np.array(v2)
    return np.dot(v1_, v2_) / (np.linalg.norm(v1_) * np.linalg.norm(v2_))

class Sample:
    def __init__(self, user_size=943, item_size=1682, file_path="u.data"):
        self.file_path = file_path
        # user数×アイテム数のリスト
        self.eval_table = [[0 for _ in range(item_size)] for _ in range(user_size)]
        # user数×user数のcos類似度テーブル
        self.sim_table = [[0 for _ in range(user_size)] for _ in range(user_size)]


    def distinguish_info(self, line):
        u_id, i_id, rating, timestamp = line.replace("\n", "").split("\t")
        # u_idとi_idはitemのindexを一つずらす
        return int(u_id)-1, int(i_id)-1, float(rating), timestamp

# ...

    def calc_cossim(self, target_u_id, target_user_eval):
        for u_id ,user_eval in enumerate(self.eval_table):
            self.sim_table[target_u_id][u_id] = cos_sim(target_user_eval, user_eval)
        # 変更
        # print(self.sim_table[target_u_id])
        return self.sim_table[target_u_id]

    # ...

    def wrapper(self, args):
        # 変更
        return self.calc_cossim(*args)

    def run_pool(self, npartitions=4):
        f = open(self.file_path , 'r')
        # userとitemのテーブル作成
        start = time.time()
        for line in f:
            u_id, i_id, rating, _ = self.distinguish_info(line)
            self.eval_table[u_id][i_id] = rating
            #print(rating)

        # テーブルに基づいてcos類似度作成
        tmp = [(target_u_id, target_user_eval) for target_u_id, target_user_eval in enumerate(self.eval_table)]

        df = pd.DataFrame(list(tmp))
        ddf = dd.from_pandas(df, npartitions)
        self.right_sim_table = ddf.apply(self.wrapper, axis=1, meta=('list')).compute(get=get)

        # print(self.right_sim_table)

        time_tmp = time.time()-start
        print("総時間:{}".format(time_tmp))


if __name__ == "__main__":
    s = Sample()
    s.run_pool()
