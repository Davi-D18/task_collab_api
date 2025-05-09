#!/usr/bin/env bash

# Força o Python a usar UTF-8 em todo o I/O
export PYTHONUTF8=1          # ativa o UTF-8 Mode do Python ≥3.7 :contentReference[oaicite:0]{index=0}
export PYTHONIOENCODING=utf-8  # garante encoding UTF-8 para stdin/stdout/stderr :contentReference[oaicite:1]{index=1}

# Repasse todos os argumentos para manage.py no modo UTF-8
python -X utf8 manage.py "$@"  # '-X utf8' habilita o modo UTF-8 (PEP 540) :contentReference[oaicite:2]{index=2}
