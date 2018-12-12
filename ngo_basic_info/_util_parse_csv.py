import csv



SOURCE_CSV = "crawled/x2.csv"

# Jan 1, 2018  ->  2018-01-01
def MMDDYYYY_to_date8(date_str):
    mapping = {'Jan':'01', 'Feb':'02', 'Mar':'03',  'Apr':'04', 'May':'05', 'Jun':'06',
               'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}

    MMDD, year = date_str.split(", ")
    month, date = MMDD.split(" ")
    return year + "-" + mapping[month] + "-" + date.zfill(2)

def date9_to_date8(date_str):

    return date_str

def _change_date_format(source_file):
    writer_handle = open("crawled/x2_date_formatted.csv", 'a', encoding='utf-8')

    with open(source_file, 'r', encoding='utf-8') as f:
        csv_reader = csv.reader(f)

        count = 0
        for line in csv_reader:
            if count == 0:
                count += 1
                continue

            new_line = list(line)

            if line[5] == '\xa0\xa0 -- \xa0\xa0':
                pass
            else:
                date0, date1 = "", ""
                dates = line[5].split(' -- ')
                if len(dates) == 2:
                    date0 = dates[0].strip()
                    date1 = dates[1].strip()
                else:
                    if line[5].startswith(' -- '):
                        date1 = line[5].split(' -- ')[0]
                    else:
                        date0 = line[5].split(' -- ')[0]

                if date0:
                    date0 = MMDDYYYY_to_date8(date0)
                if date1:
                    date1 = MMDDYYYY_to_date8(date1)

                new_line = new_line[:5] + [date0 + " -- " + date1] + new_line[6:]

            if line[7]:
                new_date7 = MMDDYYYY_to_date8(line[7])
                new_line = new_line[:7] + [new_date7] + new_line[8:]

            writer_handle.write(",".join(new_line) + "\n")
            #print(line)
            #print(new_line)
            count += 1

            #if count > 1000:
            #    break

# Useless as the DB output already contains newline
def _remove_newline(source_file):
    writer_handle = open("crawled/basic_info_newline_removed.csv", 'a', encoding='utf-8')

    with open(source_file, 'r', encoding='utf-8') as f:

        count = 0
        for line in  f.readlines():
            count += 1
            if 400 < count < 500:
                print(count, line)
            line0 = line.replace("\n", "")
            writer_handle.write(line0 + "\n")


if __name__ == "__main__":
    # _change_date_format("crawled/x2.csv")
    _remove_newline(r"D:\workspace\NGOCrawler\generated_files\basic_info.csv")