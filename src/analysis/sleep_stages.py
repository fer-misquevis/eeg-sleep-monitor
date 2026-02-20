"""
Módulo para classificação de estágios de sono baseado em EEG.

Classifica o estado de vigília/sono em:
- Acordado (Wake)
- N1 (sono leve)
- N2 (sono moderado)
- N3 (sono profundo/SWS)
- REM
"""


def estimate_sleep_stage(delta, theta, alpha, beta):
    """
    Estima o estágio de sono baseado nas potências das bandas de frequência.
    
    Critérios de classificação:
    - Wake: Beta elevado, Alpha moderado (ritmo alfa posterior)
    - N1: Theta aumenta, Alpha diminui (transição)
    - N2: Theta dominante, presença de spindles
    - N3: Delta > 50% (ondas lentas de alta amplitude)
    - REM: Theta elevado, Beta moderado, Delta baixo
    
    Args:
        delta (float): Potência na banda Delta (0.5-4 Hz)
        theta (float): Potência na banda Theta (4-8 Hz)
        alpha (float): Potência na banda Alpha (8-12 Hz)
        beta (float): Potência na banda Beta (13-30 Hz)
        
    Returns:
        str: Estágio de sono classificado
        
    Example:
        >>> stage = estimate_sleep_stage(0.2, 0.5, 0.1, 0.2)
        >>> print(stage)  # N1 (Leve)
    """
    total = delta + theta + alpha + beta
    
    if total == 0:
        return "Unknown"
    
    # Proporções normalizadas
    delta_ratio = delta / total
    theta_ratio = theta / total
    alpha_ratio = alpha / total
    beta_ratio = beta / total
    
    # Lógica de classificação
    if delta_ratio > 0.5:
        return "N3 (Profundo)"
    elif delta_ratio > 0.3 and theta_ratio > 0.3:
        return "N2 (Moderado)"
    elif theta_ratio > 0.4 and alpha_ratio < 0.2:
        if beta_ratio > 0.15:
            return "REM"
        else:
            return "N1 (Leve)"
    elif beta_ratio > 0.25 or alpha_ratio > 0.25:
        return "Acordado"
    else:
        return "N1 (Leve)"
