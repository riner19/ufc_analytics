import pandas as pd
from ufc_scraper import get_fighter_data, get_fighter_url


def compare_fighters(name1, name2):
    """
    1. Finds links to fighters.
    2. Downloads fighters' data.
    3. Compares fighters' data by pandas dataframe.
    4. Returns report for telegram.
    """

    # 1. getting links
    url1 = get_fighter_url(name1)
    url2 = get_fighter_url(name2)

    # if fighter not found
    if not url1 or not url2:
        return f"❌ Unable to find the fighters. Check the names: {name1}, {name2}"

    # 2. Downloading data (using ufc_scraper)
    data1 = get_fighter_data(url1)
    data2 = get_fighter_data(url2)

    if not data1 or not data2:
        return "❌ ERROR GETTING THE DATA."

    # 3. PANDAS analytics
    # create table from 2 fighters
    df = pd.DataFrame([data1, data2])

    df.set_index('Name', inplace=True)

    # Getting difference (Боец 2 - Боец 1).
    # diff() . substration
    # iloc[-1] gets last data.
    difference = df.diff().iloc[-1]

    # 4. Making report
    report = f"🥊 <b>COMPARISON: {data1['Name']} vs {data2['Name']}</b>\n"
    report += "--------------------------\n"

    # Comparing Reach
    reach_diff = difference['Reach']
    if reach_diff > 0:
        report += f"📏 <b>Reach:</b> {data2['Name']} (+{abs(reach_diff):.1f}\")\n"
    elif reach_diff < 0:
        report += f"📏 <b>Reach:</b> {data1['Name']} (+{abs(reach_diff):.1f}\")\n"
    else:
        report += f"📏 <b>Reach:</b> Same ({data1['Reach']}\")\n"

    # Comparing (Str_Acc)
    # multiply by 100 to get percentage
    acc_diff = difference['Str_Acc'] * 100
    if acc_diff > 0:
        report += f"🎯 <b>Accuracy:</b> {data2['Name']} better by {abs(acc_diff):.1f}%\n"
    elif acc_diff < 0:
        report += f"🎯 <b>Accuracy:</b> {data1['Name']} better by {abs(acc_diff):.1f}%\n"

    # Comparing punches per minute (SLpM)
    slpm_diff = difference['SLpM']
    if slpm_diff > 0:
        report += f"👊 <b>Movement pace:</b> {data2['Name']} punches more frequently  (+{abs(slpm_diff):.1f}/мин)\n"
    elif slpm_diff < 0:
        report += f"👊 <b>Movement pace:</b> {data1['Name']} puncher more frequently (+{abs(slpm_diff):.1f}/мин)\n"

    report += "--------------------------\n"
    report += "<i>All of the data from ufcstats.com</i>"

    return report


# --- Test () ---
if __name__ == "__main__":
    print(compare_fighters("Jon Jones", "Tom Aspinall"))