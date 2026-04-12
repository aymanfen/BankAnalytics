{{config(materialized='view')}}

SELECT
    Bank,
    Date,
    toYear(Date) AS Year,
    toQuarter(Date) AS Quarter,

    sumIf(IndicatorValue, IndicatorName = 'NetBankingIncome') AS PNB,
    sumIf(IndicatorValue, IndicatorName = 'NetIncome') AS NetResults,
    ABS(sumIf(IndicatorValue, IndicatorName = 'OperatingExpenses')) AS OperatingExpenses,

    sumIf(IndicatorValue, IndicatorName = 'TotalAssets') AS TotalAssets,
    sumIf(IndicatorValue, IndicatorName = 'TotalLiabilities') AS TotalLiabilities,
    sumIf(IndicatorValue, IndicatorName = 'PrivateEquity') AS Equity,

    sumIf(IndicatorValue, IndicatorName IN ('InstitutionsLoans','CustomersLoans')) AS Loans,
    sumIf(IndicatorValue, IndicatorName IN ('InstitutionsCredit','CustomersCredit')) AS Deposits,

    Account

FROM (

    SELECT *,
        CASE
            WHEN Type LIKE '%Consolidated%' THEN 'Consolidated'
            ELSE 'Normal'
        END AS Account
    FROM analytics.stg

)

GROUP BY Date, Bank, Account

ORDER BY Date, Bank