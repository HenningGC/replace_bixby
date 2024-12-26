import sys

if 'src/' not in sys.path:
    sys.path.append('src/')

from src.execute_pipeline import execute_pipeline

if __name__ == "__main__":
    print(execute_pipeline(config_path='config/pipeline_config.yml'))