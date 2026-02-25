# Отчет по заданию (TS6 Classifier Features)

## Ссылка на репозиторий
`https://github.com/Lukashevskiy/ts6-classifier`

## Ссылка на релиз с файлами
`<вставьте_ссылку_на_GitHub_Release>`

## Датасет
- Источник: `https://bastion6.erc.monash.edu/static/download/T6SE_training_data.zip`
- Локальный файл: `data/t6se-training-data.zip`
- Наборы:
  - positive: 138 последовательностей (в CSV: 139 строк с заголовком)
  - negative: 1112 последовательностей (в CSV: 1113 строк с заголовком)

## Что рассчитано
### I. Sequence-based features
- AAC: `out/positive_aac.csv`, `out/negative_aac.csv`
- DPC: `out/positive_dpc.csv`, `out/negative_dpc.csv`
- QSO: `out/positive_qso.csv`, `out/negative_qso.csv`

### II. Physicochemical features
- 7 physicochemical properties (CTDC): `out/positive_ctdc.csv`, `out/negative_ctdc.csv`
- CTDT (частота переходов A->B групп): `out/positive_ctdt.csv`, `out/negative_ctdt.csv`

## Примеры расчета (по 1 строке из positive/negative)
### AAC
- Positive example (`out/positive_aac.csv`):
```csv
id,label,AAC_A,AAC_C,AAC_D,AAC_E,...,AAC_Y
gi|77358963|ref|YP_338391.1|hypothetical,1,0.07692307692307693,0.0,0.05325443786982249,0.08875739644970414,...,0.04142011834319527
```
- Negative example (`out/negative_aac.csv`):
```csv
id,label,AAC_A,AAC_C,AAC_D,AAC_E,...,AAC_Y
gi|56416452|ref|YP_153526.1|,0,0.07017543859649122,0.017543859649122806,0.04678362573099415,0.06432748538011696,...,0.03508771929824561
```

### DPC
- Positive example: `out/positive_dpc.csv`
- Negative example: `out/negative_dpc.csv`
- Формат столбцов: `DPC_AA ... DPC_YY` (400 признаков).

### QSO
- Positive example (`out/positive_qso.csv`): признаки вида `QSO_QSOSW*`, `QSO_QSOgrant*`
- Negative example (`out/negative_qso.csv`): те же группы признаков.

### CTDC (7 physicochemical properties)
- Positive example: `out/positive_ctdc.csv`
- Negative example: `out/negative_ctdc.csv`
- Формат: `CTDC_<property>_G1/G2/G3`, где `<property>`:
  - `hydrophobicity`, `polarity`, `charge`, `secondary_structure`,
  - `solvent_accessibility`, `polarizability`, `vdw_volume`.

### CTDT
- Positive example: `out/positive_ctdt.csv`
- Negative example: `out/negative_ctdt.csv`
- Формат: `CTDT_<property>_12`, `CTDT_<property>_13`, `CTDT_<property>_23`.

## Полные файлы выгрузки
- Общие таблицы:
  - `out/positive_features.csv`, `out/negative_features.csv`, `out/all_features.csv`
  - и TSV-версии: `out/*_features.tsv`
- По каждому блоку отдельно:
  - `out/*_aac.csv|tsv`
  - `out/*_dpc.csv|tsv`
  - `out/*_qso.csv|tsv`
  - `out/*_ctdc.csv|tsv`
  - `out/*_ctdt.csv|tsv`

## Как воспроизвести
```bash
cd /home/dmitriyl/bioinformatics/ts6classifier
PYTHONPATH=src venv/bin/python scripts/make_features.py
```

## Что приложено в релиз
- `REPORT.md`
- Все файлы `out/*.csv`
- Все файлы `out/*.tsv`
