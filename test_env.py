import torch
import transformers
import captum
import shap
import spacy

print('\n--- Environment Check ---')
print(f'PyTorch Version  : {torch.__version__}')
print(f'Transformers     : {transformers.__version__}')
print(f'Captum (XAI)     : {captum.__version__}')
print(f'SHAP (XAI)       : {shap.__version__}')
print('STATUS: Setup complete and ready!')
