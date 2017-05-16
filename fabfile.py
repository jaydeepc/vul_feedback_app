import os
from fabric.api import task

@task()
def run_sql_injection_tests():
    os.system('pytest -m inject')