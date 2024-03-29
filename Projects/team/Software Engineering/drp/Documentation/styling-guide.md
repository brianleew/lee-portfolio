# Team DRP Coding Style guide

## File names

We have already fallen into a convention of using kebab case for filenames. Future files should also follow this convention by separating each word in the filename with a dash, preferably also using entirely lowercase letters to keep the names as uniform as possible.

Examples of proper file names would be :

```
docker-compose.yml
meter-data.csv
mysql-to-flask.py
```
## Variable and Function names

Since we are working with several languages within this project, we want to try to keep the variable names consistent across them all so that the code is easier to understand. Because of this we have decided to use camel case, while also including the variable type before the name. This should let the code be as easy to understand as possible across all of our platforms.

Examples of proper variable names would be :
```
strFirstName
intMeterID
divPageOne
```
### Javascript Functions

Functions should follow these same rules, with the type of variable they return preceding their name.

Examples of proper Function names in javascript would be :
```
strFormatDateline(dateCurrDate)
voidCreateNewDiv(objMeter)
intGetMax(arrInts)
```

### Flask Functions


## Code Comments

For our purposes, exact dates of changes are not the most important thing. Since our team is relatively small the most important things are quickly knowing the purpose of code, and the person who last updated it. That will let us know who to consult about the section.

Examples of a proper header comment is below :
```
## Purpose :
## Original Author : 
## Last Updated By:
```