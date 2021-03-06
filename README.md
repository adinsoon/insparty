# insparty
Inspire / In Party

Inspire others by your ideas

Find teams that you want to contribute to

# Running locally
Clone the repo to your machine:
```console
$ git clone git@github.com:adinsoon/insparty.git
```
Then setup .env.template file and re-name it to .env
```env
#example
DEBUG=1

SERVER_IP=domain.tld
DEV_IP=X.X.X.X
DJANGO_PORT=xxxx

POSTGRES_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=!!pleasechangeme!!
POSTGRES_SERVICE=postgres
POSTGRES_PORT=5432
DATABASE=postgres

SECRET_KEY=!!pleasechangeme!!
```
In the main directory, open your terminal and run
```console
$ docker-compose up --build
```
After building the project and passing tests, you should be ready to open the server in your browser:
```console
ins_back    | Ran XXX tests in XX.XXXs
ins_back    | 
ins_back    | OK
ins_back    | --------------------------
ins_back    | Fixing ownership of files
ins_back    | --------------------------
ins_back    | --------------------------
ins_back    | Run command
ins_back    | runserver X.X.X.X:xxxx
ins_back    | --------------------------
ins_back    | Watching for file changes with StatReloader
ins_back    | Performing system checks...
ins_back    | 
ins_back    | System check identified no issues (0 silenced).
ins_back    | MM - DD, YYYY - HH:mm:ss
ins_back    | Django version 3.x.x, using settings 'config.settings'
ins_back    | Starting development server at http://X.X.X.X:xxxx/
ins_back    | Quit the server with CONTROL-C.
```
