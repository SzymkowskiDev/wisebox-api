
# WiseBox API
This repo contains a ready-to-deploy code of the API that serves the needs of the [WiseBox frontend app](https://github.com/SzymkowskiDev/wisebox-app).

In other words, this is the place for Python backend.

## ⚙ Dependencies
Dependencies are listed in the `requirements.txt` file. To install project dependencies open Python interpreter of your choice e.g. Anaconda Prompt, then navigate to the project's directory and run `pip install -r requirements.txt`.

## 🚀 How to run
### How to access the API on the web?

Navigate [https://d4ttvo.deta.dev/docs](https://d4ttvo.deta.dev/docs) to access the REST API deployed to a server.

### How to run the API locally?

> Before proceeding install required packages as explaned in section ⚙ Dependencies.

Then...

Open a Python interpreter e.g. Anaconda prompt and navigate to the project's directory.

In the console run the command `uvicorn main:app`.

The API will open in the browser at http://127.0.0.1:8000/docs

### How to deploy the API to deta.sh?

1. [Create an account at deta](https://web.deta.sh/home/szymkowskidev/default/overview)

2. [Install the Deta Command Line Tool](https://docs.deta.sh/docs/cli/install/)

3. Open command prompt and navigate to the project's directory. Then run the command `deta login`.

4. Then run the command `deta deploy`.

## 🔗 Related Projects
* The top level repo [WiseBox](https://github.com/SzymkowskiDev/WiseBox)
* The kanban board [WiseBox Project](https://github.com/users/SzymkowskiDev/projects/7/views/1)
* Frontend app [wisebox-api](https://github.com/SzymkowskiDev/wisebox-app)
* API can be accessed online [here](https://d4ttvo.deta.dev/docs)

## 🎓 Learning materials
* Web framework for building API: [FastAPI](https://fastapi.tiangolo.com/)
* Relational database [SQLite](https://www.sqlite.org/index.html)
* Object Relational Mapper [SQLAlchemy](https://docs.sqlalchemy.org/en/14/tutorial/index.html#unified-tutorial)
* Free API hosting's deployment CLI [Deta CLI](https://docs.deta.sh/docs/cli/commands)

## 📝 How to use the REST API?
**Example 1. Title**

Description of the example.
```javascript
CODE GOES HERE
```
**Example 2. Title**

Description of the example.
```javascript
CODE GOES HERE
```

## 📄 License
[MIT License](https://choosealicense.com/licenses/mit/) ©️ 2019-2020 [Kamil Szymkowski](https://github.com/SzymkowskiDev "Get in touch!")

[![](https://img.shields.io/badge/license-MIT-green?style=plastic)](https://choosealicense.com/licenses/mit/)





