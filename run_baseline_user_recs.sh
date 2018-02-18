

item_recommendation --training-file=media_lite_training.csv --test-file=media_lite_test.csv --measures=prec@5,prec@10,recall@5,recall@10 --recommender=BPRMF > user_rec_BPRMF.out
item_recommendation --training-file=media_lite_training.csv --test-file=media_lite_test.csv --measures=prec@5,prec@10,recall@5,recall@10 --recommender=WRMF > user_rec_WRMF.out

python3 -m gemsearch.runners.send_slack_message





$ ../../../my_media_lite_build/item_recommendation.exe --training-file=media_lite_training.csv --                           test-file=media_lite_test.csv --measures=prec@5,prec@10,recall@5,recall@10 --recommender=BPRMF
loading_time 1.74
memory 89
training data: 912 users, 459960 items, 856144 events, sparsity 99.79591
test data:     912 users, 162809 items, 214494 events, sparsity 99.85554
BPRMF num_factors=10 bias_reg=0 reg_u=0.0025 reg_i=0.0025 reg_j=0.00025 num_iter=30 LearnRate=0.0                           5 uniform_user_sampling=True with_replacement=False update_j=True
loss_num_sample_triples=3000
training_time 00:01:52.6320420 prec@5 0,01031 prec@10 0,00987 recall@5 0,00055 recall@10 0,00096                            num_items 533345 num_lists 912 testing_time 00:03:50.9470850
memory 130
