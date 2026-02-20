"""
Módulo de análise de sinais EEG.

Este módulo contém funções para análise de sinais EEG,
incluindo cálculo de potência de bandas, detecção de spindles
e classificação de estágios de sono.
"""

from .bandpower import bandpower
from .spindles import detect_spindles
from .sleep_stages import estimate_sleep_stage

__all__ = ['bandpower', 'detect_spindles', 'estimate_sleep_stage']
