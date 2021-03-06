# 基準の実装
import time
import numpy as np

def cos_sim(v1, v2):
    v1_ = np.array(v1)
    v2_ = np.array(v2)
    return np.dot(v1_, v2_) / (np.linalg.norm(v1_) * np.linalg.norm(v2_))

class Sample:
    def __init__(self, user_size=943, item_size=1682, file_path="ml-100k/u.data"):
        self.file_path = file_path
        # user数×アイテム数のリスト
        self.eval_table = [[0 for _ in range(item_size)] for _ in range(user_size)]
        # user数×user数のcos類似度テーブル
        self.sim_table = [[0 for _ in range(user_size)] for _ in range(user_size)]


    def distinguish_info(self, line):
        u_id, i_id, rating, timestamp = line.replace("\n", "").split("\t")
        # u_idとi_idはitemのindexを一つずらす
        return int(u_id)-1, int(i_id)-1, float(rating), timestamp


    def calc_cossim(self, target_u_id, target_user_eval):
        for u_id ,user_eval in enumerate(self.eval_table):
            self.sim_table[target_u_id][u_id] = cos_sim(target_user_eval, user_eval)


    def run(self):
        f = open(self.file_path , 'r')
        # userとitemのテーブル作成
        start = time.time()
        for line in f:
            u_id, i_id, rating, _ = self.distinguish_info(line)
            self.eval_table[u_id][i_id] = rating

        # テーブルに基づいてcos類似度作成
        for target_u_id, target_user_eval in enumerate(self.eval_table):
            self.calc_cossim(target_u_id, target_user_eval)
        alltime = time.time()-start
        print("総時間:{}".format(alltime))


if __name__ == "__main__":
    s = Sample()
    s.run()
