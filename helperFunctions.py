#Train and Predictee need to have column names in the same order
#correctOrder ensures that the Training set and the song that's to be predicted have their columns in the correct order
def matchOrder(incorrectShape, correctShape):
    return(incorrectShape[correctShape.columns.values])