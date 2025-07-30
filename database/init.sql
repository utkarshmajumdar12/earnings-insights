-- Dimensions
CREATE TABLE IF NOT EXISTS dim_company (
  company_id SERIAL PRIMARY KEY,
  cik        TEXT UNIQUE,
  ticker     TEXT UNIQUE,
  sector     TEXT
);

CREATE TABLE IF NOT EXISTS dim_period (
  period_id  SERIAL PRIMARY KEY,
  fiscal_year INT,
  fiscal_qtr  INT,
  period_end  DATE,
  UNIQUE (fiscal_year, fiscal_qtr)
);

-- Fact table
CREATE TABLE IF NOT EXISTS fact_earnings (
  fact_id     BIGSERIAL PRIMARY KEY,
  company_id  INT REFERENCES dim_company,
  period_id   INT REFERENCES dim_period,
  revenue     NUMERIC(18,2),
  op_income   NUMERIC(18,2),
  eps_basic   NUMERIC(10,2),
  filed_ts    TIMESTAMP,
  UNIQUE (company_id, period_id)
);

-- Transcript sentiment
CREATE TABLE IF NOT EXISTS fact_transcript (
  trans_id    BIGSERIAL PRIMARY KEY,
  company_id  INT REFERENCES dim_company,
  period_id   INT REFERENCES dim_period,
  call_date   DATE,
  sentiment_compound NUMERIC(5,4),
  sentiment_pos NUMERIC(5,4),
  sentiment_neg NUMERIC(5,4),
  sentiment_neu NUMERIC(5,4)
);

-- Exception view
CREATE MATERIALIZED VIEW IF NOT EXISTS vw_margin_spike AS
SELECT f.*, 
       ROUND(op_income / NULLIF(revenue,0) * 100,2) AS margin_pct,
       LAG(ROUND(op_income / NULLIF(revenue,0) *100,2))
         OVER (PARTITION BY company_id ORDER BY p.period_end) AS prev_margin_pct,
       CASE WHEN ABS(
         (op_income / NULLIF(revenue,0)) -
         LAG(op_income / NULLIF(revenue,0)) OVER (PARTITION BY company_id ORDER BY p.period_end)
       ) > 0.025 THEN 'FLAG' END AS margin_spike
FROM fact_earnings f
JOIN dim_period p USING(period_id);
