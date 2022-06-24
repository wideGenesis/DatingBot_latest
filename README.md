## Hi there 👋 I'm a Backend python developer and data scientist

<a href="https://t.me/DJWOMS">
  <img align="left" alt="Telegram" width="22px" src="https://camo.githubusercontent.com/5c1975da7d9ab735ceb71c57b6c7e48ff3e08ca4/68747470733a2f2f6564656e742e6769746875622e696f2f537570657254696e7949636f6e732f696d616765732f7376672f74656c656772616d2e737667">
</a>
<a href="https://www.linkedin.com/in/michael-omelchenko-100453156/">
  <img align="left" alt="LinkedIN" width="22px" src="https://raw.githubusercontent.com/peterthehan/peterthehan/master/assets/linkedin.svg" />
</a>

</br>

## Technology stack

**Back-end**

![Python](https://img.shields.io/badge/-Python-black?style=flat-square&logo=Python)
![Django](https://img.shields.io/badge/-Django-0aad48?style=flat-square&logo=Django)
![Django Rest Framework](https://img.shields.io/badge/DRF-red?style=flat-square&logo=Django)
![FastAPI](https://img.shields.io/badge/-FastAPI-%2300C7B7?style=flat-square&logo=FastAPI)
![Flask](https://img.shields.io/badge/-Flask-%232c3e50?style=flat-square&logo=Flask)
![ORMAR](https://img.shields.io/badge/-ORMAR-DD0031?style=flat-square&logo=ORMAR)
![SqlAlchemy](https://img.shields.io/badge/-SqlAlchemy-FCA121?style=flat-square&logo=SqlAlchemy)
![Celery](https://img.shields.io/badge/-Celery-%2300C7B7?style=flat-square&logo=Celery)
![Celery](https://img.shields.io/badge/-Celery-%2300C7B7?style=flat-square&logo=Celery)

**Databases**

![Postgresql](https://img.shields.io/badge/-Postgresql-%232c3e50?style=flat-square&logo=Postgresql)
![Mysql](https://img.shields.io/badge/-Postgresql-%232c3e50?style=flat-square&logo=Postgresql)
![MS SQL](https://img.shields.io/badge/-Postgresql-%232c3e50?style=flat-square&logo=Postgresql)
![Redis](https://img.shields.io/badge/-Redis-FCA121?style=flat-square&logo=Redis)

**Front-end**

![HTML5](https://img.shields.io/badge/-HTML5-%23E44D27?style=flat-square&logo=html5&logoColor=ffffff)
![CSS3](https://img.shields.io/badge/-CSS3-%231572B6?style=flat-square&logo=css3)

**Tools**

![Docker](https://img.shields.io/badge/-Docker-46a2f1?style=flat-square&logo=docker&logoColor=white)
![IntelliJ](https://img.shields.io/badge/-IntelliJ%20IDEA-ffce5a?style=flat-square&logo=jetbrains)
![Postman](https://img.shields.io/badge/Postman-FCA121?style=flat-square&logo=postman)

![Linux](https://img.shields.io/badge/Linux-black?style=flat-square&logo=linux)
![Git](https://img.shields.io/badge/-Git-black?style=flat-square&logo=git)
![GitHub](https://img.shields.io/badge/-GitHub-181717?style=flat-square&logo=github)
![GitLab](https://img.shields.io/badge/-GitLab-FCA121?style=flat-square&logo=gitlab)


## 𝗦𝘁𝗮𝘁𝘀

![DJWOMS github stats](https://github-readme-stats.vercel.app/api?username=wideGenesis&show_icons=true&theme=dracula&include_all_commits=true&count_private=true)
![DJWOMS Languages](https://github-readme-stats.vercel.app/api/top-langs/?username=wideGenesis&layout=compact&count_private=true&theme=gruvbox)


https://stackoverflow.com/questions/64943693/what-are-the-best-practices-for-structuring-a-fastapi-project

https://christophergs.com/tutorials/ultimate-fastapi-tutorial-pt-8-project-structure-api-versioning/#structure

https://swagger.io/specification/

https://github.com/tiangolo/full-stack-fastapi-postgresql

https://developer.twitter.com/en/docs/api-reference-index

https://api.cloudflare.com/#getting-started-resource-ids

Success Response (example)
{
  "result": {
    "id":"2d4d028de3015345da9420df5514dad0",
    "type":"A",
    "name":"blog.example.com",
    "content":"2.6.4.5",
    "proxiable":true,
    "proxied":false,
    "ttl":1,
    "priority":0,
    "locked":false,
    "zone_id":"cd7d068de3012345da9420df9514dad0",
    "zone_name":"example.com",
    "modified_on":"2014-05-28T18:46:18.764425Z",
    "created_on":"2014-05-28T18:46:18.764425Z"
  },
  "success": true,
  "errors": [],
  "messages": [],
  "result_info": {
    "page": 1,
    "per_page": 20,
    "count": 1,
    "total_count": 200
  }
}

Error Response (example)
{
  "result": null,
  "success": false,
  "errors": [{"code":1003,"message":"Invalid or missing zone id."}],
  "messages": []
}

HTTP response codes
Code	Status	Description
200	OK	request successful
304	Not Modified
400	Bad Request	request was invalid
401	Unauthorized	user does not have permission
403	Forbidden	request not authenticated
429	Too many requests	client is rate limited
405	Method Not Allowed	incorrect HTTP method provided
415	Unsupported Media Type	response is not valid JSON

Get User Details
Patch Edit User
Post Create User
Delete User

https://developer.twitter.com/en/docs/api-reference-index
Endpoints and Methods Examples

## REST API
При реализации ручек для потребителей API описываю в ручке следущее:
- ```summary``` - краткое описание ручки
- ```status_code``` - успешый конечный код  
- ```response_model``` - Возвращаемая схема данных Pydantic
- ```responses``` - Все возможные варианты ответы ручки кроме серверных (500-х)
- ```Многострочные докстринги``` - Описываю полное описание ручки вместе с бизнес-логикой которая должна быть выполнена и валидация данных.

```
@router.get(
    "/{account_id}",
    summary='Get account by id',
    status_code=status.HTTP_200_OK,
    response_model=AccountData,
    responses={
        **USER_BASE_RESPONSES,
        status.HTTP_200_OK: {"description": BaseMessage.obj_data.value},
        status.HTTP_404_NOT_FOUND: {
            "model": MessageErrorSchema,
            "description": AccountErrors.account_not_found.docs_response
        },
    },
)
async def get_account_by_id_request(account_id: int) -> AccountData:
    """
    Get account by id.

    *Business-logic*:
        -  Account must be in database
    """

    return await service_accounts.get_account_by_id(account_id)

```
Префикс _request делается чтобы не получить проблему с неймингом при вызове из слоя Logic если импортируется только одна функция из слоя.

## Как ходят данные в проекте
![](https://habrastorage.org/webt/lo/2p/sa/lo2psa2bbtir0p1caxdfcgmymkw.png)

## Композиция файлов в проекте
### **API | Routes**
- Прием данных
- Отдача данных

### **Logic | Servises**
- Принимают данные из слоя Routes
- Делают бизнес-проверки (например наличие пользователя по ID)
- Поднимают HTTP исключения
- Общаются со слоями Crud, Clients, Modules
- Возвращают Pydantic объект в слой Routes

### **Core**
Ядро приложение с настройками.
```
    - config.py  # Все настройки и параметры приложения
    - main.py  # Главный модуль приложения FastApi object
    - middleware.py
    - scheduler.py  # CRON задачи приложения
    - urls.py # Подключение роутов приложения
```
### **DB**
Находятся конфигурационные параметры и настройки БД
### **Enums** и **Schemas**
Выделены отдельной папкой на практике показало более удобное использование и переиспользование их в других модулях.
### **Modules**
Папка предназначена для хранения отдельных модулей системы которыми могут выступать интеграции с другими системами как Zoom, Stripe и т.д.
Процесс интеграции с другими системами не всегда позволяет написать код в общем стиле из-за этого проще вынести в отдельную папку.
### **Clients**
Если у вас есть собственные сервисы с которыми происходит общение например по HTTP тогда в этой папке будет какой-нибудь базовый HTTP-класс от которого будут наследоваться другие клиенты и общаться с сервисами.
###  **Serializer**
Подгонка данных из табличных объектов в Pydantic объекты.