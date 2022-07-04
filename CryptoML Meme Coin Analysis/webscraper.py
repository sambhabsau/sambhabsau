from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

holders_df = pd.DataFrame(columns=["name", "num_holders"])
url = "https://etherscan.io/tokens"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
headers = {'user-agent': USER_AGENT}

for i in range(1, 21):
    html_text = requests.get(url, headers=headers, params={"p": i}).text
    etherscan_soup = BeautifulSoup(html_text, 'lxml')
    table_of_tokens = etherscan_soup.find(id="tblResult").tbody
    rows = table_of_tokens.find_all("tr")
    for row in rows:
        row_data = row.find_all("td")
        coin_name = row_data[1].find("a").text
        num_holders = row_data[6].text.split(' ')[0]
        tmp_df = pd.DataFrame({"name": coin_name, "num_holders": num_holders}, index=[0])
        holders_df = holders_df.append(tmp_df, ignore_index=True)
    time.sleep(5)

holders_df.to_csv("holders.csv")
