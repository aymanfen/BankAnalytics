from dagster import Definitions, asset

@asset
def hello_dagster():
    return "Dagster is running 🚀"

defs = Definitions(
    assets=[hello_dagster]
)
