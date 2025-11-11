# algoritmos.py
# Implementação de algoritmos de ordenação com contagem de comparações, trocas e tempo.

import time
from copy import deepcopy

# -------------------------------------------------
# CLASSE RESULTADO
# -------------------------------------------------
class Result:
    def __init__(self, lista, comparacoes=0, trocas=0, tempo=0.0):
        self.lista = lista
        self.comparacoes = comparacoes
        self.trocas = trocas
        self.tempo = tempo


# -------------------------------------------------
# DECORADOR PARA MEDIR TEMPO
# -------------------------------------------------
def timed(fn):
    """Mede o tempo de execução e garante atualização de tempo em Result."""
    def wrapper(*args, **kwargs):
        t0 = time.time()
        res = fn(*args, **kwargs)
        t1 = time.time()
        tempo_exec = t1 - t0

        if isinstance(res, Result):
            res.tempo = tempo_exec
            return res
        elif isinstance(res, tuple) and len(res) == 3:
            return Result(res[0], res[1], res[2], tempo_exec)
        else:
            return Result(res, 0, 0, tempo_exec)
    return wrapper


# -------------------------------------------------
# FUNÇÃO AUXILIAR PARA PEGAR O VALOR DA CHAVE
# -------------------------------------------------
def key_value(item, chave):
    """Extrai um valor comparável (numérico ou string) de cada item."""
    try:
        val = item[chave] if isinstance(item, dict) else getattr(item, chave, None)
    except Exception:
        return None

    if isinstance(val, (list, tuple, set)):
        if len(val) > 0:
            val = val[0]
        else:
            return None

    try:
        if hasattr(val, "item"):
            val = val.item()
    except Exception:
        pass

    if val is None or str(val).strip() == "":
        return None

    try:
        return float(val)
    except Exception:
        return str(val).lower()


# -------------------------------------------------
# ALGORITMOS DE ORDENAÇÃO
# -------------------------------------------------

@timed
def bubble_sort(lista, chave):
    dados = deepcopy(lista)
    n = len(dados)
    comparacoes = 0
    trocas = 0

    for i in range(n):
        for j in range(0, n - i - 1):
            comparacoes += 1
            if key_value(dados[j], chave) > key_value(dados[j + 1], chave):
                dados[j], dados[j + 1] = dados[j + 1], dados[j]
                trocas += 1

    return Result(dados, comparacoes, trocas)


@timed
def insertion_sort(lista, chave):
    dados = deepcopy(lista)
    comparacoes = 0
    trocas = 0

    for i in range(1, len(dados)):
        key_item = dados[i]
        j = i - 1
        while j >= 0:
            comparacoes += 1
            if key_value(dados[j], chave) > key_value(key_item, chave):
                dados[j + 1] = dados[j]
                trocas += 1
                j -= 1
            else:
                break
        dados[j + 1] = key_item

    return Result(dados, comparacoes, trocas)


@timed
def merge_sort(lista, chave):
    """Merge Sort com contagem de comparações e trocas."""
    comparacoes = 0
    trocas = 0

    def _merge(left, right):
        nonlocal comparacoes, trocas
        merged = []
        i = j = 0
        while i < len(left) and j < len(right):
            comparacoes += 1
            if key_value(left[i], chave) <= key_value(right[j], chave):
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
            trocas += 1
        while i < len(left):
            merged.append(left[i])
            i += 1
            trocas += 1
        while j < len(right):
            merged.append(right[j])
            j += 1
            trocas += 1
        return merged

    def _merge_sort(lst):
        if len(lst) <= 1:
            return lst
        mid = len(lst) // 2
        left = _merge_sort(lst[:mid])
        right = _merge_sort(lst[mid:])
        return _merge(left, right)

    sorted_list = _merge_sort(deepcopy(lista))
    return Result(sorted_list, comparacoes, trocas)


@timed
def quick_sort(lista, chave):
    """Quick Sort com contagem de comparações e trocas."""
    import sys
    sys.setrecursionlimit(3000)

    comparacoes = 0
    trocas = 0

    def _quick(lst, depth=0):
        nonlocal comparacoes, trocas
        if len(lst) <= 1 or depth > 1000:
            return lst

        pivot = key_value(lst[len(lst) // 2], chave)
        if pivot is None:
            return lst

        left, equal, right = [], [], []

        for item in lst:
            val = key_value(item, chave)
            if val is None:
                continue
            comparacoes += 1
            if val < pivot:
                left.append(item)
                trocas += 1
            elif val > pivot:
                right.append(item)
                trocas += 1
            else:
                equal.append(item)

        return _quick(left, depth + 1) + equal + _quick(right, depth + 1)

    sorted_list = _quick(deepcopy(lista))
    return Result(sorted_list, comparacoes, trocas)


# -------------------------------------------------
# TESTE LOCAL (opcional)
# -------------------------------------------------
if __name__ == "__main__":
    from random import shuffle
    lista = list(range(10))
    shuffle(lista)

    for nome, func in [
        ("bubble", bubble_sort),
        ("insertion", insertion_sort),
        ("merge", merge_sort),
        ("quick", quick_sort)
    ]:
        res = func(lista, None)
        print(f"{nome:10s} -> tempo: {res.tempo:.6f}s | comps: {res.comparacoes} | trocas: {res.trocas}")
