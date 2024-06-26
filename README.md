# Тестовое задание Python Developer

Этот репозиторий содержит решение тестового задания Python Developer, выполненного в рамках процесса собеседования.

## Описание задачи

Задача состояла в написании алгоритма агрегации статистических данных о зарплатах сотрудников компании по временным промежуткам. Данные были предоставлены в виде коллекции MongoDB.

## Примеры входных данных и соответствующих ответов
### Входные данные

Алгоритм принимает на вход следующие параметры:
- Дата и время начала агрегации (ISO формат)
- Дата и время окончания агрегации (ISO формат)
- Тип агрегации: hour, day, month

### Выходные данные

На выходе алгоритм формирует:
- Агрегированный массив данных (`dataset`)
- Подписи к значениям агрегированного массива данных в ISO формате (`labels`)

Пример ответа:
1. Входные данные:
   ```
   {
       "dt_from": "2022-09-01T00:00:00",
       "dt_upto": "2022-12-31T23:59:00",
       "group_type": "month"
   }
   ```
   Ответ:
   ```
   {"dataset": [5906586, 5515874, 5889803, 6092634], "labels": ["2022-09-01T00:00:00", "2022-10-01T00:00:00", "2022-11-01T00:00:00", "2022-12-01T00:00:00"]}
   ```

2. Входные данные:
   ```
   {
       "dt_from": "2022-10-01T00:00:00",
       "dt_upto": "2022-11-30T23:59:00",
       "group_type": "day"
   }
   ```
   Ответ:
   ```
   {"dataset": [0, 0, 0, 195028, 190610, 193448, 203057, 208605, 191361, 186224, 181561, 195264, 213854, 194070,
               208372, 184966, 196745, 185221, 196197, 200647, 196755, 221695, 189114, 204853, 194652, 188096, 215141,
               185000, 206936, 200164, 188238, 195279, 191601, 201722, 207361, 184391, 203336, 205045, 202717, 182251,
               185631, 186703, 193604, 204879, 201341, 202654, 183856, 207001, 204274, 204119, 188486, 191392, 184199,
               202045, 193454, 198738, 205226, 188764, 191233, 193167, 205334],
   "labels": ["2022-10-01T00:00:00", "2022-10-02T00:00:00", "2022-10-03T00:00:00", ...]}
   ```

### Реализация Telegram бота

Решение также включает реализацию Telegram бота, который принимает от пользователей текстовые сообщения содержащие JSON с входными данными и возвращает агрегированные данные в ответ.

## Импорт данных в MongoDB

Для импорта предоставленной коллекции данных в MongoDB можно использовать команду:
```
mongorestore --db rlt_test --collection salaries C:\UserPath\sample_collection.bson
```

## Запуск бота

Для запуска бота необходимо указать токен в файле `/files/envs/.env` и выполнить файл `python bot.py`.

## Ссылка на коллекцию данных

Коллекция со статистическими данными доступна по [ссылке](https://drive.google.com/file/d/1pcNm2TAtXHO4JIad9dkzpbNc4q7NoYkx/view?usp=sharing).


