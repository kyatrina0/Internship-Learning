# Supermarket Sales Analytics (Capstone Project)

Customer segmentation, sales forecasting and order value prediction on supermarket order data.

Week 12 capstone of the internship. The main work is in [`capstone_supermarket.ipynb`](capstone_supermarket.ipynb).

## 1. Problem statement

A supermarket wants to use its order history to answer three questions:

1. **Who are the most valuable customers?** (customer segmentation)
2. **How much will we sell in the next few months?** (monthly sales forecast)
3. **What drives the value of an order?** (order value prediction)

**Success criteria**

- The forecast beats simple baselines on the last 6 months, which the model never sees during training.
- The order value model beats a "predict the average" baseline on unseen data.
- The customer groups are clearly different and usable for a business decision.

## 2. Data

Supermarket order lines (date, ship date, customer, location, category, sub-category, sales). See [`data/README.md`](data/README.md) for the required columns and where to place the file.

**Cleaning:** dates converted to real dates, rows with missing key fields removed, duplicates removed, impossible values removed (ship date before order date, sales of zero or less). The notebook prints a log of how many rows each step removes.

## 3. Approach

| Step | What was done |
|---|---|
| EDA | Sales by year, month (seasonality), category, region, segment, sub-category, state; distribution of sales values |
| Customer segmentation | RFM (recency, frequency, monetary) on log-scaled values, standardised, KMeans; k chosen by silhouette score between 3 and 6 |
| Forecasting | Monthly sales; time-based split (last 6 months as test). Models: naive, 3-month moving average, seasonal naive, linear trend + monthly seasonality, Holt-Winters (if `statsmodels` is installed). Best model refit on all data to forecast the next 6 months |
| Order value prediction | Target is log(1 + Sales). Baseline (average), Linear Regression, Random Forest, Gradient Boosting in a preprocessing pipeline. 5-fold cross-validation picks the best model; test set used once. Permutation importance for interpretation. Also compares with my Week 11 approach |

## 4. Results

Everything below comes from the notebook run on the Kaggle Superstore `train.csv` file (9,800 rows, Jan 2015 - Dec 2018, 793 customers). All numbers are in [`results_summary.md`](results_summary.md), and the charts are in [`figures/`](figures/).

**Customer segmentation (RFM + KMeans, k = 4)**

| Group | Customers | Avg days since last order | Avg orders | Share of sales |
|---|---|---|---|---|
| Tier 1 (highest spend) | 233 (29%) | 98 | 8.7 | 50.6% |
| Tier 2 | 199 (25%) | 20 | 6.7 | 23.6% |
| Tier 3 | 274 (35%) | 223 | 4.9 | 24.1% |
| Tier 4 | 87 (11%) | 350 | 2.6 | 1.7% |

The silhouette score is 0.255, so the groups overlap. The top 20% of customers give 48.5% of sales. Tier 3 is the best win-back target; Tier 4 contributes very little.

**Forecasting (tested on the last 6 months of 2018)**

| Model | MAE | MAPE |
|---|---|---|
| Linear trend + monthly seasonality (best) | 14,668 | 17.6% |
| Seasonal naive | 20,867 | 26.1% |
| Naive (last month) | 31,637 | 35.6% |
| 3-month moving average | 36,186 | 41.0% |

The forecast for Jan-Jun 2019 is about 33k-67k per month (March highest). The best model was below the actual sales in most test months, so it may under-predict if growth continues.

**Order value prediction (target: log sales, test set)**

| Model | R2 (log) | MAE |
|---|---|---|
| Baseline (average) | 0.000 | 229.9 |
| Linear Regression (chosen by cross-validation) | 0.447 | 196.2 |
| Random Forest | 0.437 | 196.4 |
| Gradient Boosting | 0.452 | 194.8 |
| Linear Regression on raw Sales (Week 11 approach) | -0.173 | 232.8 |

Category and sub-category are by far the most important features. The three log-scale models are almost equal, so the simplest one was chosen. The Week 11 approach has a higher R2 on the original sales scale (0.14 vs 0.07), but a larger typical error; both are low on that scale because very large orders cannot be predicted without quantity, price or discount.

**Main findings:** sales grew from about 459k (2016) to 722k (2018); Technology is the top category (36.6%), West the top region (31.4%), and November the strongest month.

## 5. How to run

```bash
pip install -r requirements.txt
# put supermarket.csv in the data/ folder
jupyter notebook capstone_supermarket.ipynb
```

Run all cells. Outputs: `figures/*.png`, `results_summary.md`, `results.json`.

## 6. Repository structure

```
capstone_supermarket.ipynb   main analysis (cleaning, EDA, models)
data/                        put supermarket.csv here
figures/                     charts created by the notebook
results_summary.md           created by the notebook (key numbers)
presentation/                slides (`node make_deck.js .. out.pptx` rebuilds them from results.json)
reflection.md                what I learned
requirements.txt
```

## 7. Limitations

- No quantity, discount, price or profit columns, so the order value model can only use categories and dates.
- Only a few years of monthly data, so seasonality is estimated from few points.
- The forecast is tested on a single 6-month window.
- The order-level split is random, so lines from the same order can be in both train and test.
- Customer tiers are based on past buying behaviour only.

## 8. What I would improve with more time

1. Add quantity, discount and profit and predict profit, not only sales.
2. Use walk-forward validation and compare SARIMA or Prophet.
3. Forecast per category or region.
4. Split order data by customer or time to avoid leakage.
5. Build an interactive dashboard (Streamlit).
6. Test the customer tiers with a real campaign (A/B test).

## 9. Reflection

See [`reflection.md`](reflection.md).
