import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import preprocessing, decomposition

def plot_bar(df,column_lst):
    """
    Plot bar charts of desired columns

    Parameters
    ----------
    df: pandas.DataFrame
    column_lst: list of strings (column names to plot)

    Returns
    -------
    None
    """
    plt.figure(figsize=(20,11))
    for i,col in enumerate(column_lst):
        col_df=pd.DataFrame(df[col].value_counts()).reset_index()
        plt.subplot(2, 3, i+1)
        sns.barplot(x=col_df['index'], y=col_df[col])
        plt.xlabel(col,fontsize=15)
        plt.ylabel("Count")


def plot_hists(df, column_lst):
    """
    Plot bar charts of desired columns

    Parameters
    ----------
    df: pandas.DataFrame
    column_lst: list of strings (column names to plot)

    Returns
    -------
    None
    """

    for col in column_lst:
        plt.figure(figsize=(5,5))
        plt.subplot(1,1,1)
        sns.distplot(df[col])
        plt.xticks([])
        plt.yticks([])
        name="images/"+col+".png"
        plt.savefig(name)

def impute_med(df, column_lst):
    """
    Impute Median in columns with NaN values

    Parameters
    ----------
    df: pandas.DataFrame with missing values
    column_lst: list of strings (column names with missing values)

    Returns
    -------
    pandas.DataFrame
        With missing values imputed with the median of the column
    """

    for col in column_lst:
        df[col].fillna((df[col].median()), inplace=True)
    return(df)

def scree_plot_ev(princ_comp_an):
    vals = princ_comp_an.explained_variance_ratio_
    fig = plt.figure(figsize=(10, 6), dpi=250)
    cum_var = np.cumsum(vals)
    ax = fig.add_subplot(111)

    ax.plot(range(len(vals) + 1), np.insert(cum_var, 0, 0), color = 'r', marker = 'o')
    ax.bar(range(len(vals)), vals, alpha = 0.8)

    ax.axhline(0.9, color = 'g', linestyle = "--")
    ax.set_xlabel("Principal Component", fontsize=12)
    ax.set_ylabel("Variance Explained (%)", fontsize=12)

    plt.title("Scree Plot", fontsize=16)

if __name__=="__main__":
    #Read and clean data
    df= pd.read_csv("BGC_data.csv")
    df["Race/Ethnicity"].fillna("AI",inplace=True)
    impute_med(df,["2","3 (out of 4)","7","22","23","25","26"])
    surv_quest=df.drop(['ID', 'Group', 'Age', "Grade in fall '18", 'Gender', 'Race/Ethnicity'],axis=1)
    #Plots for EDA
    quest_to_plot=['1', '2', '3 (out of 4)', '4 (out of 4)', '5', '6', '7', '8', '9', '10',
       '11', '12', '13', '14', '15', 'SCHOOL16', '17', '18', '19', '20', '21',
       '22', '23', '24', '25', '26', '27', '28', '29', '30']
    print("apples")
    plot_hists(surv_quest,quest_to_plot)
    print("bananas")
    demo_to_plot=['Gender','Race/Ethnicity','Group','Age',"Grade in fall '18"]
    plot_bar(df,demo_to_plot)
    plt.savefig("images/demo_bar.png")
    #PCA
    X=surv_quest.drop(['28', '29', '30'],axis=1)
    y=surv_quest[['28', '29', '30']].sum(axis=1)
    ss = preprocessing.StandardScaler()
    X_centered = ss.fit_transform(X)
    pca = decomposition.PCA(n_components=25)
    X_pca = pca.fit_transform(X_centered)
    scree_plot_ev(pca)
    plt.savefig("images/sn1.png")
