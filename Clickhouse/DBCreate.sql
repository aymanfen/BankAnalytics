CREATE TABLE IF NOT EXISTS analytics.stg
(
    IndicatorName String,
    Date Date,
    IndicatorValue Float64,
    Bank String,
    Type String
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(Date)
ORDER BY (Bank, Type, IndicatorName, Date);
