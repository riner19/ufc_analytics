
from ufc_scraper import get_fighter_url, get_fighter_data
import pandas as pd


# Testing work
def test_system():
    #Asking for name
    target_name = "Khabib"
    print(f"🔍 Fighter to look for: {target_name}...")

    #Looking for a link
    url = get_fighter_url(target_name)

    if url:
        print(f"✅ Link found: {url}")

        #Getting statistics
        data = get_fighter_data(url)

        #Printing result
        df = pd.DataFrame([data])
        print("\n📊 fighter Statistics:")
        print(df.to_string(index=False))  # to_string removes excess indexes
    else:
        print("❌ Fighter not found.")


if __name__ == "__main__":
    test_system()