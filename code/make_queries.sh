#!/usr/bin/env bash

python3 -m torch.distributed.launch --nproc_per_node=8 run.py \
    --task generation \
    --model_name Michau/t5-base-en-generate-headline \
    --per_device_eval_batch_size 32 \
    --run_name docTquery-XORQA-generation \
    --max_length 256 \
    --valid_file data/xorqa_data/100k/xorqa_corpus.tsv \
    --output_dir temp \
    --dataloader_num_workers 10 \
    --report_to wandb \
    --logging_steps 100 \
    --num_return_sequences 10
