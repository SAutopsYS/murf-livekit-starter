"""Deterministic math solver. Never guesses. Never raises to callers."""

from __future__ import annotations

import ast
import operator
import re
from fractions import Fraction

from specialists.schemas import MathSolveResult, specialist_error

_ALLOWED_BINOPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}
_WORD_ADD = re.compile(
    r"\b(more|adds?|buys?|gets?|plus|sum|total|जोड़|और)\b",
    re.IGNORECASE,
)
_WORD_SUB = re.compile(
    r"\b(left|gives?|loses?|minus|remain|remaining|घटा|बचे)\b",
    re.IGNORECASE,
)
_WORD_MUL = re.compile(
    r"\b(times|each|groups? of|multipl|गुणा)\b",
    re.IGNORECASE,
)
_WORD_DIV = re.compile(
    r"\b(shared|split|divided|per|भाग)\b",
    re.IGNORECASE,
)
_NUM_RE = re.compile(r"\d+(?:\.\d+)?")
_PERCENT_OF_RE = re.compile(
    r"(\d+(?:\.\d+)?)\s*%\s*(?:of)?\s*(\d+(?:\.\d+)?)",
    re.IGNORECASE,
)
_FRACTION_OP_RE = re.compile(
    r"(\d+)\s*/\s*(\d+)\s*([+\-x\u00d7*\u00f7/])\s*(\d+)\s*/\s*(\d+)",
)
_SIMPLE_OP_RE = re.compile(
    r"(-?\d+(?:\.\d+)?)\s*([+\-x\u00d7*\u00f7/])\s*(-?\d+(?:\.\d+)?)",
)
_FRACTION_OF_RE = re.compile(
    r"(\d+)\s*/\s*(\d+)\s+of\s+(\d+(?:\.\d+)?)",
    re.IGNORECASE,
)


def _format_number(value: float | Fraction) -> str:
    if isinstance(value, Fraction):
        if value.denominator == 1:
            return str(value.numerator)
        return f"{value.numerator}/{value.denominator}"
    if abs(value - round(value)) < 1e-9:
        return str(round(value))
    return f"{value:.4f}".rstrip("0").rstrip(".")


def _safe_eval(expression: str) -> float:
    tree = ast.parse(expression, mode="eval")
    return float(_eval_node(tree.body))


def _eval_node(node: ast.AST) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return -_eval_node(node.operand)
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_BINOPS:
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        if isinstance(node.op, ast.Div) and right == 0:
            raise ZeroDivisionError
        return float(_ALLOWED_BINOPS[type(node.op)](left, right))
    raise ValueError("unsupported")


def _classify_topic(text: str) -> str:
    lowered = text.lower()
    if "%" in text or "percent" in lowered or "प्रतिशत" in text:
        return "percentages"
    if "/" in text or "fraction" in lowered or "भिन्न" in text:
        return "fractions"
    if any(
        token in lowered for token in ("word", "has ", "have ", "apples", "pencils")
    ):
        return "word_problems"
    if (
        any(token in text for token in ("\u00d7", "*", "x", "X"))
        or "multipl" in lowered
    ):
        return "multiplication"
    if any(token in text for token in ("\u00f7", "/")) or "divid" in lowered:
        return "division"
    if "-" in text or "subtract" in lowered:
        return "subtraction"
    if "+" in text or "add" in lowered:
        return "addition"
    return "arithmetic"


def _solve_percent(text: str) -> MathSolveResult | None:
    match = _PERCENT_OF_RE.search(text)
    if match is None:
        return None
    part = float(match.group(1))
    whole = float(match.group(2))
    answer = part / 100.0 * whole
    return {
        "error": False,
        "topic": "percentages",
        "expression": f"{part}% of {whole}",
        "steps": [
            f"Write {part}% as {part}/100.",
            f"Multiply {part}/100 by {whole}.",
        ],
        "answer": _format_number(answer),
    }


