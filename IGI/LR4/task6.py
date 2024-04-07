import pandas as pd

test_series = pd.Series([-10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10])
# Series внешне похож на одномерный массив, но на самом деле это ассоцциативный массив:
print(test_series)

# Поэтому создать Series можно и так:
test_series = pd.Series({'1': -10, '2': -8, '3': -6, '4': -4, 4: 'wew'})

# Обратимся отдельно к индексам и к значениям: 
print(f"Индексы: {test_series.index}")
print(f"Значения: {test_series.values}")

# Series поддерживают индексацию, как и обычные массивы: 
print(f"test_series[4]={test_series[4]}")

# При создании Series можно указать значения для индексов (размерности должны совпадать):
test_series = pd.Series([-10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10], index=['first', 'second', 'third', '4', '5', '6', '7', '8', '9', '10', '11'])
print(test_series)

# Series позволяет получать доступ к нескольким элементам одновременно: 
test_series[['first', 'second']] = -1
print(f"{test_series[['first', 'second']]}\n")

# Индексы можно менять динамически
test_series.index = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

# DataFrame - табличная структура данных
data_frame = pd.DataFrame({
    'name':  ['Liza', 'Petya', 'Katya', 'Viktor'],
    'pet':   ['cat',  'dog',   'duck',  'rabbit'],
    'hobby': ['IT',   'med',   'teach', 'draw']
}) #, index=["Gird", "Boy", "Girl", "Boy"]

print("Таблица data_frame\n", data_frame)

# В DataFrame столбцы таблицы - это объекты Series, к которым можно обратиться по ключу
print('\nСтрока name - это Series:\n', data_frame['name'])

# Ко всем столбцам можно обратиться так
print('\n', data_frame.columns)

# А строки по умолчанию имеют целочисленную индексацию:
print('\n', data_frame.index)

# Индексацию по строкам можно изменить динамически (как у объекта Series)
data_frame.index = ['Girl', 'Boy', 'Girl', 'Boy']
data_frame.index_name = 'GN'
print(data_frame)

# Доступ к строкам по индексу можно осуществить 2-мя способами
# loc - используем строковый ключ
print('\nloc: \n', data_frame.loc['Girl'])
# iloc - используем целочисленный ключ
print('\niloc: \n', data_frame.iloc[0])

# Также можно узнать количество строк в таблице
print('\nrow count:\n',len(data_frame))

# Можно напечатать несколько верхних или нижних столбцов:
print('\nhead(2):\n', data_frame.head(2))
print('\ntail(2):\n', data_frame.tail(2))

# loc может работать более сложным способом
# в первый аргумент передать интересующие строки, а во второй - столбцы
print('\ncomplex loc: \n', data_frame.loc[['Girl'], 'pet'])

# можно также использовать срезы и фильтры:
print('\nslice loc:\n', data_frame.loc['Girl', 'pet':'hobby'])

# DataFrame позволяет добавлять, переименовывать и удалять столбцы
data_frame['country']=['BR', 'RF', 'UK', "BK"]
print('\nnew column:\n', data_frame)
data_frame = data_frame.rename(columns={'pet': 'best pet'})
print('\nrenamed column:\n', data_frame)
data_frame = data_frame.drop(['hobby'], axis='columns')
print('\ndeleted column:\n', data_frame)

# Поработаем с данными!

# Сохраним старые данные 
data_frame.to_csv('pandas.csv', sep=';', quotechar="'")

# Возьмем наши данные из задания 1 в формате csv и считаем их
data_frame = pd.read_csv('students.csv')
print('\nnew data:\n', data_frame)

# Теперь поработаем с анализом данных!
data_frame = pd.DataFrame({
    'name':     ['John', 'Mike', 'Loly', 'Emma', 'Justin', 'Mark', 'Gigi'],
    'age':      [23,     28,      19,     12,     45,       32,    34],
    'country':  ['UK',   'USA',  'USA',  'UK',   'FR',     'AV',   'GR'],
    'married':  [1,      1,       0,      0,      1,        1,     1]
})
print('\ndata for analysing:\n', data_frame)

# Сгруппируем данные по странам и женатым:
print(data_frame.groupby('country')['married'].count())

# Получим количество уникальных стран
print('\nunique countries:\n', len(data_frame['country'].unique()))

# Подсчитаем сумму возрастов в каждой стране
print('\nage sum:\n', data_frame.groupby('country')['age'].sum())

# Расчитаем средний возраст по стране
print('\nage mean:\n', data_frame.groupby('country')['age'].mean())

# Определим самого старого
print('\nthe oldest:\n', data_frame.sort_values(by='age', ascending=False))

# Отфильтруем данные и получим список женатых
print('\nmarried:\n', data_frame[data_frame['married']==1])

# Получаем список тех, кто старше 30 лет
print('\nolder than 30:\n', data_frame[data_frame['age']>=30])

# Напечатаем общую информацию о таблице
print('\ngeneral info: \n', data_frame.describe())

# Можно комбинировать таблицы
print(pd.concat([data_frame, data_frame]))