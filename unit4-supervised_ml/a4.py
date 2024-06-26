# CS305 Park University
# Assignment #4 Starter Code
# Supervised Learning Lab

from learnProblem import Data_from_file, Learner, Evaluate
from learnDT import DT_learner
from learnCrossValidation import K_fold_dataset
from statistics import mean, mode

# In this assignment you'll perform supervised learning and analyze
# the results of the process. The initial steps are in the main function
# below where you will develop a baseline for the iris dataset and
# also test decision tree analysis against this dataset.
#
# Following that, you will need to complete the definition of the
# k-nearest-neighbor learner class (described in your reading)
# and additionally analyze it against the other techniques over
# several values of its "hyperparameter" k. Euclidean distance will
# be used in every case. 

class KNN_learner(Learner):
    """Lazy learning algorithm for a categorical target and numeric features"""
    def __init__(self,
                 dataset,
                 k=1,
                 train=None):
        self.dataset = dataset
        self.target = dataset.target
        self.k = k
        if train is None:
            self.train = self.dataset.train
        else:
            self.train = train

    def learn(self):
        """defines the k-nn prediction function to be returned
          the function will rely on the original dataset for predictions
        """
        def ev(ex):
            # find neighbors of ex
            ns = list(self.get_neighbors(ex, self.k))
            classes = set(map(self.target, self.train)) # all possible classes
            t = self.majority_vote(ns) # most common class among neighbors
            return { c: 1 if t == c else 0 for c in classes}  # prediction dictionary
        return ev
        
    def majority_vote(self, exs):
        """determines the most common target classification among examples"""
        return mode(map(self.target, exs))


#
# NOTE: Step 1 is below in the main function
#

# 5. 
# TODO: complete the definition of the euclidean distance function
    def euclidean_dist(self, ex1, ex2):
        """find euclidean distance between features of two examples"""
        return sum((a - b) ** 2 for a, b in zip(ex1[:-1], ex2[:-1])) ** 0.5
# 6.
# TODO: complete the definition of the get_neighbors function    
    def get_neighbors(self, ex, k):
        """generate the k closest neighbors of example 'ex'"""
        distances = [(other_ex, self.euclidean_dist(ex, other_ex))
                 for other_ex in self.train if other_ex != ex]
        distances.sort(key=lambda x: x[1])
        return [ex for ex, dist in distances[:k]]

def main():
    folds = 10
    trials = 100
    dataset_filename = 'data/iris.data'
    bl_acc=0
    dt_acc=0

    for i in range(trials):
# 1.
# TODO: load the dataset (using the specified filename)
# store it in the variable 'data'.
# We're not using cross validation so use the defaults for
# creating a training and test set.
        data = Data_from_file('data/iris.data', target_index=-1)

# 2.
# TODO: create the baseline predictor (always guess the mode)
# hint: look at the implementation of majority_vote and check
# the notes. 
        domain = set(map(lambda x: x[4], data.train))
        mode_value = mode(map(lambda x: x[4], data.train))
        baseline = lambda x: {v: 1 if v==mode_value else 0 for v in domain}
        
        bl_acc += data.evaluate_dataset(data.test,
                                       baseline,
                                       Evaluate.accuracy)
# 3.         
# in the end results, you'll see that the accuracy for the
# baseline is a little worse than what you might consider
# for random guessing. Why do you suppose that is the case
# for this dataset?
# TODO: Briefly answer in comments

# ANSWER: My first thoughts on why the accuracy is so low for the baseline, is when calculating the mode with such a small dataset, which doesn't represent the distribution.
    bl_acc /= trials
    
# 4.
# TODO: load the dataset again, but make sure all examples are
# training examples (since we'll use cross-validation).
# store it in the variable 'data'.
    data = Data_from_file(dataset_filename, prob_test=0, target_index=-1)
    for i in range(trials):
        cvdata = K_fold_dataset(data, folds)
        dt_acc += cvdata.validation_error(DT_learner, Evaluate.accuracy)
    dt_acc /= trials
    
    # 7. 
    # TODO: add k values to the list you want to check for accuracy
    kvals = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21]
    knn_accs = []  # will hold accuracies for each k value
    for k in kvals:
        acc = 0
        for i in range(trials):
            cvdata = K_fold_dataset(data, folds)
            # Adjust the lambda function to pass only 'ds' and 'train' to KNN_learner
            acc += cvdata.validation_error(lambda ds, train: KNN_learner(ds, k=k, train=train),
                                           Evaluate.accuracy)
        acc /= trials
        knn_accs.append(acc)
    
    print('after', trials, 'trials...')
    print('basline accuracy:', bl_acc)
    print('decision tree accuracy:', dt_acc)
    print('knn accuracy for:')
    for i in range(len(kvals)):
        print('k =',kvals[i],':', knn_accs[i])
    
# 8. 
# TODO: what methods are working the best? Add brief comments to
# your final submission.

# ANSWER: The best method would be the knn, which is determined from the accuracy of the test results. The results were ~2-4% more accurate then the DT reults, and ~70% higher than the baseline 
  
if __name__ == '__main__':
  main()
