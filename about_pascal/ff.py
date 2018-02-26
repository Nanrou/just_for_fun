from werkzeug.local import LocalStack
test_stack = LocalStack()
test_stack.push({'abc': '123'})
test_stack.push({'abc': '1234'})

def get_item():
    return test_stack.pop()

item = get_item()

print(item['abc'])
print(item['abc'])

from werkzeug.local import LocalStack, LocalProxy
test_stack = LocalStack()
test_stack.push({'abc': '123'})
test_stack.push({'abc': '1234'})

def get_item():
    return test_stack.pop()

item = LocalProxy(get_item)

print(item['abc'])
print(item['abc'])