from dataclasses import dataclass
import pandas as pd
from typing import Dict, List, Callable, Any

class InvalidColumnNames(Exception):
    """Exception that will be raised if the user does not have the proper 
    columns in the cases and controls.
    """
    def __init__(self, columns: List[str]) -> None:
        super().__init__(f"Found columns {', '.join(columns)} within the provided DataFrame. Expected the dataframe to contain the columns 'grid', 'sex', 'age'")

@dataclass
class Matcher:
    """
    Matcher class with two attributes: cases and controls. These 
    attributes are dataframes that have the ids for each case/control 
    and information to match to such as Sex, or Age
    """
    cases: pd.DataFrame
    controls: pd.DataFrame
    match_ratio: int

    @staticmethod
    def sex_age_match(cases: pd.DataFrame, controls: pd.DataFrame, ratio: int) -> Dict[str, List[str]]:
        """Staticmethod that will be the default matching method for the class. 
        Users can customize this by passing there own matching function to the 
        match method
        
        Parameters
        ----------
        cases : pd.DataFrame 
            dataframe that has a column called grids and then has information to 
            match on such as sex and age. These grids should all be cases and should 
            be have a status column that has the value 1.
        
        controls : pd.DataFrame 
            dataframe that has all of the information used in matching for the control 
            grids. The program expects a column a column called grids, sex, and age and 
            status. The status of all these grids should be 0.

        ratio : int
            ratio of how many controls to match with cases
            
        Returns
        -------
        Dict[str, List[str]]
            returns a dictionary where all the keys are a case and all the controls are in 
            a list.
        
        Raises
        ------
        InvalidColumnNames
            If the cases and controls dataframes do not have the columns 'grids', 'sex', 'age' 
            then it raises an exception
        """
        # Checking to make sure both classes have the appropriate columns. Otherwise raise an error
        Matcher._check_right_cols(cases)

        Matcher._check_right_cols(controls)

        data_subset = cases["grids", "sex", "age"]

        for row in data_subset.itertuples():
            print(row)

    def match(self, match_func: Callable[[pd.DataFrame, pd.DataFrame], Any] = sex_age_match) -> Any:
        """Method that will perform the actual matching
        
        Parameters
        ----------
        match_func : Callable[[pd.DataFrame, pd.DataFrame], Any]
            matching function that will be used to perform matching. The function 
            should take two dataframes as inputs. These will be passed as keyword 
            arguments: 'cases', 'controls'
        """
        match_func(cases=self.cases, controls=self.controls, ratio=self.match_ratio)

    @staticmethod
    def _check_right_cols(df: pd.DataFrame, expected_cols: List[str]) -> None:
        """Staticmethod that will check if the dataframe has the correct columns
        
        Parameters
        ----------
        df : pd.DataFrame 
            dataframe that will be checked to see if certain columns are present
        
        expected_cols : List[str]
            list of columns that we expect to be in the dataframe
        
        Raises
        ------
        InvalidColumnNames
            If the cases and controls dataframes do not have the columns 'grids', 'sex', 'age' 
            then it raises an exception
        """
        df_cols = df.columns

        if [col not in df_cols for col in expected_cols]:
            raise InvalidColumnNames(df_cols)

   

# with open("als_case_control.txt") as f:
#     next(f)
#     for line in f:
#         spline = line.rstrip().split("\t")
#         grid_id = spline[0]
#         if spline[3] == "1" and spline[1] == "1":
#             male_case[grid_id] = spline[1:3]
#         elif spline[3] == "1" and spline[1] == "0":
#             female_case[grid_id] = spline[1:3]
#         elif spline[3] == "0" and spline[1] == "1":
#             male_con_dic[grid_id] = spline[1:3]
#         elif spline[3] == "0" and spline[1] == "0":
#             female_con_dic[grid_id] = spline[1:3]



# def match(case_dic, con_dic, used, sex_status) -> dict:
#     pair_dic = {}
#     x = 0
#     for case in case_dic:
#         pair_dic[case] = []
#         for con in con_dic:
#             if(con not in used and len(pair_dic[case])<1):
#                 if(int(con_dic[con][0])==sex_status):

#                     age_diff = abs(float((con_dic[con])[1])-float((case_dic[case])[1]))

#                     if(age_diff<5):
#                         pair_dic[case].append(con)
#                         used.append(con)
#                         x+=1
#                         print(x)
#     return pair_dic
# # call first for males
# pairs_male_dict = match(male_case, male_con_dic, [], 1)

# #call for females
# pairs_female_dict = match(female_case, female_con_dic, [], 0)


# with open("als_matched_cases_and_controls_one_to_one_2_14_23.txt","w", encoding="utf-8") as output:
#     for case, control_list in pairs_male_dict.items():
#         for con in control_list:
#             output.write(f"{case}\t{con}\n")
#     for case, control_list in pairs_female_dict.items():
#         for con in control_list:
#             output.write(f"{case}\t{con}\n")

