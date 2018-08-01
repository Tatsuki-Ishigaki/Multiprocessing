## コサイン類似度のファイル

```
cos
 | --- ml-100k    読み込むデータが入っているファイル
 | --- python  
 |       |  ---  movielens.py                並列化なしのプログラム
 |       |  ---  multipro_movielens.py	     multiprocessingを使った並列プログラム
 |       |  ---  joblib_movielens.py         joblibを使った並列プログラム
 |       |  ---  dask_movielens.py           daskを使った並列プログラム
 |
 | --- Java
         |  ---  movielens.java              並列化なしのプログラム
         |  ---  multithre_movielens.java    omp4jを使った並列プログラム
         |  ---  omp4j-1.2.jar               並列化するためのライブラリ

```

## 画像読み込みのファイル

```
ReadPicture
 | - multiprocessing.jpynb  並列化なしとありを関数で分けている並列有無併用プログラム
```
