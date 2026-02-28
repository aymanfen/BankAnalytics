{{config(materialized='table')}}

SELECT
    Bank,Date,Year,Quarter,
    TotalAssets,
    TotalLiabilities,
    Equity,
    Loans,
    Deposits,
    ROUND(NetResults / NULLIF(TotalAssets, 0), 4)      AS ROA,
    ROUND(NetResults / NULLIF(Equity, 0), 4)            AS ROE,
    ROUND(TotalAssets / NULLIF(Equity, 0), 4)            AS Leverage,
    ROUND(Equity / NULLIF(TotalAssets, 0), 4)            AS EquityRatio,
    ROUND(Loans / NULLIF(Deposits, 0), 4)                 AS LoanstoDeposits,
    Account, StatementType
    

FROM {{ref('IntermediateMetrics')}}
ORDER BY Date, Bank