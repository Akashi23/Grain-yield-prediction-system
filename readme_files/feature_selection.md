## Feature Selection with XGBoostRegressor with feature_importances_

```
from xgboost import XGBRegressor
model = XGBRegressor()
model.fit(data_x, data_y)
feature_assess = model.feature_importances_
plt.bar(range(len(model.feature_importances_)), model.feature_importances_)
plt.show()
```

```
from xgboost import XGBRegressor
model = XGBRegressor()
model.fit(data_x, data_y)
feature_assess = model.feature_importances_
plt.bar(range(len(model.feature_importances_)), model.feature_importances_)
plt.show()
```

```
f = {}
p = 0
ls = list(data.columns) 
for i in feature_assess:
    if i >  1.0e-05:
        f[p] = i
    p += 1
print(f)
for i in f:
    data = data.drop(columns=[ls[i]])
print(data)
```
