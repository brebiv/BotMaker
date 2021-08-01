# BotMaker

## Web-interface preview

![Dashboard page](https://i.imgur.com/Aew69Bs.png)
![Builder page](https://i.imgur.com/ILDW7hQ.png)
![Add command modal](https://i.imgur.com/wFbs4zw.png)

## Installation guide

Clone repository

```bash
$ git clone https://github.com/brebiv/BotMaker
$ cd BotMaker
```

Create virtual environment

```bash
$ python3 -m venv venv
```

Activate virtual environment

```bash
$ source venv/bin/activate
```

Install python requirements

```bash
$ pip install -r requirements.txt
```

Migrate Django database

```bash
$ python manage.py migrate
```

Create Django superuser account

```bash
$ python manage.py createsuperuser
```

Run local Django development server and run BotRunner instance.

You should use two terminal windows or run them in the background.

```bash
$ python manage.py runserver
$ python manage.py runbotrunner
```

Go to http://localhost:8000/admin. Login with credntials you set in `createsuperuser` step.

Go to bots folder and click add bot. Input bot token and choose owner.

You can register new bot and obtain token from Telegram Bot `@BotFather`.

Now go to http://localhost:8000/ click Dashboard button there input PIN-code which is 10891089. Done. You have installed BotRunner localy. Congrats. Now try to figure out how to use it on your own. It does not refresh commands automatically, so you have to click stop and then start button to make bot respond to commands you've made.
