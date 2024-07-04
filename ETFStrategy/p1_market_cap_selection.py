


import csv


# Part 1:  stock pool selection:
# '''select the stock to be included into the stock pool'''
# csv path
input_csv_file = 'web_scraping_raw_data/StockList.csv'
output_csv_file = 'web_scraping_raw_data/top_mar_cap_companies.csv'

# selected columns in header
selected_columns = [1,2,10,11,13]
columns_to_clean = [1,10,11,13]


# clean data
def clean_cell(cell):
    return cell.replace('"', '').replace('=', '').replace(',', '')

def should_delete(line):
    '''length of ticker > 4, check after selecting columns'''
    length_ticker = len(str(line[0]))
    listing_year = float(line[4])
    return length_ticker > 4 or str(line[0]).startswith('0') or listing_year < 3

# open CSV file
companies = []
with open(input_csv_file, mode='r', encoding='utf-8-sig') as file:
    reader = csv.reader(file)
    headers = next(reader)

    # selected header
    selected_headers = [headers[i] for i in selected_columns]
    # print(selected_headers)

    # read every line
    for line in reader:
        selected_line = [
            clean_cell(line[i]) if i in columns_to_clean
            else line[i] for i in selected_columns]
        companies.append(selected_line)
    # print(companies)

    # sort by market cap
    top_mar_cap_companies = sorted(companies, key=lambda x: int(x[3]), reverse=True)
    # print(top_mar_cap_companies)

    # write into new csv, and do not write non-stock rows
    with open(output_csv_file, mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow(selected_headers)
        for row in top_mar_cap_companies:
            if not should_delete(row):
                writer.writerow(row)


    print(f"top market cap companies by market cap were written into {output_csv_file}")