def _solve_fraction_op(text: str) -> MathSolveResult | None:
    match = _FRACTION_OP_RE.search(text)
    if match is None:
        of_match = _FRACTION_OF_RE.search(text)
        if of_match is None:
            return None
        left = Fraction(int(of_match.group(1)), int(of_match.group(2)))
        whole = Fraction(of_match.group(3))
        answer = left * whole
        return {
            "error": False,
            "topic": "fractions",
            "expression": f"{left} of {whole}",
            "steps": [
                f"Write the fraction {left}.",
                f"Multiply by {whole}.",
            ],
            "answer": _format_number(answer),
        }
    left = Fraction(int(match.group(1)), int(match.group(2)))
    op = match.group(3)
    right = Fraction(int(match.group(4)), int(match.group(5)))
    ops = {
        "+": left + right,
        "-": left - right,
        "*": left * right,
        "x": left * right,
        "\u00d7": left * right,
        "/": left / right if right != 0 else None,
        "\u00f7": left / right if right != 0 else None,
    }
    answer = ops.get(op)
    if answer is None:
        return None
    return {
        "error": False,
        "topic": "fractions",
        "expression": f"{left} {op} {right}",
        "steps": [
            f"Write both numbers as fractions: {left} and {right}.",
            f"Compute {left} {op} {right}.",
        ],
        "answer": _format_number(answer),
    }


def _solve_simple(text: str) -> MathSolveResult | None:
    match = _SIMPLE_OP_RE.search(text.replace("\u00d7", "*").replace("\u00f7", "/"))
    if match is None:
        return None
    left = match.group(1)
    op = match.group(2)
    right = match.group(3)
    mapped = {"x": "*", "X": "*", "\u00d7": "*", "\u00f7": "/"}.get(op, op)
    expression = f"{left}{mapped}{right}"
    try:
        value = _safe_eval(expression)
    except (ValueError, ZeroDivisionError, SyntaxError):
        return None
    topic = _classify_topic(f"{left}{op}{right}")
    return {
        "error": False,
        "topic": topic,
        "expression": f"{left} {op} {right}",
        "steps": [
            f"Identify the numbers {left} and {right}.",
            f"Apply the operation {op}.",
        ],
        "answer": _format_number(value),
    }


def _solve_word_problem(text: str) -> MathSolveResult | None:
    numbers = [float(item) for item in _NUM_RE.findall(text)]
    if len(numbers) < 2:
        return None
    left, right = numbers[0], numbers[1]
    if _WORD_MUL.search(text):
        op, value, topic = "*", left * right, "word_problems"
    elif _WORD_DIV.search(text) and right != 0:
        op, value, topic = "/", left / right, "word_problems"
    elif _WORD_SUB.search(text):
        op, value, topic = "-", left - right, "word_problems"
    elif _WORD_ADD.search(text):
        op, value, topic = "+", left + right, "word_problems"
    else:
        return None
    return {
        "error": False,
        "topic": topic,
        "expression": f"{_format_number(left)} {op} {_format_number(right)}",
        "steps": [
            f"Find the two amounts: {_format_number(left)} and {_format_number(right)}.",
            f"Use {op} because of the wording in the problem.",
        ],
        "answer": _format_number(value),
    }


def solve_math(expression: str) -> MathSolveResult:
    """Solve a basic math problem. Returns a structured error when unsure."""
    if not isinstance(expression, str) or not expression.strip():
        return specialist_error("Unable to solve this math problem.", "unsolvable")  # type: ignore[return-value]

    text = expression.strip()
    for solver in (
        _solve_percent,
        _solve_fraction_op,
        _solve_simple,
        _solve_word_problem,
    ):
        try:
            result = solver(text)
        except Exception:
            return specialist_error(
                "Unable to solve this math problem.",
                "unsolvable",
            )  # type: ignore[return-value]
        if result is not None:
            return result

    return specialist_error("Unable to solve this math problem.", "unsolvable")  # type: ignore[return-value]
