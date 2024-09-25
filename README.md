# E-commerce product scrapping
## Steps
1. Open project.
2. Open Terminal in same directory
3. [Optional] To support caching, follow guide and install redis-stack 
   ```
   https://redis.io/docs/latest/operate/oss_and_stack/install/install-stack/linux/
   ```
4. RUN 
    ```sh
    python3 -m venv venv
    source env/bin/activate
    pip install -r requirements.txt
    ```
5. To start the webserver, run
   ```sh
   fastapi dev main.py
   ```
6. Server is now live at
    ```
   http://127.0.0.1:8000/
   ```
7. For API docs, please visit:
   ```
   http://127.0.0.1:8000/docs
   ```
