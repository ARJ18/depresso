from dagster import asset,Output,MetadataValue
import pandas as pd

@asset
def load_train_csv() -> Output:
    df = pd.read_csv("data/train.csv")
    return Output(
        df,
        metadata={
            "Train Data":MetadataValue.md(df.head(5).to_markdown())
        }
    )

@asset
def load_test_csv() -> Output:
    df = pd.read_csv("data/test.csv")
    return Output(
        df,
        metadata={
            "Test Data":MetadataValue.md(df.head(5).to_markdown())
        }
    )