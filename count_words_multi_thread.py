import threading


def count_words(filename):
    word_count = {}

    with open(filename, 'r') as file:
        for line in file:
            words = line.split()

            for word in words:
                # Remove special characters
                cleaned_word = ''.join(c.lower() for c in word if c.isalnum())

                if cleaned_word:
                    word_count[cleaned_word] = word_count.get(cleaned_word, 0) + 1

    return word_count


def count_words_multithreaded(filename, num_threads=4):
    word_count = {}
    lock = threading.Lock()

    def count_words_thread(start_line, end_line):
        nonlocal word_count

        thread_word_count = count_words(filename)

        with lock:
            for word, count in thread_word_count.items():
                word_count[word] = word_count.get(word, 0) + count

    with open(filename, 'r') as file:
        lines = file.readlines()

    total_lines = len(lines)
    lines_per_thread = total_lines // num_threads

    threads = []
    for i in range(num_threads):
        start_line = i * lines_per_thread
        end_line = (i + 1) * lines_per_thread if i < num_threads - 1 else total_lines

        thread = threading.Thread(target=count_words_thread, args=(start_line, end_line))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return word_count


# Usage example
filename = 'gpl-3.0.txt'
word_count = count_words_multithreaded(filename, num_threads=4)
for word, count in word_count.items():
    print(f'{word}: {count}')
