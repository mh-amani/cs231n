from builtins import range
import numpy as np
from random import shuffle
from past.builtins import xrange

def softmax_loss_naive(W, X, y, reg):
    """
    Softmax loss function, naive implementation (with loops)

    Inputs have dimension D, there are C classes, and we operate on minibatches
    of N examples.

    Inputs:
    - W: A numpy array of shape (D, C) containing weights.
    - X: A numpy array of shape (N, D) containing a minibatch of data.
    - y: A numpy array of shape (N,) containing training labels; y[i] = c means
      that X[i] has label c, where 0 <= c < C.
    - reg: (float) regularization strength

    Returns a tuple of:
    - loss as single float
    - gradient with respect to weights W; an array of same shape as W
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)

    #############################################################################
    # TODO: Compute the softmax loss and its gradient using explicit loops.     #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    num_sample = X.shape[0]
    num_classes = W.shape[1]

    for i in range(num_sample):
      # loss
      score = X[i].dot(W)
      score -= np.max(score)
      score_exp = np.exp(score)
      score_exp_sum = np.sum(score_exp)
      loss += np.log(score_exp_sum) - score[y[i]]
      
      # gradient
      dW[:,y[i]] -= X[i]
      for j in range(num_classes):
        dW[:,j] += X[i] * np.exp(score[j]) / score_exp_sum

    loss /= num_sample
    loss += reg * np.sum(W**2)

    dW /= num_sample
    dW += 2 * reg * W

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
    """
    Softmax loss function, vectorized version.

    Inputs and outputs are the same as softmax_loss_naive.
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)

    #############################################################################
    # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    num_sample = X.shape[0]
    num_classes = W.shape[1]

    # loss
    score = X.dot(W)
    score -= np.max(score, axis=1).reshape(num_sample,1)
    score_exp = np.exp(score)
    score_exp_sum = np.sum(score_exp, axis=1)
    mask = np.eye(num_classes)[y]
    score_masked = score * mask
    loss += np.sum(np.log(score_exp_sum)) - np.sum(score_masked)
    loss /= num_sample
    loss += reg * np.sum(W**2)

    # gradient
    dW += np.divide(X , score_exp_sum.reshape(num_sample,1)).T.dot(score_exp)
    dW -= X.T.dot(mask)
    dW /= num_sample
    dW += 2 * reg * W

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW
