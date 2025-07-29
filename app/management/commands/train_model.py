from django.core.management.base import BaseCommand
from recommend_engine.data_loader import prepare_training_data
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pickle
import pandas as pd


class Command(BaseCommand):
    help = 'Train recommendation model and save as pickle'

    def handle(self, *args, **kwargs):
        df = prepare_training_data()

        if df.empty:
            self.stdout.write("No ratings found. Please add some before training.")
            return

        # 🚧 Encode categorical features before training
        
        X_raw = df.drop(columns=['rating'])

        X_encoded = pd.get_dummies(X_raw, drop_first=True)

        y = df['rating'] > 3.5

        X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2)
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        model = RandomForestClassifier()
        model.fit(X_train_scaled, y_train)

        with open('recommend_engine/random_forest.pkl', 'wb') as f:
            pickle.dump(model, f)

        with open('recommend_engine/input_columns.pkl', 'wb') as f:
            pickle.dump(X_encoded.columns.tolist(), f)

        self.stdout.write(self.style.SUCCESS("Model trained and saved as random_forest.pkl"))
