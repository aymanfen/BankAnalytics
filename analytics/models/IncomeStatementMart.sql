{{config(materialized='table')}}

SELECT 
    Bank, Date, Quarter, Year, 
    -- PNB
    PNB,
    ROUND((PNB - lagInFrame(PNB) OVER WYoY) / NULLIF(lagInFrame(PNB) OVER WYoY, 0), 4) AS PNBGrowthYoY,
    ROUND((PNB - lagInFrame(PNB) OVER WQoQ) / NULLIF(lagInFrame(PNB) OVER WQoQ, 0), 4) AS PNBGrowthQoQ,
    -- Net Results
    NetResults,
    ROUND((NetResults - lagInFrame(NetResults) OVER WYoY) / NULLIF(lagInFrame(NetResults) OVER WYoY, 0), 4) AS NetResultsGrowthYoY,
    ROUND((NetResults - lagInFrame(NetResults) OVER WQoQ) / NULLIF(lagInFrame(NetResults) OVER WQoQ, 0), 4) AS NetResultsGrowthQoQ,
    -- Operating Expenses
    OperatingExpenses,
    ROUND((OperatingExpenses - lagInFrame(OperatingExpenses) OVER WYoY) / NULLIF(lagInFrame(OperatingExpenses) OVER WYoY, 0), 4) AS OperatingExpensesGrowthYoY,
    ROUND((OperatingExpenses - lagInFrame(OperatingExpenses) OVER WQoQ) / NULLIF(lagInFrame(OperatingExpenses) OVER WQoQ, 0), 4) AS OperatingExpensesGrowthQoQ,
    -- Other Indicators
    ROUND(NetResults / NULLIF(PNB, 0), 4)             AS NetMargin,
    ROUND(OperatingExpenses / NULLIF(PNB, 0), 4)      AS CosttoIncome,
    Account, StatementType

FROM {{ref('IntermediateMetrics')}}
WINDOW
    WYoY AS (PARTITION BY Bank ORDER BY Date ROWS BETWEEN 4 PRECEDING AND CURRENT ROW),
    WQoQ AS (PARTITION BY Bank ORDER BY Date ROWS BETWEEN 1 PRECEDING AND CURRENT ROW)

ORDER BY Date, Bank