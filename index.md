This is a bot that you can tupe some text from a question and it find it in your data bases that you is create (sript and how it need look is further in documentacion)



in this repository have 2 sripts:
app.py
this a sript that  is convert docx documents in a json format that have structure that i need to a work in a bot 
format
```
{
    "question": "1.2 На реалізацію якої системи спрямоване Типове положення",
    "options": [
        {
            "text": "Безперервного навчання з питань О.П. посадових осіб та інших працівників",
            "is_correct": true
        },
        {
            "text": "Надання до медичної допомоги потерпілим від нещасних випадків",
            "is_correct": true
        },
        {
            "text": "Навчання правил поведінки у разі виникнення аварій",
            "is_correct": true
        },
        {
            "text": "Навчання правил поведінки у разі виникнення пожежі",
            "is_correct": false
        }
    ]
}
```
bot.py
this is main sript where you can run a bot 
also you need to change token of telegram in line 11
```
TOKEN = 'Your Token'
```
that it work you need to add file in format `data_().json`


To work in PythonAnyWhere you need to run this comand 
`pip3 install --user pyTelegramBotAPI`