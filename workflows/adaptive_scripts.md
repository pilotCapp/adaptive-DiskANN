# Partitions
## 16
### MRL
```bash
./apps/utils/fvecs_to_bin float data/sift/partitions/16/index_mrl.fvecs data/sift/partitions/16/index_mrl.fbin
./apps/utils/fvecs_to_bin float data/sift/partitions/16/query_mrl.fvecs data/sift/partitions/16/query_mrl.fbin
```

```bash
./apps/build_memory_index  --data_type float --dist_fn l2 --data_path data/sift/partitions/16/index_mrl.fbin --index_path_prefix data/sift/partitions/16/index_sift_mrl_R64_L100_A1.2 -R 64 -L 100 --alpha 1.2
 ./apps/search_memory_index  --data_type float --dist_fn l2 --index_path_prefix data/sift/partitions/16/index_sift_mrl_R64_L100_A1.2 --query_file data/sift/partitions/16/query_mrl.fbin  --gt_file data/sift/sift_query_base_gt100 -K 10 -L 10 20 30 40 50 100 --result_path data/sift/res
 ```
### vanilla
```bash
./apps/utils/fvecs_to_bin float data/sift/partitions/16/index_base.fvecs data/sift/partitions/16/index_base.fbin
./apps/utils/fvecs_to_bin float data/sift/partitions/16/query_base.fvecs data/sift/partitions/16/query_base.fbin
```

```bash
./apps/build_memory_index  --data_type float --dist_fn l2 --data_path data/sift/partitions/16/index_base.fbin --index_path_prefix data/sift/partitions/16/index_sift_base_R64_L100_A1.2 -R 64 -L 100 --alpha 1.2
 ./apps/search_memory_index  --data_type float --dist_fn l2 --index_path_prefix data/sift/partitions/16/index_sift_base_R64_L100_A1.2 --query_file data/sift/partitions/16/query_base.fbin  --gt_file data/sift/sift_query_base_gt100 -K 10 -L 10 20 30 40 50 100 --result_path data/sift/res
 ```

## 45
### MRL
```bash
./apps/utils/fvecs_to_bin float data/sift/partitions/45/index_mrl.fvecs data/sift/partitions/45/index_mrl.fbin
./apps/utils/fvecs_to_bin float data/sift/partitions/45/query_mrl.fvecs data/sift/partitions/45/query_mrl.fbin
```

```bash
./apps/build_memory_index  --data_type float --dist_fn l2 --data_path data/sift/partitions/45/index_mrl.fbin --index_path_prefix data/sift/partitions/45/index_sift_mrl_R64_L100_A1.2 -R 64 -L 100 --alpha 1.2
 ./apps/search_memory_index  --data_type float --dist_fn l2 --index_path_prefix data/sift/partitions/45/index_sift_mrl_R64_L100_A1.2 --query_file data/sift/partitions/45/query_mrl.fbin  --gt_file data/sift/sift_query_base_gt100 -K 10 -L 10 20 30 40 50 100 --result_path data/sift/res
 ```
### vanilla
```bash
./apps/utils/fvecs_to_bin float data/sift/partitions/45/index_base.fvecs data/sift/partitions/45/index_base.fbin
./apps/utils/fvecs_to_bin float data/sift/partitions/45/query_base.fvecs data/sift/partitions/45/query_base.fbin
```

```bash
./apps/build_memory_index  --data_type float --dist_fn l2 --data_path data/sift/partitions/45/index_base.fbin --index_path_prefix data/sift/partitions/45/index_sift_base_R64_L100_A1.2 -R 64 -L 100 --alpha 1.2
 ./apps/search_memory_index  --data_type float --dist_fn l2 --index_path_prefix data/sift/partitions/45/index_sift_base_R64_L100_A1.2 --query_file data/sift/partitions/45/query_base.fbin  --gt_file data/sift/sift_query_base_gt100 -K 10 -L 10 20 30 40 50 100 --result_path data/sift/res
 ```
## 83
### MRL
```bash
./apps/utils/fvecs_to_bin float data/sift/partitions/83/index_mrl.fvecs data/sift/partitions/83/index_mrl.fbin

./apps/utils/fvecs_to_bin float data/sift/partitions/83/query_mrl.fvecs data/sift/partitions/83/query_mrl.fbin

./apps/build_memory_index  --data_type float --dist_fn l2 --data_path data/sift/partitions/83/index_mrl.fbin --index_path_prefix data/sift/partitions/83/index_sift_mrl_R64_L100_A1.2 -R 64 -L 100 --alpha 1.2

 ./apps/search_memory_index  --data_type float --dist_fn l2 --index_path_prefix data/sift/partitions/83/index_sift_mrl_R64_L100_A1.2 --query_file data/sift/partitions/83/query_mrl.fbin  --gt_file data/sift/sift_query_base_gt100 -K 10 -L 10 20 30 40 50 100 --result_path data/sift/res
 ```
