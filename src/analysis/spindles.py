"""
Módulo para detecção de spindles do sono.

Spindles são oscilações rápidas características do estágio N2,
com frequência entre 11-16 Hz e duração típica de 0.5-2 segundos.
"""

import numpy as np
from .bandpower import bandpower


def detect_spindles(signal, sf, sigma_history):
    """
    Detecta spindles do sono baseado na banda sigma (11-16 Hz).
    
    Spindles são detectados quando a potência sigma excede
    2.5x a média do baseline histórico.
    
    Args:
        signal (array): Sinal EEG da janela atual
        sf (int): Frequência de amostragem (Hz)
        sigma_history (list): Lista com histórico de potências sigma
        
    Returns:
        tuple: (spindle_detected, sigma_power, spindle_index)
            - spindle_detected (bool): True se spindle foi detectado
            - sigma_power (float): Potência atual na banda sigma
            - spindle_index (float): Razão entre potência atual e baseline
            
    Example:
        >>> signal = np.random.randn(768)  # 3 segundos @ 256 Hz
        >>> history = []
        >>> detected, power, index = detect_spindles(signal, 256, history)
    """
    # Potência na banda sigma (spindles)
    sigma_power = bandpower(signal, sf, (11, 16))
    
    # Adiciona à história
    sigma_history.append(sigma_power)
    if len(sigma_history) > 10:
        sigma_history.pop(0)
    
    # Se não temos histórico suficiente, não podemos detectar
    if len(sigma_history) < 5:
        return False, sigma_power, 0.0
    
    # Calcula baseline (média das últimas medições)
    baseline = np.mean(sigma_history[:-1])
    
    # Spindle detectado se a potência atual é 2.5x maior que o baseline
    threshold = baseline * 2.5
    spindle_detected = bool(sigma_power > threshold and sigma_power > 0.1)
    
    # Índice de spindle (quanto maior, mais provável N2)
    spindle_index = float(sigma_power / baseline) if baseline > 0 else 0.0
    
    return spindle_detected, sigma_power, spindle_index
