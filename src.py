import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import decomposition
from sklearn.model_selection import train_test_split,KFold
from numpy.linalg import svd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

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

def same_scale(df,column_lst):
    """
    Get all questions on same scale (a few columns are out of 4)

    Parameters
    ----------
    df: pandas.DataFrame with columns to transform
    column_lst: list of strings (column to be transformed).

    Returns
    -------
    pandas.DataFrame
        with new, transformed columns and old columns dropped
    """
    for col in column_lst:
        name=col+"_ss"
        df[name]=df[col]*(5/4)
        df.drop([col],inplace=True,axis=1)

def get_matrix_svd(features,num_topics):
    """
    Performs PCA via singular value decomposition.

    Parameters
    ----------
    features: pandas.DataFrame of features
    num_topics: number of topics to return

    Returns
    -------
    U: pandas.DataFrame (shape= # participants by num_topics)... relates the participants to the topics.
    sigma: numpy.array (len=num_topics)... gives the singular value of each topic (how much variance is explained by each topic).
    VT: pandas.DataFrame (shape= num_topics by # questions)... relates topics to the questions.
    """

    mat = pd.DataFrame(features)
    questions = mat.columns
    participants = mat.index
    # Compute SVD
    U, sigma, VT = svd(mat)

    k = num_topics
    topics = [f'latent_topic_{i}' for i in range(k)]

    # Keep top k concepts for comparison
    U = U[:,:k]
    sigma = sigma[:k]
    VT = VT[:k,:]

    # Make pretty
    U, sigma, VT = (np.around(x,2) for x in (U,sigma,VT))
    U = pd.DataFrame(U, index = participants, columns = topics)
    VT = pd.DataFrame(VT, index = topics, columns = questions)

    print('\nMatrix U: participants-topic')
    print(U)
    print('\nMatrix S: singular values')
    print(sigma)
    print('\nMatrix V: topic-questions')
    print(VT)
    return(U,sigma,VT)

def get_matrix_nmf(features, num_topics):
    """
    Performs non-negative matrix factorization.

    Parameters
    ----------
    features: pandas.DataFrame of features.
    num_topics: number of topics to return.

    Returns
    -------
    W: pandas.DataFrame (shape= # participants by num_topics)... relates the participants to the topics.
    H: pandas.DataFrame (shape= num_topics by # questions)... relates the topics to the questions.
    """

    mat = pd.DataFrame(features)
    nmf = decomposition.NMF(n_components = num_topics)
    nmf.fit(mat)

    W = nmf.transform(mat)
    H = nmf.components_

    W = pd.DataFrame(W)
    H = pd.DataFrame(H)

    W,H = (np.around(x,2) for x in (W, H))

    # this shows the components
    print(W.head(30), '\n\n', H.head(num_topics))
    return(W,H)

def fit_nmf(features,num_topics):
    nmf = decomposition.NMF(n_components=num_topics)
    nmf.fit(features)
    W = nmf.transform(features)
    H = nmf.components_
    return nmf.reconstruction_err_

def plt_recon_error(features,num_topics):
    error = [fit_nmf(features,i) for i in range(1,num_topics+1)]
    plt.plot(range(1,num_topics+1), error)
    plt.xlabel('Number of Topics (k)')
    plt.ylabel('Reconstruction Error')
    plt.title("Reconstruction Error by k")

def train_mod_kfold_accuracy(mod,Xs,y):

    k_fold=KFold(n_splits=3)

    accuracies1 = []
    for train_index, test_index in k_fold.split(Xs):

        mod.fit(Xs[train_index], y[train_index])
        y_predict = mod.predict(Xs[test_index])
        y_true = y[test_index]
        accuracies1.append(accuracy_score(y_true, y_predict))

    return ("accuracy mod1:", np.average(accuracies1))



