from pipeline_handler import PipelineHandler, Pipeline, Stage, Job
from utils import load_config
from typing import List, Dict

def load_stages(stages: List) -> List[Stage]:

    stage_list = list()

    for stage in stages:
        stage_list.append(Stage(name=stage))

    return stage_list

def load_job(job: Dict[str, str]) -> Job:

    job_stage = job['stage']
    job_method = job['method']
    job_method_params = job['params']

    return Job(stage=job_stage, method=job_method, params=job_method_params)


def load_pipeline(config_path: str) -> Pipeline:

    pipeline_config = load_config(config_path)

    stages = load_stages(pipeline_config['stages'])
    variables = pipeline_config['variables']

    jobs = dict()
    for key in pipeline_config.keys():
        if "job" in key:
            job = load_job(pipeline_config[key])
            jobs[key.split(':')[-1]] = job

    return Pipeline(stages=stages, variables=variables, jobs=jobs)



def execute_pipeline(config_path: str) -> str:

    pipeline_config = load_pipeline(config_path)

    pipeline_handler = PipelineHandler(pipeline_config=pipeline_config)
    
    status = pipeline_handler.execute_pipeline()

    return status
