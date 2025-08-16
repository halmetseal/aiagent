class Calculator:
    def __init__(self):
        self.operators = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
        }
        self.precedence = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
        }

    def evaluate(self, expression):
        if not expression or expression.isspace():
            return None
        try:
            result = eval(expression)
            return result
        except (SyntaxError, NameError, TypeError) as e:
            raise ValueError(f"Invalid expression: {e}")

    def _evaluate_infix(self, tokens):
        values = []
        operators = []

        for token in tokens:
            if token in self.operators:
                while operators and self.precedence[token] <= self.precedence.get(operators[-1], 0):
                    op = operators.pop()
                    val2 = values.pop()
                    val1 = values.pop()
                    values.append(self.operators[op](val1, val2))
                operators.append(token)
            else:
                try:
                    values.append(float(token))
                except ValueError:
                    raise ValueError("Invalid token")

        while operators:
            op = operators.pop()
            val2 = values.pop()
            val1 = values.pop()
            values.append(self.operators[op](val1, val2))

        return values[0]