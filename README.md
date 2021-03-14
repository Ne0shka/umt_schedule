# Бот для группы ВК ОГБПОУ УМТ

---

### Функционал бота:
* Получение расписания с сайта техникума и отправка в личные сообщения

---

#### Протестировать: [Ссылка на группу ВК](https://vk.com/umt_raspisanie)

#### Запуск: `python -m src`

---

## Инструкция по установке

##### Для Windows

* Установите программу `poppler` ([рекомендуется версия от @oschwartz10612](https://github.com/oschwartz10612/poppler-windows/releases/)) и добавьте её в [PATH](https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/)
* Установите зависимости в Python: `pip install -r requirements.txt`

##### Для Linux

* Большинство дистрибутивов поставляются с `pdftoppm` и `pdftocairo`. Если и то, и другое отсутствует - установите `poppler-utils` с помощью пакетного менеджера вашей ОС
* Установите зависимости в Python: `pip install -r requirements.txt`

---

#### PR, код-ревью и любая критика приветствуются.
