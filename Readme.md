## Don't You (Project Around Discs)? Calibrating Intervertebral Disc Finite Element Model With a Neural Network Surrogate and Projected Gradient Descent

This repository contains the implementation of our paper. The project aims to reproduce the results presented in the paper and provide a reference implementation for further research and experimentation.

## Abstract
Accurate calibration of Finite Element (FE) models for intervertebral discs (IVD) is essential for their reliability and application in diagnosing and planning treatments for spinal conditions. Traditional calibration methods are time-consuming and computationally intensive, requiring iterative, derivative-free optimization algorithms that often take hours or days to converge. 

This study addresses these challenges by introducing a novel, efficient, and effective calibration method for an L4L5 IVD FE model using a Neural Network (NN) surrogate model. The NN surrogate predicts simulation outcomes with high accuracy, significantly reducing the computational cost associated with traditional FE runs. A Projected Gradient Descent (PGD) approach guided by gradients of the NN surrogate is proposed to efficiently calibrate FE models. Our method explicitly enforces feasibility with a projection step, thus maintaining material bounds throughout the optimization process. 

The proposed method is evaluated against a state-of-the-art Genetic Algorithm (GA) baseline on a synthetic dataset and real-world experimental measurements. Our approach demonstrates superior performance, achieving a mean $\mathcal{R}^2$ score of 0.99 on synthetic data while reducing calibration time. On experimental specimens, our method consistently outperforms the GA baseline in terms of Mean Absolute Error (MAE). However both methods show increased error at extreme moments due to FE model limitations. Future research will investigate alternative data generation techniques and improved FE models to more effectively manage patient-specific, variable geometries.

### Installation

To set up the environment, please follow these steps:

1. Install Python 3.10.13 or a compatible version.
2. Install conda.

### Setup

To create the conda environment, execute the following commands:

```shell
conda env create -f IVD-CALIBNN.yml
conda activate IVD-CALIBNN
```

### Usage

Here are the steps to use this repository:

1. **Dataset**: The training set used to train our surrogate models and the synthetic test data can be found in the `/datasets` directory.
2. **Model Checkpoint**: A checkpoint of the trained surrogate neural network is available in the `/trained_models` directory.
3. **Model Training**: To train the surrogate models, refer to the `model_training.ipynb` notebook for the code and hyperparameters.
4. **FE Model Calibration**: For an example code on how to calibrate experimental data, check out the `pgd_calibration.ipynb` notebook.

### Citation

If you use this code or find it helpful in your research, please consider citing our paper:

```
@article{author2022paper,
    title={Paper Title},
    author={Author, John and Co-Author, Jane},
    journal={Journal of Research},
    year={2022},
    volume={10},
    number={2},
    pages={100-120},
    doi={10.1234/jr.2022.1234}
}
```

### License

This project is licensed under the [MIT License](LICENSE).