# Adaptive scripts

## Create PAQ Dataset
1. RUN:
chmod +x embed-sentences-to-fvecs.py

2. Generate text-embeddings using pretrained mrl encoder (fast on cpu, uses streaming, select max_rows after need)

./embed-sentences-to-fvecs.py \
  --dataset sentence-transformers/paq \
  --output_dir ../build/data \
  --max_rows 10000000 \
  --query_count 10000

3. Change to build directory
cd ../build

4. Create bin files for generated dataset
./apps/utils/fvecs_to_bin float data/sentence-transformers/paq/base.fvecs data/sentence-transformers/paq/base.fbin
./apps/utils/fvecs_to_bin float data/sentence-transformers/paq/query.fvecs data/sentence-transformers/paq/query.fbin

## Compute groundtruth

./apps/utils/compute_groundtruth  --data_type float --dist_fn l2 --base_file data/sentence-transformers/paq/base.fbin --query_file  data/sentence-transformers/paq/query.fbin --gt_file data/sentence-transformers/paq/gt100 --K 100

## Create Index and Search

### BASELINE

#### Sift
```bash
 ./apps/build_memory_index  --data_type float --dist_fn l2 --data_path data/sift/sift_mrl.fbin --index_path_prefix data/sift/index_128 -R 64 -L 100 --alpha 1.2 --partition_dims 128

 ./apps/search_memory_index  --data_type float --dist_fn l2 --index_path_prefix data/sift/index_128 --query_file data/sift/sift_query_mrl.fbin  --gt_file data/sift/gt100 -K 1 -L 10 20 30 40 50 100 --result_path data/sift/res --partition_dims 128
```

#### PAQ

```bash
./apps/build_memory_index  --data_type float --dist_fn l2 --data_path data/sentence-transformers/paq/base.fbin --index_path_prefix data/sentence-transformers/paq/index_1024 -R 64 -L 200 --alpha 1.2 --partition_dims 1024

./apps/search_memory_index  --data_type float --dist_fn l2 --index_path_prefix data/sentence-transformers/paq/index_1024 --query_file data/sentence-transformers/paq/query.fbin  --gt_file data/sentence-transformers/paq/gt100 -K 1 -L 10 20 30 40 50 100 200 --result_path data/sentence-transformers/paq/res --partition_dims 1024
```


### Adaptive
### MRL
```bash
 ./apps/build_memory_index  --data_type float --dist_fn l2 --data_path data/sift/sift_mrl.fbin --index_path_prefix data/sift/index_48_128 -R 64 -L 200 --alpha 1.2 --partition_dims 48 128

./apps/search_memory_index  --data_type float --dist_fn l2 --index_path_prefix data/sift/index_48_128 --query_file data/sift/sift_query_mrl.fbin  --gt_file data/sift/gt100 -K 1 -L 20 40 60 80 100 200 --result_path data/sift/res --partition_dims 48 128
```


### PAQ

```bash

./apps/build_memory_index  --data_type float --dist_fn l2 --data_path data/sentence-transformers/paq/base.fbin --index_path_prefix data/sentence-transformers/paq/index_256_1024 -R 64 -L 400 --alpha 1.2 --partition_dims 256 1024

./apps/search_memory_index  --data_type float --dist_fn l2 --index_path_prefix data/sentence-transformers/paq/index_256_1024 --query_file data/sentence-transformers/paq/query.fbin  --gt_file data/sentence-transformers/paq/gt100 -K 1 -L 20 40 60 80 100 200 400 --result_path data/sentence-transformers/paq/res --partition_dims 256 1024
```







# DISK_TEST

## Disk implementation is not currently working. Can be tested, however remember pq_dim is hard-coded and needs to be altered based on requirements

```bash


./apps/build_memory_index  --data_type float --dist_fn l2 --data_path data/sentence-transformers/paq/base.fbin --index_path_prefix data/sentence-transformers/paq/index_256_1024 -R 64 -L 400 --alpha 1.2 --partition_dims 256 1024

./apps/search_memory_index  --data_type float --dist_fn l2 --index_path_prefix data/sentence-transformers/paq/index_256_1024 --query_file data/sentence-transformers/paq/query.fbin  --gt_file data/sentence-transformers/paq/gt100 -K 1 -L 20 40 60 80 100 200 400 --result_path data/sentence-transformers/paq/res --partition_dims 256 1024

./apps/utils/compute_groundtruth  --data_type float --dist_fn l2 --base_file data/sift/sift_learn.fbin --query_file  data/sift/sift_query.fbin --gt_file data/sift/sift_query_learn_gt100 --K 100

# Using 0.003GB search memory budget for 100K vectors implies 32 byte PQ compression
./apps/build_disk_index --data_type float --dist_fn l2 --data_path data/sentence-transformers/paq/base.fbin --index_path_prefix data/sentence-transformers/paq/disk_index_256_1024 -R 64 -L 200 -B 1.0 -M 64 --build_PQ_bytes

 ./apps/search_disk_index  --data_type float --dist_fn l2 --index_path_prefix data/sift/disk_index_sift_learn_R32_L50_A1.2 --query_file data/sift/sift_query.fbin  --gt_file data/sift/sift_query_learn_gt100 -K 1 -L 20 40 60 80 100 200 400 --result_path data/sift/res --num_nodes_to_cache 10000

 

## Test baseline
./apps/build_disk_index --data_type float --dist_fn l2 --data_path data/sift/sift_mrl.fbin --index_path_prefix data/sift/disk_index_baseline -R 64 -L 200 -B 1.0 -M 64

 ./apps/search_disk_index  --data_type float --dist_fn l2 --index_path_prefix data/sift/disk_index_baseline --query_file data/sift/sift_query_mrl.fbin  --gt_file data/sift/gt100 -K 1 -L 10 20 30 40 80 100 --result_path data/sift/res --num_nodes_to_cache 10000

 ## Test lower
./apps/build_disk_index --data_type float --dist_fn l2 --data_path data/sift/sift_mrl.fbin --index_path_prefix data/sift/disk_index_lower -R 64 -L 200 -B 1.0 -M 64

 ./apps/search_disk_index  --data_type float --dist_fn l2 --index_path_prefix data/sift/disk_index_lower --query_file data/sift/sift_query_mrl.fbin  --gt_file data/sift/gt100 -K 1 -L 10 20 30 40 80 100 --result_path data/sift/res --num_nodes_to_cache 10000

```
