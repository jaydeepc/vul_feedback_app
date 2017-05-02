import os
from fabric.api import task

@task()
def run_tests():
    os.system('pytest')