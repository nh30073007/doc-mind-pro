{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "ba8b3698-2680-4cce-9cbd-fec7b21ca61b",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "PyTorch version: 2.5.0+cpu\n",
      "CUDA available: False\n",
      "CUDA not available. Check installation.\n"
     ]
    }
   ],
   "source": [
    "# test_torch.py\n",
    "import torch\n",
    "\n",
    "print(\"PyTorch version:\", torch.__version__)\n",
    "print(\"CUDA available:\", torch.cuda.is_available())\n",
    "if torch.cuda.is_available():\n",
    "    print(\"CUDA device count:\", torch.cuda.device_count())\n",
    "    print(\"CUDA device name:\", torch.cuda.get_device_name(0))\n",
    "else:\n",
    "    print(\"CUDA not available. Check installation.\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "18da69b0-6b89-4b49-b901-311ab331efaf",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
