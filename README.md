# Второе ревью

* [Телеграм-бот](#Телеграм-бот)  
    * [Изменение информации о долгах](#Изменение-информации-о-долгах)  
    * [Выгрузка информации о долгах](#Выгрузка-информации-о-долгах)  
* [Поиск информации в интернете](#Поиск-информации-в-интернете)  

## Телеграм-бот
Бот запоминает кто, за что, кому, сколько должен
Используется база данных со стандартными полями "имя", "сумма", "обстоятельства" и т.д. (возможны изменения в названиях и/или добавление полей).

### Изменение информации о долгах
Пользователь вводит ключевые слова, описанные в приветственном гайде, в зависимости от необходимой инфомации. Например, взял в долг/дал в долг+сколько+у кого/кому+где и т. д. Возможно, когда-нибудь бот будет парсить и нестандартные предложения, т.е. не будет шаблонных фраз для внесения изменений.  
После внесения информации о чьем-то долге, бот сразу выводит сообщение "Теперь такой-то должен столько-то".  
Также, будет возможна отмена последнего внесенного изменения (например, "отменить последнний долг").  

### Выгрузка информации о долгах
Аналогично предыдущему пункту бот по ключевым словам, которые ввёл пользователь, выгружает запрашиваемую информацию в диалоговое окно или в файл на выбор.

## Поиск информации в интернете




