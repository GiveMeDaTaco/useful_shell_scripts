class QueryBuilder:
    def __init__(self, checks, elig_table, agg_table):
        self.checks = checks
        self.elig_table = elig_table
        self.agg_table = agg_table
    
    def build_query(self):
        checks_str = ", ".join([f"MIN({check}) AS {check}" for check in self.checks])
        
        # AggregatedData CTE
        aggregated_data_cte = f"""
        WITH AggregatedData AS (
            SELECT
                identifier1,
                {checks_str}
            FROM {self.elig_table}
            GROUP BY identifier1
        )
        """

        # RemainingAfterChecks CTE
        remaining_after_checks_cases = []
        for i, check in enumerate(self.checks):
            conditions = " AND ".join([f"{self.checks[j]} = 1" for j in range(i + 1)])
            remaining_after_checks_cases.append(f"CASE WHEN {conditions} THEN 1 ELSE 0 END AS {check}")

        remaining_after_checks_str = ", ".join(remaining_after_checks_cases)
        remaining_after_checks_cte = f"""
        , RemainingAfterChecks AS (
            SELECT
                identifier1,
                {remaining_after_checks_str}
            FROM AggregatedData
        )
        """

        # RemainingWithoutCheck CTE
        remaining_without_check_cases = []
        for i, check in enumerate(self.checks):
            conditions = " AND ".join([f"{self.checks[j]} = 1" for j in range(len(self.checks)) if j != i])
            remaining_without_check_cases.append(f"CASE WHEN {conditions} THEN 1 ELSE 0 END AS Without_{check}")

        remaining_without_check_str = ", ".join(remaining_without_check_cases)
        remaining_without_check_cte = f"""
        , RemainingWithoutCheck AS (
            SELECT
                identifier1,
                {remaining_without_check_str}
            FROM AggregatedData
        )
        """

        # Gains CTE
        gains_cases = []
        for check in self.checks:
            gains_cases.append(f"SUM(Without_{check}) - SUM({self.checks[-1]}) AS {check}")

        gains_str = ", ".join(gains_cases)
        gains_cte = f"""
        , Gains AS (
            SELECT
                {gains_str}
            FROM RemainingWithoutCheck
        )
        """

        # Final SELECT
        final_select_cases = ", ".join([f"{check} AS gain_{check}" for check in self.checks])
        final_select = f"""
        SELECT
            {final_select_cases}
        FROM Gains;
        """

        # Combine all parts
        query = aggregated_data_cte + remaining_after_checks_cte + remaining_without_check_cte + gains_cte + final_select
        return query

# Example usage
checks = ['check_1', 'check_2', 'check_3']
elig_table = "YourTableName"
agg_table = "AggregatedDataTable"
query_builder = QueryBuilder(checks, elig_table, agg_table)
query = query_builder.build_query()
print(query)


class QueryBuilder:
    def __init__(self, checks, elig_table):
        self.checks = checks
        self.elig_table = elig_table
    
    def build_query(self):
        # Building the MIN checks part for AggregatedData
        min_checks_str = ", ".join([f"MIN({check}) AS min_{check}" for check in self.checks])
        
        # AggregatedData CTE
        aggregated_data_cte = f"""
        WITH AggregatedData AS (
            SELECT
                identifier1,
                {min_checks_str}
            FROM {self.elig_table}
            GROUP BY identifier1
        )
        """

        # RemainingAfterChecks CTE
        remaining_after_checks_cases = []
        for i, check in enumerate(self.checks):
            conditions = " AND ".join([f"min_{self.checks[j]} = 1" for j in range(i + 1)])
            remaining_after_checks_cases.append(f"CASE WHEN {conditions} THEN 1 ELSE 0 END AS remaining_after_{check}")

        remaining_after_checks_str = ", ".join(remaining_after_checks_cases)
        remaining_after_checks_cte = f"""
        , RemainingAfterChecks AS (
            SELECT
                identifier1,
                {remaining_after_checks_str}
            FROM AggregatedData
        )
        """

        # Final SELECT
        final_select_cases = ", ".join([f"SUM(remaining_after_{check}) AS remaining_after_{check}" for check in self.checks])
        final_select = f"""
        SELECT
            {final_select_cases}
        FROM RemainingAfterChecks;
        """

        # Combine all parts
        query = aggregated_data_cte + remaining_after_checks_cte + final_select
        return query

# Example usage
checks = ['check_1', 'check_2', 'check_3']
elig_table = "YourTableName"
query_builder = QueryBuilder(checks, elig_table)
query = query_builder.build_query()
print(query)
