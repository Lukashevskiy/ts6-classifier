# REPORT v2.0 (T6SE Classifier)

## Репозиторий
`https://github.com/Lukashevskiy/ts6-classifier`

## Что сделано в текущей версии
В репозитории подготовлен полный ноутбук для задачи классификации эффекторных белков:
- [notebooks/model_ensemble_t6se.ipynb](/home/dmitriyl/bioinformatics/ts6classifier/notebooks/model_ensemble_t6se.ipynb)

Реализованы этапы:
1. Загрузка данных признаков (`out/all_features.csv`) и проверка качества данных.
2. Подготовка признаков:
- удаление служебных полей (`id`, `label`);
- удаление константных признаков (`VarianceThreshold`);
- отбор информативных признаков (`SelectPercentile`, ANOVA F-score);
- масштабирование (`StandardScaler`) для SVM/MLP.
3. Сравнение нелинейных моделей на одинаковой методологии:
- `SVM (RBF)`;
- `RandomForest`;
- `MLP`.
4. Валидация:
- `StratifiedKFold` (5-fold);
- метрики: `F1`, `ROC-AUC`, `PR-AUC`, `balanced accuracy`.
5. Тюнинг только одной модели через `GridSearchCV`:
- `SVM_RBF` (подбор `C`, `gamma`, `select__percentile`).
6. Сравнение baseline vs tuned-модель на отложенном test.
7. Блок сохранения лучшей модели для следующего задания через `pickle`.

## Используемые данные
- Источник архива: `https://bastion6.erc.monash.edu/static/download/T6SE_training_data.zip`
- Локально: `data/t6se-training-data.zip`
- Сформированные признаки:
- `out/all_features.csv` (основной файл для моделирования)
- `out/positive_features.csv`, `out/negative_features.csv`
- отдельные таблицы `AAC/DPC/QSO/CTDC/CTDT` в `out/`

## Выводы по подходу
1. Для дисбалансного датасета (~8:1) основная метрика отбора модели: `F1` (плюс контроль `PR-AUC`).
2. Подготовка признаков через pipeline обязательна для честной кросс-валидации и исключения leakage.
3. Тюнинг одной модели (`SVM_RBF`) снижает вычислительную нагрузку и соответствует требованию сравнить подходы + выполнить подбор параметров.

## Сохранение и загрузка модели
После запуска финальных ячеек ноутбука сохраняются:
- `models/t6se_best_model.pkl`
- `models/t6se_best_model_metadata.json`

Пример загрузки:
```python
import pickle
import pandas as pd
from pathlib import Path

model_path = Path("models/t6se_best_model.pkl")
with open(model_path, "rb") as f:
    model = pickle.load(f)

# df_new должен содержать те же feature-колонки, что и в train
df_new = pd.read_csv("out/all_features.csv").drop(columns=["id", "label"]).head(5)
pred = model.predict(df_new)
proba = model.predict_proba(df_new)[:, 1]
print(pred, proba)
```

## Как воспроизвести
```bash
cd /home/dmitriyl/bioinformatics/ts6classifier
venv/bin/python scripts/make_features.py
```
Далее открыть и выполнить:
- `notebooks/model_ensemble_t6se.ipynb`
