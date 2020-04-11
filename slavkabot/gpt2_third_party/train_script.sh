#!/usr/bin/env bash
# cd ru_transformers
# conda activate gpt
export PATH="$PATH:\C:\Users\DELL\Anaconda3"
export TRAIN_FILE=data
export CUDA_VISIBLE_DEVICES=0
export MODEL_SIZE=gpt2
export OUTPUT=output_yt/s
export BS=8
export LR=5e-5
python run_lm_finetuning.py --output_dir=output_yt\s_new --model_type=gpt2 --model_name_or_path=output_yt\s\checkpoint-1910207 --do_train --train_data_file=data --per_gpu_train_batch_size 8 --save_steps=1000 --logging_steps=1 --fp16 --fp16_opt_level O2 --warmup_samples 1000 --learning_rate 5e-5 --tokenizer_class YTEncoder --tokenizer_name bpe/yt.model --do_eval --evaluate_during_training --eval_steps 400 --eval_data_file=data/valid --unfreeze_level 1 --lr_decay --overwrite_output_dir --block_size=35 --num_train_epochs=5
python run_lm_finetuning.py --output_dir=output_yt\s_new --model_type=gpt2 --model_name_or_path=output_yt\s\checkpoint-1910207 --do_train --train_data_file=data --per_gpu_train_batch_size 8 --save_steps=1000 --logging_steps=1 --fp16 --fp16_opt_level O2 --warmup_samples 1000 --learning_rate 5e-5 --tokenizer_class YTEncoder --tokenizer_name bpe/yt.model --do_eval --evaluate_during_training --eval_steps 400 --eval_data_file=data/valid --unfreeze_level 1 --lr_decay --overwrite_output_dir --block_size=35