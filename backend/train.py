import pandas as pd
import joblib

from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

from config import path_to_data, filename
from config import features_for_train


class Train():
    data = pd.read_csv(path_to_data)

    def encoder(self, df, feature):
        le = LabelEncoder()
        le.fit(df[feature])
        df[feature] = le.transform(df[feature])

    def encode_data(self, df):
        object_types = ['soil', 'region', 'weatherDesc', 'winddir16Point']
        for i in object_types:
            self.encoder(df, i)
        return df

    def normalize(self):
        features = features_for_train
        data = self.encode_data(self.data)
        data_changed = data[features]
        data_y = data_changed['crop']
        data_x = data_changed.drop(columns=['crop'])
        scaler = MinMaxScaler()
        scaler.fit(data_x)
        if 'crop' in features:
            features.remove('crop')
        data_x = pd.DataFrame(scaler.transform(data_x), columns=features)

        return data_x, data_y

    def train(self):
        print('INFO: Normalize data!')
        data_x, data_y = self.normalize()
        print('INFO: Split data!')
        data_x_train, data_x_test, data_y_train, data_y_test = train_test_split(data_x,
                                                                                data_y,
                                                                                test_size=0.20,
                                                                                random_state=42)
        print('INFO: Train data!')
        model = XGBRegressor()
        model.fit(data_x_train, data_y_train)
        data_y_pred = model.predict(data_x_test)
        print('INFO: Model predicted(mse): ', mean_squared_error(data_y_test, data_y_pred))
        joblib.dump(model, filename)

if __name__ == "__main__":
    train = Train()
    train.train()