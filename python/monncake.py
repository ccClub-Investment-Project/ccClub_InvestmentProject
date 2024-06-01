def parse_date(date_str):
    parts = date_str.split('-')
    year = int(parts[0])
    month = int(parts[1])
    day = int(parts[2])
    return year, month, day

def check_date(date_str):
    year, month, day = parse_date(date_str)
    if year < 1  or month < 1 or month > 12 or day < 1 or day > 31:
        return False
    # 正確的話回傳日期數字

def calculate_price(pack_id, exp_date, single_price, amount):
    if not check_date(exp_date):
        return f"{pack_id} has labeling problem!"

    # Check if single_price is valid
    if single_price not in [60, 70, 80]:
        return f"{pack_id} has labeling problem!"

    # Check if amount is valid
    if amount not in [3, 6, 9, 12]:
        return f"{pack_id} has labeling problem!"

    year, month, day = parse_date(exp_date)
    total_price = single_price * amount

    if (year >= 2023 and month >= 10 and day >= 14) or (year >= 2023 and month>=11):
        pack_price = total_price
    elif year >= 2023 and month >= 10 and day >= 7 :
        pack_price = total_price * 0.8
    elif (year >= 2023 and month >= 9 and day >= 27) or (year == 2023 and month>=10):
        pack_price = total_price * 0.6
    else:
        return f"{pack_id} has expired, it should not be sold."

    return f"{pack_id} should be sold at price {pack_price:.0f}"

n = int(input().strip())
for _ in range(n):
    pack_id, exp_date, single_price, amount = input().split(',')
    pack_id = pack_id.strip()
    exp_date = exp_date.strip()
    single_price = int(single_price.strip())
    amount = int(amount.strip())
    print(calculate_price(pack_id, exp_date, single_price, amount))