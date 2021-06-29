export EMBED_WEIGHTS="demo/weights/"
export EMBED_CONFIG="integration_test/train_opt.yaml"
export NN_EMBEDDING_DATASET="demo/learned_dataset.json"
export NN_EMBEDDING_LENGTH="48"
tmux new-session 'bash --init-file <( sleep 2; echo "python -m nearest_neighbors_db.start_server" )' \; \
split-window 'bash --init-file <( sleep 2; echo "python embedding_service/server.py" )' \; \
split-window -h 'bash --init-file <( sleep 2; echo "python temp_db/server.py" )' \; \
split-window -h 'bash --init-file <( sleep 2; echo "(cd search_frontend; python -m http.server)" )' \; \
split-window -h 'bash --init-file <( sleep 2; echo "python search_backend/server.py" )' \;
