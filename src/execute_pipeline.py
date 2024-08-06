from pipeline_handler import PipelineHandler, Pipeline, Stage
from utils import load_config_update_credentials
from typing import List

def load_stages(stage_list) -> List[Stage]:

    stages = list()

    for stage in stage_list:
        stages.append(Stage(name=stage['stage'], method=stage.get('method',''), params=stage.get('params','')))

    return stages


def execute_pipeline(config_path: str) -> str:

    stages = load_stages(load_config_update_credentials(config_path))

    pipeline_config = Pipeline(pipeline=stages)
    pipeline_handler = PipelineHandler(pipeline_config=pipeline_config)
    
    status = pipeline_handler.execute_pipeline()

    return status
