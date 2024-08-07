from preprocessor import Preprocessor, File
from AWSHandler import AWSClientConfig, AWSClient
from download_data import DataDownloader, S3FileConfig
from utils import extract_utterances
from pydantic import BaseModel, Field, SecretStr
from dotenv import load_dotenv, find_dotenv
from typing import List, Any, Dict, Callable, Set
import os
import json

class Stage(BaseModel):
    name: str = Field(..., description="Name of the stage")

class Job(BaseModel):
    stage: str = Field(..., description="The stage of the job")
    method: str = Field(..., description="The method to be executed")
    params: Dict[str, Any] = Field(default_factory=dict, description="The parameters for the method")

class Pipeline(BaseModel):
    stages: List[Stage] = Field(..., description="The list of pipeline stages")
    variables: Dict[str, str] = Field(default_factory=dict, description="Environment variables")
    jobs: Dict[str, Job] = Field(..., description="The jobs to be executed in the pipeline")

class PipelineHandlerError(Exception):
    """Custom exception for pipeline handler errors."""
    pass

class PipelineHandler:

    def __init__(self, pipeline_config: Pipeline):

        self.config = pipeline_config

        self._apply_env_variables()
        self._set_credentials_create_client(region_name=os.getenv("AWS_REGION"), 
                                                 aws_access_key_id=os.getenv("AWS_ACCESS_KEY"), 
                                                 aws_secret_access_key=os.getenv("AWS_SECRET_KEY"))

        self.job_builtin_methods = {
            "download_from_s3": self._download_from_s3,
            "merge_files": self._merge_files,
            "process_file": self._process_file
        }
    
    def execute_pipeline(self):

        for stage in self.config.stages:

            for job_name, job_config in self.config.jobs.items():

                if job_config.stage == stage.name:
                    print(f"Executing Job: {job_name} in Stage: {stage.name}")
                    
                    # try:
                    self._execute_job(job_config.method, job_config.params)
                    # except Exception as e:
                    #     raise PipelineHandlerError(f"Error in job '{job_name}': {str(e)}") from e
        
        return "Success"

    def _execute_job(self, job_method: str, job_params: Dict[str, Any]):
        self.job_builtin_methods[job_method](**job_params)

    def _apply_env_variables(self):
        load_dotenv()
        for key, value in self.config.variables.items():
            os.environ[key] = value

    def _set_credentials_create_client(self, region_name: str, aws_access_key_id: str, aws_secret_access_key: str):
        self.client = AWSClient(config=AWSClientConfig(
                                    service_name='s3',
                                    region_name = region_name,
                                    aws_access_key_id = SecretStr(aws_access_key_id),
                                    aws_secret_access_key = SecretStr(aws_secret_access_key))).get_client()

    def _download_from_s3(self, s3_bucket: str, **s3_params):
        DataDownloader.download_data(aws_client=self.client, 
                                     s3_config=S3FileConfig(
                                                bucket_name = s3_bucket,
                                                prefix = s3_params.get('prefix', ''),
                                                output_dir = s3_params.get('output_dir',''),
                                                contain_str = s3_params.get('contain_str', ''),
                                                extension = s3_params.get('extension', '')
                                            ))

    def _get_existing_methods(self):
        all_attributes = dir(self)
        return [attr for attr in all_attributes if callable(getattr(self, attr)) and not attr.startswith("__")]
    
    def _merge_files(self, strategy: str, *merge_args, **merge_params):
        '''
        Merges files based on the passed method and other optional parameters set by consumer.
        '''
        Preprocessor.merge_files(strategy=strategy, *merge_args, **merge_params)

    def _process_file(self, method: str, file_path: str, *process_args, **process_params):
        filename, file_extension = os.path.splitext(file_path)
        Preprocessor.process_file(
            file=File(name=filename, path=file_path, extension=file_extension),
            fileProcessor=method,
            *process_args,
            **process_params
        )