### vanilla
```bash
./apps/utils/fvecs_to_bin float data/sift/partitions/83/index_base.fvecs data/sift/partitions/83/index_base.fbin

./apps/utils/fvecs_to_bin float data/sift/partitions/83/query_base.fvecs data/sift/partitions/83/query_base.fbin


./apps/build_memory_index  --data_type float --dist_fn l2 --data_path data/sift/partitions/83/index_base.fbin --index_path_prefix data/sift/partitions/83/index_sift_base_R64_L100_A1.2 -R 64 -L 100 --alpha 1.2

 ./apps/search_memory_index  --data_type float --dist_fn l2 --index_path_prefix data/sift/partitions/83/index_sift_base_R64_L100_A1.2 --query_file data/sift/partitions/83/query_base.fbin  --gt_file data/sift/sift_query_base_gt100 -K 10 -L 10 20 30 40 50 100 --result_path data/sift/res
 ```
## 128
### MRL
```bash
./apps/utils/fvecs_to_bin float data/sift/partitions/128/index_mrl.fvecs data/sift/partitions/128/index_mrl.fbin

./apps/utils/fvecs_to_bin float data/sift/partitions/128/query_mrl.fvecs data/sift/partitions/128/query_mrl.fbin

./apps/build_memory_index  --data_type float --dist_fn l2 --data_path data/sift/partitions/128/index_mrl.fbin --index_path_prefix data/sift/partitions/128/index_sift_mrl_R64_L100_A1.2 -R 64 -L 100 --alpha 1.2

 ./apps/search_memory_index  --data_type float --dist_fn l2 --index_path_prefix data/sift/partitions/128/index_sift_mrl_R64_L100_A1.2 --query_file data/sift/partitions/128/query_mrl.fbin  --gt_file data/sift/sift_query_base_gt100 -K 10 -L 10 20 30 40 50 100 --result_path data/sift/res
 ```
### vanilla
```bash
./apps/utils/fvecs_to_bin float data/sift/partitions/128/index_base.fvecs data/sift/partitions/128/index_base.fbin

./apps/utils/fvecs_to_bin float data/sift/partitions/128/query_base.fvecs data/sift/partitions/128/query_base.fbin


./apps/build_memory_index  --data_type float --dist_fn l2 --data_path data/sift/partitions/128/index_base.fbin --index_path_prefix data/sift/partitions/128/index_sift_base_R64_L100_A1.2 -R 64 -L 100 --alpha 1.2

 ./apps/search_memory_index  --data_type float --dist_fn l2 --index_path_prefix data/sift/partitions/128/index_sift_base_R64_L100_A1.2 --query_file data/sift/partitions/128/query_base.fbin  --gt_file data/sift/sift_query_base_gt100 -K 10 -L 10 20 30 40 50 100 --result_path data/sift/res
 ```



## ADAPTIVE
### MRL
```bash

./apps/build_memory_index  --data_type float --dist_fn l2 --data_path data/sift/sift_base_learned.fbin --index_path_prefix data/sift/index_sift_mrl_R64_L100_A1.2 -R 64 -L 100 --alpha 1.2 --partition_dims 128

./apps/search_memory_index  --data_type float --dist_fn l2 --index_path_prefix data/sift/index_sift_mrl_R64_L100_A1.2 --query_file data/sift/sift_query_learned.fbin  --gt_file data/sift/sift_query_learn_gt100 -K 10 -L 10 20 30 40 50 100 --result_path data/sift/res
 ```

## VANILLA
```bash
 ./apps/build_memory_index  --data_type float --dist_fn l2 --data_path data/sift/sift_base.fbin --index_path_prefix data/sift/index_sift_base_R64_L100_A1.2 -R 64 -L 100 --alpha 1.2

./apps/search_memory_index  --data_type float --dist_fn l2 --index_path_prefix data/sift/index_sift_base_R64_L100_A1.2 --query_file data/sift/sift_query.fbin  --gt_file data/sift/sift_query_base_gt100 -K 10 -L 10 20 30 40 50 100 --result_path data/sift/res
 ```
