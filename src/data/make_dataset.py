# -*- coding: utf-8 -*-
import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
import numpy as np
from dataclasses import dataclass
from src.features.build_features import DataTransformationConfig
from src.features.build_features import DataTransformation
from src.models.train_model import modelTrainer


@dataclass
class DataIngestionConfig:
    train_data_path:str = os.path.join('../../data/interim', 'train.csv')
    test_data_path:str = os.path.join('../../data/interim', 'test.csv')
    raw_data_path:str = os.path.join('../../data/raw','raw_data.csv')
    log_data_path:str = os.path.join('../../data/interim','Log_Transformed_Features.csv')
    
class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

            
    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")

        try:
            # --- 1. Data Ingestion (Read and Save Raw Data) ---
            df = pd.read_csv('../../data/raw/AmesHousing.csv')
            logging.info('Read the dataset as data frame')

            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            # --- 2. Data Transformation (Split and Log-Transform Data) ---
            Data_Transformation = DataTransformation()
            
            # This calls the transformation logic and gets the split DataFrames
            train_data, test_data, log_transormed_df = Data_Transformation.basic_data_transformation(df)

            # --- 3. Save Split Data ---
            # Ensure the directory for train/test data exists
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)

            test_data.to_csv(self.ingestion_config.test_data_path, index=False, header=True)
            train_data.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            log_transormed_df.to_csv(self.ingestion_config.log_data_path, index=False, header=True)

            logging.info('Ingestion and initial transformation (split) of the data is completed')

            # --- 4. Return Paths (The Fix for the previous error) ---
            # This returns the paths to the saved train and test data, 
            # which will be unpacked by the calling function.
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
            
        except Exception as e:
            raise CustomException(e,sys)
            

if __name__ == "__main__":
    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion()
    
    data_transformation = DataTransformation()
    train_arr, test_arr,_= data_transformation.initiate_data_transform(train_data, test_data)
    
    modeltrainer = modelTrainer()
    # print(train_arr)
    print(modeltrainer.initiate_model_trainer(train_array = train_arr,test_array = test_arr))