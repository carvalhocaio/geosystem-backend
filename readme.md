# GeoSystem

## Requisitos
- Python 3.8.5
- Oracle 19.8

## Configuração do client do Oracle
1 - Fazer download do client do Oracle, **versão 19.8**
> Realizar download do versão basic, sqlplus e devel. Devem ser da extensão `.rpm`    

Download => [Oracle Client](https://www.oracle.com/database/technologies/instant-client/linux-x86-64-downloads.html)  

2 - Realizar a instalação dos arquivos
```
sudo alien -i oracle-instantclient19.8-basic-12.1.0.2.0-1.x86_64.rpm
sudo alien -i oracle-instantclient19.8-sqlplus-12.1.0.2.0-1.x86_64.rpm
sudo alien -i oracle-instantclient19.8-devel-12.1.0.2.0-1.x86_64.rpm
```

3 - Instalar as dependências do Oracle
```
sudo apt install libaio1
```

4 - Adicionar as variáveis ao path
```
sudo vim ~/.bashrc
```

> No caso do **zsh** utilizar: `sudo vim  ~/.zshrc`

4.1 - Adicionar conteúdo ao final do arquivo
```
export PATH=$PATH:$ORACLE_HOME/bin
export ORACLE_HOME=/usr/lib/oracle/19.8/client64
export LD_LIBRARY_PATH=/usr/lib/oracle/19.8/client64/lib/${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}
```

5 - Configurar o TNS  
5.1 - Extrair o arquivo do wallet no diretório: `/usr/lib/oracle/19.8/client64/lib/network/admin`
  
5.2 - Editar o arquivo sqlnet.ora
```
sudo vim sqlnet.ora
```
  
5.2.1 - Alterar o conteúdo para:
```
WALLET_LOCATION = (SOURCE = (METHOD = file) (METHOD_DATA = (DIRECTORY="/usr/lib/oracle/19.8/client64/lib/network/admin")))
SSL_SERVER_DN_MATCH=yes
``` 


## Execução do projeto

1 - Clonar o projeto:
```
https://gitlab.com/sch_dev/geosystem/geosystem-backend.git
```

2 - Baixar o pipenv
```
pip install pipenv
```

3 - Criar o ambiente de desenvolvimento
```
pipenv shell
```

4 - Baixar as dependências do projeto
```
pipenv sync
```

5 - Criar o arquivo .env e definir as configurações do banco de dados e do projeto
```
DEBUG=
TEMPLATE_DEBUG=
SECRET_KEY=
ALLOWED_HOSTS=

DATABASE_NAME=

DATABASE_AGRICOLA=
DATABASE_PASSWORD_AGRICOLA=
``` 

6 - Realizar as migrações com o banco de dados
``` 
python manage.py makemigrations
```

```
python manage.py migrate --run-syncdb
```

7 - Executar o projeto
```
python manage.py runserver
```

---

*Equipe de Desenvolvimento - Scheffer*