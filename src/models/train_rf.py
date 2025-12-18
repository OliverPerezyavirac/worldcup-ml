import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

DATA_PATH = 'data/processed/worldcup_dataset.csv'
df = pd.read_csv(DATA_PATH)

FEATURES = [
    "fifa_rank",
    "fifa_points",
    "fifa_variation",
    "qualifier_Position",
    "qualifier_Points",
    "qualifier_Goal_Difference",
    "confederation",
    "is_host",
    "auto_qualify"
]

TARGET = "target"

x = df[FEATURES]
y = df[TARGET]

x_train, x_test, y_train, y_test = train_test_split(
    x,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)

categorical_features = ["confederation"]
numeric_features = [col for col in FEATURES if col != "confederation"]

preprocessor = ColumnTransformer( transformers=[
    ("cat", OneHotEncoder(handle_unknown = "ignore"), categorical_features),
    ("num", "passthrough", numeric_features)
])

rf_model = RandomForestClassifier(
    n_estimators=300,
    max_depth = 10,
    min_samples_split=5,
    min_samples_leaf=2,
    class_weight="balanced",
    random_state=42
)

model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("calssifier", rf_model)
    ]
)

model.fit(x_train, y_train)

y_pred = model.predict(x_test)

print("Confusión matrix")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report")
print(classification_report(y_test, y_pred))
