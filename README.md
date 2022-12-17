# HuntyTest

Desarrollo de prueba técnica.


## Requisitos del sistema

+ [Git](https://git-scm.com/)
+ [Docker](https://www.docker.com/)
+ [Docker Compose](https://docs.docker.com/compose/)


## Configurar ambiente local
### Primero, clonar repositorio

```
git clone git@github.com:RobertArzolaC/HuntyTest.git
```


### Pasos para configurar un entorno de desarrollo dockerizado

En mi opinión, esta es la forma más fácil de poner el proyecto en marcha.


#### 1. Construir imagen

```
docker-compose build
```

#### 2. Correr contenedores

```
docker-compose up -d
```

#### 3. Aplicar migraciones

```
docker-compose exec web aerich upgrade
```

Visitar [http://localhost:8004/docs](http://localhost:8004/docs). Deberías ver la documentación de la api ;)


### Otros comandos

#### Ejecutar los tests

```
docker-compose exec web python -m pytest
```

#### Ejecutar los tests y evaluar el coverage

```
docker-compose exec web python -m pytest --cov="."
```


## Lenguaje usado
+ [Python](https://www.python.org/)


## Herramientas usadas
+ [FastAPI](https://fastapi.tiangolo.com/)
+ [Asyncpg](https://github.com/MagicStack/asyncpg)
+ [PostgreSQL](http://www.postgresql.org/)
+ [Tortoise ORM](https://tortoise-orm.readthedocs.io/en/latest/)
+ [Aerich](https://github.com/tortoise/aerich)
+ [Docker](https://www.docker.com/)
+ [pre-commit](https://pre-commit.com/)
+ [Gunicorn](https://gunicorn.org/)


## Diagrama entidad relación
![Estructura de las tablas](https://raw.githubusercontent.com/RobertArzolaC/HuntyTest/master/assets/DEF.png)


## Recursos
+ [Integración del ORM de Python tortoise con FastAPI](https://coffeebytes.dev/integracion-del-orm-de-python-tortoise-con-fastapi/)
+ [Tortoise Documentation](https://tortoise.github.io/examples/fastapi.html)
+ [Python Tortoise ORM Integration with FastAPI](https://medium.com/nerd-for-tech/python-tortoise-orm-integration-with-fastapi-c3751d248ce1)
+ [Tortoise ORM migrations with aerich](https://ashfakmeethal.medium.com/tortoise-orm-migrations-with-aerich-5ebb7238bed5)


## Author

* **Robert Arzola Castillo** - *Initial work*


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
