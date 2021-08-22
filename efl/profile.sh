temp_file=$(mktemp)
echo "saving to $temp"
python -m cProfile -o $temp_file main.py
snakeviz $temp_file
rm $temp_file
