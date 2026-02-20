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
    delta_ratio = delta
    theta_ratio = theta
    alpha_ratio = alpha
    beta_ratio = beta
    
    # Lógica de classificação baseada em ratios de potência por banda
    # Delta: 0.5–4 Hz | Theta: 4–8 Hz | Alpha: 8–13 Hz | Beta: 13–30 Hz | Gamma: >30 Hz

    if delta_ratio > 0.50 and delta_ratio < 4.0:
        # Delta dominante = sono profundo
        return "N3 (Profundo)"

    elif theta_ratio > 4.1 and theta_ratio < 8.0:
        # Delta elevado com theta presente = sono moderado
        return "N2 (Moderado)"

    elif alpha_ratio > 8.1 and alpha_ratio < 13.0:
        # Theta dominante, alpha baixo = sonolência/sono leve
        if beta_ratio > 13.1 and beta_ratio < 30.0:
            # Beta elevado junto com theta = característica REM
            return "REM"
        else:
            return "Acordado"

    #elif beta_ratio > 0.30 or gamma_ratio > 0.15:
        # Beta/Gamma dominantes = foco ativo ou alerta
    #    return "Acordado (Alerta)"

    else:
        return "N1 (Leve)"
