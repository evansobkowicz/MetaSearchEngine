import math

class Calc:


    # Calculate Inverse Document Frequency (log(DF total/DF))
    def idf(self, df, total):
        return math.log10(total/df)


    # Calculate 1 + Log TF
    def log_tf(self, tf):
        return 1 + math.log10(tf)


    # Calculate TF-IDF for a document
    def tf_idf(self, df, total, tf):
        return self.idf(df, total) * self.log_tf(tf)

