package headFirst.Collection;

import java.util.*;

// 外部递归采用栈来做辅助

public class CompositeIterator implements Iterator {
    Stack stack = new Stack();

    public CompositeIterator(Iterator iterator) {
        stack.push(iterator);
    }

    public boolean hasNext() {
        if (stack.empty()) {
            return false;
        } else {
            Iterator iterator = (Iterator) stack.peek();
            if (!iterator.hasNext()) {  // 当前这个迭代器已经空了，就从栈中去掉
                stack.pop();
                return hasNext();
            } else {
                return true;
            }
        }
    }

    public Object next() {
        if (hasNext()) {
            Iterator iterator = (Iterator) stack.peek();
            MenuComponent component = (MenuComponent) iterator.next();
            if (component instanceof Menu) {  // 遇到菜单就放到顶部，注意，这个时候必定是已经循环完菜单的子项，开始循环新的菜单项
                stack.push(component.createIterator());
//                Iterator ii = component.createIterator();
//                stack.push(ii);
//                System.out.println(ii);
            }
            return component;
        } else {
            return null;
        }
    }

    public void remove() {
        throw new UnsupportedOperationException();
    }
}
