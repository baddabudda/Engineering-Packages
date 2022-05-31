import pandas as pd

titanic = pd.read_csv("titanic.csv", sep = ",")
print(titanic["Age"].head(5))
print(titanic[["Age", "Sex"]].head(5))
titanic["Realtives"] = titanic["SibSp"] + titanic["Parch"]
print(len(titanic[titanic["Realtives"] != 0]))
print(len(titanic.loc[(titanic["Embarked"]=='S'),"PassengerId"]))
print(f"Survived:", len(titanic[titanic["Survived"] == 1]))
print(f"Not survived:", len(titanic[titanic["Survived"] == 0]))

titanic["Pclass"] = titanic["Pclass"].map(lambda x: "Elite" if x == 1 else ("Middle" if x == 2 else "Prol"))

titanic["Fare_bin"] = "Expensive"
titanic.loc[(titanic.Fare < 20), "Fare_bin"] = "Cheap"
print(titanic)
