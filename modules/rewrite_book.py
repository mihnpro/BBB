if __name__ == "__main__":
    with open("./../books/master_and_margarita.txt", 'r', encoding='utf-8') as file:
        book = file.read()
        index = 1
        start = 0
        end = 3000
        while len(book) > end:
            while book[end] != '.':
                end += 1
            with open(f"./../books/chapter/chapter_{index}.txt", 'w', encoding='utf-8') as file:
                file.write(book[start:end+1])

            start = end + 1
            end += 3001
            index += 1
