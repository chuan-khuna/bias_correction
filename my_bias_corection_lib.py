import numpy as np
from sklearn.linear_model import LinearRegression

class BiasCorrection:
    def __init__(self, observed_data, model_data):
        """
            create Bias coorection model

            observed_data: observation data array
            model_data: model data array
        """
        self.obsrv = np.array(observed_data)
        self.model = np.array(model_data)
        self.mean_model = np.mean(self.model)
        self.mean_obsrv = np.mean(self.obsrv)
    
    def constant_diff(self):
        """
            calculate constant for subtract from model data
            
            bias coorection technique:
                model_corrected = model - c

            where c = mean(model) - mean(observed)

            return constant c
        """
        c = self.mean_model - self.mean_obsrv
        return c

    def coef_ratio(self):
        """
            calculate cooeficient for multiply model data

            bias correction technique:
                model_corrected = model * k

            where k = 1/(mean(model)/mean(observed))

            return coeficient k
        """
        k = 1/(self.mean_model/self.mean_obsrv)
        return k

    def linear_regression(self):
        """
            calculate coefficient and intercept to adjust model

            bias correction technique:
                model_corrected = a*model + b
                # calculate from sklearn
            
            return coefficient a,  intercept b
        """
        lr = LinearRegression()
        lr.fit(self.model.reshape(-1, 1), self.obsrv)

        return round(lr.coef_[0], 3), round(lr.intercept_, 3)