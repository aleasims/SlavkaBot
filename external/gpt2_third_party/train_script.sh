#!/usr/bin/env bash
# cd ru_transformers
# conda activate gpt
python run_lm_finetuning.py --output_dir=output_yt\s_slavka_only_1 --model_type=gpt2 --model_name_or_path=output_yt\s_new9\checkpoint-1937135 --do_train --train_data_file=data\slavka_only --per_gpu_train_batch_size 5 --save_steps=200 --logging_steps=1 --fp16 --fp16_opt_level O2 --warmup_samples 1000 --learning_rate 5e-5 --tokenizer_class YTEncoder --tokenizer_name bpe/yt.model --do_eval --evaluate_during_training --eval_steps 400 --eval_data_file=data\slavka_only\valid --unfreeze_level 7 --lr_decay --overwrite_output_dir --block_size=120 --num_train_epochs=5
