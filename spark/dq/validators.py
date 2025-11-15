from typing import Dict, List, Tuple
from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def validate_not_null(df: DataFrame, columns: List[str]) -> Tuple[str, int]:
    expr = " OR ".join([f"{c} IS NULL" for c in columns])
    fails = df.filter(expr).count()
    return ("not_null", fails)


def validate_unique(df: DataFrame, columns: List[str]) -> Tuple[str, int]:
    dup_count = df.groupBy([F.col(c) for c in columns]).count().filter("count > 1").count()
    return ("unique", dup_count)


def validate_value_range(df: DataFrame, column: str, min_value: float, max_value: float) -> Tuple[str, int]:
    fails = df.filter((F.col(column) < min_value) | (F.col(column) > max_value)).count()
    return ("value_range", fails)


def validate_regex(df: DataFrame, column: str, pattern: str) -> Tuple[str, int]:
    fails = df.filter(~F.col(column).rlike(pattern)).count()
    return ("regex", fails)


def validate_row_count_between(df: DataFrame, min_rows: int, max_rows: int) -> Tuple[str, int]:
    n = df.count()
    fails = 0 if (n >= min_rows and n <= max_rows) else 1
    return ("row_count_between", fails)


def validate_allowed_values(df: DataFrame, column: str, allowed: List[str]) -> Tuple[str, int]:
    fails = df.filter(~F.col(column).isin(allowed)).count()
    return ("allowed_values", fails)


def validate_no_future_dates(df: DataFrame, column: str) -> Tuple[str, int]:
    fails = df.filter(F.col(column) > F.current_date()).count()
    return ("no_future_dates", fails)


def validate_non_negative(df: DataFrame, column: str) -> Tuple[str, int]:
    fails = df.filter(F.col(column) < 0).count()
    return ("non_negative", fails)


def run_standard_checks(df: DataFrame) -> Dict[str, int]:
    results: Dict[str, int] = {}
    checks = [
        validate_row_count_between(df, 1, 10_000_000),
    ]
    for key, fails in checks:
        results[key] = fails
    return results


