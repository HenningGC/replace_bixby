from preprocessor import Preprocessor, File
from AWSHandler import AWSClientConfig, AWSClient
from download_data import DataDownloader, S3FileConfig
from utils import extract_utterances
from pydantic import BaseModel, Field, SecretStr
from dotenv import load_dotenv, find_dotenv
from typing import List, Any, Dict, Callable
import os
import json

class Stage(BaseModel):
    name: str = Field(..., description="The name of the pipeline stage")
    method: str = Field(..., description="The method of to be executed")
    params: Dict[str, Any] = Field(default_factory=dict, description="The parameters for the method")

class Pipeline(BaseModel):
    pipeline: List[Stage] = Field(..., description="The list of pipeline stages")

class PipelineHandlerError(Exception):
    """Custom exception for pipeline handler errors."""
    pass

class PipelineHandler:

    def __init__(self, pipeline_config: Pipeline):

        self.config = pipeline_config
        self.stage_methods = {
            "set_credentials": self._set_credentials,
            "download_files": self._download_files,
            "merge_files": self._merge_files,
        }
        # for stage in pipeline_config.pipeline:
        #     self._create_dynamic_method(stage.method, )
    
    def execute_pipeline(self):
        for stage in self.config.pipeline:
            print(stage)
            stage_name = stage.name
            stage_method_name = stage.method
            stage_params = stage.params

            try:
                self._execute_stage(stage_name, stage_method_name, stage_params)
            except Exception as e:
                print(e)
                return "Failure"

        return "Success"

    def _execute_stage(self, stage_name: str, stage_method_name: str, stage_params: Dict[str, Any]):
        try:
            method = self.stage_methods.get(stage_method_name,'')
            if method:
                self.stage_methods[method](**stage_params)
                print(stage_name,method)
            else:
                self.stage_methods[stage_name](**stage_params)
                print(stage_name)
                
        except Exception as e:
            raise PipelineHandlerError(f"Error in stage '{stage_name}': {str(e)}") from e

    def _set_credentials(self, region_name: str, aws_access_key_id: 'str', aws_secret_access_key: 'str'):
        self.client = AWSClient(config=AWSClientConfig(
                                    service_name='s3',
                                    region_name = region_name,
                                    aws_access_key_id = SecretStr(aws_access_key_id),
                                    aws_secret_access_key = SecretStr(aws_secret_access_key))).get_client()

    def _download_files(self, s3_bucket: str, **s3_params):
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
        
    # def _create_dynamic_method(self, method_name: str, method: Callable):

    #     setattr(self, method_name, method)

    def _merge_files(self, method: str, *merge_args, **merge_params):
        '''
        Merges files based on the passed method and other optional parameters set by consumer.
        '''
        Preprocessor.merge_files(method=method, *merge_args, **merge_params)

    def _process_file(self, method: str, file_path: str, *process_args, **process_params):
        filename, file_extension = os.path.splitext(file_path)
        Preprocessor.process_file(
            file=File(name=filename, path=file_path, extension=file_extension),
            fileProcessor=method,
            *process_args,
            **process_params
        )