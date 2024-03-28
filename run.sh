function trap_term() {
	echo "probgram is wanted to be terminated!"
}
trap trap_term SIGTERM

python3 main.py
