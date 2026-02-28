{{config(materialized='view')}}

SELECT
    Bank,
    Date,
    toYear(Date) AS Year,
    toQuarter(Date) AS Quarter,
    sumIf(IndicatorValue, IndicatorName = 'Produit Net Bancaire')    AS PNB,
    sumIf(IndicatorValue, IndicatorName = 'Resultat Net')            AS NetResults,
    sumIf(IndicatorValue, IndicatorName = 'Charges Exploitation')    AS OperatingExpenses,
    sumIf(IndicatorValue, IndicatorName = 'Total Actif')             AS TotalAssets,
    sumIf(IndicatorValue, IndicatorName = 'Total Passif')            AS TotalLiabilities,
    sumIf(IndicatorValue, IndicatorName = 'Capitaux Propres')        AS Equity,
    sumIf(IndicatorValue, IndicatorName = 'Creances Clientele')      AS Loans,
    sumIf(IndicatorValue, IndicatorName = 'Dettes Clientele')        AS Deposits,   
    CASE
        WHEN Type LIKE '%Consolidated%' THEN 'Consolidated'
        ELSE 'Normal'
    END AS Account,

    CASE
        WHEN Type LIKE '%IncomeStatement%' THEN 'IncomeStatement'
        WHEN Type LIKE '%Assets%'    THEN 'Assets'
        WHEN Type LIKE '%Liabilities%'    THEN 'Liabilities'
    END AS StatementType


FROM analytics.stg
GROUP BY Date, Bank, Type
ORDER BY Date, Bank