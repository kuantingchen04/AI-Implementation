Define csp, run backtracking and use AC-3 filtering

- Structure

    - CSP Class

        define board row: A-I, col: 1-9

        varialbes: [A1, A2, ...]
        domains: { A1:{1,2,3..9} A2:{1,2,3...9} }
        constraints (neighbors): {A1:{A2,B1,...}, A2:{A1,..} }

    - CSP Processing

    - CSP Search (Backtracking)
        backtrack_search_solver(csp, apply_ac3)

    - CSP Ordering
        Return the first variable in unassigned list

    - CSP Filtering (ac3)
        ac3_filtering(csp): apply ac-3 as preprocessor and after each assignment

- Usage
    Run `python sudoku.py`, you could specify input/output path in main() function