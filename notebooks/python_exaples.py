def decorator_with_args(a, b):
    def decorator(process):
        print(f"decorator outer_args: {a}, {b}")
        def wrapper():
            print(f"wrapper outer_args: {a}, {b}")
            return process(10)
        return wrapper
    return decorator

@decorator_with_args(1,6)
def process_args(data):
    print(f"process_args: {data}")

process_args()
