from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from enum import Enum
import re
from typing import Iterator, List


class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        return tuple((x.name, x.value) for x in cls)


# noinspection PyTypeChecker
def validar_rg(rg):
    """
    Valida RGs, retornando apenas a string de números válida.

    # RGs errados
    >>> validar_rg('abcdefghi')
    False
    >>> validar_rg('123')
    False
    >>> validar_rg('')
    False
    >>> validar_rg(None)
    False
    >>> validar_rg('123456789')
    False

    # CPFs corretos
    >>> validar_rg('293748767')
    '293748767'
    >>> validar_rg('29.374.876-7')
    '293748767'
    >>> validar_rg('  29 374 876 7  ')
    '293748767'
    """
    rg = ''.join(re.findall('\d', str(rg)))

    if (not rg) or (len(rg) < 9):
        return False

    # Pega apenas os 8 primeiros dígitos do RG e gera os 1 dígitos que faltam

    inteiros = [int(digit) for digit in rg if digit.isdigit()]
    novo = inteiros[:8]
    r = sum([(9-i)*v for i, v in enumerate(novo)]) % 11  # type: int

    if r != 10:
        f = r
    else:
        f = 0
    novo.append(f)

    # Se o número gerado coincidir com o número original, é válido
    if novo == inteiros:
        return int(rg)
    return False


# noinspection PyTypeChecker
def validar_cpf(cpf):
    """
    Valida CPFs, retornando apenas a string de números válida.

    # CPFs errados
    >>> validar_cpf('abcdefghijk')
    False
    >>> validar_cpf('123')
    False
    >>> validar_cpf('')
    False
    >>> validar_cpf(None)
    False
    >>> validar_cpf('12345678900')
    False

    # CPFs corretos
    >>> validar_cpf('95524361503')
    '95524361503'
    >>> validar_cpf('955.243.615-03')
    '95524361503'
    >>> validar_cpf('  955 243 615 03  ')
    '95524361503'
    """
    cpf = ''.join(re.findall('\d', str(cpf)))

    if (not cpf) or (len(cpf) < 11):
        return False

    # Pega apenas os 9 primeiros dígitos do CPF e gera os 2 dígitos que faltam

    # inteiros = map(int, cpf) >> erro 'map' object is not subscriptable
    inteiros = [int(digit) for digit in cpf if digit.isdigit()]
    novo = inteiros[:9]

    while len(novo) < 11:
        r = sum([(len(novo)+1-i)*v for i, v in enumerate(novo)]) % 11  # type: int

        if r > 1:
            f = 11 - r
        else:
            f = 0
        novo.append(f)

    # Se o número gerado coincidir com o número original, é válido
    if novo == inteiros:
        return int(cpf)
    return False


# noinspection PyTypeChecker
def validar_cnpj(cnpj):
    """
    Valida CNPJs, retornando apenas a string de números válidos.

    # CNPJs errados
    >>> validar_cnpj('abcdefghijklmn')
    False
    >>> validar_cnpj('123')
    False
    >>> validar_cnpj('')
    False
    >>> validar_cnpj(None)
    False
    >>> validar_cnpj('12345678901234')
    False
    >>> validar_cnpj('11222333000100')
    False

    # CNPJs corretos
    >>> validar_cnpj('11222333000181')
    '11222333000181'
    >>> validar_cnpj('11.222.333/0001-81')
    '11222333000181'
    >>> validar_cnpj('  11 222 333 0001 81  ')
    '11222333000181'
    """
    cnpj = ''.join(re.findall('\d', str(cnpj)))

    if (not cnpj) or (len(cnpj) < 14):
        return False

    # Pega apenas os 12 primeiros dígitos do CNPJ e gera os 2 dígitos que faltam
    inteiros = [int(digit) for digit in cnpj if digit.isdigit()]  # type: List[int]
    novo = inteiros[:12]  # type: Iterator[int]

    prod = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    while len(novo) < 14:
        r = sum([x*y for (x, y) in zip(novo, prod)]) % 11
        if r > 1:
            f = 11 - r
        else:
            f = 0
        novo.append(f)
        prod.insert(0, 6)

    # Se o número gerado coincidir com o número original, é válido
    if novo == inteiros:
        return int(cnpj)
    return False


def validador_cpf(cpf):
    teste = validar_cpf(cpf)
    if teste != cpf:
        raise ValidationError(
            _('%(cpf)s não é um CPF válido'),
            params={'cpf': cpf}
        )


def validador_rg(rg):
    teste = validar_rg(rg)
    if teste != rg:
        raise ValidationError(
            _('%(rg)s não é um RG válido. Utilize 0 para dígito X'),
            params={'rg': rg}
        )


def validador_cnpj(cnpj):
    if validar_cnpj(cnpj) != cnpj:
        raise ValidationError(
            _('%(cnpj)s não é um CNPJ válido'),
            params={'cnpj': cnpj}
        )
