# Visual and Language based Navigation Demo

## Description
<!-- Mention the live-server address here -->
- **Live Server**: [https://vln-webapp-backend.onrender.com]
- **Tech Stack**: Django-framework, PostgreSQL, HTML, Tailwind CSS, etc.
- **Python Version**: 3.12.1
- **Django Version**: 5.0.2
- **PostgreSQL Version**: 16

## Environment Setup
- **ALLOWED_HOSTS**: [vln-webapp-backend.onrender.com localhost]
- **DATABASE_URL**: postgres://user:password@netloc/dbname
- **DEBUG**: Set the debug mode to True for development and False for production
- **SECRET_KEY**: Set the secret key for the Django application


## Instructions
- **Start the server on localhost at port:8000 (http://127.0.0.1:8000)**
```bash
make run
```
- **Make migrations for any changes in the models**
```bash
make mig
```

- **Create superuser for admin access**
```bash
make super
```

- **Push the changes to the repository**
```bash
make push m="Commit Message"
```

<!-- 

# DBMS-LAB
## Contributors
- Grace Sharma
- Umang Singla
- Vineet Amol Pippal
- Mradul Agrawal
- Subhajyoti Halder
## Instruction
- **Create virtual environment**
```bash
sudo pip install virtualenv      # This may already be installed
virtualenv .env                  # Create a virtual environment
```
- **Run** start.sh **bash To Start Web Application**
```bash
./start.sh                       # All neccessary library will be downloaded
```
- **Open http://127.0.0.1:8000 in  your browser**
 
-->