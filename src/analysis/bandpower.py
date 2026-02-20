"""
Módulo para cálculo de potência de bandas de frequência EEG.
"""

import numpy as np
from scipy.signal import welch


def bandpower(data, sf, band):
    """
    Calcula a potência média em uma banda de frequência específica.
    
    Args:
        data (array): Sinal EEG
        sf (int): Frequência de amostragem (Hz)
        band (tuple): Tupla com (freq_min, freq_max) em Hz
        
    Returns:
        float: Potência média na banda especificada
        
    Example:
        >>> signal = np.random.randn(256)
        >>> power = bandpower(signal, 256, (8, 12))  # Banda Alpha
    """
    low, high = band
    freqs, psd = welch(data, sf, nperseg=sf*2)
    idx = np.logical_and(freqs >= low, freqs <= high)
    return float(np.mean(psd[idx]))
