import sys
import pandas as pd
import numpy as np
from src.exception import CustomException
from src import load_object
from src.logger import logging


class PredictPipeline:
    def __init__(self):
        pass

    def predict(self,features):
        # logging.info('user data is going for transformation')
        try:
            model_path='models/model.pkl'
            preprocessor_path='models/preprocessor.pkl'
            model=load_object(file_path=model_path)
            preprocessor=load_object(file_path=preprocessor_path)
            
            # The preprocessor handles all transformation (log, scaling, imputation)
            data_scaled=preprocessor.transform(features) 
            
            preds= (model.predict(data_scaled),2)
            logging.info("data is predicted")
            return preds
        
        except Exception as e:
            # Added a detailed print here to help diagnose the exact cause of the error
            print(f"Prediction Error in PredictPipeline: {e}") 
            raise CustomException(e,sys)


class CustomData:
    def __init__(self,
        Overall_Qual: int,
        Gr_Liv_Area: int,
        Garage_Cars: float,
        Garage_Area: float,
        First_Flr_SF: int,
        Total_Bsmt_SF: float,
        Lot_Area: int,
        BsmtFin_SF_1: float,
        Full_Bath: int,
        year_since_remod: int):

        # Initializing instance attributes with the RAW, UNTRANSFORMED values.
        # CRITICAL FIX: Removed np.log1p() calls here. The preprocessor handles logging.
        self.Overall_Qual = Overall_Qual
        self.Gr_Liv_Area = Gr_Liv_Area         
        self.Garage_Cars = Garage_Cars
        self.Garage_Area = Garage_Area
        self.First_Flr_SF = First_Flr_SF       
        self.Total_Bsmt_SF = Total_Bsmt_SF
        self.Lot_Area = Lot_Area
        self.BsmtFin_SF_1 = BsmtFin_SF_1       
        self.Full_Bath = Full_Bath
        self.year_since_remod = year_since_remod

    def get_data_as_data_frame(self):
        try:
            # Keys MUST match the 10 feature names expected by your reduced preprocessor/model
            custom_data_input_dict = {
                "Overall Qual": [self.Overall_Qual],
                "Gr Liv Area": [self.Gr_Liv_Area],
                "Garage Cars": [self.Garage_Cars],
                "Garage Area": [self.Garage_Area],
                "1st Flr SF": [self.First_Flr_SF], 
                "Total Bsmt SF": [self.Total_Bsmt_SF],
                "Lot Area": [self.Lot_Area],
                "BsmtFin SF 1": [self.BsmtFin_SF_1], 
                "Full Bath": [self.Full_Bath],
                "year_since_remod": [self.year_since_remod]
            }
            
            logging.info("the data frame is created")

            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys)
