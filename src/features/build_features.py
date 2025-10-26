import sys
import os
from src.logger import logging
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder,FunctionTransformer
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import StratifiedShuffleSplit
from src.exception import CustomException
from dataclasses import dataclass
from src import save_object

@dataclass
class DataTransformationConfig:
    preprocessor:str = os.path.join('../../models', 'preprocessor.pkl')
    
class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()
    
    def get_data_transformer_object(self):
        try:
            
            # 1. Load your dataset
           # NEW (Correct path: go up one level, then into 'data')
            df = pd.read_csv('../../data/interim/train.csv')

            TARGET_COLUMN = 'SalePrice' 

            X = df.drop(columns=[TARGET_COLUMN])
            
            # Identify Numerical and Categorical Columns
            numerical_features = ['Overall Qual', 'Gr Liv Area', 'Garage Cars', 'Garage Area', '1st Flr SF', 'Total Bsmt SF', 'Lot Area', 'BsmtFin SF 1', 'Full Bath', 'year_since_remod']
            # log_columns = ['Gr Liv Area', '1st Flr SF','BsmtFin SF 1']
            # normal_numerical_features = list(set(numerical_features) - set(log_columns))

            # 2. Create Preprocessing Pipelines for Robustness
            # handle missing values and encode categorical data BEFORE feature selection.
            
            
            # log_pipeline = Pipeline(steps=[
            #     ('imputer', SimpleImputer(strategy='mean')),
            #     ('log_transform', FunctionTransformer(np.log1p, validate=False)), # <--- THIS IS IT
            #     ('scaler', StandardScaler())
            # ])
# Pipeline for Numerical Features: Impute (fill NaN) then Scale
            numerical_pipeline = Pipeline([
                ('imputer', SimpleImputer(strategy='median')),
                ('scaler', StandardScaler())
            ])

            # Create a Column Transformer to apply pipelines to the correct columns
            preprocessor = ColumnTransformer(
                transformers=[
                    # ('log', log_pipeline, log_columns),
                    ('num', numerical_pipeline,numerical_features)
                ],
                remainder='drop'  # This drops any columns not specified in the transformers
            )
            
            return preprocessor

        except Exception as e:
            raise CustomException(e,sys)
        
        
    def basic_data_transformation(self,df):
        try:
            
            logging.info("basic data transformation begin")
            # here the necessary adjustment is done to get the better results
            
            df['year_since_remod'] = df['Yr Sold'] - df['Year Remod/Add']
            df['Log_SalePrice'] = np.log1p(df['SalePrice'])
                        
            df1 = df[['Overall Qual', 'Gr Liv Area', 'Garage Cars', 'Garage Area', '1st Flr SF', 'Total Bsmt SF', 'Lot Area', 'BsmtFin SF 1', 'Full Bath', 'year_since_remod','SalePrice','Log_SalePrice']].copy()
           
               
            # Splitting data through Stratified Shuffle Split using sale_pric_cat as target
            
          
            df1['Sale_price_cat'] = pd.cut(df1['Log_SalePrice'],bins = [9.4550,11.7280,11.8590,12.0910,12.3460, np.inf],labels = [1,2,3,4,5])
            split = StratifiedShuffleSplit(n_splits = 1, test_size=0.2, random_state=42)
            for train_index, test_index in split.split(df1,df1['Sale_price_cat']):
                train_data = df1.loc[test_index].drop(columns = ['Sale_price_cat', 'Log_SalePrice'])
                test_data = df1.loc[train_index].drop(columns = ['Sale_price_cat', 'Log_SalePrice'])
                
                
                
            logging.info("basic data transformation done successfully")
                
            return train_data, test_data, df1
        
        except Exception as e:
            raise CustomException(e,sys)

    def initiate_data_transform(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
                
            logging.info("read train and test data is completed")
                
            logging.info("obtaining preprocessing object")
                
            preprocessing_obj = self.get_data_transformer_object()
            
            target_column_name = "SalePrice"
            
            input_feature_train_df = train_df.drop(columns = [target_column_name], axis = 1)
            target_feature_train_df = train_df[target_column_name]
            
            input_feature_test_df = test_df.drop(columns = [target_column_name], axis = 1)
            target_feature_test_df = test_df[target_column_name]
            
            logging.info(f"Applying preprocessing object on training dataframe and testing data frame")
            
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)
            
            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[
                input_feature_test_arr, np.array(target_feature_test_df)
            ]
            logging.info(f"Saved preprocessing object.")
            save_object(file_path = self.data_transformation_config.preprocessor,obj = preprocessing_obj)
            
            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor
            )
        except Exception as e:
            raise CustomException(e,sys)