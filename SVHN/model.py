import torch
import torch.nn as nn
from torch.utils.data import Dataset
import scipy.io
import numpy as np
from PIL import Image

class SVHNDataset(Dataset):
    def __init__(self, mat_path, transform=None):
        data = scipy.io.loadmat(mat_path)
        self.images = np.transpose(data['X'], (3, 2, 0, 1)).astype(np.uint8)  # [N, C, H, W]
        self.labels = data['y'].flatten()
        self.labels[self.labels == 10] = 0
        self.transform = transform

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        img = self.images[idx]  # shape: [C, H, W]
        img = np.transpose(img, (1, 2, 0))  # 轉成 [H, W, C]
        img = Image.fromarray(img)  # ✅ 轉成 PIL.Image，才能用 ToPILImage 和 ColorJitter 等 transform
        if self.transform:
            img = self.transform(img)
        label = self.labels[idx]
        return img, label



class SVHNCNN(nn.Module):
    def __init__(self):
        super(SVHNCNN, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
        )
        self.fc = nn.Sequential(
            nn.Linear(64 * 8 * 8, 256),
            nn.ReLU(),
            nn.Linear(256, 10),
        )

    def forward(self, x):
        x = self.conv(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return x
