import os
import csv

OUTPUT_DIR = "util/"

# Generate a csv file with existing credit_id's from DB
def _prepare_existing_id(source_file):
    names = []

    with open(source_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        count = 0
        for line in reader:
            if count == 0:
                count = 1
                continue

            names.append(line[1])

    print(f"Database now has {len(names)} records.")
    print(names)

    with open(OUTPUT_DIR + "existing_names.txt", 'w', encoding='utf-8') as f:
        f.write(",".join(names))

    return names

# aggregate urls to parse
def _prepare_url_queue(folder, prefix, existing_ref):
    with open(existing_ref, 'r', encoding='utf-8') as f:
        existing_id = f.read().split(',')
    print(len(existing_id), existing_id)

    file_list = os.listdir(folder)
    url_files = [f for f in file_list if f.startswith(prefix)]
    url_queue = []

    for url_file in url_files:
        with open(folder + url_file, 'r', encoding='utf-8') as f:
            text = f.readlines()
            for line in text:
                if line == '-,-\n':
                    continue
                name, url = line.split(',')
                if name not in existing_id:
                    url_queue.append(url.replace('\n', ''))
                else:
                    existing_id.remove(name)

    print(existing_id)

    print(len(url_queue), url_queue)
    with open("util/URL_QUEUE.csv", 'w', encoding='utf-8') as f:
        f.write(",".join(url_queue))

    return url_queue


if __name__ == '__main__':
    # _prepare_existing_id(r"D:\workspace\NGOCrawler\original_files\1_trust_orig.csv")
    _prepare_url_queue(r"D:\workspace\NGOCrawler\trust\crawled\\", "URLs_", "util/existing_names.txt")