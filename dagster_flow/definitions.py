from dagster import Definitions, define_asset_job, load_assets_from_modules, AssetSelection
from dagster_flow.assets import load_data,train_model

all_assets = load_assets_from_modules([load_data, train_model])

ml_pipeline = define_asset_job(name="ml_pipeline", selection=AssetSelection.all())

defs = Definitions(
    assets=all_assets,
    jobs=[ml_pipeline],
)
