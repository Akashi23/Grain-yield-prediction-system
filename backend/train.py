import pandas as pd
import joblib
import math

from xgboost import XGBRegressor, cv, DMatrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import cross_validate

from config import path_to_data, filename, filename_scaler
from config import features_for_train



class Train():
    data = pd.read_csv(path_to_data)
    scaler_enc = None

    def encoder(self, df, feature):
        le = LabelEncoder()
        le.fit(df[feature])
        df[feature] = le.transform(df[feature])
        return le

    def encode_data(self, df):
        object_types = ['soil', 'region', 'weatherDesc', 'winddir16Point']
        for i in object_types:
            self.encoder(df, i)
        return df

    def normalize(self, data, features_for_train_):
        features = features_for_train_
        data = self.data.copy()
        data = self.encode_data(data)
        data_changed = data[features]
        print(data_changed)
        date = data_changed[['year', 'month', 'day']]
        data_y = data_changed['crop']
        data_x = data_changed.drop(columns=['crop', 'year', 'month', 'day'])
        scaler = MinMaxScaler()
        scaler.fit(data_x)
        joblib.dump(scaler, filename_scaler)
        if 'crop' in features:
            features.remove('crop')
            features.remove('year')
            features.remove('month')
            features.remove('day')
        data_x = pd.DataFrame(scaler.transform(data_x), columns=features)
        data_x = data_x.merge(date, left_index=True, right_index=True)

        return data_x, data_y

    def train(self):
        print('INFO: Normalize data!')
        data_x, data_y = self.normalize(self.data, features_for_train)
        print('INFO: Split data!')
        print(data_x)
        data_x_train, data_x_test, data_y_train, data_y_test = train_test_split(data_x,
                                                                                data_y,
                                                                                test_size=0.20,
                                                                                random_state=42)
        print('INFO: Train data!')
        model = XGBRegressor()
        model.fit(data_x_train, data_y_train)
        data_y_pred = model.predict(data_x_test)
        
        data_y_test_db = pd.DataFrame(data_y_test, columns=['crop']).reset_index(drop=True)
        data_y_pred_db = pd.DataFrame(data_y_pred, columns=['crop_pred'])
        date = self.data['date']
        region = self.data['region']
        print(self.data)
        data_x_test = data_x_test.drop(columns=['region'])
        data_x_test = data_x_test.merge(date, left_index=True, right_index=True)
        data_x_test = data_x_test.merge(region, left_index=True, right_index=True)
        print(data_x_test['date'])

        data_x_test_db = data_x_test.reset_index(drop=True)
        result = pd.concat([data_x_test_db, data_y_test_db, data_y_pred_db], axis=1)
        result.to_csv('data/dataset_train_test.csv', index=False)

        print('INFO: Model predicted(rmse): ', math.sqrt(mean_squared_error(data_y_test, data_y_pred)))
        # send_data_rmse('')

        joblib.dump(model, filename)

if __name__ == "__main__":
    train = Train()
    train.train()