if __name__=="__main__":
    #Read and clean data
    df= pd.read_csv("../../cap_data/BGC_data.csv")
    df["Race/Ethnicity"].fillna("AI",inplace=True)
    df["gender_num"]=[1 if gend=="F" else 0 for gend in df["Gender"]]
    df["club_num"]=[1 if club!="Mission" else 0 for club in df["Group"]]
    df["age_bin"]=[1 if year>10 else 0 for year in df["Age"]]
    X=df.drop(['29'],axis=1)
    y=pd.Series([0 if reten>=4 else 1 for reten in df['29']])
    X_train, X_test, y_train, y_test=train_test_split(X,y,stratify=y)
    impute_med(X_train,["2","3 (out of 4)","7","22","23","25","26"])
    surv_quest_df=X_train.drop(['ID', 'Group', 'Age', "Grade in fall '18", 'Gender', 'Race/Ethnicity','gender_num', 'club_num', 'age_bin'],axis=1)
    #Plots for EDA
    quest_to_plot_1=['1', '2', '3 (out of 4)', '4 (out of 4)', '5', '6', '7', '8', '9', '10',
        '11', '12', '13', '14', '15', 'SCHOOL16', '17', '18', '19', '20', '21',
        '22', '23', '24', '25', '26', '27','28','30']
    quest_to_plot_2=['29']
    plot_hists(surv_quest_df,quest_to_plot_1)
    plot_hists(df,quest_to_plot_2)
    demo_to_plot=['Gender','Race/Ethnicity','Group','Age',"Grade in fall '18"]
    plot_bar(X_train,demo_to_plot)
    plt.savefig("images/demo_bar.png")
    #PCA for Dimensionality Reduction
    col_to_scale=['3 (out of 4)', '4 (out of 4)','SCHOOL16']
    same_scale(surv_quest_df,col_to_scale)
    same_scale(X_test,col_to_scale) #for later on
    pca = decomposition.PCA()
    pca.fit_transform(surv_quest_df)
    scree_plot_ev(pca)
    plt.savefig("images/sn1.png")
    U,sigma,VT=get_matrix_svd(surv_quest_df,5)
    #NMF for Dimensionality Reduction/Topic Modeling
    W,H=get_matrix_nmf(surv_quest_df,5)
    plt_recon_error(surv_quest_df,25)
    plt.savefig("images/recon_error.png")
    #Random Forest for Dimensionality Reduction
    rf_feature_select=RandomForestClassifier(n_estimators=100,  n_jobs=-1, class_weight='balanced',random_state=1)
    rf_feature_select.fit(surv_quest_df, y_train)
    fi=pd.DataFrame()
    fi["question"]=surv_quest_df.columns
    fi["feature_importance"]=rf_feature_select.feature_importances_
    fi.sort_values(by='feature_importance',ascending=False,inplace=True)
    plt.figure(figsize=(25,7))
    sns.barplot(x=fi['question'], y=fi["feature_importance"])
    plt.xlabel("Questions",fontsize=15)
    plt.ylabel("Feature Importance",fontsize=15)
    plt.savefig("images/feature_import.png")
    pred=rf_feature_select.predict(surv_quest_df)
    acc=accuracy_score(y_train, pred)

    corr = df.corr()
    plt.figure(figsize=(10,10))
    sns.heatmap(corr,
            xticklabels=corr.columns.values,
            yticklabels=corr.columns.values)
    plt.savefig("images/heat.png")

    surv_quest_df["y"]=y_train
    for col in surv_quest_df.columns:
        mask=surv_quest_df["y"]==1
        df1=surv_quest_df[mask]
        df2=surv_quest_df[~mask]
        plt.figure(figsize=(10,10))
        plt.subplot(1,1,1)
        sns.distplot(df1[col],color='b')
        plt.subplot(1,1,1)
        sns.distplot(df2[col],color='g')
        plt.xticks([])
        plt.yticks([])
        name="images/"+col+"compare.png"
        plt.savefig(name)
    #All Questions and demographics
    rf_model1=RandomForestClassifier(n_estimators=100,  n_jobs=-1, class_weight='balanced')
    all_quest_demo=X_train.drop(['ID', 'Group', 'Age', "Grade in fall '18", 'Gender', 'Race/Ethnicity'],axis=1)
    acc1=train_mod_kfold_accuracy(rf_model1, all_quest_demo.values,y_train.values)
    #15 Principle Components and Demographics
    rf_model2=RandomForestClassifier(n_estimators=100,  n_jobs=-1, class_weight='balanced')
    pca15 = decomposition.PCA(n_components=15)
    X_pca = pd.DataFrame(pca15.fit_transform(surv_quest_df))
    demos=X_train[['gender_num','club_num', 'age_bin']].reset_index().drop(['index'],axis=1)
    pca_demo=pd.concat([X_pca, demos], axis=1, join_axes=[X_pca.index])
    acc2=train_mod_kfold_accuracy(rf_model2, pca_demo.values,y_train.values)
    #10 Most Important Questions
    rf_model3=RandomForestClassifier(n_estimators=100,  n_jobs=-1, class_weight='balanced')
    import_quest_lst=[question for question in fi["question"][:10]]
    import_quest_df=surv_quest_df[import_quest_lst].reset_index().drop(["index"],axis=1)
    import_quest_demos=pd.concat([import_quest_df, demos], axis=1, join_axes=[X_pca.index])
    acc3=train_mod_kfold_accuracy(rf_model3,import_quest_demos.values,y_train.values)
