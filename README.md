# Capita Selecta Computer Science: Neuro Symbolic AI

## Comparing Neuro Symbolic AI against a purely neural network based approach on Visual Question Answering
This repository focuses on Visual Question Answering, where a Neuro Symbolic AI approach with a knowledge base is compared with a purely neural network based approach. From the experiments, it follows that DeepProbLog, the framework used for the Neuro Symbolic AI approach, is able to achieve the same accuracy as the pure neural network based approach with almost 200 times less iterations. Clearly, the training is much more targeted, but however, comes at a cost. The algebraic operators internal to DeepProbLog are extremely costly and hence the actual training time is considerably slower. Another drawback of DeepProbLog is that no easy speedups can be achieved, since the algebraic operators only work on CPU's, and hence cannot benefit from accelerators such as GPU's.

Read more on the following blogpost: https://medium.com/p/621099805bc7
