## Задача

[Ссылка на описание задачи](https://gist.github.com/sherpc/22409f4184e039ebbd0ebddd3ee59122)

## Запуск

*Перед запуском, пожалуйста, установите `docker` и `docker-compose`.*

```bash
$ docker-compose up
```

### Пример запроса

```
$ curl http://localhost:8080/search?query=clj&query=clojure
{
    "90minut.pl":1,
    "bourgenbresse.fr":1,
    "clj.mx":1,
    "clj.vn":1,
    "cljlaw.com":1,
    "clojure.org":1,
    "fernweh.com":1,
    "flightradar24.com":1,
    "wa.gov":2
}
```

## Настройки

*В корне проекта опционально можно создать файл `.env`, в котором доступны следующие настройки:*

```bash
MAX_HTTP_CONNECTIONS=4  # Максимальное количество одновременных запросов
                        # к сервису bing, по умолчанию 10
```
