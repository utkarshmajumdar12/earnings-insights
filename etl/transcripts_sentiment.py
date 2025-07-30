import os, requests, pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from db import get_conn, upsert_df

API = "https://financialmodelingprep.com/api/v3/earning_call_transcript"
analyzer = SentimentIntensityAnalyzer()

def fetch_transcript(ticker, year, qtr):
    url = f"{API}/{ticker}?year={year}&quarter={qtr}&apikey={os.getenv('FMP_KEY')}"
    return requests.get(url, timeout=30).json()

def load_sentiment():
    tickers = ["TSLA", "GOOG"]
    for t in tickers:
        for y in range(2020, 2022):
            for q in range(1, 5):
                data = fetch_transcript(t, y, q)
                # Ensure data is a non-empty list with a 'content' key
                if not data or not isinstance(data, list) or len(data) == 0:
                    print(f"No transcript for {t} Q{q} {y}")
                    continue
                if "content" not in data[0]:
                    print(f"No 'content' field in transcript for {t} Q{q} {y}: {data[0]}")
                    continue

                text = data[0]["content"]
                scores = analyzer.polarity_scores(text)
                save(t, y, q, data[0].get("date"), scores)

def save(ticker, fy, fq, call_date, s):
    conn = get_conn(); cur = conn.cursor()
    cur.execute("SELECT company_id FROM dim_company WHERE ticker=%s",(ticker,))
    cid = cur.fetchone()
    if not cid: return
    cur.execute("SELECT period_id FROM dim_period WHERE fiscal_year=%s AND fiscal_qtr=%s",(fy,fq))
    pid = cur.fetchone()
    if not pid: return
    cur.execute("""INSERT INTO fact_transcript (company_id, period_id, call_date,
                  sentiment_compound, sentiment_pos, sentiment_neg, sentiment_neu)
                  VALUES (%s,%s,%s,%s,%s,%s,%s)
                  ON CONFLICT DO NOTHING""",
                (cid[0], pid[0], call_date,
                 s['compound'], s['pos'], s['neg'], s['neu']))
    conn.commit(); cur.close(); conn.close()

if __name__ == "__main__":
    load_sentiment()
