
# Setup
## Clone the repo
~~~
clone https://github.com/Davide-Cruciani/CVprojectSum2026.git
cd CVprojectSum2026
~~~

## Download additional components
Download CCN_synth in data
~~~
cd project/data
wget https://huggingface.co/datasets/sywang/CNNDetection/resolve/main/CNN_synth_testset.zip
unzip CNN_synth_testset.zip
~~~

Download TruFor weights
https://www.grip.unina.it/download/prog/TruFor/TruFor_weights.zip
and put them in /models/TruFor/weights

Download wongCNN weights
~~~
cd CVprojectSum2026/models/CNNDetection/weights/
bash ./download_weights.sh
~~~

# Usage

The project revolves around the notebook **CVprojectSum2026/project/main.ipynb**

If it is the first time, its necessary to run the dataset setup section, controlled by the vaiable **DOWLOAD** in the **Globals** section of the notebook. Set it to True to enable the dataset contruction. 

It will also be necessary to enable the **TRAINING** global variable to allow the creation of the weights for the modified model

Any execution after the first can be done with DOWNLOAD=False and TRAINING=False. 

The varibale **SOURCE_FOLDER_REMOVAL** controls if the subsections of the original datasets are preserved after the construction of the *train*, *validation* and *test* datasets

Any variable in globals that ends with **_DIR** and be chaged to adjust the position of the corresponding directories in the system

# Directories

- models: Contains the benchmark models
- JPEGAI: Contains the AI compression system
- project/analysis: Contains the saved images about frequency domain analysis
- project/data: contains the datasets
- project/results: contains the results of model evaluation in json format
- project/weights: contain the saved weights of the trained models