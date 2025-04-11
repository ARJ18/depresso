from dagster import asset, Output, MetadataValue, AssetExecutionContext, Field
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib


@asset(
        config_schema={"n_estimators": Field(int, default_value=50)}
)
def train_model(context:AssetExecutionContext, load_train_csv: Output) -> RandomForestClassifier:
    df = load_train_csv

    X = df.drop(columns=["depression"])  
    y = df["depression"]

    model = RandomForestClassifier(context.op_config["n_estimators"])
    model.fit(X, y)

    return model

@asset
def test_model(load_test_csv: Output, train_model: RandomForestClassifier) -> Output:
    model = train_model
    df = load_test_csv

    X = df.drop(columns=["depression"])  
    y = df["depression"]

    y_pred = model.predict(X)
    accuracy = accuracy_score(y,y_pred)
    
    joblib.dump(model, "models/model.pkl")
    return Output(
        "models/model.pkl",
        metadata={
            "Accuracy" : MetadataValue.text(f"{accuracy:.2%}"),
            "Model Path" : "models/model.pkl"
        }   
    )